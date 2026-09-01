/**
 * SlamDunk Technologies MCP Server (Streamable HTTP)
 * Hosted as a Cloudflare Pages Function at https://slamdunktechnologies.com/mcp
 * Implements the Model Context Protocol (MCP) so AI agents can:
 *   - read the Company Brain knowledge base (OKF)
 *   - read any page on the website
 *   - book a demo appointment (Glenn's Calendly)
 *   - request a quote
 *   - get contact/licensing info
 * Self-contained (no npm deps, no bindings) so it deploys with the site via git push.
 */

const SERVER_INFO = {
  name: 'slamdunk-mcp',
  version: '1.0.0',
};

const PROTOCOL_VERSION = '2025-06-18';

const COMPANY_BRAIN = {
  company: {
    name: 'SlamDunk Technologies',
    poweredBy: 'BuddyFetch.AI',
    tagline: 'The Agentic AI Team',
    website: 'https://slamdunktechnologies.com',
    description:
      'SlamDunk Technologies deploys intelligent BuddyFetch.AI agents for small and medium businesses - an agentic AI operating layer that mines prospects, runs workflows, handles marketing, and adapts to scale, all managed by phone, text, and email.',
  },
  contact: {
    operationsCoordinator: 'Buddy Goodwon',
    phone1: '(619) 880-5267',
    phone2: '(858) 449-0541',
    email: 'buddy@birdrockfunding.com',
    website: 'birdrockfunding.com',
    address: '5234 Cushman Place #300, San Diego, CA 92110',
    licensing: 'CA DRE# 02162832 | NMLS# 2282987',
  },
  mainFeatures: [
    {
      name: 'AI-Optimized Workflows',
      tagline: 'Utilizing new or existing Apps.',
      description:
        'Connect the tools your team already uses - your Website, POS, CRM, Fulfillment Software and Scheduling - so info flows with no need to input and export CSV files or manually enter redundant info. We add the tools you are missing, from Live Chat run by an AI worker to configured APIs, Zapier, Cloudflare Webhooks, Endpoints, and Nodes - creating an AI operating layer that turns scattered work into a clear, repeatable path.',
    },
    {
      name: 'Autonomous Agents',
      tagline: 'Managed By Phone, Text & Emails.',
      description:
        'Autonomous Agents. BuddyFetch.Ai agents plan, act, and deliver across complex tasks - eliminating repetitive but complex work from data mining to web scraping. Set up the roles, responsibilities, and tasks for each BuddyFetch.Ai agent to handle, from Social Media to Admin, with the context and persistence to take work from start to finish.',
    },
    {
      name: 'Built In Marketing Skills',
      tagline: 'Mass Calling, Text & Emailing.',
      description:
        'Built in Marketing Skills. Marketing execution on demand: Scalable Calling Agents that follow pre-programmed sales funnels to find real interested people, capture their answers, and feed them into your Point of Sale systems - then seamlessly transfer the call to employees prescreened and looking for service or a type of business. Mass email and text outreach campaigns and follow-up workflows. Real-time messaging and returned calls.',
    },
    {
      name: 'Scalable. Smart. Adaptable.',
      tagline: 'Consistency, 24/7. Built to scale.',
      description:
        'Scalable. Smart. Adaptable. We automated your business and your BuddyFetch.Ai agent handles, maintenance, upgrades and execution including scalability analyzing based on volume and turn times, interpreting when to add more AI Agents or more Humans, anticipating the need to change and adapt; additional Systems and/or refinement of Roles and Delegation. Build an operating layer that can handle the next client, campaign, and opportunity without rebuilding the business from scratch.',
    },
    {
      name: 'The Wild Wide Open Future',
      tagline: 'Enhanced Features.',
      description:
        'The Wild Wide Open Future! SlamDunk deploys intelligent BuddyFetch.AI agents. But that is only the Beginning. We have several Additional Features to take you from Wow to No WAY!',
      futureFeatures: [
        'Company Brain - a knowledge base accessible to both AI and humans, built on Googles new OKF format, so every agent and every teammate draws from the same page that not only serves up the info but fills it out customized ready to deliver.',
        'Distribution of Intelligence - delegating the right information to the right agents and employees with Delegated Permission Authority.',
        'Custom Virtual Company Mascot - unique and fun interactions that bring functionality to your brand.',
        'AI Avatar App - manage your BuddyFetch.AIs Company Mascot through a LIVE app like a FaceTime call; employees can access it too through Delegated Permission Authority; have it attend meetings through a Zoom call. It is Wild!',
        'MCP Server Conversion of Website - allows AI agents to interact with your website so it can book an appointment, get a quote, or even make a purchase.',
      ],
    },
  ],
};

