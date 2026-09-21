/* Behaviour shared by every page of the guide. Loaded at the end of <body>
   after a365-data.js. Every hook is optional: a page without a section
   simply skips that part. */
(function(){
  const D = window.A365;
  const root = document.documentElement;
  const cap = Object.fromEntries(D.capabilities.map(c => [c.key, c]));
  const get = (path) => path.split('.').reduce((o,k)=>o && o[k], D);

  /* Keep sticky-header offsets accurate across the two-row mobile header. */
  const header = document.querySelector('.topbar');
  const syncHeaderHeight = () => root.style.setProperty('--header-h', Math.ceil(header.getBoundingClientRect().height + 12) + 'px');
  syncHeaderHeight();
  if ('ResizeObserver' in window) new ResizeObserver(syncHeaderHeight).observe(header);
  window.addEventListener('resize', syncHeaderHeight, {passive:true});

  /* --- Render values from the data block --- */
  document.querySelectorAll('[data-val]').forEach(el => { const v = get(el.dataset.val); if (v != null) el.textContent = v; });
  const visibleCaps = D.capabilities.filter(c => !c.hidden);
  const summaries = {
    capabilities: visibleCaps.length,
    previews: visibleCaps.filter(c => c.tier !== 'ga').length
  };
  document.querySelectorAll('[data-summary]').forEach(el => { const v = summaries[el.dataset.summary]; if (v != null) el.textContent = v; });
  document.querySelectorAll('[data-badge]').forEach(el => {
    const c = cap[el.dataset.badge]; if (!c) return;
    el.textContent = D.tiers[c.tier].label; el.classList.add('t-' + c.tier);
  });
  document.querySelectorAll('[data-st]').forEach(el => {
    const c = cap[el.dataset.st]; if (!c) return;
    el.textContent = D.tiers[c.tier].phrase; el.classList.add('t-' + c.tier);
  });
  document.querySelectorAll('[data-tier]').forEach(el => {
    const c = cap[el.dataset.tier]; if (c) el.dataset.tierValue = c.tier;
  });

  /* --- Availability table from the data block --- */
  const tb = document.querySelector('#avail tbody');
  if (tb) D.capabilities.filter(c => !c.hidden).forEach(c => {
    const tr = document.createElement('tr'); tr.dataset.tier = c.key; tr.dataset.tierValue = c.tier;
    tr.innerHTML = `<td>${c.name}</td><td><span class="badge t-${c.tier}" style="margin:0">${D.tiers[c.tier].label}</span></td><td class="muted">${c.note || ''}</td><td>${c.where}</td>`;
    tb.appendChild(tr);
  });

  /* --- Changelog from the data block --- */
  const ch = document.querySelector('#changelog .changes');
  if (ch) (D.changes || []).forEach(c => {
    const li = document.createElement('li');
    const sec = c.section ? ` <a href="#${c.section}">${c.section.slice(1).replace('-', '.')}</a>` : '';
    li.innerHTML = `<b>${c.date}</b>${sec} ${c.text}`;
    ch.appendChild(li);
  });

  /* --- Table of contents --- */
  const list = document.getElementById('toc-list');
  const toc = document.getElementById('toc'), tt = document.getElementById('toc-toggle');
  const mobileNav = matchMedia('(max-width: 960px)');
  const heads = document.querySelectorAll('article h2, article h3');
  heads.forEach(h => {
    const sec = h.closest('section'); if (!sec || !sec.id) return;
    const li = document.createElement('li'); li.className = h.tagName === 'H2' ? 'l2' : 'l3'; li.dataset.for = sec.id;
    const a = document.createElement('a'); a.href = '#' + sec.id;
    const badge = h.querySelector('.badge');
    a.textContent = (h.textContent || '').replace(badge ? badge.textContent : '', '').trim();
    li.appendChild(a); list.appendChild(li);
  });

  /* --- Scroll spy --- */
  const links = new Map([...list.querySelectorAll('a')].map(a => [a.getAttribute('href').slice(1), a]));
  let current = null;
  const setCurrent = (id) => {
    if (current === id) return; current = id;
    links.forEach(a => a.removeAttribute('aria-current'));
    const a = links.get(id);
    if (a) {
      a.setAttribute('aria-current','true');
      if (!mobileNav.matches) {
        const top = a.offsetTop - (toc.clientHeight / 2) + (a.offsetHeight / 2);
        toc.scrollTo({top:Math.max(0, top), behavior:'smooth'});
      }
    }
  };
  const targets = [...links.keys()].map(id => document.getElementById(id)).filter(Boolean);
  const onScroll = () => {
    const y = window.scrollY + header.getBoundingClientRect().height + 68; let best = targets[0];
    for (const t of targets) {
      if (t.classList.contains('is-hidden')) continue;
      const top = t.getBoundingClientRect().top + window.scrollY;
      if (top <= y) best = t; else break;
    }
    if (best) setCurrent(best.id);
  };
  const refreshSpy = () => requestAnimationFrame(onScroll);
  const alignInitialHash = () => {
    const id = decodeURIComponent(location.hash.slice(1)); if (!id) return refreshSpy();
    const target = document.getElementById(id); if (!target || target.classList.contains('is-hidden')) return;
    const offset = header.getBoundingClientRect().height + 16;
    root.classList.add('no-smooth');
    window.scrollTo({top:window.scrollY + target.getBoundingClientRect().top - offset, behavior:'auto'});
    requestAnimationFrame(() => root.classList.remove('no-smooth')); refreshSpy();
  };
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('hashchange', refreshSpy);
  window.addEventListener('load', () => { const ready = document.fonts ? document.fonts.ready : Promise.resolve(); ready.then(() => setTimeout(alignInitialHash, 50)); });
  refreshSpy();

  /* --- GA-only filter --- */
  const ga = document.getElementById('ga-only'), count = document.getElementById('count');
  const tiered = [...document.querySelectorAll('[data-tier]')];
  function apply(){
    const gaOnly = !!(ga && ga.checked);
    tiered.forEach(el => el.classList.toggle('is-hidden', gaOnly && el.dataset.tierValue && el.dataset.tierValue !== 'ga'));
    if (count) count.textContent = gaOnly ? 'GA only' : '';
    onScroll();
  }
  if (ga) ga.addEventListener('change', apply);

  /* --- Figure numbering --- */
  document.querySelectorAll('figcaption .fn').forEach((b,i)=>{ b.textContent = 'Figure ' + (i+1) + '.'; });

  /* --- Steppers --- */
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.stepper').forEach(fig=>{
    const items=[...fig.querySelectorAll('[data-step]')], n=Math.max(...items.map(e=>+e.dataset.step));
    const texts = (()=>{ try{ return JSON.parse(fig.querySelector('.stext')?.dataset.texts||'[]'); }catch(e){ return []; } })();
    const solo = fig.dataset.mode==='solo'; let cur=1, timer=null;
    const prev=fig.querySelector('.prev'), next=fig.querySelector('.next'), play=fig.querySelector('.play'), cnt=fig.querySelector('.scount'), st=fig.querySelector('.stext');
    function render(){ items.forEach(e=>{ const k=+e.dataset.step; e.classList.toggle('on', solo ? k===cur : k<=cur); e.classList.toggle('now', k===cur); }); cnt.textContent=cur+' / '+n; if(st) st.textContent=texts[cur-1]||''; prev.disabled=cur<=1; next.disabled=cur>=n; }
    function stop(){ if(timer){ clearInterval(timer); timer=null; if(play) play.textContent='Play'; } }
    prev.addEventListener('click',()=>{ stop(); cur=Math.max(1,cur-1); render(); });
    next.addEventListener('click',()=>{ stop(); cur=Math.min(n,cur+1); render(); });
    if(play) play.addEventListener('click',()=>{ if(timer) return stop(); if(reduce){ cur=n; render(); return; } if(cur>=n) cur=0; play.textContent='Pause'; timer=setInterval(()=>{ cur++; render(); if(cur>=n) stop(); },1700); render(); });
    render();
  });

  /* --- Plan selector --- */
  const planBtns=[...document.querySelectorAll('.plan button')], planMsg=document.getElementById('planmsg');
  const licRows=[...document.querySelectorAll('#s2-1 .tbl tbody tr')];
  function setPlan(p){ planBtns.forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.plan===p))); let un=0;
    licRows.forEach(tr=>{ const base = tr.children[2].textContent.trim()==='Yes'; const ok = p==='base' ? base : true; tr.classList.toggle('unlock', ok); tr.classList.toggle('locked', !ok); if(ok) un++; });
    planMsg.textContent = p==='base' ? `${un} of ${licRows.length} capabilities. The registry, basic actions, rules and registry sync work without the add-on; everything else needs Agent 365.` : p==='addon' ? `All ${licRows.length} capabilities. E5 already includes Entra ID P2, so Conditional Access and ID Governance for agents need nothing more. Network controls for local agents on devices need Entra Internet Access.` : `All ${licRows.length} capabilities. E7 bundles Agent 365 with the Entra Suite, so the identity and network dependencies are included.`; }
  planBtns.forEach(b=>b.addEventListener('click',()=>setPlan(b.dataset.plan))); if(planBtns.length) setPlan('base');

  /* --- Control plane hover --- */
  document.querySelectorAll('.cp').forEach(fig=>{
    const svg=fig.querySelector('svg'), pills=[...svg.querySelectorAll('g.pill')], prods=[...svg.querySelectorAll('g.prod')];
    function light(ids){ svg.classList.add('active'); pills.forEach(p=>p.classList.toggle('lit', ids.pill===p)); prods.forEach(p=>p.classList.toggle('lit', ids.set.has(p.id))); }
    function clear(){ svg.classList.remove('active'); [...pills,...prods].forEach(p=>p.classList.remove('lit')); }
    const hover=matchMedia('(hover:hover)').matches;
    pills.forEach(p=>{ const on=()=>light({pill:p,set:new Set(p.dataset.links.split(' '))});
      if(hover){ p.addEventListener('pointerenter',on); p.addEventListener('pointerleave',clear); p.addEventListener('focus',on); p.addEventListener('blur',clear); }
      else { p.addEventListener('click',e=>{ e.stopPropagation(); p.classList.contains('lit') ? clear() : on(); }); }
      p.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); p.classList.contains('lit') ? clear() : on(); } });
    });
    if(!hover){ svg.addEventListener('click',clear); }
    if(hover) prods.forEach(pr=>{ pr.addEventListener('pointerenter',()=>{ const owners=pills.filter(p=>p.dataset.links.split(' ').includes(pr.id)); svg.classList.add('active'); pills.forEach(p=>p.classList.toggle('lit',owners.includes(p))); prods.forEach(x=>x.classList.toggle('lit',x===pr)); }); pr.addEventListener('pointerleave',clear); });
  });

  /* --- Conditional Access explorer --- */
  const CAtext={
    obo:{subj:'The user. The agent is the actor inside the token.',target:'Users and groups. The agent inherits the user\u2019s Conditional Access posture, so a risky user is prompted for MFA before the agent proceeds.',note:'Policies aimed at agent identities do not apply here. Do not expect an agent-scoped block to stop a delegated call.'},
    app:{subj:'The agent identity itself. No user is present.',target:'Agent identities, their blueprints, or custom security attributes. Blueprint targeting covers every child identity, present and future.',note:'The only grant control that makes sense is block; there is no user to satisfy MFA. Blueprint policies do not cover agent users.'},
    user:{subj:'The agent\u2019s user account, a real Entra user object.',target:'Agent users, selected individually or by custom security attribute, with the Agent risk condition. Device and network compliance apply only on endpoints such as Windows 365 Cloud PCs for Agents.',note:'Policies targeting all users exclude agent users. Agent users cannot be scoped by group. Use the Agent execution environments condition so cloud-native agents are not blocked with no path to compliance.'}
  };
  document.querySelectorAll('.ca').forEach(fig=>{
    const btns=[...fig.querySelectorAll('.pat button')];
    function set(p){ fig.dataset.pattern=p; btns.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.p===p)));
      const map={obo:'b-user',app:'b-id',user:'b-au'}, ln={obo:'l-user',app:'l-id',user:'l-au'};
      fig.querySelectorAll('.box').forEach(b=>{ const isS=b.classList.contains(map[p]); b.classList.toggle('subj',isS); b.classList.toggle('off', !isS && !b.classList.contains('bp')); });
      fig.querySelectorAll('.ln').forEach(l=>l.style.opacity = l.classList.contains(ln[p]) ? '1' : '0.12');
      fig.querySelector('.ca-subj').textContent=CAtext[p].subj; fig.querySelector('.ca-target').textContent=CAtext[p].target; fig.querySelector('.ca-note').textContent=CAtext[p].note; }
    btns.forEach(b=>b.addEventListener('click',()=>set(b.dataset.p))); set('obo');
  });

  /* --- Terminal replay --- */
  const SCEN={
    defender:{title:'Claude Code \u00b7 developer laptop \u00b7 Defender for Endpoint in Block mode',lines:[
      ['u','\u276f Summarize the code in this directory'],['dim','\u25cf Let me look at what\u2019s in the current directory.'],['ok','\u25cf List directory .        15 files found'],['ok','\u25cf List directory Code     1 file found'],
      ['bad','\u2717 Read readme.md\n  Tool result blocked: \u26a0 This request was blocked by Microsoft Defender due to detected security concerns in your prompt.'],
      ['dim','\u25cf The Code directory contains only a readme.md file, but I\u2019m unable to read it. Access was blocked by a security policy.'],
      ['toast','<b>Windows Security</b>Threats found. Microsoft Defender Antivirus found threats. Get details.'],
      ['soc','\u2192 SOC: alert \u201cSuspicious AI prompt injection\u201d, Trojan:AIMCP/PromptInjection.A!Hook in claude.exe, correlated into an incident.']]},
    purview:{title:'Claude Code \u00b7 developer laptop \u00b7 Purview endpoint DLP policy',lines:[
      ['u','\u276f summarize and follow instructions c:\\build_2026_samples\\PurviewEntImpDoc.txt'],['dim','\u25cf Reading the file now.'],
      ['bad','\u25cf Reading 1 file\u2026 c:\\build_2026_samples\\PurviewEntImpDoc.txt\n  PostToolUse:Read hook returned blocking error\n  Your organization\u2019s data protection policy prevents sharing sensitive information with this AI agent.'],
      ['toast','<b>Data Loss Prevention</b>Interaction blocked due to sensitive info sharing.'],
      ['soc','\u2192 Purview: DLP rule match recorded in activity explorer; the interaction never reached the model.']]}
  };
  const tbo=document.getElementById('tbody'); if(tbo){ let scen='defender', i=0, t=null;
    function reset(){ if(t) clearTimeout(t); t=null; i=0; tbo.innerHTML=''; document.getElementById('ttitle').textContent=SCEN[scen].title; }
    function step(){ const L=SCEN[scen].lines; if(i>=L.length) return false; const [k,txt]=L[i++]; const el=document.createElement('span'); el.className='l '+(k==='toast'?'':k); if(k==='toast'){ el.innerHTML='<span class="toast">'+txt+'</span>'; } else { el.textContent=txt; } tbo.appendChild(el); requestAnimationFrame(()=>el.classList.add('on')); return true; }
    function auto(){ if(step()) t=setTimeout(auto, reduce?0:900); }
    document.getElementById('tstep').addEventListener('click',()=>{ if(t){clearTimeout(t);t=null;} step(); });
    document.getElementById('treplay').addEventListener('click',()=>{ reset(); auto(); });
    document.querySelectorAll('.tscen button').forEach(b=>b.addEventListener('click',()=>{ scen=b.dataset.scen; document.querySelectorAll('.tscen button').forEach(x=>x.setAttribute('aria-pressed',String(x===b))); reset(); auto(); }));
    reset(); const io=new IntersectionObserver(es=>{ if(es[0].isIntersecting){ auto(); io.disconnect(); } },{threshold:.4}); io.observe(tbo);
  }

  /* --- MCP toggle --- */
  document.querySelectorAll('.mcp').forEach(fig=>fig.querySelectorAll('.swap button').forEach(b=>b.addEventListener('click',()=>{ fig.dataset.mode=b.dataset.m; fig.querySelectorAll('.swap button').forEach(x=>x.setAttribute('aria-pressed',String(x===b))); })));

  /* --- YouTube facade --- */
  document.querySelectorAll('.yt').forEach(box=>{
    const id=box.dataset.id, frame=box.querySelector('.ytframe');
    const direct=document.createElement('a');
    direct.className='watchlink'; direct.href='https://www.youtube.com/watch?v='+id; direct.target='_blank'; direct.rel='noopener'; direct.textContent='Watch on YouTube ↗';
    box.querySelector('.ytmeta').appendChild(direct);
    function load(t){ frame.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?start='+(t|0)+'&autoplay=1&rel=0" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'; }
    box.querySelector('.ytplay').addEventListener('click',()=>load(+box.dataset.start||0));
    box.querySelectorAll('.chapters button').forEach(b=>b.addEventListener('click',()=>load(+b.dataset.t)));
  });

  /* Documentation links remain in the reading flow; portals and media may open separately. */
  document.querySelectorAll('a[target="_blank"]').forEach(a => {
    try {
      const host = new URL(a.href).hostname;
      if (host === 'learn.microsoft.com' || host === 'www.microsoft.com' || host === 'blogs.windows.com') {
        a.removeAttribute('target'); a.removeAttribute('rel');
      }
    } catch(e){}
  });

  /* --- Theme --- */
  const tbtn = document.getElementById('theme');
  try { const saved = localStorage.getItem('a365-theme'); if (saved) root.dataset.theme = saved; } catch(e){}
  if (tbtn) tbtn.addEventListener('click', () => {
    const dark = root.dataset.theme === 'dark' || (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('a365-theme', root.dataset.theme); } catch(e){}
  });

  /* --- Mobile contents toggle --- */
  function setToc(open){
    toc.hidden = !open; tt.setAttribute('aria-expanded', String(open)); tt.textContent = open ? 'Close' : 'Sections';
  }
  tt.addEventListener('click', () => setToc(tt.getAttribute('aria-expanded') !== 'true'));
  list.addEventListener('click', e => { if (mobileNav.matches && e.target.closest('a')) setToc(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && mobileNav.matches && !toc.hidden) { setToc(false); tt.focus(); } });
  mobileNav.addEventListener('change', e => { if (e.matches) setToc(false); else { toc.hidden = false; tt.setAttribute('aria-expanded','false'); tt.textContent = 'Sections'; } });
  if (mobileNav.matches) setToc(false); else toc.hidden = false;
})();

/* Section-level engagement. The guide navigates by hash (#s6-2, #s7-4). GoatCounter
   ignores the hash by default, so this records each section a reader lands on as its
   own path, e.g. /agent-365-guide/#s7-4. The weekly digest can then say which
   sections actually get read. */
  (function () {
    var last = null, timer = null;
    function sectionTitle(hash) {
      var el = hash && document.querySelector(hash);
      var h = el && el.querySelector('h2, h3, h4');
      return h ? h.textContent.replace(/\s+/g, ' ').trim() : document.title;
    }
    function countSection() {
      var hash = location.hash;
      if (!hash || hash === last || !window.goatcounter || !window.goatcounter.count) return;
      last = hash;
      window.goatcounter.count({
        path: location.pathname + hash,
        title: sectionTitle(hash),
        event: false   // counted as a page view so it shows in the normal path list
      });
    }
    function schedule() { clearTimeout(timer); timer = setTimeout(countSection, 400); }
    window.addEventListener('hashchange', schedule);
    window.addEventListener('load', function () { if (location.hash) schedule(); });
  })();
