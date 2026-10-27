"""Regenerate equivalent Figures 1-14 plus both maps from frozen inputs, offline.

Requires Pillow>=10.1. Original publication PNGs are never overwritten. The new
drawings preserve stated data and concepts but do not claim pixel identity.
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics
from PIL import ImageDraw
from figure_tools import COLORS, arrow, axes, box, canvas, font, legend, lineplot, text, wrapped

ROOT=Path(__file__).resolve().parent
CHECKS=[]

def check(name, actual, expected, tolerance=1e-9):
    passed=abs(actual-expected)<=tolerance
    CHECKS.append({'name':name,'actual':actual,'expected':expected,'tolerance':tolerance,'pass':passed})
    if not passed:raise ValueError(f'{name}: {actual} != {expected}')

def number(value):return float(value.replace(',','').replace('US$',''))

def raw(name):
    data=json.loads((ROOT/'data/archived'/name).read_text(encoding='utf-8-sig'))
    return data[0],{(x['countryiso3code'],int(x['date'])):x['value'] for x in data[1]}

def export(number, rows, units, status, sources, assumptions=None):
    dest=ROOT/'plot_data';dest.mkdir(parents=True,exist_ok=True)
    stem=f'figure_{number:02d}'
    if rows:
        with (dest/(stem+'.csv')).open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (dest/(stem+'.json')).write_text(json.dumps({'figure':number,'status':status,'units':units,'sources':sources,'assumptions':assumptions or {},'rows':rows},indent=2),encoding='utf-8')

def save(n,image):
    dest=ROOT/'figures/regenerated';dest.mkdir(parents=True,exist_ok=True)
    path=dest/f'figure_{n:02d}_equivalent.png';image.save(path,dpi=(300,300))
    return path

def figure1():
    events=[('1950','UN federation resolution'),('1952','Federation takes effect'),('1962','Federation ends; Eritrea incorporated into Ethiopia'),('1993','Eritrean independence; Ethiopian port use continues'),('1998','Assab cargo movements end during interstate conflict'),('2000','Algiers Agreement'),('2018','Ethiopia-Eritrea peace and friendship declaration'),('2024','Ethiopia-Somalia Ankara Declaration')]
    im,d=canvas(1,'Selected historical and diplomatic milestones','Selective chronology; equally spaced events, not a proportional time scale.','Sources: references 3, 4, 5, 9, 32, 73 and 76.',height=1200)
    d.line((180,190,180,995),fill='#777777',width=5)
    for i,(year,label) in enumerate(events):
        y=195+i*110;d.ellipse((170,y,190,y+20),fill=COLORS[0]);text(d,(230,y-8),year,35,True);wrapped(d,(405,y-7),label,1080,30)
    export(1,[{'year':int(a),'milestone':b} for a,b in events],{'year':'calendar year'},'Dated historical selection; not an event-frequency dataset',[3,4,5,9,32,73,76],{'event_spacing':'equal, not elapsed-time proportional'})
    return save(1,im)

def figure2():
    labels=['Farm or factory','Dry port and customs','Road or rail','Coastal terminal','Ocean service','Overseas buyer']
    coords=[(60,230,490,420),(585,230,1015,420),(1110,230,1540,420),(1110,570,1540,760),(585,570,1015,760),(60,570,490,760)]
    im,d=canvas(2,'The export supply chain','A conceptual connected service; not a surveyed route or guaranteed sequence.','Author schematic. Every interface can influence cost and reliability.')
    for b,label in zip(coords,labels):box(d,b,label)
    for a,b in [((500,325),(570,325)),((1025,325),(1095,325)),((1325,435),(1325,550)),((1095,665),(1030,665)),((570,665),(505,665))]:arrow(d,a,b)
    export(2,[{'sequence':i,'stage':s} for i,s in enumerate(labels,1)],{},'Author conceptual diagram',[],{'geographic_route':False})
    return save(2,im)

def figure3():
    meta,data=raw('population.json');rows=[{'year':y,'population_people':data['ETH',y],'population_million':data['ETH',y]/1e6} for y in range(1993,2026)]
    for y in [1993,2010,2025]:check(f'Figure3 {y} population',data['ETH',y],{1993:53708891,2010:90538514,2025:135472051}[y])
    export(3,rows,{'population_people':'people, midyear estimates','population_million':'million people'},'Archived WDI estimates, not a cargo forecast',[13],{'years':[1993,2025],'api_lastupdated':meta.get('lastupdated')})
    im=lineplot(3,'Ethiopia population estimates','Archived World Development Indicators, 1993-2025.','Population estimates may be revised. Population does not directly determine port cargo.',[('Population',[(r['year'],r['population_million']) for r in rows],COLORS[0])],(1992,2026),(45,150),[1993,2000,2010,2020,2025],[50,75,100,125,150],'Calendar year','Million people',[(y,data['ETH',y]/1e6,f'{data["ETH",y]/1e6:.1f}') for y in [1993,2010,2025]])
    return save(3,im)

def figure4():
    mi,imp=raw('imports.json');me,exp=raw('exports.json')
    rows=[{'year':y,'imports_current_usd':imp['ETH',y],'exports_current_usd':exp['ETH',y],'imports_usd_billion':imp['ETH',y]/1e9,'exports_usd_billion':exp['ETH',y]/1e9} for y in range(1993,2026)]
    check('Figure4 2025 imports',imp['ETH',2025],23012000000);check('Figure4 2025 exports',exp['ETH',2025],7585000000)
    export(4,rows,{'imports_current_usd':'current US dollars','exports_current_usd':'current US dollars','chart_scale':'US$ billion'},'Archived WDI/WTO merchandise values; not cargo tonnes or inflation-adjusted growth',[14,15])
    return save(4,lineplot(4,'Merchandise imports and exports','Ethiopia, 1993-2025; archived WDI series.','Values are current US dollars. They do not measure cargo mass or a logistics bill.',[(label,[(r['year'],r[key]) for r in rows],color) for label,key,color in [('Imports','imports_usd_billion',COLORS[0]),('Exports','exports_usd_billion',COLORS[1])]],(1992,2026),(0,25),[1993,2000,2010,2020,2025],[0,5,10,15,20,25],'Calendar year','US$ billion, current'))

def figure5():
    shares=[[.95,.05],[.70,.20,.10],[.60,.25,.15]]
    rows=[{'portfolio':' / '.join(f'{100*s:g}' for s in a),'shares':json.dumps(a),'concentration':sum(s*s for s in a)} for a in shares]
    for a,p in zip(rows,[.905,.540,.445]):check('Figure5 '+a['portfolio'],a['concentration'],p)
    im,d=canvas(5,'Hypothetical corridor concentration','Sum of squared fractional corridor shares.','Author scenarios, not measured named-port shares. The index is not disruption probability.')
    xp,yp=axes(d,(180,230,1510,790),(0,3),(0,1),[],[0,.2,.4,.6,.8,1],'Assumed corridor shares (%)','Concentration index (unitless)')
    for i,r in enumerate(rows):
        x=xp(i+.5);d.rectangle((x-115,yp(r['concentration']),x+115,yp(0)),fill=[COLORS[3],COLORS[0],COLORS[1]][i]);text(d,(x,yp(r['concentration'])-15),f'{r["concentration"]:.3f}',32,True,anchor='mb');text(d,(x,815),r['portfolio'],30,anchor='mt')
    export(5,rows,{'concentration':'unitless sum of squared fractional shares'},'Author hypothetical scenarios',[],{'formula':'sum(share**2)','all_shares_sum_to_one':True})
    return save(5,im)

def figure6():
    im,d=canvas(6,'A simplified port cross section','Concept only; no Assab bathymetry, structure or design level is represented.','Not to scale. The separate draft-allowance arithmetic is illustrative, not channel design guidance.')
    d.rectangle((220,430,950,790),fill='#e4f1f7');d.rectangle((950,290,1450,790),fill='#f1efdf');d.line((220,430,950,430),fill=COLORS[0],width=3);d.line((220,790,1450,790),fill='#555555',width=4);d.line((950,290,1450,290),fill=COLORS[0],width=14);d.line((950,290,950,790),fill=COLORS[0],width=5);d.rectangle((460,375,780,510),fill=COLORS[1]);text(d,(620,330),'Design vessel',32,anchor='mm');text(d,(1130,245),'Quay and yard',32,anchor='mm');text(d,(1200,600),'Land',35,anchor='mm');text(d,(320,360),'Sea',35);text(d,(300,802),'Seabed',28);arrow(d,(620,540),(620,760));arrow(d,(620,760),(620,540));text(d,(420,620),'Under-keel',28,anchor='mm');text(d,(420,657),'clearance',28,anchor='mm')
    export(6,[{'term':'hypothetical vessel draft','value_m':14},{'term':'speed-effect allowance','value_m':.7},{'term':'motion allowance','value_m':.5},{'term':'remaining clearance allowance','value_m':1}],{'value_m':'metres; teaching assumptions, not drawn dimensions'},'Author schematic and separate arithmetic assumptions',[],{'not_to_scale':True,'depth_arithmetic_total_m':16.2,'datum_water_level_other_allowances_not_included':True})
    return save(6,im)

def figure7():
    rows=[{'scenario':'SSP1-1.9','description':'Very low emissions','low_m':.28,'high_m':.55},{'scenario':'SSP2-4.5','description':'Intermediate emissions','low_m':.44,'high_m':.76},{'scenario':'SSP5-8.5','description':'Very high emissions','low_m':.63,'high_m':1.01}]
    im,d=canvas(7,'Selected global sea-level projections','IPCC AR6 WGI (2021), B.5.3: likely ranges by 2100 relative to 1995-2014.','Scenario projections, not measured local change or Assab design levels. The likely range is not a physical maximum.')
    xp,yp=axes(d,(660,230,1500,790),(0,1.5),(0,3),[0,.25,.5,.75,1,1.25,1.5],[],'Global mean rise (m)','')
    for i,r in enumerate(rows):
        y=320+i*180;text(d,(620,y),r['description']+'\n'+r['scenario'],28,anchor='rm');d.line((xp(r['low_m']),y,xp(r['high_m']),y),fill=COLORS[i],width=22);text(d,(xp(r['high_m'])+16,y),f'{r["low_m"]:.2f}-{r["high_m"]:.2f} m',24,anchor='lm')
    export(7,rows,{'low_m':'metres','high_m':'metres'},'Assessed global scenario ranges, not observations',[21],{'year':2100,'reference_period':'1995-2014','likely_range_not_physical_maximum':True})
    return save(7,im)

def figure8(tables):
    names=['Ocean freight','Port and documents','Inland transport','Border cost','Inventory financing','Expected disruption']
    a=[1800,400,1000,120,20000*.18*20/365,60];b=[1850,450,800,140,20000*.18*14/365,80]
    rows=[{'component':s,'route_A_usd':x,'route_B_usd':y} for s,x,y in zip(names,a,b)]
    for i,row in enumerate(rows,1):
        for col,key in [(1,'route_A_usd'),(2,'route_B_usd')]:check(f'Figure8 Table5 row{i} col{col}',row[key],number(tables[4][i][col]),.005)
    im,d=canvas(8,'Hypothetical container cost components','The same modeled shipment; Route A and Route B do not represent measured named corridors.','Inventory assumptions: cargo value US$20,000; annual carrying rate 18%; A 20 days, B 14 days.')
    legend(d,[('Route A',COLORS[0]),('Route B',COLORS[1])],x=530)
    xp,yp=axes(d,(530,240,1500,790),(0,2000),(0,6),[0,500,1000,1500,2000],[],'US dollars per hypothetical container','')
    for i,row in enumerate(rows):
        y=270+i*90;text(d,(500,y+17),row['component'],26,anchor='rm')
        d.rectangle((xp(0),y,xp(row['route_A_usd']),y+23),fill=COLORS[0]);d.rectangle((xp(0),y+29,xp(row['route_B_usd']),y+52),fill=COLORS[1])
    export(8,rows,{'route_A_usd':'US dollars per container','route_B_usd':'US dollars per container'},'Author hypothetical costs and calculated inventory',[12],{'cargo_value_usd':20000,'annual_carrying_rate':.18,'route_A_days':20,'route_B_days':14,'route_A_total_usd':sum(a),'route_B_total_usd':sum(b),'A_minus_B_usd':sum(a)-sum(b)})
    return save(8,im)

def figure9(companion):
    rows=[{'cargo_value_usd':v,'annual_carrying_rate':.18,'extra_days':day,'cost_usd':v*.18*day/365} for v in [5000,20000,100000] for day in range(31)]
    for r in companion['hypothetical_inventory_costs.csv']:
        check('Figure9 archived inventory row',float(r['cost_usd']),float(r['cargo_value_usd'])*float(r['annual_carrying_rate'])*float(r['extra_days'])/365,1e-8)
    series=[(f'Cargo US${v:,}',[(r['extra_days'],r['cost_usd']) for r in rows if r['cargo_value_usd']==v],color) for v,color in zip([5000,20000,100000],[COLORS[3],COLORS[0],COLORS[1]])]
    export(9,rows,{'cargo_value_usd':'US dollars','cost_usd':'US dollars','extra_days':'days'},'Author inventory-carrying assumptions',[],{'annual_carrying_rate':.18,'formula':'cargo_value_usd * annual_carrying_rate * extra_days / 365','excluded':['spoilage','penalties','lost production']})
    return save(9,lineplot(9,'Hypothetical inventory carrying cost','Simple daily allocation at an assumed 18% annual carrying rate.','The carrying rate is not a quoted Ethiopian lending rate. Excludes spoilage, penalties and production interruption.',series,(0,30),(0,1600),[0,5,10,15,20,25,30],[0,400,800,1200,1600],'Additional days','Inventory cost (US$)'))

def figure10(tables,companion):
    pv=sum(1.08**-y for y in range(1,26));annual=1500/pv+30
    check('Figure10 annual equivalent cost',annual,170.52,.005)
    rows=[{'traffic_million_tonnes':traffic,'saving_usd_per_tonne':saving,'annual_equivalent_cost_usd_million':annual,'net_annual_usd_million':traffic*saving-annual} for saving in [10,20,40] for traffic in range(16)]
    for r in companion['hypothetical_project_grid.csv']:
        rate=float(r['rate']);years=int(float(r['years']));af=sum((1+rate)**-y for y in range(1,years+1));cost=float(r['capital_usd'])/af+float(r['annual_operations_usd']);expected=float(r['traffic_tonnes'])*float(r['gross_saving_usd_per_tonne'])-cost;check('Figure10 archived grid row',float(r['net_annual_benefit_usd']),expected,1e-5)
    for row in tables[5][1:]:
        for j,saving in enumerate([10,20,40],1):check('Figure10 Table6',number(row[0])*saving-annual,number(row[j]),.005)
    export(10,rows,{'traffic_million_tonnes':'million tonnes/year','saving_usd_per_tonne':'US dollars/tonne','net_annual_usd_million':'US$ million/year'},'Author investment appraisal assumptions',[],{'capital_usd_million':1500,'economic_discount_rate':.08,'years':25,'annual_om_usd_million':30,'capital_time_zero':True,'residual_value':0,'ramp_up':False,'threshold_traffic_million_tonnes':{str(s):annual/s for s in [10,20,40]}})
    series=[(f'US${s} saved/tonne',[(r['traffic_million_tonnes'],r['net_annual_usd_million']) for r in rows if r['saving_usd_per_tonne']==s],c) for s,c in zip([10,20,40],[COLORS[3],COLORS[0],COLORS[1]])]
    return save(10,lineplot(10,'Traffic and savings thresholds','US$1.5bn capital; 8% economic discount rate; 25 years; US$30m annual O&M.','Crossing zero equates assumed gross savings and annual equivalent cost. This is not an Assab estimate.',series,(0,15),(-200,450),[0,3,6,9,12,15],[-200,-100,0,100,200,300,400],'Annual traffic (million tonnes)','Net annual equivalent (US$ million)'))

def figure11():
    rows=[{'phase':'Limited additional cargo service','start':.5,'end':1.5},{'phase':'Priority roads, yards, utilities and training','start':2,'end':5},{'phase':'Substantial terminal expansion','start':3,'end':6},{'phase':'Industrial and household effects','start':5,'end':10},{'phase':'Mature coastal urban economy','start':10,'end':20}]
    im,d=canvas(11,'Conditional development windows','From an enabling agreement and safe access for authorized preparation.','A separate operating clock begins with dependable service. No site-specific schedule is asserted.')
    xp,yp=axes(d,(750,230,1500,790),(0,21),(0,5),[0,5,10,15,20],[],'Preparation years','')
    for i,r in enumerate(rows):
        y=280+i*105;wrapped(d,(55,y-20),r['phase'],650,27);d.rectangle((xp(r['start']),y-20,xp(r['end']),y+25),fill=COLORS[0]);label=f'{r["start"]:g}-{r["end"]:g}';text(d,(xp(r['end'])+10,y+2),label,23,anchor='lm') if r['start']==.5 else text(d,((xp(r['start'])+xp(r['end']))/2,y+2),label,23,anchor='mm',fill='white')
    export(11,rows,{'start':'years from preparation authorization','end':'years from preparation authorization'},'Author conditional planning windows',[],{'existing_usable_assets_required_for_early_service':True,'preparation_clock':'enabling agreement and safe access','operating_clock':'dependable commercial service starts later','site_specific_schedule':False})
    return save(11,im)

def figure12():
    im,d=canvas(12,'A conceptual coastal settlement','No geographic location, scale, fixed buffers or population forecast.','Existing residents help shape the plan. Jobs, water capacity and environmental studies govern expansion.')
    d.rounded_rectangle((60,180,1540,290),radius=7,fill='#dceef3');text(d,(800,210),'SEA AND WORKING WATERFRONT',32,True,anchor='mt');text(d,(300,260),'Fishing and shore access',26,anchor='mm');text(d,(1220,260),'Terminal and navigation',26,anchor='mm')
    nodes=[('Existing neighborhoods','Tenure, livelihoods and affordable services'),('Schools, clinic and market','Training, civic life and shaded walking routes'),('Logistics and industry','Freight access and studied risk buffers'),('Incremental housing','Serviced plots and room to grow'),('Water and electricity','Treatment, reuse, backup and reliability'),('Transport reservation','Road connections; rail after appraisal')]
    for i,(title,detail) in enumerate(nodes):
        row=i//3;col=i%3;y=330 if row==0 else 610;box(d,(60+col*500,y,520+col*500,y+200),title,detail)
    d.rectangle((60,555,1520,590),fill=COLORS[2]);text(d,(790,572),'Drainage, habitats and connected streets',25,anchor='mm',fill='white')
    export(12,[{'element':a,'role':b} for a,b in nodes],{},'Author conceptual settlement diagram',[41,45,64],{'not_to_scale':True,'no_fixed_buffer':True,'not_a_new_city_location':True})
    return save(12,im)

def figure13(tables):
    meta,data=raw('NY.GDP.MKTP.KD.json');partners=['DJI','KEN','UGA','TZA','RWA'];rows=[]
    for y in range(2014,2025):
        if not all(data.get((c,t)) is not None for c in ['ETH']+partners for t in [y-1,y]):raise ValueError('Missing frozen GDP observation; do not impute.')
        before=sum(data[c,y-1] for c in partners);now=sum(data[c,y] for c in partners)
        r={'year':y,'ethiopia_growth_percent':100*(data['ETH',y]/data['ETH',y-1]-1),'partners_aggregate_growth_percent':100*(now/before-1),'ethiopia_gdp_constant_2015_usd':data['ETH',y],'partners_gdp_sum_constant_2015_usd':now}
        r.update({c+'_growth_percent':100*(data[c,y]/data[c,y-1]-1) for c in partners});rows.append(r)
    corr=statistics.correlation([r['ethiopia_growth_percent'] for r in rows],[r['partners_aggregate_growth_percent'] for r in rows]);wo=[r for r in rows if r['year']!=2020];corr_wo=statistics.correlation([r['ethiopia_growth_percent'] for r in wo],[r['partners_aggregate_growth_percent'] for r in wo]);check('Figure13 aggregate Pearson r',corr,number(tables[12][6][2]),.005);check('Figure13 aggregate r excluding2020',corr_wo,number(tables[12][7][2]),.005)
    export(13,rows,{'growth':'percent/year','underlying_gdp':'constant 2015 US dollars'},'Historical WDI levels transformed to annual growth',[47],{'partners':partners,'aggregate':'growth of sum of partner GDP levels; excludes Ethiopia','sample':[2014,2024],'pearson_r':corr,'pearson_r_excluding_2020':corr_wo,'correlation_not_causal_effect':True})
    return save(13,lineplot(13,'Annual real GDP growth','Ethiopia and a five-partner GDP aggregate, 2014-2024.','Historical correlation: '+f'{corr:.2f}; excluding 2020: {corr_wo:.2f}. This is not an estimated coastal-access effect.',[(label,[(r['year'],r[key]) for r in rows],c) for label,key,c in [('Ethiopia','ethiopia_growth_percent',COLORS[0]),('Five-partner aggregate','partners_aggregate_growth_percent',COLORS[2])]],(2014,2024),(0,12),[2014,2016,2018,2020,2022,2024],[0,3,6,9,12],'Calendar year','Annual real growth (%)'))

def figure14(tables):
    inputs=[('Limited',6,10,.5,300,.25,1,100,.30),('Central',10,20,.7,1000,.35,3,300,.35),('Strong',15,40,.8,2000,.45,5,700,.45)];rows=[]
    for col,(label,traffic,saving,capture,capital,ratio,logcost,othercap,otherratio) in enumerate(inputs,1):
        prod=traffic*saving*capture;industry=capital*ratio;eth=prod+industry;supplier=eth*.35*.20*.55;logistics=traffic*logcost;oi=othercap*otherratio;other=supplier+logistics+oi
        vals=[prod,industry,eth,supplier,logistics,oi,other,eth+other]
        for row,v in enumerate(vals,1):check('Figure14 Table14 scenario'+str(col)+' row'+str(row),v,number(tables[13][row][col]),.05)
        rows.append(dict(scenario=label,traffic_million_tonnes=traffic,saving_usd_per_tonne=saving,productivity_capture=capture,ethiopian_additional_private_capital_usd_million=capital,ethiopian_value_added_to_capital_ratio=ratio,other_logistics_value_added_usd_per_tonne=logcost,other_additional_private_capital_usd_million=othercap,other_value_added_to_capital_ratio=otherratio,ethiopia_productivity_usd_million=prod,ethiopia_industry_usd_million=industry,ethiopia_total_usd_million=eth,other_supplier_usd_million=supplier,other_logistics_usd_million=logistics,other_industry_usd_million=oi,other_total_usd_million=other,combined_total_usd_million=eth+other))
    im,d=canvas(14,'Conditional additional annual production','Accounting illustration at Operating Year 10; constant 2026 US$ million per year.','Author assumptions require additional private capital. GDP increments are not cumulative income or net welfare.')
    legend(d,[('Ethiopia',COLORS[0]),('Other regional output',COLORS[2])],x=320)
    xp,yp=axes(d,(190,250,1500,790),(0,3),(0,2100),[],[0,500,1000,1500,2000],'Chosen assumption set','US$ million/year, constant 2026')
    for i,r in enumerate(rows):
        x=xp(i+.5);d.rectangle((x-125,yp(r['ethiopia_total_usd_million']),x+125,yp(0)),fill=COLORS[0]);d.rectangle((x-125,yp(r['combined_total_usd_million']),x+125,yp(r['ethiopia_total_usd_million'])),fill=COLORS[2]);text(d,(x,yp(r['combined_total_usd_million'])-15),f'{r["combined_total_usd_million"]:,.0f}',31,True,anchor='mb');text(d,(x,812),r['scenario'],30,anchor='mt')
    export(14,rows,{'money':'constant 2026 US$ million per year unless a field states otherwise','capital':'constant 2026 US$ million','traffic':'million tonnes/year'},'Author conditional accounting assumptions; no empirically estimated access effect',[],{'operating_year':10,'fixed_opening_date':False,'supplier_fraction':.35*.20*.55,'additionality_required':True,'may_not_be_added_to_transport_savings_or_used_to_close_infrastructure_deficit':True})
    return save(14,im)

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--figures',type=int,nargs='+',choices=range(1,15),default=list(range(1,15)))
    parser.add_argument('--skip-maps',action='store_true')
    args=parser.parse_args(argv)
    tables=json.loads((ROOT/'tables.json').read_text(encoding='utf-8'))['tables'];companion=json.loads((ROOT/'companion_rows.json').read_text(encoding='utf-8'))['tables'];paths=[]
    functions={1:figure1,2:figure2,3:figure3,4:figure4,5:figure5,6:figure6,7:figure7,8:lambda:figure8(tables),9:lambda:figure9(companion),10:lambda:figure10(tables,companion),11:figure11,12:figure12,13:lambda:figure13(tables),14:lambda:figure14(tables)}
    for n in args.figures:paths.append(functions[n]())
    if not args.skip_maps:
        from build_maps import main as maps_main
        paths += maps_main()
    results=ROOT/'results';results.mkdir(parents=True,exist_ok=True)
    report={'schema_version':1,'release':'v1.0','equivalent_not_pixel_identical':True,'originals_never_overwritten':True,'figures_requested':args.figures,'checks':CHECKS,'passed':sum(x['pass'] for x in CHECKS),'failed':[x for x in CHECKS if not x['pass']],'outputs':[{'file':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths],'input_status':'Observed historical series and hypothetical assumptions are identified separately in plot_data/ and FIGURES.md.'}
    (results/'figure_validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'outputs':len(paths),'checks_passed':report['passed'],'failed':report['failed']},indent=2))

if __name__=='__main__':main()
