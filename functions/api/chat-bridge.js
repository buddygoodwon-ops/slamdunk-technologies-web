/**
 * Chatwoot → VAPI Buddy Chat Agent bridge
 * Hosted as a Cloudflare Pages Function at https://slamdunktechnologies.com/api/chat-bridge
 *
 * Replicates the BirdRock Funding live-chat pipeline: when a visitor sends a
 * message in the Chatwoot widget (SlamDunk Technologies inbox), this endpoint
 * receives the `message_created` webhook, feeds the conversation history to the
 * VAPI Buddy assistant's Chat API, and posts the reply back into the same
 * Chatwoot conversation so the visitor sees Buddy answer in the chat.
 *
 * Self-contained (no npm deps, no KV bindings) so it deploys with the site via git push.
 * Secrets come from Cloudflare Pages env vars:
 *   VAPI_API_KEY, VAPI_ASSISTANT_ID, CHATWOOT_ACCOUNT_ID, CHATWOOT_WEBHOOK_SECRET,
 *   CHATWOOT_SESSION_EMAIL, CHATWOOT_SESSION_PASSWORD (session auth with auto re-login,
 *   because Chatwoot Cloud gates the persistent Application API token per account)
 */

const SLAMDUNK_INBOX_ID = 133705;
const MAX_HISTORY = 24;
const CHATWOOT_BASE = 'https://app.chatwoot.com';

// Chatwoot webhooks send message_type as a STRING ('incoming'/'outgoing'/'activity'/'template'),
// while the REST API returns integers (0/1/2/3). Normalize both to the numeric form used internally.
function normalizeMessageType(t) {
  if (t === undefined || t === null) return t;
  if (typeof t === 'number') return t;
  const s = String(t).toLowerCase();
  if (s === 'incoming' || s === '0') return 0;
  if (s === 'outgoing' || s === '1') return 1;
  if (s === 'activity' || s === '2') return 2;
  if (s === 'template' || s === '3') return 3;
  const n = Number(s);
  return Number.isNaN(n) ? t : n;
}

// Cached devise_token_auth session for the Chatwoot worker account
let sessionCache = null; // { headers, expiresAt }

async function getChatwootSession(env) {
  if (sessionCache && Date.now() < sessionCache.expiresAt) return sessionCache.headers;
  const email = env.CHATWOOT_SESSION_EMAIL;
  const password = env.CHATWOOT_SESSION_PASSWORD;
  if (!email || !password) throw new Error('chatwoot session not configured');
  const res = await fetch(`${CHATWOOT_BASE}/auth/sign_in`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      // Non-browser UA: when Buddy's session cap (5) is reached, Chatwoot auto-evicts
      // the oldest session for non-Mozilla clients instead of returning the 409 picker.
      // Browser UAs get a 409 session-picker response that would break this bridge.
      'user-agent': 'slamdunk-chat-bridge/1.0',
    },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error(`chatwoot login ${res.status}`);
  const headers = {
    'access-token': res.headers.get('access-token') || '',
    client: res.headers.get('client') || '',
    uid: res.headers.get('uid') || '',
    'token-type': 'Bearer',
  };
  const expiry = Number(res.headers.get('expiry')) * 1000 || Date.now() + 14 * 24 * 3600 * 1000;
  sessionCache = { headers, expiresAt: Math.min(expiry - 60_000, Date.now() + 6 * 24 * 3600 * 1000) };
  return headers;
}

async function chatwootApi(env, path, options = {}) {
  const doCall = async (headers) =>
    fetch(`https://app.chatwoot.com/api/v1/accounts/${env.CHATWOOT_ACCOUNT_ID}${path}`, {
      ...options,
      headers: { ...headers, 'content-type': 'application/json', ...(options.headers || {}) },
    });
  let res = await doCall(await getChatwootSession(env));
  if (res.status === 401 || res.status === 403) {
    sessionCache = null;
    res = await doCall(await getChatwootSession(env));
  }
  return res;
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json' },
  });
}

