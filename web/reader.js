'use strict';
// Deliberately small Markdown reader: no HTML parsing, images, scripts or embedded content.
function markdownDOM(text,doc=document){
 const make=(tag,t)=>{const e=doc.createElement(tag);if(t!==undefined)e.textContent=t;return e;};
 function inline(parent,s){const re=/`([^`\n]+)`|\*\*([^*\n]+)\*\*|\[([^\]]+)\]\(([^\s)]+)\)/g;let end=0,m;while((m=re.exec(s))){parent.append(doc.createTextNode(s.slice(end,m.index)));if(m[1]!==undefined)parent.append(make('code',m[1]));else if(m[2]!==undefined)parent.append(make('strong',m[2]));else{let u;try{u=new URL(m[4]);}catch{}if(u&&u.protocol==='https:'&&!u.username&&!u.password){const a=make('a',m[3]+'（来源）');a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';parent.append(a);}else parent.append(doc.createTextNode(m[0]));}end=re.lastIndex;}parent.append(doc.createTextNode(s.slice(end)));return parent;}

 const root=make('div'),lines=String(text).split('\n');let i=0;
 while(i<lines.length){const line=lines[i];if(!line.trim()){i++;continue;}const fence=/^\s*(`{3,}|~{3,})([a-zA-Z0-9_-]*)\s*$/.exec(line);if(fence){const body=[];i++;while(i<lines.length&&!new RegExp('^\\s*'+fence[1][0]+'{'+fence[1].length+',}\\s*$').test(lines[i]))body.push(lines[i++]);if(i<lines.length)i++;const pre=make('pre'),code=make('code',body.join('\n'));pre.append(code);root.append(pre);continue;}const h=/^(#{1,6})\s+(.+)$/.exec(line);if(h){root.append(inline(make('h'+Math.min(6,h[1].length+2)),h[2]));i++;continue;}
 if(line.includes('|')&&i+1<lines.length&&/^\s*\|?\s*:?-{3,}/.test(lines[i+1])){const table=make('table'),wrap=make('div');wrap.className='table-scroll';const cells=s=>s.trim().replace(/^\||\|$/g,'').split('|').map(x=>x.trim());const head=make('thead'),tr=make('tr');cells(line).forEach(c=>tr.append(inline(make('th'),c)));head.append(tr);table.append(head);i+=2;const body=make('tbody');while(i<lines.length&&lines[i].includes('|')&&lines[i].trim()){const row=make('tr');cells(lines[i++]).forEach(c=>row.append(inline(make('td'),c)));body.append(row);}table.append(body);wrap.append(table);root.append(wrap);continue;}
 const item=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(line);if(item){const list=make(/^\s*\d/.test(line)?'ol':'ul');while(i<lines.length){const m=/^\s*(?:[-*]|\d+\.)\s+(.+)$/.exec(lines[i]);if(!m)break;list.append(inline(make('li'),m[1]));i++;}root.append(list);continue;}
 root.append(inline(make('p'),line));i++;
 }return root;
}
function deepLinkID(search,key,ids){const id=new URLSearchParams(search).get(key);return ids.has(id)?id:null;}


// Explicit reader projection. Never recursively render source-bundle machine metadata.
function researchChapterDOM(chapter,cases,doc=document){
 const make=(tag,t)=>{const e=doc.createElement(tag);if(t!==undefined)e.textContent=t;return e;};
 const copy=(parent,label,value)=>{if(typeof value==='string'&&value.trim()){if(label)parent.append(make('h4',label));parent.append(markdownDOM(value,doc));}};
 const d=chapter.data,root=make('div');
 const topics={roles:['岗位地图','按岗位理解任务拆解、人工验收与授权边界。'],industries:['行业地图','用合成行业任务学习输入、步骤、验收和风险判断。'],learning:['学习方法','学习、写作、研究检索、知识管理、无障碍与多语言练习。'],'creative-design':['设计专题','界面、设计系统、图像、演示与资产溯源的合成教学流程。'],'creative-music':['音乐与音频专题','配乐、编曲、混音、转录和音频后期的合成教学流程。'],'creative-video':['视频与动画专题','视频生成、剪辑、字幕、动画与交付的合成教学流程。']};
 const topic=topics[chapter.id]||['研究资料','代表性教学资料，并非完整市场目录。'];
 root.append(make('h3',topic[0]));copy(root,'',topic[1]);
 root.append(make('p',`收录 ${(d.cases||[]).length} 个教学流程、${(d.sources||[]).length} 条登记来源；来源核查日期：${d.checked_at||'未提供'}。不是全部岗位、行业或产品目录。`));
 copy(root,'证据与使用边界','以下是原创合成教学方案，未实测完整工作流，也不代表真实部署、质量保证或效率收益。来源只支持其明确描述的能力与限制。许可、费用、版本、账号权限和素材权利必须在实际使用前复核；上传、付费、外部写入和发布仍需批准。');
 if(Array.isArray(d.coverage_gaps)){root.append(make('h4','尚未覆盖与待核验'));const ul=make('ul');for(const gap of d.coverage_gaps)if(typeof gap==='string'){const li=make('li');li.append(markdownDOM(gap,doc));ul.append(li);}root.append(ul);}
 if(chapter.id==='industries'){copy(root,'行业教学正文（稿件版本说明属于采集记录）',d.content_markdown);copy(root,'行业覆盖与边界',d.coverage_markdown);}
 const list=make('div');root.append(make('h4','实践与适用边界'),list);
 for(const raw of d.cases||[]){const id=chapter.id.startsWith('creative-')?raw.id:chapter.id+'-'+String(raw.id).toLowerCase();const c=cases.find(c=>c.id===id);if(!c)continue;const item=make('details');item.append(make('summary',c.title));copy(item,'',c.summary);const a=make('a','打开完整实践与验收');a.href='?case='+encodeURIComponent(c.id);item.append(a);
 for(const [key,label] of [['evidence_note','证据说明'],['license','许可'],['risks','风险与授权'],['cost','费用'],['compute_cost','计算费用'],['permission_boundary','权限'],['applicable_versions','适用版本'],['lifecycle','生命周期'],['historical_context','历史边界'],['practice_status','实践证据状态'],['failure_recovery','失败恢复']])copy(item,label,c[key]);list.append(item);}
 root.append(make('h4','来源与证据范围'));
 for(const source of d.sources||[]){const row=make('div');copy(row,'',source.title||source.publisher_title||'来源');for(const url of source.urls||[source.url])if(typeof url==='string'){const a=make('a','阅读原始来源');try{const u=new URL(url);if(u.protocol==='https:'&&!u.username&&!u.password){a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';row.append(a);}}catch{}}
 copy(row,'','核查日期：'+(source.checked_at||d.checked_at||'未提供'));
 for(const key of ['verified_claim','supports','notes','notes_zh','claim_scope','evidence_scope','license_status'])copy(row,'',source[key]);root.append(row);}
 const raw=make('details');raw.open=false;raw.append(make('summary','原始资料 · 历史采集快照，不代表当前整合状态'),make('p','以下保留采集时的全部原字段。适配、整合与发布状态可能已经变化；请勿将内部元数据视为当前产品状态。'),make('pre',JSON.stringify(d,null,2)));root.append(raw);return root;
}
if(typeof module!=='undefined')module.exports={markdownDOM,deepLinkID,researchChapterDOM};
