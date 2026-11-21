import json, base64, sys, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..'))
P=lambda *a: os.path.join(*a)
MC = "https://qcdesigns.me/p/022d282b"
PROTO = sys.argv[1] if len(sys.argv)>1 else "prototype/"
needs = [
 {"name":"Journey mapping and service blueprints","listPill":"Strong","panelPill":"Strong match",
  "title":"I map the whole service, including where it breaks down",
  "buttons":[{"label":"Full case study","href":MC}],
  "quote":"Map current-state journeys to create service blueprints and understand structural bottlenecks, user pain points and technological process issues.",
  "why":[["Mentor Collective","Using data from 100+ participants over 14 studies, I mapped first-time journeys for mentors and mentees from recruitment to program end, covering thinking, feeling, pain points, touchpoints and improvements."],
         ["Mentor Collective","Point of failure: my analysis uncovered a widespread ghosting issue, so I created two more journeys for the ghosted mentor and the ghosting mentee."],
         ["farmers.gov","Found an upstream bottleneck: by interviewing field and program staff, I learned why producers arrived at conservation visits unprepared, before any screen was involved."]],
  "images":[{"src":"img/journeys.jpg","crop":290,"pos":"50% 18%","alt":"The first-year mentorship journey map for mentors and mentees, with a section on what happens when a relationship goes quiet","cap":"Journey maps built from 14 studies (~100 participants). Click to enlarge."}]},
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
 {"name":"Plain language and accessibility","listPill":"In-progress","panelPill":"Partial match","partial":True,
  "title":"I've tested applicant-facing words. Notices and decision letters are next.",
  "quote":"Plain language guidance for applicant-facing content, including instructions, notices, status updates, and decision letters, so applicants know what is required, where their request stands, and what comes next.",
  "why":[["VA.gov","Designed an informed-choice page Veterans could act on: 8 of 9 understood their options."],
         ["VA.gov","Surfaced a wording finding that changed the design: 7 of 9 Veterans couldn't imagine skipping a section and still getting a fair rating. Optional rarely feels optional."],
         ["VA.gov","Worked with accessibility staff so the multi-response pattern met WCAG and could be reused across VA."],
         ["My plan","Start with the status updates and notices applicants see most, rewrite them in plain language, and test them with applicants before rolling them out."]],
  "template":"plain"},
 {"name":"Bridging policy, product and engineering","listPill":"Strong","panelPill":"Strong match",
  "title":"I get policy, product and engineering partners moving in one direction",
  "buttons":[{"label":"VA Design System","href":"https://design.va.gov/"}],
  "quote":"Act as a Coordinator between policy teams and technical developers, ensuring digital solutions accurately reflect regulatory requirements without sacrificing usability.",
  "why":[["Mentor Collective","Created a new workflow adopted by all 3 teams, bringing engineers, a product manager, a content designer and a learning lead onto one product vision."],
         ["farmers.gov","Usability-tested the design system with 6 designers from 4 teams: 98% task completion and 6 recommendations, from navigation to a change log."],
         ["VA.gov","Drove the research plan, conversation guide, prototype and timeline for the Copy of Submission study through changing circumstances."]],
  "images":[{"src":"img/workflow.jpg","alt":"Team Nala new process in four stages: discovery and research, team spikes the roadmap, design and developer estimation, build","cap":"The workflow I created for all teams: research feeds the roadmap and developer estimates."}]},
 {"name":"Permitting and housing","listPill":"In-progress","panelPill":"Partial match","partial":True,
  "title":"I've redesigned public applications. I haven't worked on permits yet.",
  "quote":"Develop new workflows to rebuild the permit and license journey at the agency level, prioritizing housing construction.",
  "why":[["farmers.gov","Closest match: producers apply for USDA conservation programs much like builders apply for permits. I proposed a step-by-step tool and simpler navigation (Fund, Manage, Conserve) so they arrive prepared."],
         ["VA.gov","Worked inside regulatory form logic: optional sections and evidence routing, where the rules decide what an applicant has to provide."],
         ["My plan","Start where PLAT starts: shadow county permit staff and sit in on a stalled housing review before proposing any fix, then test it small and measure."]]},
]
t = open(P(HERE,'template.html')).read()
t = t.replace('{{STAGE}}', open(P(HERE,'stage.html')).read())
t = t.replace('{{VA_DECK}}', '#work').replace('{{VA_DECK_ATTR}}', ' aria-disabled="true" title="Link to be added"')
logos = json.load(open(P(HERE,'..','animation','logos.json')))
t = t.replace('{{LOGOS}}', json.dumps(logos))
t = t.replace('{{NEEDS}}', json.dumps(needs, ensure_ascii=False).replace('</', '<\\/'))
open(P(ROOT,'index.html'),'w').write(t)
# self-contained build: inline the images
s = t.replace('"src": "prototype/"','"src": "https://qcdesignsme.github.io/DesignPLAT/prototype/"').replace('"href": "prototype/"','"href": "https://qcdesignsme.github.io/DesignPLAT/prototype/"')
for name in ['journeys','admin-flow','handoff','workflow']:
    b = base64.b64encode(open(P(ROOT,'img',f'{name}.jpg'),'rb').read()).decode()
    s = s.replace(f'img/{name}.jpg', 'data:image/jpeg;base64,'+b)
open(P(HERE,'qian-chen-maryland-plat.html'),'w').write(s)
print(len(t)//1024, 'KB index;', len(s)//1024, 'KB self-contained')
