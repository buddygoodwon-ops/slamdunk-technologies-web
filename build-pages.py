from pathlib import Path
root = Path(__file__).parent
template = (root / 'page-template.html').read_text(encoding='utf-8')
second_home = (root / 'second-home-template.html').read_text(encoding='utf-8')

def svg(paths):
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
  ('future.html', 'The Wild Wide Open Future', 'Enhanced Features.',
   svg('<path d="M12 2 4 5v6c0 5 3.4 9.4 8 11 4.6-1.6 8-6 8-11V5z"/><path d="M8.5 12.2l2.3 2.3 4.7-4.9"/>')),
]

# --- Wild Wide Open Future: custom bullets, each opens one level down ---
# (Custom Pre-Loaded Agents dropped per Glenn 1:20 AM — too many bullet points)
custom_features = [
  ('company-brain.html', 'Company Brain', 'Accessible by AI and Humans.',
   svg('<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/>')),
  ('distribution.html', 'Distribution of Intelligence', 'Delegated Permission Authority.',
   svg('<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path d="M8.2 11l7.6-4M8.2 13l7.6 4"/>')),
  ('virtual-mascot.html', 'Custom Virtual Company Mascot', 'Unique and Fun Interactions.',
   svg('<circle cx="12" cy="12" r="9"/><path d="M9 10h.01"/><path d="M15 10h.01"/><path d="M8.5 14a5 5 0 0 0 7 0"/>')),
  ('avatar-app.html', 'AI Avatar App', 'Managed BuddyFetch AIs through LIVE app.',
   svg('<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>')),
  ('mcp-server.html', 'MCP Server Conversion of Website', 'Allows AI to interact with your Website.',
   svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18"/>')),
]

# --- The 4 original bullet pages (future.html is the Second Home, built separately) ---
# Headline format matches Home: line 1 white, second line gradient (purple->blue)
pages = [
  ('workflows.html', 'AI-Optimized Workflows',
   'Your apps.<br><span class="grad">One intelligent flow.</span>',
   'Connect the tools your team already uses and let an AI operating layer turn scattered work into a clear, repeatable path.'),
  ('agents.html', 'Autonomous Agents',
   'An AI team<br><span class="grad">that keeps moving.</span>',
   'BuddyFetch agents plan, act, and deliver across complex tasks — with the context and persistence to take work from start to finish.'),
  ('marketing.html', 'Built-in Marketing Skills',
   'More conversations.<br><span class="grad">Less busywork.</span>',
   'Put practical marketing execution on demand: research, outreach, follow-up, content, and reporting working together as one growth system.'),
  ('smart.html', 'Scalable. Smart. Adaptable.',
   'A system that gets better<br><span class="grad">under pressure.</span>',
   'Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.'),
]

# --- Level-down pages under The Wild Wide Open Future ---
future_pages = [
  ('company-brain.html', 'Company Brain',
   'One brain<br><span class="grad">for your entire company.</span>',
   "A knowledge base accessible to both AI and humans, built on Google's new OKF format — so every agent and every teammate draws from the same living source of truth."),
  ('distribution.html', 'Distribution of Intelligence',
   'The right intelligence,<br><span class="grad">in the right hands.</span>',
   'Distribute intelligence across your organization with delegated permission authority — every agent knows exactly what it can access, act on, and approve, and every agent knows what information it is permitted to give every employee.'),
  ('virtual-mascot.html', 'Custom Virtual Company Mascot',
   'A face and personality<br><span class="grad">for your brand.</span>',
   'A custom virtual company mascot creates unique and fun interactions — turning routine support into moments your customers remember.'),
  ('avatar-app.html', 'AI Avatar App',
   'Your AI team,<br><span class="grad">live in your pocket.</span>',
   'Manage your BuddyFetch AIs through a LIVE avatar app — see your agents, steer their work, and talk with them in real time from anywhere.'),
  ('mcp-server.html', 'MCP Server Conversion of Website',
   'Make your website<br><span class="grad">AI-native and Human Friendly</span>',
   'Convert your existing website with an MCP server so AI can interact with it directly — your business becomes part of the agentic web, so it can book appointment, get a quote, or even make a purchase.'),
]

def feature_list(items, active_file=None, active_main=None, exclude_active=False):
    out = []
    for fname, ftitle, fdesc, fic in items:
        is_active = fname == active_file or fname == active_main
        if exclude_active and is_active:
            continue  # current page's bullet hidden -> more room for the paragraph
        out.append(
            f'          <div class="feature">\n'
            f'            <a class="feature-icon" href="{fname}" aria-label="{ftitle}">{fic}</a>\n'
            f'            <div>\n'
            f'              <h3><a href="{fname}">{ftitle}</a></h3>\n'
            f'              <p>{fdesc}</p>\n'
            f'            </div>\n'
            f'          </div>'
        )
    return '\n'.join(out)

main_menu_html = feature_list(main_features)
main_menu_block = ('<div class="section-label">Main Menu</div>\n'
                   '        <div class="features compact">\n' + main_menu_html + '\n        </div>')

def render(template, values):
    html = template
    for key, value in values.items():
        html = html.replace('{{' + key + '}}', value)
    return html

# 1) Second Home: The Wild Wide Open Future (custom bullets ONLY — no home bullets here)
future_html = second_home.replace('{{CUSTOM_FEATURES}}', feature_list(custom_features))
(root / 'future.html').write_text(future_html, encoding='utf-8')

# 2) The 4 standard bullet pages (side list = other 4 main bullets only)
for filename, title, heading, lead in pages:
    values = {'TITLE': title, 'DESCRIPTION': lead, 'HEADING': heading, 'LEAD': lead,
              'BACK_HREF': 'index.html', 'BACK_LABEL': '← Back to home', 'LIST_LABEL': '',
              'HEADING_CLASS': 'heading-wide' if filename == 'distribution.html' else '',
              'FEATURES': feature_list(main_features, active_main=filename, exclude_active=True),
              'MAIN_MENU_BLOCK': ''}
    (root / filename).write_text(render(template, values), encoding='utf-8')

# 3) Level-down pages (side list = other 4 custom bullets + the home-page bullet points)
for filename, title, heading, lead in future_pages:
    values = {'TITLE': title, 'DESCRIPTION': lead, 'HEADING': heading, 'LEAD': lead,
              'BACK_HREF': 'future.html', 'BACK_LABEL': '← The Wild Wide Open Future',
              'LIST_LABEL': 'THE BEGINNING',
              'HEADING_CLASS': 'heading-wide mcp-heading' if filename == 'mcp-server.html' else '',
              'FEATURES': feature_list(custom_features, active_file=filename, exclude_active=True),
              'MAIN_MENU_BLOCK': main_menu_block}
    (root / filename).write_text(render(template, values), encoding='utf-8')

print(f'built {len(pages)} main pages + future.html (second home) + {len(future_pages)} level-down pages')