const PAGES = [
  'index.html',
  'workflows.html',
  'agents.html',
  'marketing.html',
  'smart.html',
  'future.html',
  'company-brain.html',
  'distribution.html',
  'virtual-mascot.html',
  'avatar-app.html',
  'mcp-server.html',
];

// ---------- JSON-RPC helpers ----------
function jsonOk(body, sessionId) {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Mcp-Session-Id, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  };
  if (sessionId) headers['Mcp-Session-Id'] = sessionId;
  return new Response(JSON.stringify(body), { status: 200, headers });
}

function jsonError(id, code, message) {
  return jsonOk({
    jsonrpc: '2.0',
    id: id ?? null,
    error: { code, message },
  });
}

// ---------- Tool definitions ----------
const TOOLS = [
  {
    name: 'get_company_brain',
    description:
      'Get the SlamDunk Technologies Company Brain knowledge base: company info, contact, licensing, and all service features (workflows, autonomous agents, marketing, scalable smart adaptable, wild wide open future features).',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'get_page_content',
    description:
      'Fetch the current text content of any page on slamdunktechnologies.com. Returns clean text of the requested page. Pages: ' +
      PAGES.join(', '),
    inputSchema: {
      type: 'object',
      properties: {
        page: {
          type: 'string',
          description: 'Page filename, e.g. company-brain.html or index.html',
        },
      },
      required: ['page'],
    },
  },
  {
    name: 'book_demo',
    description:
      'Book a demo appointment with SlamDunk Technologies. Returns the demo booking URL (Glenn Wilbor 30-minute Calendly) and instructions. Call this when a user wants to schedule a demo or talk to a human.',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Prospect name (optional prefill)' },
        email: { type: 'string', description: 'Prospect email (optional prefill)' },
      },
      required: [],
    },
  },
  {
    name: 'request_quote',
    description:
      'Request a quote for BuddyFetch.AI agentic AI services. Returns the quote request flow (email and phone) and a ready-to-send email template with the prospect details.',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: 'Prospect name' },
        email: { type: 'string', description: 'Prospect email' },
        company: { type: 'string', description: 'Company name' },
        needs: { type: 'string', description: 'What they need (workflows, agents, marketing, etc.)' },
      },
      required: ['name', 'email'],
    },
  },
  {
    name: 'get_contact_info',
    description: 'Get SlamDunk Technologies / BirdRock Funding contact information: phones, email, address, licensing.',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
];

// ---------- Tool implementations ----------
async function handleTool(name, args) {
  const a = args || {};
  switch (name) {
    case 'get_company_brain':
      return { content: [{ type: 'text', text: JSON.stringify(COMPANY_BRAIN, null, 2) }] };

    case 'get_page_content': {
      const page = String(a.page || 'index.html').replace(/^\/+/, '');
      const clean = page.split('?')[0].split('#')[0];
      if (!PAGES.includes(clean)) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Unknown page "${clean}". Available pages: ${PAGES.join(', ')}` }],
        };
      }
      let raw;
      try {
        const resp = await fetch(`https://slamdunktechnologies.com/${clean}`, { redirect: 'follow' });
        raw = await resp.text();
      } catch (e) {
        return {
          isError: true,
          content: [{ type: 'text', text: `Failed to fetch page: ${e.message}` }],
        };
      }
      const text = raw
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<[^>]+>/g, ' ')
        .replace(/&nbsp;/g, ' ')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&#39;|&apos;/g, "'")
        .replace(/&quot;/g, '"')
        .replace(/\s+/g, ' ')
        .trim();
      return {
        content: [{ type: 'text', text: `Content of ${clean} (from https://slamdunktechnologies.com/${clean}):\n\n${text}` }],
      };
    }

    case 'book_demo': {
      const params = new URLSearchParams();
      if (a.name) params.set('name', String(a.name));
      if (a.email) params.set('email', String(a.email));
      const qs = params.toString();
      const url = `https://calendly.com/glenn-wilbor-birdrockfunding/30min${qs ? '?' + qs : ''}`;
      return {
        content: [
          {
            type: 'text',
            text:
              `Demo booking prepared. Give the user this link to pick a time (schedules directly with the founder):\n${url}\n\n` +
              'The demo is a 30-minute call hosted on Calendly. If the user needs help immediately, they can call (619) 880-5267.',
          },
        ],
      };
    }

    case 'request_quote': {
      const quote = {
        name: a.name,
        email: a.email,
        company: a.company || 'Not provided',
        needs: a.needs || 'General BuddyFetch.AI inquiry',
      };
      const subject = encodeURIComponent(`Quote Request - ${quote.name}${quote.company !== 'Not provided' ? ' - ' + quote.company : ''}`);
      const mailto = `mailto:buddy@birdrockfunding.com?subject=${subject}`;
      return {
        content: [
          {
            type: 'text',
            text:
              `Quote request prepared for ${quote.name} (${quote.email}).\n\n` +
              `Send it via email to buddy@birdrockfunding.com, subject "Quote Request - ${quote.name}${quote.company !== 'Not provided' ? ' - ' + quote.company : ''}":\n${mailto}\n\n` +
              'Email template body:\n' +
              `"Hi Buddy,\n\nWe are interested in a quote for BuddyFetch.AI agentic AI services.\n\nName: ${quote.name}\nCompany: ${quote.company}\nWhat we need: ${quote.needs}\n\nPlease reach me at ${quote.email}.\n\nThank you!"\n\n` +
              'Alternative: the prospect can call (619) 880-5267 or book a demo at https://calendly.com/glenn-wilbor-birdrockfunding/30min',
          },
        ],
      };
    }

    case 'get_contact_info':
      return { content: [{ type: 'text', text: JSON.stringify(COMPANY_BRAIN.contact, null, 2) }] };

    default:
      return { isError: true, content: [{ type: 'text', text: `Unknown tool: ${name}` }] };
  }
}

