from pathlib import Path
root = Path(__file__).parent
template = (root / 'page-template.html').read_text(encoding='utf-8')
second_home = (root / 'second-home-template.html').read_text(encoding='utf-8')

def svg(paths, extra=''):
    return f'<svg width="21.25" height="21.25" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'

# --- Main menu: the 5 original bullets (each icon clickable -> its page) ---
main_features = [
  ('workflows.html', 'AI-Optimized Workflows', 'Utilizing new or existing Apps.',
   '<svg width="21.25" height="21.25" viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3.5l3 3-9.5 9.5 1.5 1.5L10.5 8l3 3"/><path d="M14 2.5l7.5 7.5-2 2L12 4.5z"/><path d="M2.5 21.5l3-3"/></svg>'),
  ('agents.html', 'Autonomous Agents', 'Managed By Phone, Text &amp; Emails.',
   '<svg width="21.25" height="21.25" viewBox="0 0 24 24"><polygon points="13 2 4 14 11 14 10 22 20 10 13 10 13 2" fill="#ffffff"/></svg>'),
  ('marketing.html', 'Built In Marketing Skills', 'Mass Calling, Text &amp; Emailing.',
   '<svg width="21.25" height="21.25" viewBox="0 0 24 24" fill="none" stroke-width="1.5"><circle cx="10.5" cy="13.5" r="9"/><circle cx="10.5" cy="13.5" r="5.7"/><circle cx="10.5" cy="13.5" r="2.2" fill="#ffffff"/><path d="M21 3 14 10M18.2 3.8l-1.7 1.7M20.2 5.8l-1.7 1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
  ('smart.html', 'Scalable. Smart. Adaptable.', 'Consistency, 24/7. Built to scale.',
   svg('<path d="M4 17 10 11l4 4 6-8"/><path d="M15 7h5v5"/>')),
  ('future.html', 'Wild Wide Open Future', 'Enhanced Features.',
   svg('<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="M8.5 12.2l2.3 2.3 4.7-4.9"/>')),
]

# --- Wild Wide Open Future: custom bullets, each opens one level down ---
custom_features = [
  ('custom-agents.html', 'Custom Pre-Loaded Agents', 'Complete certain tasks or operate specific websites.',
   svg('<path d="M12 2 3 7v10l9 5 9-5V7z"/><path d="M3 7l9 5 9-5"/><path d="M12 12v10"/>')),
  ('company-brain.html', 'Company Brain', "Accessible AI and Humans. Knowledge Base in Google's new OKF format.",
   svg('<rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>')),
  ('distribution.html', 'Distribution of Intelligence', 'Delegated Permission Authority.',
   svg('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M8.2 11l7.6-4M8.2 13l7.6 4"/>')),
  ('virtual-mascot.html', 'Custom Virtual Company Mascot', 'Unique and Fun Interactions.',
   svg('<circle cx="12" cy="12" r="9"/><path d="M9 10h.01"/><path d="M15 10h.01"/><path d="M8.5 14a5 5 0 0 0 7 0"/>')),
  ('avatar-app.html', 'AI Avatar App', 'Managed BuddyFetch AIs through LIVE app.',
   svg('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>')),
  ('mcp-server.html', 'MCP Server Conversion of Website', 'Allows AI to interact with your Website.',
   svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18"/>')),
]

# --- The 5 original bullet pages ---
pages = [
  ('workflows.html', 'AI-Optimized Workflows', 'Your apps. One intelligent flow.',
   'Connect the tools your team already uses and let an AI operating layer turn scattered work into a clear, repeatable path.'),
  ('agents.html', 'Autonomous Agents', 'An AI team that keeps moving.',
   'BuddyFetch agents plan, act, and deliver across complex tasks — with the context and persistence to take work from start to finish.'),
  ('marketing.html', 'Built-in Marketing Skills', 'More conversations. Less busywork.',
   'Put practical marketing execution on demand: research, outreach, follow-up, content, and reporting working together as one growth system.'),
  ('smart.html', 'Scalable. Smart. Adaptable.', 'A system that gets better under pressure.',
   'Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.'),
]

# --- Level-down pages under Wild Wide Open Future ---
future_pages = [
  ('custom-agents.html', 'Custom Pre-Loaded Agents', 'Agents ready on day one.',
   'BuddyFetch agents arrive pre-loaded and trained for specific tasks — completing defined work or operating specific websites from day one, with no setup marathon required.'),
  ('company-brain.html', 'Company Brain', 'One brain for your entire company.',
   "A knowledge base accessible to both AI and humans, built on Google's new OKF format — so every agent and every teammate draws from the same living source of truth."),
  ('distribution.html', 'Distribution of Intelligence', 'The right intelligence, in the right hands.',
   'Distribute intelligence across your organization with delegated permission authority — every agent knows exactly what it can access, act on, and approve.'),
  ('virtual-mascot.html', 'Custom Virtual Company Mascot', 'A face and personality for your brand.',
   'A custom virtual company mascot creates unique and fun interactions — turning routine support into moments your customers remember.'),
  ('avatar-app.html', 'AI Avatar App', 'Your AI team, live in your pocket.',
   'Manage your BuddyFetch AIs through a LIVE avatar app — see your agents, steer their work, and talk with them in real time from anywhere.'),
  ('mcp-server.html', 'MCP Server Conversion of Website', 'Make your website AI-native.',
   'Convert your existing website with an MCP server so AI can interact with it directly — your business becomes part of the agentic web.'),
]

def render(template, values):
    html = template
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    return html

def feature_list(items, active_file=None, active_main=None):
    out = []
    for fname, ftitle, fdesc, fic in items:
        is_active = fname == active_file or fname == active_main
        active = ' active' if is_active else ''
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

main_menu_html = feature_list(main_features)
custom_list_all = feature_list(custom_features)

# 1) Second Home: Wild Wide Open Future
future_html = second_home.replace('{{CUSTOM_FEATURES}}', feature_list(custom_features))
future_html = future_html.replace('{{MAIN_FEATURES}}', main_menu_html)
(root / 'future.html').write_text(future_html, encoding='utf-8')

# 2) The 5 original bullet pages (side list = main menu)
for filename, title, heading, lead in pages:
    values = {'TITLE': title, 'DESCRIPTION': lead, 'HEADING': heading, 'LEAD': lead,
              'BACK_HREF': 'index.html', 'BACK_LABEL': '← Back to home', 'LIST_LABEL': '',
              'FEATURES': feature_list(main_features, active_main=filename)}
    html = template
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    (root / filename).write_text(html, encoding='utf-8')

# 3) Level-down pages under Wild Wide Open Future (side list = custom bullets)
for filename, title, heading, lead in future_pages:
    values = {'TITLE': title, 'DESCRIPTION': lead, 'HEADING': heading, 'LEAD': lead,
              'BACK_HREF': 'future.html', 'BACK_LABEL': '← Wild Wide Open Future',
              'LIST_LABEL': 'THE BEGINNING',
              'FEATURES': feature_list(custom_features, active_file=filename)}
    html = template
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    (root / filename).write_text(html, encoding='utf-8')

print(f'built {len(pages)} main pages + future.html (second home) + {len(future_pages)} level-down pages')