"""Reproduce the numerical companion baseline dated 27 October 2026.

Inputs are frozen public WDI responses, explicit teaching assumptions, and the
included machine-readable tables. No manuscript, network, or API key is needed.
The comparison count inventories calculations, not a quality certification.
"""
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import hashlib
import argparse
import json
import math
import statistics

OUT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--tables-only', action='store_true', help='Use the included machine-readable tables; this is also the default.')
parser.add_argument('--output', type=Path, default=OUT/'results/core_models.json', help='Output JSON path.')
args = parser.parse_args()
EVIDENCE = OUT/'data/archived'
COASTAL = EVIDENCE
checks = []

def check(name, actual, printed, tolerance, page, unit, basis='Companion teaching assumptions'):
    checks.append(dict(name=name, actual=actual, printed=printed,
                       tolerance=tolerance, difference=actual-printed,
                       pass_=abs(actual-printed)<=tolerance,
                       unit=unit, basis=basis))

def number(cell):
    return float(cell.replace(',', '').replace('US$', '').replace('%', ''))

snapshot=json.loads((OUT/'tables.json').read_text(encoding='utf-8'))
tables=snapshot['tables']
table_source='Included machine-readable table baseline (tables.json); no full manuscript is required.'
assert len(tables)==15

def read_wdi(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    return data[0], {(r['countryiso3code'],int(r['date'])):r['value'] for r in data[1]}

meta_pop, pop = read_wdi(EVIDENCE/'population.json')
meta_imp, imp = read_wdi(EVIDENCE/'imports.json')
meta_exp, exp = read_wdi(EVIDENCE/'exports.json')
meta_real, real = read_wdi(COASTAL/'NY.GDP.MKTP.KD.json')
meta_nom, nominal = read_wdi(COASTAL/'NY.GDP.MKTP.CD.json')

for row in tables[1][1:]:
    year=int(row[0])
    for name,data,scale,col,tol,unit in [
        ('population',pop,1e6,1,.005,'million people'),
        ('imports',imp,1e9,2,.0005,'US$ billion current'),
        ('exports',exp,1e9,3,.0005,'US$ billion current')]:
        check(f'Table 2 {year} {name}',data['ETH',year]/scale,number(row[col]),tol,45,unit,'Raw archived WDI')
ratio=pop['ETH',2025]/pop['ETH',1993]
check('population ratio',ratio,2.52234,.000005,172,'ratio','Raw archived WDI')
check('population change',(ratio-1)*100,152.23,.005,172,'percent','Raw archived WDI')
check('population CAGR',(ratio**(1/32)-1)*100,2.93,.005,172,'percent/year','Raw archived WDI')
check('2025 export/import ratio',100*exp['ETH',2025]/imp['ETH',2025],32.96,.005,173,'percent','Raw archived WDI')
check('2025 merchandise balance',(exp['ETH',2025]-imp['ETH',2025])/1e9,-15.427,.0005,173,'US$ billion current','Raw archived WDI')
check('2024 export/import ratio',100*exp['ETH',2024]/imp['ETH',2024],29.41,.005,173,'percent','Raw archived WDI')
for shares,printed in [([.95,.05],.905),([.7,.2,.1],.540),([.6,.25,.15],.445)]:
    check('HHI '+str(shares),sum(s*s for s in shares),printed,.0005,47,'unitless')
    check('shares sum '+str(shares),sum(shares),1,1e-12,47,'unitless')
check('reserve route cover',15/100*100,15,1e-10,48,'percent of normal demand')
check('nominal-value example growth',(15_000/10_000-1)*100,50,1e-10,46,'percent')
check('alternative route disadvantage',130+90-200,20,1e-10,76,'US$/shipment')
check('crane moves',20*.60*8760,105120,1e-10,81,'moves/year')
check('loaded trucks/day',5e6/350/20,714,.5,82,'loaded trips/day')

inventories=[20_000*.18*d/365 for d in [20,14]]
routes=[[1800,400,1000,120,inventories[0],60],[1850,450,800,140,inventories[1],80]]
for c in range(2):
    for j,v in enumerate(routes[c]):
        check(f'Table 5 route {c+1} component {j+1}',v,number(tables[4][j+1][c+1]),.005,96,'US$/container')
    check(f'Table 5 route {c+1} total',sum(routes[c]),number(tables[4][-1][c+1]),.005,96,'US$/container')
saving=sum(routes[0])-sum(routes[1])
check('container saving',saving,119.18,.005,96,'US$/container')
check('container saving percent',100*saving/sum(routes[0]),3.3,.05,96,'percent')
for days,printed in [(1,9.86),(6,59.18),(10,98.63)]:
    check('inventory reduction '+str(days),20_000*.18*days/365,printed,.005,97,'US$/container')
check('other route components higher',sum(routes[1][i]-routes[0][i] for i in [0,1,3,5]),140,1e-10,97,'US$/container')
check('reliability example mean',(.5*5+.5*15),10,1e-10,98,'days')

# Independently discount one currency unit at each year end. CRF is its inverse,
# rather than copying the author's algebraic expression.
def annuity_factor(rate,years=25):
    return math.fsum((1+rate)**(-t) for t in range(1,years+1))
def equivalent(capital,rate,om,years=25):
    return capital/annuity_factor(rate,years)+om
ann=equivalent(1500,.08,30)
check('capital recovery factor',1/annuity_factor(.08),.0936788,.00000005,174,'1/year')
check('annual capital cost',1500/annuity_factor(.08),140.52,.005,99,'US$ million/year')
check('annual equivalent cost',ann,170.52,.005,99,'US$ million/year')
for s,p in [(10,17.05),(20,8.53),(40,4.26)]:
    check('project traffic threshold at '+str(s),ann/s,p,.005,100,'million tonnes/year')
for row in tables[5][1:]:
    traffic=number(row[0])
    for col,s in enumerate([10,20,40],1):
        check(f'Table 6 traffic {traffic} saving {s}',traffic*s-ann,number(row[col]),.005,100,'US$ million/year')
for row,rate in zip(tables[6][1:],[.04,.08,.12]):
    cost=equivalent(1500,rate,30)
    check(f'Table 7 {rate} annual cost',cost,number(row[1]),.005,102,'US$ million/year')
    check(f'Table 7 {rate} traffic',cost/20,number(row[2]),.005,102,'million tonnes/year')
check('Mombasa throughput growth',(40.99/35.98-1)*100,13.9,.05,116,'percent')
check('retail price pass-through',.2*.1*100,2,1e-10,143,'percent')

subtotals=[]
for col in [1,2,3]:
    subtotal=sum(number(r[col]) for r in tables[9][1:6]);subtotals.append(subtotal)
    for idx,v in [(6,subtotal),(7,subtotal*.25),(8,subtotal*1.25)]:
        check(f'Table 10 column {col} row {idx}',v,number(tables[9][idx][col]),.05,144,'US$ million constant 2026')
hub=equivalent(2075,.08,45)
check('hub annual equivalent',hub,239.4,.05,145,'US$ million/year constant 2026')
check('hub traffic threshold',hub/20,11.97,.005,145,'million tonnes/year')
check('hub uncovered cost',hub-200,39.4,.05,145,'US$ million/year')
check('construction eligible assets',(1660-80),1580,1e-10,146,'US$ million')
personyears=1580e6*.18/9000
check('construction person-years',personyears,31600,.5,146,'person-years')
check('average concurrent construction workers',personyears/6,5267,.5,146,'workers')
check('peak construction workers',personyears/6*1.5,7900,.5,146,'workers')
for row,anchor,ratio in zip(tables[11][1:],[5000,15000,30000],[.75,1,1.25]):
    jobs=anchor*(1+ratio);residents=jobs*.7/1.5*4
    check('Table 12 '+row[0]+' jobs',jobs,number(row[2]),.5,149,'positions')
    check('Table 12 '+row[0]+' residents',residents,number(row[3]),.5,149,'additional people')
for share,p in [(.4,32000),(.9,72000)]:
    check('medium residents share '+str(share),30000*share/1.5*4,p,.5,149,'additional people')
check('medium households',30000*.7/1.5,14000,.5,149,'households')
check('domestic water delivered',56000*100/1000,5600,.5,150,'m3/day')
check('water produced',5600/(1-.2),7000,.5,150,'m3/day')
check('desalination electricity',7000*4/1000,28,.05,150,'MWh/day')
check('settlement area low',56000/10000,5.6,.05,150,'km2')
check('settlement area high',56000/5000,11.2,.05,150,'km2')

partners=['DJI','KEN','UGA','TZA','RWA']
def growths(data,end):
    history=[]
    for year in range(2011,end+1):
        if not all(data.get((c,y)) is not None for c in ['ETH']+partners for y in [year-1,year]):
            continue
        row={'year':year}
        row.update({c:100*(data[c,year]/data[c,year-1]-1) for c in ['ETH']+partners})
        row['aggregate']=100*(sum(data[c,year] for c in partners)/sum(data[c,year-1] for c in partners)-1)
        history.append(row)
    return history
def correlations(history):
    result={c:statistics.correlation([x['ETH'] for x in history],[x[c] for x in history])
            for c in partners+['aggregate']}
    without=[x for x in history if x['year']!=2020]
    result['aggregate_excluding2020']=statistics.correlation([x['ETH'] for x in without],[x['aggregate'] for x in without])
    return result
history=growths(real,2024);corr=correlations(history)
for row,key in zip(tables[12][1:],partners+['aggregate','aggregate_excluding2020']):
    check('Table 13 '+key,corr[key],number(row[2]),.005,152,'Pearson r','Archived raw real GDP; independent growth/correlation')

production=[]
for label,traffic,cost,capture,capital,ratio,logistics,regional_cap,regional_ratio in [
    ('Limited',6,10,.5,300,.25,1,100,.3),
    ('Central',10,20,.7,1000,.35,3,300,.35),
    ('Strong',15,40,.8,2000,.45,5,700,.45)]:
    product=traffic*cost*capture;industry=capital*ratio;eth=product+industry
    supply=eth*.35*.2*.55;logistic=traffic*logistics;otherindustry=regional_cap*regional_ratio
    other=supply+logistic+otherindustry
    production.append([product,industry,eth,supply,logistic,otherindustry,other,eth+other])
for col,values in enumerate(production,1):
    for row,value in enumerate(values,1):
        check(f'Table 14 scenario {col} row {row}',value,number(tables[13][row][col]),.05,155,'US$ million/year constant 2026','Author hypothetical accounting assumptions; no empirical identification')
baseline=nominal['ETH',2024]*1.02**2*1.06**12/1e9
check('2024 Ethiopia GDP',nominal['ETH',2024]/1e9,149.7,.05,157,'US$ billion current','Raw archived WDI')
check('hypothetical scale comparator',baseline,313.5,.05,157,'US$ billion constant 2026')
for v,p in [(105,.03),(490,.16),(1380,.44)]:
    check('GDP increment scale '+str(v),v/(baseline*1000)*100,p,.005,157,'percent')
check('supplier coefficient',.35*.2*.55,.0385,.00005,154,'unitless')
for share,p in [(.1,19.25),(.2,38.5),(.3,57.75)]:
    check('supplier per US$1bn at '+str(share),1000*.35*share*.55,p,.005,154,'US$ million/year')
other=production[1][6]
for factor,ep,op in [(.35,171.5,53.9),(1.,490,153.9),(1.3,637,200.)]:
    check('maturity Ethiopia '+str(factor),490*factor,ep,.05,157,'US$ million/year')
    check('maturity other '+str(factor),other*factor,op,.05,157,'US$ million/year')
for share,p in [(.4,7.5),(.2,3.8),(.1,1.9)]:
    check('country supply allocation '+str(share),production[1][3]*share,p,.05,157,'US$ million/year')
check('Eritrea host logistics plus industry',30+105,135,.05,157,'US$ million/year')
check('jurisdiction Ethiopia',490+135,625,.05,157,'US$ million/year')
check('jurisdiction preserves total',625+production[1][3],643.9,.05,158,'US$ million/year')
check('regional downside',production[1][3]-30,-11.1,.05,158,'US$ million/year')
check('Ethiopia employment equivalents',490e6/20000,24500,.5,158,'worker equivalents')
check('other employment equivalents',other*1e6/15000,10258,.5,158,'worker equivalents')
for name,a,p in [('entrants',2000*6,12000),('graduates',2000*6*.8,9600),
                 ('placements',2000*6*.8*.65,6240),('women',2000*6*.3,3600),
                 ('local entrants',2000*6*.5,6000)]:
    check('training '+name,a,p,.5,158,'people/placements')
for row,domestic,da,diaspora,fa in zip(tables[14][1:],[1e6,2e6,5e6],[10,25,40],[50e3,200e3,500e3],[100,250,400]):
    gifts=(domestic*da+diaspora*fa)/1e6
    check('Table 15 '+row[0]+' gifts',gifts,number(row[1]),.5,162,'US$ million over five years')
    check('Table 15 '+row[0]+' capital share',gifts/2075*100,number(row[2]),.05,162,'percent')

# Frozen-vintage replication and current-vintage confirmation are separate.
live_comparison=[]
for indicator,old in [('SP.POP.TOTL',pop),('TM.VAL.MRCH.CD.WT',imp),('TX.VAL.MRCH.CD.WT',exp),('NY.GDP.MKTP.KD',real),('NY.GDP.MKTP.CD',nominal)]:
    path=OUT/'data/verification_2026_10_27'/('economics_live_'+indicator+'.json')
    if not path.exists():
        live_comparison.append({'indicator':indicator,'access':'unavailable'})
        continue
    metadata,now=read_wdi(path)
    differences=[{'country':k[0],'year':k[1],'archived':v,'live':now.get(k)} for k,v in old.items() if v!=now.get(k)]
    added=[{'country':k[0],'year':k[1],'value':v} for k,v in now.items() if k not in old]
    live_comparison.append(dict(indicator=indicator,metadata=metadata,common_records=len(old),differences=differences,new_observations=added))
live_real=read_wdi(OUT/'data/verification_2026_10_27/economics_live_NY.GDP.MKTP.KD.json')[1]
updated_history=growths(live_real,2025)

# Check unrounded companion data used for the original teaching charts as a
# separate consistency inventory. These are recalculated from row assumptions,
# never trusted as raw observations or inputs to the substantive conclusions.
companion_consistency=[]
comparison_snapshot=json.loads((OUT/'companion_rows.json').read_text(encoding='utf-8'))['tables']
for filename in ['hypothetical_inventory_costs.csv','hypothetical_financing.csv','hypothetical_project_grid.csv']:
    rows=comparison_snapshot[filename]
    failures=[]
    for index,row in enumerate(rows,1):
        v={k:float(value) for k,value in row.items()}
        if 'inventory' in filename:
            expected={'cost_usd':v['cargo_value_usd']*v['annual_carrying_rate']*v['extra_days']/365}
        elif 'financing' in filename:
            annual=equivalent(v['capital_usd'],v['rate'],30e6,int(v['years']))
            expected={'annualized_capital_usd':annual-30e6,'annual_total_usd':annual,'break_even_tonnes_at_20_usd_saving':annual/20}
        else:
            annual=equivalent(v['capital_usd'],v['rate'],v['annual_operations_usd'],int(v['years']))
            expected={'annualized_cost_usd':annual,'net_annual_benefit_usd':v['traffic_tonnes']*v['gross_saving_usd_per_tonne']-annual}
        for key,value in expected.items():
            if not math.isclose(v[key],value,rel_tol=1e-12,abs_tol=1e-6):
                failures.append({'row':index,'field':key,'archived':v[key],'recomputed':value})
    companion_consistency.append({'file':'companion_rows.json:'+filename,'rows':len(rows),'failures':failures})

# Illustrative adverse tests of the author's own formulas, not forecasts.
# Infrastructure assumptions do not establish an NPV for Assab.
diagnostics={
    'ch8_NPV_at_10Mt_20USD_8percent_USDm':-1500+(200-30)*annuity_factor(.08),
    'ch8_BCR_at_10Mt_20USD_8percent':200*annuity_factor(.08)/(1500+30*annuity_factor(.08)),
    'ch13_hub_NPV_at_10Mt_20USD_8percent_USDm':-2075+(200-45)*annuity_factor(.08),
    'ch13_hub_BCR_at_10Mt_20USD_8percent':200*annuity_factor(.08)/(2075+45*annuity_factor(.08)),
    'ch13_hub_traffic_break_even_at_rate4_8_12_Mt':[equivalent(2075,r,45)/20 for r in [.04,.08,.12]],
    'ch13_Ethiopia_GDP_without_assumed_additional_private_capital_and_without_unestimated_capture_USDm':0,
    'ch13_industry_share_of_central_combined_GDP_percent':(350+105)/production[1][7]*100,
    'ch13_new_private_capital_required_USDm':1000+300,
    'ch13_central_hub_plus_additional_private_capital_USDm':2075+1000+300,
    'ch13_displaced_regional_logistics_stress_USDm':production[1][3]-30,
    'historical_correlations_through2024':corr,
    'updated_correlations_through2025':correlations(updated_history),
    'updated_observation_count':len(updated_history),
    'scope_note':'No teaching input is treated as observed Assab traffic/cost, available finance, net jobs or empirically identified GDP.'
}
out={'baseline_date':'2026-10-27','method':__doc__,
     'table_source':table_source,
     'raw_inputs':[str(Path('data/archived')/x) for x in ['population.json','imports.json','exports.json']]+[str(Path('data/archived')/x) for x in ['NY.GDP.MKTP.KD.json','NY.GDP.MKTP.CD.json']],
     'numeric_comparison_count':len(checks),'passed':sum(c['pass_'] for c in checks),
     'failed':[c for c in checks if not c['pass_']],
     'checks':checks,'verification_snapshot_comparison':live_comparison,'economic_diagnostics':diagnostics}
out['stored_teaching_rows_consistency']=companion_consistency
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:out[k] for k in ['numeric_comparison_count','passed','failed','economic_diagnostics']},indent=2))
