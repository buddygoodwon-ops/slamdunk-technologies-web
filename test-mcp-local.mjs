// Local test harness for functions/mcp.js (simulates Pages Function environment)
import { onRequest } from './functions/mcp.js';

async function post(bodyObj) {
  const req = new Request('https://slamdunktechnologies.com/mcp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bodyObj),
  });
  const resp = await onRequest({ request: req });
  const text = await resp.text();
  console.log('POST', JSON.stringify(bodyObj).slice(0, 80), '=>', resp.status, text.slice(0, 400));
  return JSON.parse(text);
}

// 1. initialize
const init = await post({
  jsonrpc: '2.0', id: 1, method: 'initialize',
  params: { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'test', version: '0' } },
});
console.log('serverInfo:', init.result.serverInfo.name, init.result.protocolVersion);

// 2. tools/list
const list = await post({ jsonrpc: '2.0', id: 2, method: 'tools/list' });
console.log('tools:', list.result.tools.map(t => t.name).join(', '));

// 3. tools/call get_company_brain
const brain = await post({ jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'get_company_brain', arguments: {} } });
console.log('brain ok:', brain.result && !brain.result.isError);

// 4. tools/call get_page_content (company-brain.html)
const page = await post({ jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'get_page_content', arguments: { page: 'company-brain.html' } } });
console.log('page content head:', page.result.content[0].text.slice(0, 150));
console.log('contains Company Brain:', page.result.content[0].text.includes('Company Brain'));

// 5. tools/call book_demo
const book = await post({ jsonrpc: '2.0', id: 5, method: 'tools/call', params: { name: 'book_demo', arguments: { name: 'Test Prospect', email: 'test@example.com' } } });
console.log('book_demo:', book.result.content[0].text.slice(0, 150));

// 6. unknown tool -> error
const bad = await post({ jsonrpc: '2.0', id: 6, method: 'tools/call', params: { name: 'nope', arguments: {} } });
console.log('unknown tool is error:', !!bad.error);

// 7. bad page -> isError
const badPage = await post({ jsonrpc: '2.0', id: 7, method: 'tools/call', params: { name: 'get_page_content', arguments: { page: 'evil.html' } } });
console.log('bad page rejected:', badPage.result.isError);

console.log('ALL TESTS DONE');