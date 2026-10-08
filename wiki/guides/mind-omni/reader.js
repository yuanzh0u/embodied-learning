(() => {
  'use strict';
  const data = window.RESEARCH_DATA;
  const $ = id => document.getElementById(id);
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const external = (url,label) => `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(label)} ↗</a>`;
  let selected = 0;
  function selectFigure(index,focus=false) {
    selected = index; const f=data.figures[index];
    $('figure-tabs').querySelectorAll('button').forEach((b,i)=>{b.setAttribute('aria-selected',String(i===index));b.tabIndex=i===index?0:-1;if(focus&&i===index)b.focus();});
    $('figure-panel').setAttribute('aria-labelledby',`figure-tab-${index}`);
    $('figure-title').textContent=f.name; $('figure-kicker').textContent=f.kicker;
    const img=$('architecture-image');img.src=f.asset;img.alt=f.alt;
    $('figure-button').setAttribute('aria-label',`放大 ${f.name} 论文原图`);
    $('figure-source').textContent=`论文 ${f.figure} · ${f.version} · 作者原图`;
    $('paper-source').href=f.paper;
    $('reading-strip').innerHTML=f.steps.map((s,i)=>`<div class="reading-step"><span>0${i+1}</span><div><h3>${esc(s[0])}</h3><p>${esc(s[1])}</p></div></div>`).join('');
    $('figure-boundary').textContent=f.boundary;
  }
  $('figure-tabs').innerHTML=data.figures.map((f,i)=>`<button type="button" role="tab" id="figure-tab-${i}" aria-controls="figure-panel" aria-selected="${i===0}" tabindex="${i===0?0:-1}" data-figure="${i}">${esc(f.name)}</button>`).join('');
  $('figure-tabs').addEventListener('click',e=>{const b=e.target.closest('[data-figure]');if(b)selectFigure(Number(b.dataset.figure));});
  $('figure-tabs').addEventListener('keydown',e=>{let i=selected;if(e.key==='ArrowRight')i=(i+1)%data.figures.length;else if(e.key==='ArrowLeft')i=(i-1+data.figures.length)%data.figures.length;else if(e.key==='Home')i=0;else if(e.key==='End')i=data.figures.length-1;else return;e.preventDefault();selectFigure(i,true);});
  function openImage(){const f=data.figures[selected];$('zoom-title').textContent=f.name+' · '+f.figure;$('zoom-image').src=f.asset;$('zoom-image').alt=f.alt;$('zoom-caption').textContent=f.version+' · 作者原图，未重绘 · '+f.paper;document.querySelector('.zoom-scroll').classList.remove('actual');$('zoom-toggle').textContent='查看原尺寸';$('image-dialog').showModal();}
  $('enlarge').addEventListener('click',openImage);$('figure-button').addEventListener('click',openImage);$('close-image').addEventListener('click',()=>$('image-dialog').close());
  $('zoom-toggle').addEventListener('click',()=>{const actual=document.querySelector('.zoom-scroll').classList.toggle('actual');$('zoom-toggle').textContent=actual?'适应窗口':'查看原尺寸';});
  function paperHTML(p){return `<details class="paper" data-paper-focus="${esc(p.id)}"><summary><span class="paper-name">${esc(p.name)}</span><span class="paper-question">${esc(p.short)}</span><span class="paper-year">${esc(p.published)}</span></summary><div class="paper-content"><h3>模型怎样工作</h3><p>${esc(p.method)}</p><h3>在哪里验证</h3><p>${esc(p.evaluation)}</p><h3>阅读时保留的边界</h3><p class="paper-limit">${esc(p.boundary)}</p><div class="paper-links">${external(p.url,'原论文 · '+p.version)}<button class="text-button" data-report="technology-stack.md">展开技术栈对照</button></div></div></details>`;}
  $('paper-groups').innerHTML=data.groups.map(g=>`<section class="paper-group"><div class="group-heading"><h2>${esc(g.title)}</h2><p>${esc(g.subtitle)}</p></div>${g.ids.map(id=>paperHTML(data.papers[id])).join('')}</section>`).join('');
  $('industrial-cases').innerHTML=data.industry.map(x=>`<article class="industry"><span class="tiny-label">企业公开披露</span><h3>${esc(x.name)}</h3><p>${esc(x.summary)}</p>${external(x.url,'查看原始来源')}</article>`).join('');
  function personHTML(p){return `<details class="person"><summary><strong>${esc(p.name)}</strong><span class="person-role">${esc(p.direction)}</span></summary><div class="person-body"><p><strong>论文 / 系统：</strong>${esc(p.works)}</p><p><strong>发表时机构：</strong>${esc(p.affiliation)}</p><p><strong>明确角色：</strong>${esc(p.role)}</p><p><strong>当前公开状态：</strong>${esc(p.current)}</p><p>核查于 ${esc(p.checked)} · ${p.sources.map(s=>external(s.url,s.label)).join(' / ')}</p></div></details>`;}
  $('people-list').innerHTML=`<h2 class="section-subtitle">理想相关合作人员</h2>${data.people.filter(p=>p.liauto).map(personHTML).join('')}<details class="people-rest"><summary>其他核心团队 · ${data.people.filter(p=>!p.liauto).length} 位人员</summary>${data.people.filter(p=>!p.liauto).map(personHTML).join('')}</details>`;
  $('report-grid').innerHTML=data.reportOrder.map(id=>{const r=data.reports[id];return `<article class="report-card"><h2>${esc(r.label)}</h2><p>${esc(r.description)}</p><div class="links"><button class="text-button" data-report="${esc(id)}">在线阅读 →</button><a href="reports/${encodeURIComponent(id)}" download>下载 Markdown</a></div></article>`;}).join('');
  function openReport(id){const r=data.reports[id];if(!r)return;$('report-title').textContent=r.label;$('report-body').innerHTML=r.html;if(!$('report-dialog').open)$('report-dialog').showModal();$('report-dialog').scrollTop=0;}
  document.addEventListener('click',e=>{const b=e.target.closest('[data-report]');if(b){e.preventDefault();openReport(b.dataset.report);}});
  $('close-report').addEventListener('click',()=>$('report-dialog').close());
  for(const id of ['image-dialog','report-dialog'])$(id).addEventListener('click',e=>{if(e.target===$(id)){const r=$(id).getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)$(id).close();}});
  function route(){const id=location.hash.slice(1).split('?')[0];const valid=['architecture','papers','people','reports'].includes(id)?id:'architecture';for(const s of document.querySelectorAll('.view'))s.hidden=s.id!==valid;for(const a of document.querySelectorAll('.rail nav a')){const active=a.hash==='#'+valid;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}window.scrollTo(0,0);}

  const system=data.system;
  function goPaper(id){history.replaceState(null,'','#papers');route();const p=$('paper-groups').querySelector(`[data-paper-focus="${id}"]`);if(p){p.open=true;p.querySelector('summary').focus();p.scrollIntoView({block:'start',behavior:'auto'});}}
  function selectModule(id){const m=system.modules.find(x=>x.id===id);if(!m)return;
    $('module-nav').querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.module===id)));
    $('module-detail').innerHTML=`<span class="tiny-label">${esc(m.role)} · ${esc(m.name)}</span><h2>${esc(m.question)}</h2><p class="module-summary">${esc(m.summary)}</p><div class="module-io"><div><h3>输入</h3><p>${esc(m.inputs)}</p></div><div><h3>输出</h3><p>${esc(m.outputs)}</p></div></div><div class="module-connections"><h3>在体系中的连接</h3><p>${esc(m.connection)}</p></div><details><summary>证据支持到哪里？</summary><div><p>${esc(m.evidence)}</p><p class="boundary">${esc(m.limit)}</p><div class="module-links">${m.sources.map(x=>external(x[0],x[1])).join('')}</div></div></details><details><summary>展开核心工作${m.paper_ids.length?' · '+m.paper_ids.length+' 篇':' · 官方定位'}</summary><div>${m.paper_ids.length?m.paper_ids.map(pid=>paperHTML(data.papers[pid])).join(''):'<p class="empty">暂不把项目定位当作完整方法论文；沿下方延伸研究理解问题。</p>'}${m.figure!==null?`<button class="text-button" data-module-figure="${m.figure}">查看这项工作的原始架构图 →</button>`:''}</div></details><details><summary>沿这个问题继续延伸</summary><div>${m.extensions.map(x=>`<button class="extension-link" data-go-paper="${esc(x[0])}">${esc(x[1])} →</button>`).join('')}</div></details>`;
  }
  $('module-nav').innerHTML=system.modules.map(m=>`<button data-module="${esc(m.id)}" aria-pressed="false" aria-controls="module-detail">${esc(m.name)}<span>${esc(m.role)}</span></button>`).join('');
  $('module-nav').addEventListener('click',e=>{const b=e.target.closest('[data-module]');if(b)selectModule(b.dataset.module);});
  $('outside-map').innerHTML='<p>这些工作按问题与总图连接。除非论文明确说明，不把相似方法或共同作者当作 Mind-Omni 的已集成模块。</p><ul>'+system.related_outside_map.map(x=>`<li><button class="text-button" data-go-paper="${esc(x[0])}">${esc(data.papers[x[0]].name)}</button> · ${esc(x[1])}</li>`).join('')+'</ul>';
  document.addEventListener('click',e=>{const paper=e.target.closest('[data-go-paper]');if(paper)goPaper(paper.dataset.goPaper);const fig=e.target.closest('[data-module-figure]');if(fig){$('architecture-deep').open=true;selectFigure(Number(fig.dataset.moduleFigure));$('architecture-deep').scrollIntoView({block:'start'});}});
  $('system-zoom').addEventListener('click',()=>{$('zoom-title').textContent='Mind-Omni · 官方项目总图';$('zoom-image').src=system.image;$('zoom-image').alt='Mind-Omni 官方研究体系总图';$('zoom-caption').textContent='官方网页原始留存 · '+system.checked_at+' · '+system.source_url;document.querySelector('.zoom-scroll').classList.remove('actual');$('zoom-toggle').textContent='查看原尺寸';$('image-dialog').showModal();});
  selectModule('u1');

  window.addEventListener('hashchange',route);selectFigure(0);route();
})();
