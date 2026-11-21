import json, base64, sys, os, re
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
P=lambda *a: os.path.join(*a)
MC = "https://qcdesigns.me/p/022d282b"
PROTO = sys.argv[1] if len(sys.argv)>1 else "prototype/"
needs = [
 {"name":"Journey mapping and service blueprints","listPill":"Strong","panelPill":"Strong match",
  "title":"I map the whole service, including where it breaks down",
  "buttons":[{"label":"Full case study","href":MC},{"label":"Interactive journey map","href":"https://qcdesignsme.github.io/mentorship-journey/"}],
  "quote":"Map current-state journeys to create service blueprints and understand structural bottlenecks, user pain points and technological process issues.",
  "why":[["Mentor Collective","Using data from 100+ participants over 14 studies, I mapped first-time journeys for mentors and mentees from recruitment to program end, covering thinking, feeling, pain points, touchpoints and improvements."],
         ["Mentor Collective","Point of failure: my analysis uncovered a widespread ghosting issue, so I created two more journeys for the ghosted mentor and the ghosting mentee."],
         ["farmers.gov","Found an upstream bottleneck: by interviewing field and program staff, I learned why producers arrived at conservation visits unprepared, before any screen was involved."]],
  "embed":{"src":"https://qcdesignsme.github.io/mentorship-journey/","title":"Interactive mentorship journey map, Mentor Collective","poster":"img/journeys.jpg","posterAlt":"The first-year mentorship journey map for mentors and mentees, with a section on what happens when a relationship goes quiet","cap":"Live journey map built from 14 studies (~100 participants). Explore it here.","live":True,"pdf":"docs/mentorship-journey-map.pdf"}},
 {"name":"Research with applicants and agency staff","listPill":"Strong","panelPill":"Strong match",
  "title":"I research with the people who apply and the staff who review",
  "quote":"Design and facilitate user-experience engagements (interviews, surveys, usability tests) with applicants and agency staff.",
  "why":[["VA.gov","Co-ran concept testing of the VA mental health claim form with 9 Veterans, with safeguards: screening calls that named sensitive topics, optional recordings and breaks, few observers."],
         ["farmers.gov","Interviewed USDA field and program staff, the people who prepare applicants, to see the process from the reviewer's side."],
         ["Mentor Collective","Ran four rounds of testing with 8 program managers, the staff who set up programs for participants."]],
  "template":"flow0781"},
 {"name":"Prototypes engineers can build from","listPill":"Strong","panelPill":"Strong match",
  "title":"I hand engineers working prototypes built on the design system",
  "buttons":[{"label":"Full case study","href":MC},{"label":"Interactive Prototype","href":PROTO}],
  "quote":"Deliver recommendations in a form DoIT can build from (e.g. clickable prototypes) aligned to the state's design system.",
  "why":[["Mentor Collective","Program managers worked in a legacy tool with 50%+ error rates. Testing showed they reuse tasks rather than create them, so I rebuilt the flow library-first: find, review, adjust, confirm."]],

  "embed":{"src":PROTO,"title":"Interactive prototype: Mentor Collective Add Task(s) flow, sample data","poster":"img/admin-flow.jpg","posterAlt":"Redesigned Add Task(s) flow: search, filters, a task table and a Selected Tasks panel","cap":"After: a library-first flow with clear steps and inline guidance. Try it here (sample data)."}},
]
t = open(P(HERE,'template.html')).read()
t = t.replace('{{STAGE}}', open(P(HERE,'stage.html')).read())
t = t.replace('{{VA_DECK}}', 'https://docs.google.com/presentation/d/1PJMzhC_bHXLRla_EMOYpd7CS-TB2OLsN/edit?usp=sharing&amp;ouid=106767017034375755000&amp;rtpof=true&amp;sd=true').replace('{{VA_DECK_ATTR}}', '')
# every link to another site opens in a new tab, with a screen-reader hint
def _newtab(m):
    tag, inner = m.group(1), m.group(2)
    if 'target=' in tag: return m.group(0)
    return tag + ' target="_blank" rel="noopener">' + inner + '<span class="sr"> (opens in a new tab)</span></a>'
t = re.sub(r'(<a\b[^>]*\bhref="https?:[^"]*"[^>]*)>(.*?)</a>', _newtab, t, flags=re.S)
logos = json.load(open(P(HERE,'..','animation','logos.json')))
t = t.replace('{{LOGOS}}', json.dumps(logos))
t = t.replace('{{NEEDS}}', json.dumps(needs, ensure_ascii=False).replace('</', '<\\/'))
open(P(ROOT,'index.html'),'w').write(t)
# self-contained build: inline the images
s = t.replace('"pdf": "docs/','"pdf": "https://qcdesignsme.github.io/DesignPLAT/docs/').replace('"src": "prototype/"','"src": "https://qcdesignsme.github.io/DesignPLAT/prototype/"').replace('"href": "prototype/"','"href": "https://qcdesignsme.github.io/DesignPLAT/prototype/"')
for name in ['journeys','admin-flow','handoff','workflow']:
    b = base64.b64encode(open(P(ROOT,'img',f'{name}.jpg'),'rb').read()).decode()
    s = s.replace(f'img/{name}.jpg', 'data:image/jpeg;base64,'+b)
open(P(HERE,'qian-chen-maryland-plat.html'),'w').write(s)
print(len(t)//1024, 'KB index;', len(s)//1024, 'KB self-contained')