export async function onRequestPost(context) {
  const env = context.env || {};
  const {
    VAPI_API_KEY,
    VAPI_ASSISTANT_ID,
    CHATWOOT_ACCOUNT_ID,
    CHATWOOT_WEBHOOK_SECRET,
  } = env;

  const url = new URL(context.request.url);
  const providedSecret = url.searchParams.get('secret') || context.request.headers.get('x-chatwoot-secret');
  if (!CHATWOOT_WEBHOOK_SECRET || providedSecret !== CHATWOOT_WEBHOOK_SECRET) {
    return json({ ok: false, error: 'unauthorized' }, 401);
  }

  if (!VAPI_API_KEY || !VAPI_ASSISTANT_ID || !CHATWOOT_ACCOUNT_ID) {
    return json({ ok: false, error: 'bridge not configured' }, 500);
  }

  let payload;
  try {
    payload = await context.request.json();
  } catch {
    return json({ ok: false, error: 'bad json' }, 400);
  }

  if (payload.event !== 'message_created') {
    return json({ ok: true, ignored: payload.event });
  }

  // message_type: 0=incoming (visitor), 1=outgoing (agent/bot), 2=activity, 3=template
  // Webhook payloads use string labels; the Chatwoot REST API uses integers. Normalize both.
  const message = payload.message_type !== undefined
    ? { type: normalizeMessageType(payload.message_type), content: payload.content, id: payload.id }
    : { type: normalizeMessageType(payload.data?.message?.message_type), content: payload.data?.message?.content, id: payload.data?.message?.id };
  const conversationId = payload.conversation?.id || payload.conversation_id || payload.data?.conversation?.id;
  const inboxId = payload.inbox?.id || payload.data?.inbox?.id;

  // Only react to real visitor text messages in the SlamDunk inbox
  if (message.type !== 0 || !message.content || message.content.trim() === '') {
    return json({ ok: true, ignored: 'not an incoming text message' });
  }
  if (inboxId && inboxId !== SLAMDUNK_INBOX_ID) {
    return json({ ok: true, ignored: 'other inbox' });
  }
  if (!conversationId) {
    return json({ ok: false, error: 'missing conversation id' }, 400);
  }

  // 1) Pull conversation history from Chatwoot (visitor + agent text messages)
  const histRes = await chatwootApi(env, `/conversations/${conversationId}/messages`);
  if (!histRes.ok) {
    return json({ ok: false, error: `chatwoot history ${histRes.status}` }, 502);
  }
  const histData = await histRes.json();
  const items = (histData.payload || histData.data?.messages || [])
    .slice()
    .sort((a, b) => (a.id || 0) - (b.id || 0))
    .filter((m) => {
      const t = normalizeMessageType(m.message_type);
      return (t === 0 || t === 1) && m.content && m.content.trim() !== '';
    })
    .slice(-MAX_HISTORY)
    .map((m) => {
      const t = normalizeMessageType(m.message_type);
      return { role: t === 0 ? 'user' : 'assistant', content: String(m.content).slice(0, 2000) };
    });

  if (!items.length || items[items.length - 1].role !== 'user') {
    items.push({ role: 'user', content: String(message.content).slice(0, 2000) });
  }

  // 2) Ask the VAPI Buddy Chat Agent
  const vapiRes = await fetch('https://api.vapi.ai/chat', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${VAPI_API_KEY}`,
      'content-type': 'application/json',
    },
    body: JSON.stringify({ assistantId: VAPI_ASSISTANT_ID, input: items }),
  });
  const vapiData = await vapiRes.json().catch(() => null);
  if (!vapiRes.ok || !vapiData) {
    return json({ ok: false, error: `vapi ${vapiRes.status}` }, 502);
  }
  const output = Array.isArray(vapiData.output)
    ? vapiData.output.filter((o) => o.role === 'assistant').map((o) => o.content).join('\n').trim()
    : (typeof vapiData.output === 'string' ? vapiData.output : '').trim();
  if (!output) {
    return json({ ok: false, error: 'empty vapi output' }, 502);
  }

  // 3) Post Buddy's reply back into the Chatwoot conversation
  const replyRes = await chatwootApi(env, `/conversations/${conversationId}/messages`, {
    method: 'POST',
    body: JSON.stringify({ content: output, message_type: 'outgoing', private: false }),
  });
  if (!replyRes.ok) {
    return json({ ok: false, error: `chatwoot reply ${replyRes.status}` }, 502);
  }

  return json({ ok: true, conversationId, replied: output.slice(0, 120) });
}

export async function onRequestGet(context) {
  return json({
    ok: true,
    service: 'slamdunk-vapi-chat-bridge',
    target: 'VAPI Buddy Chat Agent',
    configured: Boolean(
      context.env && context.env.VAPI_API_KEY && context.env.VAPI_ASSISTANT_ID && context.env.CHATWOOT_SESSION_EMAIL
    ),
  });
}
