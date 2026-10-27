"""Draw the approved expanded Figure 1 from explicit dated event input.

Output: 1320 x 1740 pixels at 300 dpi = 4.4 x 5.8 inches.
The two stacked sections are selective and are not proportional time scales.
"""
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Henok Kefelegn
import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw
from figure_tools import font

WIDTH, HEIGHT, DPI = 1320, 1740, 300

def build_figure1(root=None):
    root=Path(root or Path(__file__).resolve().parent)
    source=root/'plot_data/figure_01_events.json'
    spec=json.loads(source.read_text(encoding='utf-8'))
    image=Image.new('RGB',(WIDTH,HEIGHT),'white')
    draw=ImageDraw.Draw(image)
    ink='#17323e';blue='#254b68';muted='#48585f';checks=[]
    def put(x,y,value,size=39,bold=False,fill=ink,width=None):
        face=font(size,bold)
        bounds=draw.textbbox((x,y),value,font=face)
        if width is not None:
            assert bounds[2] <= x+width, (value,bounds,x+width)
        assert bounds[0]>=0 and bounds[2]<=WIDTH-35 and bounds[3]<=HEIGHT-20, (value,bounds)
        draw.text((x,y),value,font=face,fill=fill)
        checks.append({'text':value,'font_px':size,'bbox':list(bounds),'within_canvas':True})
    put(55,28,'Selected historical and diplomatic milestones',46,True,width=1210)
    put(55,93,'A selective chronology, not a proportional time scale',34,False,muted,width=1210)
    y=165
    rows=[]
    for section in spec['sections']:
        draw.rounded_rectangle((45,y,1275,y+64),radius=7,fill='#e8f0f4')
        put(65,y+9,section['label'],37,True,width=1170)
        y+=90
        for group in section['groups']:
            lines=group['events']
            lineheight=48
            groupheight=max(91,len(lines)*lineheight+22)
            # A small divider separates event groups without implying elapsed time.
            draw.line((65,y+groupheight-9,1255,y+groupheight-9),fill='#e0e5e7',width=2)
            for j,event in enumerate(lines):
                yy=y+j*lineheight
                date=event['date']
                if date=='First centuries CE':
                    put(65,yy-4,'First centuries',33,True,blue,width=260)
                    put(65,yy+34,'CE',33,True,blue,width=260)
                elif date=='Fourth century CE':
                    put(65,yy-4,'Fourth century',33,True,blue,width=260)
                    put(65,yy+34,'CE',33,True,blue,width=260)
                else:
                    put(65,yy,date,38,True,blue,width=260)
                put(365,yy,event['label'],event.get('font_px',39),width=890)
                rows.append({'section':section['label'],'date':date,'milestone':event['label'],'book_references':';'.join(str(n) for n in event['references'])})
            y+=groupheight
        y+=27
    assert y <= 1568, y
    put(55,1590,'1993 independence and the 1998 port-cargo interruption',32,True,width=1210)
    put(55,1631,'are distinct events. See Table 1 and Chapter 1 for context.',32,False,muted,width=1210)
    put(55,1686,'Sources [1-5, 9, 32, 33, 73, 75, 76]. Dates identify events, not continuing rights.',24,False,muted,width=1210)
    dest=root/'figures/regenerated';dest.mkdir(parents=True,exist_ok=True)
    target=dest/'figure_01_equivalent.png';image.save(target,dpi=(DPI,DPI))
    data=root/'plot_data';data.mkdir(parents=True,exist_ok=True)
    with (data/'figure_01.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    metadata={'figure':1,'status':'Selected historical events; expanded approved correction dated 27 October 2026','units':{'date':'calendar year or stated ancient period'},'sources':[1,2,3,4,5,9,32,33,73,75,76],'assumptions':{'not_a_proportional_time_scale':True,'no_continuous_territorial_control_or_present_rights_inferred':True},'rows':rows,'render':{'pixels':[WIDTH,HEIGHT],'dpi':DPI,'intended_inches':[4.4,5.8],'minimum_main_event_font_px':37,'main_event_font_points_at_intended_size':37/300*72}}
    (data/'figure_01.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    results=root/'results';results.mkdir(parents=True,exist_ok=True)
    (results/'figure_01_layout_checks.json').write_text(json.dumps({'pixels':[WIDTH,HEIGHT],'dpi':DPI,'intended_inches':[4.4,5.8],'all_text_bounds_checked':True,'text_elements':checks,'last_group_bottom_px':y,'sources_input':'plot_data/figure_01_events.json'},indent=2),encoding='utf-8')
    return target

if __name__=='__main__':
    print(build_figure1())
