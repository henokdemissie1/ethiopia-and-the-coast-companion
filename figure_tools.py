"""Small portable Pillow drawing helpers for equivalent companion figures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS = ['#254b68', '#ad632d', '#418b7c', '#686868', '#827099', '#bf9b32']

def font(size, bold=False):
    names = (['DejaVuSans-Bold.ttf', 'Arial Bold.ttf', 'arialbd.ttf'] if bold
             else ['DejaVuSans.ttf', 'Arial.ttf', 'arial.ttf'])
    candidates = names + ([str(Path('C:/Windows/Fonts') / names[-1])]
                         if Path('C:/Windows/Fonts').exists() else [])
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    # Pillow >=10.1 includes a scalable default font. No OS font is mandatory.
    return ImageFont.load_default(size=size)

def text(draw, xy, value, size=28, bold=False, anchor=None, fill='#17323e'):
    draw.text(xy, str(value), font=font(size, bold), fill=fill, anchor=anchor)

def wrapped(draw, xy, value, width, size=25, fill='#42545d', line_height=None):
    x, y = xy
    line_height = line_height or int(size * 1.4)
    current = ''
    for word in str(value).split():
        trial = (current + ' ' + word).strip()
        if draw.textbbox((0, 0), trial, font=font(size))[2] > width and current:
            text(draw, (x, y), current, size, fill=fill)
            y += line_height
            current = word
        else:
            current = trial
    if current:
        text(draw, (x, y), current, size, fill=fill)
        y += line_height
    return y

def canvas(number, title, subtitle='', note='', width=1600, height=1000):
    im = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(im)
    text(draw, (55, 28), f'Figure {number} | {title}', 39, True)
    if subtitle:
        wrapped(draw, (55, 90), subtitle, width - 110, 25)
    if note:
        wrapped(draw, (55, height - 110), note, width - 110, 23)
    text(draw, (55, height - 32), 'Equivalent regeneration for the public companion; original book image is preserved separately.', 18, fill='#666666')
    return im, draw

def legend(draw, items, y=150, x=190):
    for label, color in items:
        draw.line((x, y+14, x+56, y+14), fill=color, width=7)
        text(draw, (x+70, y), label, 26)
        x += 90 + draw.textbbox((0,0), label, font=font(26))[2]

def axes(draw, bounds, x_range, y_range, xticks, yticks, xlabel, ylabel):
    left, top, right, bottom = bounds
    xmin, xmax = x_range
    ymin, ymax = y_range
    xp = lambda x: left + (x-xmin)/(xmax-xmin)*(right-left)
    yp = lambda y: bottom - (y-ymin)/(ymax-ymin)*(bottom-top)
    for y in yticks:
        p = yp(y)
        draw.line((left,p,right,p), fill='#dce4e7', width=2)
        text(draw, (left-18,p), f'{y:g}', 26, anchor='rm')
    for x in xticks:
        p = xp(x)
        draw.line((p,bottom,p,bottom+9), fill='#42545d', width=2)
        text(draw, (p,bottom+20), f'{x:g}', 26, anchor='mt')
    draw.line((left,top,left,bottom,right,bottom), fill='#42545d', width=3)
    text(draw, (left,top-40), ylabel, 25)
    text(draw, ((left+right)/2,bottom+67), xlabel, 27, anchor='mt')
    if ymin < 0 < ymax:
        draw.line((left,yp(0),right,yp(0)), fill='#48545b', width=3)
    return xp, yp

def lineplot(number, title, subtitle, note, series, x_range, y_range, xticks, yticks, xlabel, ylabel, annotate=None):
    im, draw = canvas(number,title,subtitle,note)
    legend(draw, [(a,c) for a,_,c in series])
    xp, yp = axes(draw,(180,240,1510,790),x_range,y_range,xticks,yticks,xlabel,ylabel)
    for label, points, color in series:
        draw.line([(xp(x),yp(y)) for x,y in points],fill=color,width=6)
    for x,y,label in annotate or []:
        xx,yy=xp(x),yp(y)
        draw.ellipse((xx-6,yy-6,xx+6,yy+6),fill=COLORS[0])
        text(draw,(xx,yy-16),label,25,True,anchor='mb')
    return im

def arrow(draw, start, end, color='#254b68'):
    import math
    x1,y1=start;x2,y2=end
    draw.line((x1,y1,x2,y2),fill=color,width=4)
    a=math.atan2(y2-y1,x2-x1)
    p1=(x2-18*math.cos(a-.45), y2-18*math.sin(a-.45))
    p2=(x2-18*math.cos(a+.45), y2-18*math.sin(a+.45))
    draw.line((p1,(x2,y2),p2),fill=color,width=4)

def box(draw, bounds, label, detail='', fill='#e8f0f4'):
    x0,y0,x1,y1=bounds
    draw.rounded_rectangle(bounds,radius=8,fill=fill,outline='#99afb9',width=2)
    wrapped(draw,(x0+20,y0+20),label,x1-x0-40,29,fill='#17323e')
    if detail:
        wrapped(draw,(x0+20,y0+85),detail,x1-x0-40,22)
