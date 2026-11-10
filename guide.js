/* Behaviour shared by every page of the guide. Loaded at the end of <body>
   after a365-data.js. Every hook is optional: a page without a section
   simply skips that part. Each part also runs on its own: if one throws,
   say because an element it expects has been renamed, the console names the
   part that was skipped and every other part still runs. */
(function(){
  const D = window.A365 || { capabilities: [], changes: [], tiers: {} };
  if (!window.A365) console.warn('guide.js: a365-data.js did not load, so statuses, prices and the changelog will not render');
  const root = document.documentElement;
  const cap = Object.fromEntries(D.capabilities.map(c => [c.key, c]));
  const get = (path) => path.split('.').reduce((o,k)=>o && o[k], D);
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const part = (name, fn) => { try { fn(); } catch (e) { console.warn('guide.js: ' + name + ' skipped.', e); } };

  /* Shared by several parts. Lookups only; each part checks what it needs. */
  const header = document.querySelector('.topbar');
  const headerHeight = () => header ? header.getBoundingClientRect().height : 0;
  const list = document.getElementById('toc-list');
  const toc = document.getElementById('toc'), tt = document.getElementById('toc-toggle');
  const mobileNav = matchMedia('(max-width: 960px)');
  let onScroll = () => {};   /* the scroll spy replaces this when the contents panel exists */

  /* --- Sticky header --- */
  part('sticky header', () => {
    /* Keep sticky-header offsets accurate across the two-row mobile header. */
    if (!header) return;
    const syncHeaderHeight = () => root.style.setProperty('--header-h', Math.ceil(headerHeight() + 12) + 'px');
    syncHeaderHeight();
    if ('ResizeObserver' in window) new ResizeObserver(syncHeaderHeight).observe(header);
    window.addEventListener('resize', syncHeaderHeight, {passive:true});
  });

  /* --- Render values from the data block --- */
  part('data values', () => {
  document.querySelectorAll('[data-val]').forEach(el => { const v = get(el.dataset.val); if (v != null) el.textContent = v; });
  const shown = D.capabilities.filter(c => !c.hidden);
  const summaries = {
    capabilities: shown.length,
    previews: shown.filter(c => c.tier !== 'ga').length
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
  });

  /* Dates in the data file read "9 November 2026". */
  const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
  const parseDay = (s) => { const m = /^(\d{1,2}) (\w+) (\d{4})$/.exec(s || ''); const mo = m ? MONTHS.indexOf(m[2]) : -1; return mo < 0 ? null : new Date(Date.UTC(+m[3], mo, +m[1])); };
  const isoDay = (d) => d.toISOString().slice(0, 10);
  const shortDay = (s) => { const m = /^(\d{1,2}) (\w+)/.exec(s); return m ? m[1] + ' ' + m[2].slice(0, 3) : s; };
  const secLabel = (id) => id.slice(1).replace('-', '.');

  /* --- Status board: chapter 10's table, its filters and the status meter ---
     The rows in index.html are a static copy for crawlers; these are rendered
     from the data file, so a status is right even when that copy is stale. */
  const TIER_ORDER = ['ga', 'preview', 'frontier', 'roadmap'];
  const visibleCaps = D.capabilities.filter(c => !c.hidden);
  const family = (where) => /Global Secure Access/.test(where) ? 'Global Secure Access' : /Entra/.test(where) ? 'Entra' : /Defender/.test(where) ? 'Defender' : /Purview/.test(where) ? 'Purview' : /Intune|Windows/.test(where) ? 'Intune and Windows' : 'Admin centre';
  const FAMILIES = ['Admin centre', 'Entra', 'Global Secure Access', 'Purview', 'Defender', 'Intune and Windows'];
  const filter = { tier: '', family: '', q: '' };
  let applyBoard = () => {};

  part('status board', () => {
  const tb = document.querySelector('#avail tbody'); if (!tb) return;
  const hasSection = (id) => id && document.getElementById(id);
  tb.innerHTML = '';
  const rows = visibleCaps.map(c => {
    const tr = document.createElement('tr'); tr.dataset.tier = c.key; tr.dataset.tierValue = c.tier;
    const read = hasSection(c.sec) ? `<a href="#${c.sec}">${secLabel(c.sec)}</a>` : '';
    tr.innerHTML = `<td class="c-name">${c.name}</td><td class="c-status"><span class="badge t-${c.tier}">${D.tiers[c.tier].label}</span></td><td class="c-note muted">${c.note || ''}</td><td class="c-where">${c.where}</td><td class="c-read">${read}</td>`;
    tb.appendChild(tr);
    return { tr, c, fam: family(c.where), text: (c.name + ' ' + (c.note || '') + ' ' + c.where + ' ' + D.tiers[c.tier].label).toLowerCase() };
  });

  const tools = document.getElementById('board-tools'), count = document.getElementById('board-count');
  const empty = document.getElementById('board-empty'), reset = document.getElementById('board-reset');
  const famCount = (f) => rows.filter(r => r.fam === f).length;
  if (tools) {
    tools.innerHTML = `<div class="chips" role="group" aria-label="Filter by product"><button type="button" data-fam="" aria-pressed="true">All products</button>${FAMILIES.filter(famCount).map(f => `<button type="button" data-fam="${f}" aria-pressed="false">${f} <i>${famCount(f)}</i></button>`).join('')}</div><label class="find"><span>Find</span><input type="search" id="board-q" placeholder="MCP, Conditional Access, Bedrock" autocomplete="off" spellcheck="false"></label>`;
    tools.querySelectorAll('[data-fam]').forEach(b => b.addEventListener('click', () => { filter.family = b.dataset.fam; applyBoard(); }));
    tools.querySelector('#board-q').addEventListener('input', e => { filter.q = e.target.value.trim().toLowerCase(); applyBoard(); });
  }
  const clearAll = () => { filter.tier = filter.family = filter.q = ''; const q = document.getElementById('board-q'); if (q) q.value = ''; applyBoard(); };
  const clear = document.getElementById('board-clear'), copy = document.getElementById('board-copy');
  if (reset) reset.addEventListener('click', clearAll);
  if (clear) clear.addEventListener('click', clearAll);

  /* The address bar follows the status and product filters, so the view can be shared. */
  const viewQuery = () => { const p = new URLSearchParams(); if (filter.tier) p.set('status', filter.tier); if (filter.family) p.set('product', filter.family.toLowerCase()); const q = p.toString(); return q ? '?' + q : ''; };
  const syncAddress = () => { try { const want = location.pathname + viewQuery() + location.hash; if (want !== location.pathname + location.search + location.hash) history.replaceState(null, '', want); } catch (e) {} };
  if (copy) {
    copy.hidden = false;
    copy.addEventListener('click', () => {
      const url = location.origin + location.pathname + viewQuery() + '#s10';
      const done = () => { copy.textContent = 'Link copied'; setTimeout(() => { copy.textContent = 'Copy link to this view'; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, () => window.prompt('Copy this link', url));
      else window.prompt('Copy this link', url);
    });
  }

  /* Which filters readers reach for goes to the weekly digest: one count per filter per visit,
     as #filter-preview or #filter-defender. What is typed in the find box is never recorded. */
  const counted = new Set();
  const countFilter = (v) => { if (!v || counted.has(v) || !window.goatcounter || !window.goatcounter.count) return; counted.add(v);
    window.goatcounter.count({ path: location.pathname + '#filter-' + v.toLowerCase().replace(/[^a-z]+/g, '-'), title: 'Status board filter: ' + v, event: false }); };

  applyBoard = () => {
    let shown = 0;
    rows.forEach(r => {
      const out = (filter.tier && r.c.tier !== filter.tier) || (filter.family && r.fam !== filter.family) || (filter.q && !r.text.includes(filter.q));
      r.tr.classList.toggle('f-out', !!out);
      if (!out && !r.tr.classList.contains('is-hidden')) shown++;
    });
    if (tools) tools.querySelectorAll('[data-fam]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.fam === filter.family)));
    document.querySelectorAll('.meter [data-tier-filter]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.tierFilter === filter.tier)));
    const gaOnly = !!(document.getElementById('ga-only') || {}).checked;
    if (count) count.textContent = shown === rows.length ? `${rows.length} controls` : `Showing ${shown} of ${rows.length} controls` + (gaOnly ? '. The GA only switch in the header is on.' : '');
    if (empty) empty.hidden = shown > 0;
    const wrap = document.querySelector('.board-tbl'); if (wrap) wrap.hidden = shown === 0;
    if (clear) clear.hidden = !(filter.tier || filter.family || filter.q) || shown === 0;
    syncAddress(); countFilter(filter.tier); countFilter(filter.family);
  };

  /* A link can open the board already filtered: index.html?status=preview&product=Defender#s10 */
  try {
    const qs = new URLSearchParams(location.search), st = (qs.get('status') || '').toLowerCase(), pr = (qs.get('product') || '').toLowerCase();
    if (TIER_ORDER.includes(st)) filter.tier = st;
    const f = FAMILIES.find(x => x.toLowerCase() === pr); if (f) filter.family = f;
  } catch (e) {}
  applyBoard();
  });

  /* --- Status meter: one bar, a segment per status, sized by how many controls hold it --- */
  part('status meter', () => {
  const n = Object.fromEntries(TIER_ORDER.map(t => [t, visibleCaps.filter(c => c.tier === t).length]));
  const total = visibleCaps.length; if (!total) return;
  const board = document.getElementById('board');
  document.querySelectorAll('.meter[data-meter]').forEach(el => {
    const hero = el.dataset.meter === 'hero';
    const seg = TIER_ORDER.filter(t => n[t]).map(t => `<button type="button" class="seg s-${t}" style="flex-grow:${n[t]}" data-tier-filter="${t}" aria-pressed="false" title="${D.tiers[t].label}: ${n[t]} of ${total}"><b>${n[t]}</b><span>${D.tiers[t].label}</span></button>`).join('');
    el.innerHTML = `<p class="k">${hero ? 'Status today' : 'Filter by status'}</p><div class="meter-bar" role="group" aria-label="Controls by status. Select one to filter the list.">${seg}</div>` + (hero && board ? `<p class="meter-more"><a href="#s10">All ${total} controls, with what each one needs</a></p>` : '');
    el.querySelectorAll('[data-tier-filter]').forEach(b => b.addEventListener('click', () => {
      filter.tier = filter.tier === b.dataset.tierFilter ? '' : b.dataset.tierFilter;
      if (hero) { filter.tier = b.dataset.tierFilter; filter.family = ''; }
      applyBoard();
      if (hero && board) { location.hash = '#s10'; }
    }));
  });
  applyBoard();
  });

  /* --- Latest changes: the newest entries about the product, not about the guide --- */
  const productChanges = (D.changes || []).filter(c => c.kind !== 'guide' && c.section);
  part('latest changes', () => {
  const here = /(^|\/)(index\.html)?$/.test(location.pathname);
  document.querySelectorAll('.latest[data-latest]').forEach(box => {
    const ol = box.querySelector('.latest-list'); if (!ol) return;
    productChanges.slice(0, +box.dataset.latest || 3).forEach(c => {
      const d = parseDay(c.date), li = document.createElement('li');
      const first = (c.text.match(/^.*?\.(?= [A-Z]|$)/) || [c.text])[0].replace(/\.$/, '');
      const secHref = (here || document.getElementById(c.section) ? '' : 'index.html') + '#' + c.section;
      li.innerHTML = `<a class="when" href="changes.html${d ? '#d' + isoDay(d) : ''}">${shortDay(c.date)}</a><a class="sec" href="${secHref}">${secLabel(c.section)}</a><span>${first}.</span>`;
      ol.appendChild(li);
    });
  });
  });

  /* --- Table of contents and scroll spy --- */
  part('contents panel', () => {
  if (!list || !toc) return;
  const heads = document.querySelectorAll('article h2, article h3');
  heads.forEach(h => {
    const sec = h.closest('section'); if (!sec || !sec.id) return;
    const li = document.createElement('li'); li.className = h.tagName === 'H2' ? 'l2' : 'l3'; li.dataset.for = sec.id;
    const a = document.createElement('a'); a.href = '#' + sec.id;
    const badge = h.querySelector('.badge');
    a.textContent = (h.textContent || '').replace(badge ? badge.textContent : '', '').trim();
    li.appendChild(a); list.appendChild(li);
  });

  /* Scroll spy */
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
  onScroll = () => {
    const y = window.scrollY + headerHeight() + 68; let best = targets[0];
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
    const offset = headerHeight() + 16;
    root.classList.add('no-smooth');
    window.scrollTo({top:window.scrollY + target.getBoundingClientRect().top - offset, behavior:'auto'});
    requestAnimationFrame(() => root.classList.remove('no-smooth')); refreshSpy();
  };
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('hashchange', refreshSpy);
  window.addEventListener('load', () => { const ready = document.fonts ? document.fonts.ready : Promise.resolve(); ready.then(() => setTimeout(alignInitialHash, 50)); });
  refreshSpy();
  });

  /* --- Updated markers: sections the last fortnight of product changes touched --- */
  part('updated markers', () => {
  const reviewed = parseDay(D.reviewed); if (!reviewed) return;
  const here = !!document.getElementById('board') || /licensing\.html$/.test(location.pathname);
  if (!here) return;
  const newest = new Map();
  productChanges.forEach(c => { const d = parseDay(c.date); if (d && (reviewed - d) / 864e5 <= 14 && !newest.has(c.section)) newest.set(c.section, c.date); });
  newest.forEach((date, id) => {
    const sec = document.getElementById(id); if (!sec) return;
    const h = sec.querySelector('h2, h3'); if (!h) return;
    const p = document.createElement('p'); p.className = 'upd';
    p.innerHTML = `<a href="changes.html#d${isoDay(parseDay(date))}">Updated ${date.replace(/ \d{4}$/, '')}</a>`;
    (h.closest('.shead') || h).after(p);
    const li = list && list.querySelector(`li[data-for="${id}"]`);
    if (li) { li.classList.add('has-upd'); const a = li.querySelector('a'); if (a) a.insertAdjacentHTML('beforeend', '<span class="vh"> (updated)</span>'); }
  });
  });

  /* --- GA-only filter --- */
  part('GA-only filter', () => {
  const ga = document.getElementById('ga-only'), count = document.getElementById('count');
  const tiered = [...document.querySelectorAll('[data-tier]')];
  function apply(){
    const gaOnly = !!(ga && ga.checked);
    tiered.forEach(el => el.classList.toggle('is-hidden', gaOnly && el.dataset.tierValue && el.dataset.tierValue !== 'ga'));
    if (count) count.textContent = gaOnly ? 'GA only' : '';
    applyBoard();
    onScroll();
  }
  if (ga) ga.addEventListener('change', apply);
  });

  /* --- Figure numbering --- */
  part('figure numbering', () => {
  document.querySelectorAll('figcaption .fn').forEach((b,i)=>{ b.textContent = 'Figure ' + (i+1) + '.'; });
  });

  /* --- Steppers --- */
  document.querySelectorAll('.stepper').forEach(fig=>part('stepper', ()=>{
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
  }));

  /* --- Plan selector --- */
  part('plan selector', () => {
  const planBtns=[...document.querySelectorAll('.plan button')], planMsg=document.getElementById('planmsg');
  const licRows=[...document.querySelectorAll('#s2-1 .tbl tbody tr')];
  function setPlan(p){ planBtns.forEach(b=>b.setAttribute('aria-pressed', String(b.dataset.plan===p))); let un=0;
    licRows.forEach(tr=>{ const base = tr.children[2].textContent.trim()==='Yes'; const ok = p==='base' ? base : true; tr.classList.toggle('unlock', ok); tr.classList.toggle('locked', !ok); if(ok) un++; });
    planMsg.textContent = p==='base' ? `${un} of ${licRows.length} capabilities. The registry, basic actions, rules and registry sync work without the add-on; everything else needs Agent 365.` : p==='addon' ? `All ${licRows.length} capabilities. E5 already includes Entra ID P2, so Conditional Access and ID Governance for agents need nothing more. Network controls for local agents on devices need Entra Internet Access.` : `All ${licRows.length} capabilities. E7 bundles Agent 365 with the Entra Suite, so the identity and network dependencies are included.`; }
  planBtns.forEach(b=>b.addEventListener('click',()=>setPlan(b.dataset.plan))); if(planBtns.length) setPlan('base');
  });

  /* --- Control plane hover --- */

  /* --- Conditional Access explorer --- */
  const CAtext={
    obo:{subj:'The user. The agent is the actor inside the token.',target:'Users and groups. The agent inherits the user\u2019s Conditional Access posture, so a risky user is prompted for MFA before the agent proceeds.',note:'Policies aimed at agent identities do not apply here. Do not expect an agent-scoped block to stop a delegated call.'},
    app:{subj:'The agent identity itself. No user is present.',target:'Agent identities, their blueprints, or custom security attributes. Blueprint targeting covers every child identity, present and future.',note:'The only grant control that makes sense is block; there is no user to satisfy MFA. Blueprint policies do not cover agent users.'},
    user:{subj:'The agent\u2019s user account, a real Entra user object.',target:'Agent users, selected individually or by custom security attribute, with the Agent risk condition. Device and network compliance apply only on endpoints such as Windows 365 Cloud PCs for Agents.',note:'Policies in the Users assignment exclude agent users, however they are targeted. Agent users cannot be scoped by group. Use the Agent execution environments condition so cloud-native agents are not blocked with no path to compliance.'}
  };
  document.querySelectorAll('.ca').forEach(fig=>part('Conditional Access figure', ()=>{
    const btns=[...fig.querySelectorAll('.pat button')];
    function set(p){ fig.dataset.pattern=p; btns.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.p===p)));
      const map={obo:'b-user',app:'b-id',user:'b-au'}, ln={obo:'l-user',app:'l-id',user:'l-au'};
      fig.querySelectorAll('.box').forEach(b=>{ const isS=b.classList.contains(map[p]); b.classList.toggle('subj',isS); b.classList.toggle('off', !isS && !b.classList.contains('bp')); });
      fig.querySelectorAll('.ln').forEach(l=>l.style.opacity = l.classList.contains(ln[p]) ? '1' : '0.12');
      fig.querySelector('.ca-subj').textContent=CAtext[p].subj; fig.querySelector('.ca-target').textContent=CAtext[p].target; fig.querySelector('.ca-note').textContent=CAtext[p].note; }
    btns.forEach(b=>b.addEventListener('click',()=>set(b.dataset.p))); set('obo');
  }));

  /* --- Terminal replay --- */
  part('terminal replay', () => {
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
  });

  /* --- MCP toggle --- */
  part('MCP toggle', () => {
  document.querySelectorAll('.mcp').forEach(fig=>fig.querySelectorAll('.swap button').forEach(b=>b.addEventListener('click',()=>{ fig.dataset.mode=b.dataset.m; fig.querySelectorAll('.swap button').forEach(x=>x.setAttribute('aria-pressed',String(x===b))); })));
  });

  /* --- YouTube facade --- */
  document.querySelectorAll('.yt').forEach(box=>part('video', ()=>{
    const id=box.dataset.id, frame=box.querySelector('.ytframe');
    const direct=document.createElement('a');
    direct.className='watchlink'; direct.href='https://www.youtube.com/watch?v='+id; direct.target='_blank'; direct.rel='noopener'; direct.textContent='Watch on YouTube ↗';
    box.querySelector('.ytmeta').appendChild(direct);
    function load(t){ frame.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?start='+(t|0)+'&autoplay=1&rel=0" title="YouTube video" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'; }
    box.querySelector('.ytplay').addEventListener('click',()=>load(+box.dataset.start||0));
    box.querySelectorAll('.chapters button').forEach(b=>b.addEventListener('click',()=>load(+b.dataset.t)));
  }));

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
  part('theme toggle', () => {
  const tbtn = document.getElementById('theme');
  try { const saved = localStorage.getItem('a365-theme'); if (saved) root.dataset.theme = saved; } catch(e){}
  if (tbtn) tbtn.addEventListener('click', () => {
    const dark = root.dataset.theme === 'dark' || (!root.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('a365-theme', root.dataset.theme); } catch(e){}
  });
  });

  /* --- Mobile contents toggle --- */
  part('mobile contents toggle', () => {
  if (!toc || !tt || !list) return;
  function setToc(open){
    toc.hidden = !open; tt.setAttribute('aria-expanded', String(open)); tt.textContent = open ? 'Close' : 'Sections';
  }
  tt.addEventListener('click', () => setToc(tt.getAttribute('aria-expanded') !== 'true'));
  list.addEventListener('click', e => { if (mobileNav.matches && e.target.closest('a')) setToc(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && mobileNav.matches && !toc.hidden) { setToc(false); tt.focus(); } });
  mobileNav.addEventListener('change', e => { if (e.matches) setToc(false); else { toc.hidden = false; tt.setAttribute('aria-expanded','false'); tt.textContent = 'Sections'; } });
  if (mobileNav.matches) setToc(false); else toc.hidden = false;
  });
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