// ---------- MCP request handling ----------
async function handlePost(request) {
  const body = await request.json().catch(() => null);
  if (!body || body.jsonrpc !== '2.0') return jsonError(null, -32600, 'Invalid Request: JSON-RPC 2.0 expected');
  const { id, method, params } = body;
  const sessionId = request.headers.get('Mcp-Session-Id') || crypto.randomUUID();

  switch (method) {
    case 'initialize': {
      const clientProtocol = params?.protocolVersion;
      return jsonOk(
        {
          jsonrpc: '2.0',
          id,
          result: {
            protocolVersion: PROTOCOL_VERSION,
            capabilities: { tools: { listChanged: false } },
            serverInfo: SERVER_INFO,
            instructions:
              'This MCP server exposes SlamDunk Technologies (slamdunktechnologies.com, powered by BuddyFetch.AI). Use get_company_brain for the knowledge base, get_page_content to read any site page, book_demo to schedule a demo with the founder, request_quote for quotes, get_contact_info for contact details.',
          },
        },
        sessionId
      );
    }
    case 'notifications/initialized':
      return new Response(null, { status: 202, headers: { 'Access-Control-Allow-Origin': '*' } });
    case 'ping':
      return jsonOk({ jsonrpc: '2.0', id, result: {} }, sessionId);
    case 'tools/list':
      return jsonOk({ jsonrpc: '2.0', id, result: { tools: TOOLS } }, sessionId);
    case 'tools/call': {
      const { name, arguments: args } = params || {};
      if (!name) return jsonError(id, -32602, 'Invalid params: tool name required');
      const okTool = TOOLS.find((t) => t.name === name);
      if (!okTool) return jsonError(id, -32602, `Unknown tool: ${name}`);
      try {
        const result = await handleTool(name, args);
        return jsonOk({ jsonrpc: '2.0', id, result }, sessionId);
      } catch (e) {
        return jsonOk(
          { jsonrpc: '2.0', id, result: { isError: true, content: [{ type: 'text', text: `Tool error: ${e.message}` }] } },
          sessionId
        );
      }
    }
    default:
      return jsonError(id, -32601, `Method not found: ${method}`);
  }
}

// GET: SSE stream (streamable HTTP spec) - announces the POST endpoint, stays open
// until the client disconnects (Workers terminates the stream then; no timers needed)
function handleGet(url) {
  const encoder = new TextEncoder();
  let controllerRef;
  const stream = new ReadableStream({
    start(controller) {
      controllerRef = controller;
      controller.enqueue(encoder.encode(`event: endpoint\ndata: ${url.pathname}\n\n`));
    },
    cancel() {},
  });
  // Keep the connection alive so clients can receive future server messages;
  // if the client disconnects, the Worker suspends/terminates automatically.
  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type, Mcp-Session-Id, Authorization',
      'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    },
  });
}

// ---------- Pages Function entry ----------
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Mcp-Session-Id, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
        'Access-Control-Max-Age': '86400',
      },
    });
  }
  if (request.method === 'GET') return handleGet(url);
  if (request.method === 'POST') return handlePost(request);
  return new Response('Method Not Allowed', { status: 405 });
}