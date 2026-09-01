from pathlib import Path
root = Path(__file__).parent
template = (root / 'page-template.html').read_text(encoding='utf-8')

pages = [
  ('workflows.html', 'AI-Optimized Workflows', 'AI-OPTIMIZED WORKFLOWS', 'Your apps. One intelligent flow.', 'Connect the tools your team already uses and let an AI operating layer turn scattered work into a clear, repeatable path.', ['Automated handoffs', 'Fewer dropped balls', 'Clear ownership at every stage', 'A workflow that improves as it runs']),
  ('agents.html', 'Autonomous Agents', 'AUTONOMOUS AGENTS', 'An AI team that keeps moving.', 'BuddyFetch agents plan, act, and deliver across complex tasks — with the context and persistence to take work from start to finish.', ['Plan the objective', 'Use connected tools', 'Adapt to new information', 'Deliver a clear result']),
  ('marketing.html', 'Built-in Marketing Skills', 'BUILT-IN MARKETING SKILLS', 'More conversations. Less busywork.', 'Put practical marketing execution on demand: research, outreach, follow-up, content, and reporting working together as one growth system.', ['Research the right audience', 'Create useful content', 'Reach out with context', 'Follow up while interest is warm']),
  ('smart.html', 'Scalable. Smart. Adaptable.', 'SCALABLE. SMART. ADAPTABLE.', 'A system that gets better under pressure.', 'Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.', ['Start focused', 'Scale what works', 'Keep humans in the loop', 'Measure the impact']),
  ('future.html', 'Wild Wide Open Future', 'WILD WIDE OPEN FUTURE', 'Open the door to what is next.', 'Agentic AI is not a single feature. It is a new way to imagine what your team can accomplish when execution is no longer the bottleneck.', ['See possibilities sooner', 'Prototype without heavy lift', 'Turn ideas into operating systems', 'Keep upgrading the advantage']),
]

for filename, title, kicker, heading, lead, points in pages:
    html = template
    values = {'TITLE': title, 'DESCRIPTION': lead, 'KICKER': kicker, 'HEADING': heading, 'LEAD': lead}
    active = filename.replace('.html', '')
    for key in ['WORKFLOWS', 'AGENTS', 'MARKETING', 'SMART', 'FUTURE']:
        values['ACTIVE_' + key] = 'active' if key.lower() == active else ''
    points_html = ''.join(f'          <li><a class="point-icon" href="#" aria-hidden="true">✦</a><span>{p}</span></li>\n' for p in points)
    values['POINTS'] = points_html
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    (root / filename).write_text(html, encoding='utf-8')
print(f'built {len(pages)} pages')
