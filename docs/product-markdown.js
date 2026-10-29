'use strict';
// Safe product-only Markdown subset. No HTML or arbitrary local URL resolution.
function productMarkdownDOM(text,doc=document,resolveLocal=()=>null){
 const make=(tag,t)=>{const e=doc.createElement(tag);if(t!==undefined)e.textContent=t;return e;};
 function inline(parent,s){const re=/`([^`\n]+)`|\*\*([^*\n]+)\*\*|\[([^\]]+)\]\(([^\s)]+)\)/g;let end=0,m;while((m=re.exec(s))){parent.append(doc.createTextNode(s.slice(end,m.index)));if(m[1]!==undefined)parent.append(make('code',m[1]));else if(m[2]!==undefined)parent.append(make('strong',m[2]));else{let u;try{u=new URL(m[4]);}catch{}if(u&&u.protocol==='https:'&&!u.username&&!u.password){const a=make('a',m[3]+'（来源）');a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';parent.append(a);}else{const href=resolveLocal(m[4]);if(href){const a=make('a',m[3]);a.href=href;parent.append(a);}else parent.append(doc.createTextNode(m[0]));}}end=re.lastIndex;}parent.append(doc.createTextNode(s.slice(end)));return parent;}

 const root=make('div'),lines=String(text).split('\n');let i=0;
 while(i<lines.length){const line=lines[i];if(!line.trim()){i++;continue;}const fence=/^\s*(`{3,}|~{3,})([a-zA-Z0-9_-]*)\s*$/.exec(line);if(fence){const body=[];i++;while(i<lines.length&&!new RegExp('^\\s*'+fence[1][0]+'{'+fence[1].length+',}\\s*$').test(lines[i]))body.push(lines[i++]);if(i<lines.length)i++;const pre=make('pre'),code=make('code',body.join('\n'));if(fence[2])code.className='language-'+fence[2];pre.append(code);root.append(pre);continue;}const h=/^(#{1,6})\s+(.+)$/.exec(line);if(h){root.append(inline(make('h'+Math.min(6,h[1].length+2)),h[2]));i++;continue;}
 if(line.includes('|')&&i+1<lines.length&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1])){const table=make('table'),wrap=make('div');wrap.className='table-scroll';const cells=s=>s.trim().replace(/^\||\|$/g,'').split('|').map(x=>x.trim());const head=make('thead'),tr=make('tr');cells(line).forEach(c=>tr.append(inline(make('th'),c)));head.append(tr);table.append(head);i+=2;const body=make('tbody');while(i<lines.length&&lines[i].includes('|')&&lines[i].trim()){const row=make('tr');cells(lines[i++]).forEach(c=>row.append(inline(make('td'),c)));body.append(row);}table.append(body);wrap.append(table);root.append(wrap);continue;}
 const item=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(line);if(item){const list=make(/^\s*\d/.test(line)?'ol':'ul');while(i<lines.length){const m=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(lines[i]);if(!m)break;list.append(inline(make('li'),m[1]));i++;}root.append(list);continue;}
 root.append(inline(make('p'),line));i++;
 }return root;
}
if(typeof module!=='undefined')module.exports={productMarkdownDOM};
