// Offline DOM model with node movement; not browser layout evidence.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
class E{
 constructor(tag){this.tag=tag;this.tagName=tag.toUpperCase();this.children=[];this.textContent='';this.events={};this.value='';this.className='';this.dataset={};this.classList={toggle(){}};}
 detach(x){if(x.parentElement){const a=x.parentElement.children;a.splice(a.indexOf(x),1);}x.parentElement=this;}
 append(...xs){xs.forEach(x=>{this.detach(x);this.children.push(x);});}
 prepend(...xs){[...xs].reverse().forEach(x=>{this.detach(x);this.children.unshift(x);});}
 insertBefore(x,b){this.detach(x);const i=this.children.indexOf(b);if(i<0)this.children.push(x);else this.children.splice(i,0,x);}
 replaceChildren(...xs){this.children.forEach(x=>x.parentElement=null);this.children=[];this.append(...xs);}
 setAttribute(k,v){this[k]=v;}removeAttribute(k){delete this[k];}addEventListener(k,f){this.events[k]=f;}focus(){this.focused=true;}scrollIntoView(){this.scrolled=true;}
 querySelectorAll(tag){return this.children.flatMap(x=>[...(x.tag===tag?[x]:[]),...(x.querySelectorAll?.(tag)||[])]);}querySelector(tag){return this.querySelectorAll(tag)[0]||null;}
}
const all=e=>[e,...(e.children||[]).flatMap(all)],text=e=>(e.textContent||'')+(e.children||[]).map(text).join(' ');
function fixture(root){
 const ctx={URL,URLSearchParams,console};vm.createContext(ctx);vm.runInContext(fs.readFileSync(path.join(root,'web/app.js'),'utf8'),ctx);
 const ids={};for(const id of ['search','role','industry','topic','content','pagination','view-title','view-description','search-tools','filter-panel','task-shortcuts','progress','status','progress-text','meter','chapters','export','import','reset','clear'])ids[id]=new E('div');
 ctx.location={search:'',hash:'',href:'https://example.test/agentwork/library.html'};ctx.history={state:{},replaceState(s,t,u){this.state=s;ctx.location.href=u;},pushState(s,t,u){this.state=s;ctx.location.href=u;},back(){}};
 ctx.window={scrollY:0,scrollTo(){},events:{},addEventListener(k,f){this.events[k]=f;},confirm:()=>true};ctx.document={createElement:t=>new E(t),createTextNode:t=>({textContent:t}),getElementById:id=>ids[id]||all(ids.content).find(n=>n.id===id),querySelector:()=>new E('label'),querySelectorAll:()=>[]};
 vm.runInContext(fs.readFileSync(path.join(root,'web/reader.js'),'utf8'),ctx);ctx.fixtureData=JSON.parse(fs.readFileSync(path.join(root,'site/data.json')));vm.runInContext('data=fixtureData',ctx);
 return {ctx,ids,run:s=>vm.runInContext(s,ctx)};
}
function anchors(f){return Object.fromEntries(all(f.ids.content).filter(n=>/^(section-|reading-(?:sub-)?\d)/.test(n.id||'')).map(n=>[n.id,{tag:n.tagName,text:text(n)}]));}
module.exports={fixture,all,text,anchors};
