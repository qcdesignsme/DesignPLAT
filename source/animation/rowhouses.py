"""Generates source/page/stage.html: an original pen-and-ink drawing of three Baltimore
rowhouses (SVG), plus a flamingo, a crab, and an oriole. Run from the repo root:
    python3 source/animation/rowhouses.py && python3 source/page/build.py
Strokes with class "ink" are drawn in order by the hero script; "sk" is the faint sketch layer."""
import random, math, os
random.seed(7)
G=312  # sidewalk line
out=[]; sk=[]
def f(v): return f"{v:.1f}".rstrip('0').rstrip('.')
def wob(x1,y1,x2,y2,j=0.7):
    mx,my=(x1+x2)/2+random.uniform(-j,j),(y1+y2)/2+random.uniform(-j,j)
    return f"M{f(x1)} {f(y1)}Q{f(mx)} {f(my)} {f(x2)} {f(y2)}"
def ink(d,cls='',w=1.0): out.append(f'<path class="ink {cls}" data-w="{w}" d="{d}"/>')
def sketch(d): sk.append(f'<path class="sk" d="{d}"/>')
def rectd(x,y,w,h): return f"M{f(x)} {f(y)}H{f(x+w)}V{f(y+h)}H{f(x)}Z"

houses=[  # x0,x1,top, window cols, upper row tops, ground window (cx,top), door (cx,top,w,h,arched)
 dict(x0=36,x1=196,top=None,cols=[80,154],rows=[118,188],gw=(154,248),door=(80,236,24,60,True)),
 dict(x0=196,x1=376,top=44,cols=[246,326],rows=[86,164],gw=(246,244),door=(330,232,28,64,False)),
 dict(x0=376,x1=556,top=58,cols=[426,506],rows=[98,172],gw=(426,246),door=(510,234,26,62,False)),
]
WW,WH=22,48
def roofA(x): return 98-12*(x-36)/160

def window(cx,top,lit_i):
    x=cx-WW/2
    out.append(f'<rect class="glass" data-i="{lit_i}" x="{f(x+1.5)}" y="{f(top+1.5)}" width="{WW-3}" height="{WH-3}"/>')
    ink(rectd(x,top,WW,WH),'',1.0)
    ink(wob(cx,top,cx,top+WH,.4)+wob(x,top+WH/2,x+WW,top+WH/2,.4),'',.8)
    d=''
    for k in range(7):  # radiating brick lintel
        a=math.radians(212+k*(116/6)); r1,r2=14,22; c=(cx,top+12)
        d+=wob(c[0]+r1*math.cos(a),c[1]+r1*math.sin(a),c[0]+r2*math.cos(a),c[1]+r2*math.sin(a),.3)
    ink(d,'',.6)
    ink(wob(x-3,top+WH+2,x+WW+3,top+WH+2,.3),'',.6)  # sill
    sketch(rectd(x,top,WW,WH))

def door(cx,top,w,h,arched):
    x=cx-w/2
    if arched:
        r=w/2; ink(f"M{f(x)} {f(top+h)}V{f(top+r)}A{f(r)} {f(r)} 0 0 1 {f(x+w)} {f(top+r)}V{f(top+h)}")
        d=''
        for k in range(7):
            a=math.radians(200+k*(140/6)); c=(cx,top+r)
            d+=wob(c[0]+(r+3)*math.cos(a),c[1]+(r+3)*math.sin(a),c[0]+(r+10)*math.cos(a),c[1]+(r+10)*math.sin(a),.3)
        ink(d,'',.6)
    else:
        ink(rectd(x,top,w,h)); ink(wob(x,top+14,x+w,top+14,.3),'',.6)
        ink(rectd(x+4,top+20,w-8,16)+rectd(x+4,top+40,w-8,18),'',.6)
        d=''
        for k in range(7):
            a=math.radians(212+k*(116/6)); c=(cx,top+12)
            d+=wob(c[0]+16*math.cos(a),c[1]+16*math.sin(a),c[0]+25*math.cos(a),c[1]+25*math.sin(a),.3)
        ink(d,'',.6)
    sketch(rectd(x,top,w,h))
    # white marble stoop (Baltimore)
    for i,(y0,y1,ww) in enumerate([(top+h,top+h+5,w+8),(top+h+5,top+h+10,w+18),(top+h+10,G,w+28)]):
        out.append(f'<path class="marble ink" data-w="0.8" d="{rectd(cx-ww/2,y0,ww,y1-y0)}"/>')
    ink(wob(cx+w/2+12,top+h-26,cx+w/2+15,G,.4),'',.6)  # rail

