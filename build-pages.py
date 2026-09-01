from pathlib import Path
root = Path(__file__).parent
t = (root/'page-template.html').read_text(encoding='utf-8')

pages = [
('workflows.html','AI-Optimized Workflows','AI-OPTIMIZED WORKFLOWS','Your apps. One intelligent flow.','Connect the tools your team already uses and let an AI operating layer turn scattered work into a clear, repeatable path.','What changes when work flows','A connected workflow can capture the request, route the next action, keep people informed, and surface the result — without asking your team to babysit every step.','Automated handoffs','Fewer dropped balls','Clear ownership at every stage','A workflow that improves as it runs','From intake to completion, the right action happens at the right time.','SlamDunk turns your existing apps into a smarter way to work.'),
('agents.html','Autonomous Agents','AUTONOMOUS AGENTS','An AI team that keeps moving.','BuddyFetch agents plan, act, and deliver across complex tasks — with the context and persistence to take work from start to finish.','Built for action','Agents do more than answer questions. They understand the objective, choose the next step, use the tools available, and report back when the job is done.','Plan the objective','Use connected tools','Adapt to new information','Deliver a clear result','You stay in control while the work moves forward.','Give your team leverage, not another dashboard to manage.'),
('marketing.html','Built-in Marketing Skills','BUILT-IN MARKETING SKILLS','More conversations. Less busywork.','Put practical marketing execution on demand: research, outreach, follow-up, content, and reporting working together as one growth system.','Marketing that ships','Good marketing is consistent, responsive, and close to the customer. Agentic workflows help you keep momentum without adding another full-time workload.','Research the right audience','Create useful content','Reach out with context','Follow up while interest is warm','Every touchpoint gets sharper with real feedback.','Turn attention into conversations — then conversations into revenue.'),
('smart.html','Scalable. Smart. Adaptable.','SCALABLE SYSTEMS','A system that gets better under pressure.','Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.','Designed for the next level','Start with one high-value workflow. Expand when it works. Your AI team should adapt to your process, your people, and the pace of your growth.','Start focused','Scale what works','Keep humans in the loop','Measure the impact','Simple enough to launch. Flexible enough to last.','Growth should add possibility — not piles of repetitive work.'),
('future.html','Wild Wide Open Future','WILD WIDE OPEN FUTURE','Open the door to what is next.','Agentic AI is not a single feature. It is a new way to imagine what your team can accomplish when execution is no longer the bottleneck.','The future is practical','The best future-facing systems begin with a real business problem today. We help you create the first win, then build from evidence into opportunity.','See possibilities sooner','Prototype without heavy lift','Turn ideas into operating systems','Keep upgrading the advantage','The path is open — and you do not have to walk it alone.','Let’s build the version of your business that has room to run.')
]
for fn,title,kicker,heading,lead,section,quote,*rest in pages:
    # rest = 4 list items, quote_by
    items, quote_by = rest[:4], rest[4]
    cards = ''.join(f'      <article class="content-card"><div class="number">0{i+1:02d}</div><h2>{x}</h2><p>{y}</p></article>\n' for i,(x,y) in enumerate(zip(items, [quote_by, 'Built around the work that matters most.', 'Clearer action with less friction.', 'Momentum you can measure.'])))
    lis = ''.join(f'      <li>{x}</li>\n' for x in items)
    vals={'TITLE':title,'DESCRIPTION':lead,'KICKER':kicker,'HEADING':heading,'LEAD':lead,'CARDS':cards,'SECTION_TITLE':section,'LIST':lis,'QUOTE':quote,'QUOTE_BY':quote_by}
    out=t
    for k,v in vals.items(): out=out.replace('{{'+k+'}}',v)
    (root/fn).write_text(out,encoding='utf-8')
print('built',len(pages),'pages')
