import json, math, struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops

W=Path(__file__).parent
from figure_tools import font
def lines():
    b=(W/'map_data/ne_50m_coastline.shp').read_bytes();pos=100
    while pos<len(b):
        n,size=struct.unpack_from('>ii',b,pos);pos+=8;c=b[pos:pos+size*2];pos+=size*2
        if len(c)<44 or struct.unpack_from('<i',c)[0] not in (3,5):continue
        np,npt=struct.unpack_from('<ii',c,36);ix=list(struct.unpack_from('<'+'i'*np,c,44))+[npt]
        pts=[struct.unpack_from('<dd',c,44+4*np+16*k) for k in range(npt)]
        for k in range(np):yield pts[ix[k]:ix[k+1]]
COAST=list(lines())
LOCATIONS=json.loads((W/'map_data/selected_locations.json').read_text(encoding='utf-8'))['records']
PORTS={r['name']:(r['longitude'],r['latitude']) for r in LOCATIONS if r['name']!='Addis Ababa'}
ADDIS=next((r['longitude'],r['latitude']) for r in LOCATIONS if r['name']=='Addis Ababa')
manifest=[]
def make(name,bounds,axes=False):
    x0,x1,y0,y1=bounds
    width=1800; margin=125; pw=width-2*margin; ph=round(pw*(y1-y0)/(x1-x0)/math.cos(math.radians((y0+y1)/2)))
    height=ph+210
    im=Image.new('RGB',(width,height),'white');d=ImageDraw.Draw(im)
    left,top=margin,35;right,bottom=left+pw,top+ph
    def xy(lon,lat):return (left+(lon-x0)/(x1-x0)*pw, top+(y1-lat)/(y1-y0)*ph)
    for lon in range(math.ceil(x0/2)*2,int(x1)+1,2):
        x,_=xy(lon,y0);d.line((x,top,x,bottom),fill='#dedede',width=2);d.text((x,bottom+15),str(lon)+'°E',anchor='mt',font=font(39),fill='#555555')
    for lat in range(math.ceil(y0/4)*4,int(y1)+1,4):
        _,y=xy(x0,lat);d.line((left,y,right,y),fill='#dedede',width=2);d.text((left-15,y),str(abs(lat))+'°'+('N' if lat>=0 else 'S'),anchor='rm',font=font(39),fill='#555555')
    overlay=Image.new('RGBA',im.size,(0,0,0,0));od=ImageDraw.Draw(overlay)
    for coords in COAST:
        if not any(x0-.5<=x<=x1+.5 and y0-.5<=y<=y1+.5 for x,y in coords):continue
        od.line([xy(*p) for p in coords],fill='#333333',width=4)
    mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).rectangle((left,top,right,bottom),fill=255)
    overlay.putalpha(ImageChops.multiply(overlay.getchannel('A'),mask))
    im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im)
    if axes:
        for p in ['Massawa','Assab','Djibouti','Berbera']:
            a,b=xy(*ADDIS),xy(*PORTS[p]);length=math.dist(a,b)
            for st in range(0,int(length),28):
                f=st/length;g=min((st+12)/length,1)
                d.line((a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f,a[0]+(b[0]-a[0])*g,a[1]+(b[1]-a[1])*g),fill='#777777',width=4)
    labels=[('Ethiopia',37.4,7.0),('Eritrea',37.5,16.2),('Somalia',47.0,5.2),('Kenya',36.5,-1),('Yemen',46.5,15.8),('Sudan',34.8,16.5)]
    if axes:labels=[('Ethiopia',37.5,10.9),('Eritrea',38.0,16.5),('Yemen',45.5,15.6)]
    for text,lon,lat in labels:
        if x0+.8<lon<x1-.8 and y0+.6<lat<y1-.6:d.text(xy(lon,lat),text,anchor='mm',font=font(43,True),fill='#777777',stroke_width=4,stroke_fill='white')
    seas=[('Red Sea',41.3,16.5),('Gulf of Aden',46.4,12.7)]
    for t,x,y in seas:
        if x0+.7<x<x1-.7 and y0+.7<y<y1-.7:d.text(xy(x,y),t,anchor='mm',font=font(43),fill='#555555',stroke_width=3,stroke_fill='white')
    offsets={'Massawa':(20,-42),'Assab':(22,-35),'Djibouti':(25,25),'Berbera':(23,15),'Mombasa':(25,0)}
    for p,loc in PORTS.items():
        if not(x0<=loc[0]<=x1 and y0<=loc[1]<=y1):continue
        x,y=xy(*loc);d.ellipse((x-10,y-10,x+10,y+10),fill='black');dx,dy=offsets[p]
        d.text((x+dx,y+dy),p,font=font(46,True),fill='black',stroke_width=4,stroke_fill='white')
    x,y=xy(*ADDIS);d.rectangle((x-10,y-10,x+10,y+10),fill='black');d.text((x-20,y+22),'Addis Ababa',anchor='rt',font=font(46,True),fill='black',stroke_width=4,stroke_fill='white')
    d.rectangle((left,top,right,bottom),outline='#888888',width=2)
    d.text((width-120,70),'N',anchor='mt',font=font(40,True),fill='black');d.line((width-120,175,width-120,125),fill='black',width=4);d.polygon([(width-120,110),(width-132,135),(width-108,135)],fill='black')
    d.text((left,height-55),'Dotted lines are comparison axes, not transport routes.' if axes else 'Selected places and coastlines; boundaries omitted.',font=font(35),fill='#333333')
    out=W/'figures'/'regenerated'/name;out.parent.mkdir(parents=True,exist_ok=True);im.save(out,dpi=(400,400));manifest.append({'file':str(out.relative_to(W)).replace(chr(92),'/'),'bounds':bounds,'coordinates':PORTS|{'Addis Ababa':ADDIS},'projection':'Equirectangular geographic graticule; orientation only','axes':axes,'pixels':list(im.size)})
def main():
    manifest.clear()
    make('map1_orientation_equivalent.png',(33,50,-5,19))
    make('map2_comparison_equivalent.png',(36,48,7,18),True)
    dest=W/'results';dest.mkdir(parents=True,exist_ok=True)
    (dest/'map_regeneration.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return [W/x['file'] for x in manifest]

if __name__=='__main__':
    print([str(x) for x in main()])