lit=0; excl={}
for hi,h in enumerate(houses):
    x0,x1=h['x0'],h['x1']; E=[]
    if hi==0:
        ink(f"M{x0} {G}V98"+wob(36,98,196,86)[0:0]+f"L196 86",'',1.2)
        ink(wob(30,96,198,83)+wob(30,96,30,99,.2),'',1)
        ink("M128 92V58Q137 50 146 58V90",'',1)  # chimney
        ink(wob(131,62,143,62,.3),'',.5)
        sketch(f"M{x0} {G}V98L196 86")
    elif hi==1:
        t=h['top']; ink(f"M{x0} {G}V{t}H{x1}V{G}",'',1.2)
        ink(wob(190,t-4,382,t-4)+wob(190,t-8,382,t-8),'',1)
        ink(wob(x0,t+20,x1,t+20),'',1)
        ink(rectd(190,t-8,12,26)+rectd(370,t-8,12,26),'',.8)
        ink(''.join(wob(x,t+11,x,t+16,.2) for x in range(206,368,6)),'',.25)
        sketch(f"M{x0} {G}V{t}H{x1}V{G}")
    else:
        t=h['top']; ink(f"M{x0} {t}H{x1}V{G}",'',1.2)
        ink(wob(370,t-4,562,t-4)+wob(372,t-8,560,t-8),'',1)
        ink(wob(x0,t+18,x1,t+18),'',1)
        ink(rectd(552,t-8,10,24),'',.8)
        ink(''.join(wob(x,t+9,x,t+14,.2) for x in range(386,550,6)),'',.25)
        sketch(f"M{x0} {t}H{x1}V{G}")
    for top in h['rows']:
        for cx in h['cols']:
            window(cx,top,lit); lit+=1; E.append((cx-WW/2-5,cx+WW/2+5,top-24,top+WH+4))
    gx,gt=h['gw']; window(gx,gt,lit); lit+=1; E.append((gx-WW/2-5,gx+WW/2+5,gt-24,gt+WH+4))
    dc,dt,dw,dh,ar=h['door']; door(dc,dt,dw,dh,ar); E.append((dc-dw/2-17,dc+dw/2+17,dt-26,G+1))
    # brick hatching, broken around openings
    ytop=(86 if hi==0 else h['top']+(22 if hi==1 else 20))+6
    hatch=[]
    y=ytop
    while y<G-2:
        xa=x0+2 if hi else max(x0+2,36+(98-(y-4))*160/12)
        segs=[(xa,x1-2)]
        for (a,b,ya,yb) in E:
            if ya<=y<=yb:
                ns=[]
                for (s,e) in segs:
                    if b<=s or a>=e: ns.append((s,e))
                    else:
                        if a>s: ns.append((s,a))
                        if b<e: ns.append((b,e))
                segs=ns
        for s,e in segs:
            s2=s+random.uniform(0,3); e2=e-random.uniform(0,3)
            if e2-s2>4: hatch.append(wob(s2,y+random.uniform(-.4,.4),e2,y+random.uniform(-.4,.4),.6))
        y+=6.5
    # group hatching a few rows per path so it draws in sweeps
    for i in range(0,len(hatch),3): ink(''.join(hatch[i:i+3]),'h',.28)

def shrub(xa,xb,seed):
    random.seed(seed); d=f"M{f(xa)} {G}"; x=xa
    for row,yb in [(0,G),(1,G-7)]:
        x=xa+row*6; d+=f"M{f(x)} {f(yb)}"
        while x<xb-row*6:
            r=random.uniform(4,7); dx=random.uniform(5,8); x+=dx
            d+=f"A{f(r)} {f(r)} 0 1 1 {f(x)} {f(yb+random.uniform(-2,2))}"
    ink(d,'',.35)
