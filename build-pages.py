from pathlib import Path
root = Path(__file__).parent
template = (root / 'page-template.html').read_text(encoding='utf-8')

# Side bullet list — identical to Home page features (icon, title, tagline, link)
features = [
  ('workflows.html', 'AI-Optimized Workflows', 'Utilizing new or existing Apps.',
   '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3.5l3 3-9.5 9.5 1.5 1.5L10.5 8l3 3"/><path d="M14 2.5l7.5 7.5-2 2L12 4.5z"/><path d="M2.5 21.5l3-3"/></svg>'),
  ('agents.html', 'Autonomous Agents', 'Managed By Phone, Text &amp; Emails.',
   '<svg viewBox="0 0 24 24"><polygon points="13 2 4 14 11 14 10 22 20 10 13 10 13 2" fill="#ffffff"/></svg>'),
  ('marketing.html', 'Built In Marketing Skills', 'Mass Calling, Text &amp; Emailing.',
   '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.5"><circle cx="10.5" cy="13.5" r="9"/><circle cx="10.5" cy="13.5" r="5.7"/><circle cx="10.5" cy="13.5" r="2.2" fill="#ffffff"/><path d="M21 3 14 10M18.2 3.8l-1.7 1.7M20.2 5.8l-1.7 1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
  ('smart.html', 'Scalable. Smart. Adaptable.', 'Consistency, 24/7. Built to scale.',
   '<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 17 10 11l4 4 6-8"/><path d="M15 7h5v5"/></svg>'),
  ('future.html', 'Wild Wide Open Future', 'Enhanced Features.',
   '<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="M8.5 12.2l2.3 2.3 4.7-4.9"/></svg>'),
]

pages = [
  ('workflows.html', 'AI-Optimized Workflows', 'Your apps. One intelligent flow.',
   'Connect the tools your team already uses and let an AI operating layer turn scattered work into a clear, repeatable path.'),
  ('agents.html', 'Autonomous Agents', 'An AI team that keeps moving.',
   'BuddyFetch agents plan, act, and deliver across complex tasks — with the context and persistence to take work from start to finish.'),
  ('marketing.html', 'Built-in Marketing Skills', 'More conversations. Less busywork.',
   'Put practical marketing execution on demand: research, outreach, follow-up, content, and reporting working together as one growth system.'),
  ('smart.html', 'Scalable. Smart. Adaptable.', 'A system that gets better under pressure.',
   'Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.'),
  ('future.html', 'Wild Wide Open Future', 'Open the door to what is next.',
   'Agentic AI is not a single feature. It is a new way to imagine what your team can accomplish when execution is no longer the bottleneck.'),
]

def build_features(active_file):
    out = []
    for fname, ftitle, fdesc, fic in features:
        active = ' active' if fname == active_file else ''
        out.append(
            f'          <div class="feature{active}">\n'
            f'            <a class="feature-icon" href="{fname}" aria-label="{ftitle}">{fic}</a>\n'
            f'            <div>\n'
            f'              <h3><a href="{fname}">{ftitle}</a></h3>\n'
            f'              <p>{fdesc}</p>\n'
            f'            </div>\n'
            f'          </div>'
        )
    return '\n'.join(out)

for filename, title, heading, lead in pages:
    html = template
    values = {'TITLE': title, 'DESCRIPTION': lead, 'HEADING': heading, 'LEAD': lead,
              'FEATURES': build_features(filename)}
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    (root / filename).write_text(html, encoding='utf-8')
print(f'built {len(pages)} pages')