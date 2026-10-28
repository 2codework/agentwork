const test=require('node:test'),assert=require('node:assert/strict');
const {markdownDOM,deepLinkID}=require('../web/reader.js');
class N{constructor(tag,text=''){this.tag=tag;this.textContent=text;this.children=[];}append(...xs){this.children.push(...xs);}}
const doc={createElement:t=>new N(t),createTextNode:t=>new N('#text',t)};
const all=n=>[n,...n.children.flatMap(all)];
test('headings and lists render as DOM',()=>{const a=all(markdownDOM('# Hello\n- One\n- Two',doc));assert.equal(a.filter(x=>x.tag==='h3').length,1);assert.equal(a.filter(x=>x.tag==='li').length,2);});
test('simple tables render accessible header and cells',()=>{const a=all(markdownDOM('| A | B |\n| --- | --- |\n| 1 | 2 |',doc));assert.equal(a.filter(x=>x.tag==='th').length,2);assert.equal(a.filter(x=>x.tag==='td').length,2);});
test('HTML is inert text, never executable DOM',()=>{const a=all(markdownDOM('<script>alert(1)</script>\n<img src=x onerror=alert(1)>',doc));assert.ok(!a.some(x=>['script','img'].includes(x.tag)));assert.ok(a.some(x=>x.textContent.includes('<script>')));});
test('only safe https links become anchors',()=>{const a=all(markdownDOM('[good](https://example.org/a) [bad](javascript:alert) [bad](data:text/html,x) [bad](https://u:p@example.org)',doc));assert.equal(a.filter(x=>x.tag==='a').length,1);assert.equal(a.find(x=>x.tag==='a').rel,'noopener noreferrer');});
test('deep link validates exact existing IDs',()=>{const ids=new Set(['music-musicgen-sketch']);assert.equal(deepLinkID('?case=music-musicgen-sketch','case',ids),'music-musicgen-sketch');assert.equal(deepLinkID('?case=missing','case',ids),null);assert.equal(deepLinkID('?case=%3Cscript%3E','case',ids),null);});