shrub(104,176,1); shrub(204,296,2); shrub(384,476,3)
ink(wob(6,G,654,G,1.2),'',1.2); ink(wob(6,332,654,332,1.2),'',1)
FX,FY,FW,FH=588,146,66,44  # Maryland flag on a pole at the right
ink(f"M{FX} {G}V{FY-6}",'',1.4); ink(f"M{FX-3} {FY-6}a3 3 0 1 1 6 0a3 3 0 1 1 -6 0",'',.4)
sketch(f"M{FX} {G}V{FY-6}"); sketch(rectd(FX,FY,FW,FH))
ink(''.join(wob(x,G+3,x-6,329,.3) for x in range(40,650,70)),'',.4)
sketch(f"M6 {G}H654")
for yy in (118,188,248,86,164): sketch(f"M14 {yy}H646")


def mdflag():
    """State flag of Maryland: Calvert (gold/black paly with a counterchanged bend) and
    Crossland (red/white quarterly with a counterchanged bottony cross) quarters."""
    GOLD,BLK,RED,WHT='#EAAA00','#1B1B1B','#C8102E','#FFFFFF'
    w,h=FW/2,FH/2; s=['<defs>']
    s.append(f'<clipPath id="mdBend"><path d="M0 0L{w*.22} 0L{w} {h*.78}L{w} {h}L{w*.78} {h}L0 {h*.22}Z"/></clipPath>')
    s.append(f'<clipPath id="mdCross"><path d="M{w/2-1.6} 0h3.2v{h/2-1.6}h{w/2-1.6+1.6}v3.2h-{w/2-1.6+1.6}v{h/2-1.6}h-3.2v-{h/2-1.6}h-{w/2-1.6}v-3.2h{w/2-1.6}z"/></clipPath>')
    def pales(a,b): return ''.join(f'<rect x="{i*w/6:.2f}" y="0" width="{w/6+.05:.2f}" height="{h}" fill="{a if i%2==0 else b}"/>' for i in range(6))
    s.append(f'<g id="mdCalvert">{pales(GOLD,BLK)}<g clip-path="url(#mdBend)">{pales(BLK,GOLD)}</g></g>')
    def quarters(a,b): return f'<rect width="{w/2}" height="{h/2}" fill="{a}"/><rect x="{w/2}" width="{w/2}" height="{h/2}" fill="{b}"/><rect y="{h/2}" width="{w/2}" height="{h/2}" fill="{b}"/><rect x="{w/2}" y="{h/2}" width="{w/2}" height="{h/2}" fill="{a}"/>'
    bot=''.join(f'<circle cx="{x}" cy="{y}" r="1.5"/>' for x,y in [(w/2-1.8,1.2),(w/2+1.8,1.2),(w/2-1.8,h-1.2),(w/2+1.8,h-1.2),(1.2,h/2-1.8),(1.2,h/2+1.8),(w-1.2,h/2-1.8),(w-1.2,h/2+1.8)])
    s.append(f'<clipPath id="mdBot">{bot}</clipPath>')
    s.append(f'<g id="mdCrossland">{quarters(WHT,RED)}<g clip-path="url(#mdCross)">{quarters(RED,WHT)}</g><g clip-path="url(#mdBot)">{quarters(RED,WHT)}</g></g>')
    s.append(f'<g id="mdFlag"><use href="#mdCalvert"/><use href="#mdCrossland" x="{w}"/><use href="#mdCrossland" y="{h}"/><use href="#mdCalvert" x="{w}" y="{h}"/><rect width="{FW}" height="{FH}" fill="none" stroke="#fff" stroke-width=".8"/></g>')
    N=15; s.append(''.join(f'<clipPath id="mdS{i}"><rect x="{i*FW/N-.3:.2f}" y="-2" width="{FW/N+.6:.2f}" height="{FH+4}"/></clipPath>' for i in range(N)))
    s.append('</defs>')
    sl=''.join(f'<g class="fslice" data-i="{i}" data-n="{N}"><use href="#mdFlag" clip-path="url(#mdS{i})"/></g>' for i in range(N))
    return ''.join(s)+f'<g id="ldrFlag" transform="translate({FX},{FY}) scale(0,1)">{sl}</g>'

art=f'''<svg viewBox="0 0 660 340" focusable="false">
  {mdflag()}
  <g class="sketch" id="ldrSketch">{''.join(sk)}</g>
  <g id="ldrInk">{''.join(out)}</g>
  <!-- lawn flamingo (Hampden), rises out of the shrubs -->
  <clipPath id="abvGround"><rect x="0" y="0" width="660" height="{G}"/></clipPath>
  <g clip-path="url(#abvGround)"><g id="ldrFlamingo" transform="translate(0,60)">
    <path d="M176 {G}V292M181 {G}V294" stroke="#F2938C" stroke-width="1.6" fill="none"/>
    <path d="M166 282c2-9 20-11 26-2-4 9-22 10-26 2z" fill="#F2938C" stroke="#fff" stroke-width="1"/>
    <path d="M170 282c-6-6-8-14-2-22 3-4 9-3 9 2" fill="none" stroke="#F2938C" stroke-width="3" stroke-linecap="round"/>
    <circle cx="176" cy="260" r="3.4" fill="#F2938C" stroke="#fff" stroke-width=".8"/>
    <path d="M179 259l6 3-4 3" fill="#1B1B1B" stroke="#fff" stroke-width=".6" stroke-linejoin="round"/>
    <circle cx="176.6" cy="259" r=".8" fill="#1B1B1B"/>
  </g></g>
  <!-- blue crab, steamed -->
  <g id="ldrCrab" transform="translate(260,0)"><g id="ldrCrabBody"><g transform="translate(468 323) scale(1.2) translate(-468 -323)">
    <path d="M454 324l-7 4M455 327l-7 5M457 329l-5 6M482 324l7 4M481 327l7 5M479 329l5 6" stroke="#D54309" stroke-width="2" stroke-linecap="round"/>
    <ellipse cx="468" cy="323" rx="14" ry="7.5" fill="#D54309" stroke="#fff" stroke-width="1"/>
    <path d="M463 317v-4M473 317v-4" stroke="#fff" stroke-width="1.2"/><circle cx="463" cy="312" r="1.6" fill="#1B1B1B" stroke="#fff" stroke-width=".7"/><circle cx="473" cy="312" r="1.6" fill="#1B1B1B" stroke="#fff" stroke-width=".7"/>
    <g id="ldrClawL"><path d="M456 320l-8-7" stroke="#D54309" stroke-width="2.4" stroke-linecap="round"/><path d="M448 313c-5-1-6-6-2-8l2 4 2-4c3 3 2 7-2 8z" fill="#D54309" stroke="#fff" stroke-width=".7"/></g>
    <g id="ldrClawR"><path d="M480 320l8-7" stroke="#D54309" stroke-width="2.4" stroke-linecap="round"/><path d="M488 313c5-1 6-6 2-8l-2 4-2-4c-3 3-2 7 2 8z" fill="#D54309" stroke="#fff" stroke-width=".7"/></g>
  </g></g></g>
  <!-- Baltimore oriole, lands on the cornice -->
  <g id="ldrOriole" transform="translate(340,-80)"><g id="ldrOrioleBody"><g transform="translate(300 40) scale(1.6) translate(-300 -40)">
    <path d="M292 30l-9 5 3-6z" fill="#1B1B1B" stroke="#fff" stroke-width=".7"/>
    <ellipse cx="300" cy="30" rx="9" ry="6" fill="#FF8A1C" stroke="#fff" stroke-width=".8"/>
    <circle cx="308" cy="24" r="4.6" fill="#1B1B1B" stroke="#fff" stroke-width=".8"/>
    <path d="M312 23l5 1.5-5 1.5z" fill="#A9AEB1"/>
    <circle cx="309.5" cy="23" r=".9" fill="#fff"/>
    <path d="M298 36v4M302 36v4" stroke="#fff" stroke-width="1"/>
    <path id="ldrWing" d="M297 28c-6-2-10 1-11 4 5 1 10 0 12-2z" fill="#1B1B1B" stroke="#fff" stroke-width=".8"/>
  </g></g>
  <text id="ldrNote" x="330" y="22" fill="#FFBE2E" font-size="13" opacity="0">♪</text></g>
</svg>'''
here=os.path.dirname(os.path.abspath(__file__))
open(os.path.join(here,'..','page','stage.html'),'w').write(art)
print(len(out),'ink strokes,',len(art)//1024,'KB')
