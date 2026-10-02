from pathlib import Path

p = Path('index.html')
s = p.read_text()
marker = '/* MOBILE COMPACT SALES EXPERIENCE V2 */'
if marker in s:
    print('compact mobile experience already applied')
    raise SystemExit(0)

css = r'''

/* MOBILE COMPACT SALES EXPERIENCE V2 */
@media (max-width:760px){
  /* Keep mobile readable, but stop stacking every desktop block vertically. */
  #ignite-offers-v7 .journey{padding:16px}
  #ignite-offers-v7 .journey-head{margin-bottom:14px}
  #ignite-offers-v7 .journey-head h3{font-size:24px;line-height:1.08}
  #ignite-offers-v7 .stage-grid{
    display:flex;
    gap:10px;
    overflow-x:auto;
    scroll-snap-type:x mandatory;
    scrollbar-width:none;
    margin-right:-16px;
    padding-right:16px;
  }
  #ignite-offers-v7 .stage-grid::-webkit-scrollbar{display:none}
  #ignite-offers-v7 .stage-card{
    flex:0 0 84%;
    scroll-snap-align:start;
    min-height:150px;
    padding:17px;
  }
  #ignite-offers-v7 .stage-top{margin-bottom:15px}
  #ignite-offers-v7 .stage-card h4{font-size:21px;margin-bottom:6px}
  #ignite-offers-v7 .stage-card p{font-size:14px;line-height:1.5}

  /* Calculator: headline economics first, details on demand. */
  #ignite-offers-v7 .calc-output-panel{padding:15px}
  #ignite-offers-v7 .calc-hero-results{gap:9px}
  #ignite-offers-v7 .calc-hero-card{padding:15px;min-height:0}
  #ignite-offers-v7 .calc-hero-card strong{font-size:34px}
  #ignite-offers-v7 .calc-metrics.mobile-compact-hidden,
  #ignite-offers-v7 .calc-recovery.mobile-compact-hidden{display:none!important}

  #ignite-offers-v7 .mobile-detail-toggle{
    width:100%;
    margin:10px 0 14px;
    min-height:46px;
    border:1px solid rgba(255,255,255,.11);
    border-radius:12px;
    background:rgba(255,255,255,.035);
    color:#eef2f5;
    font-size:14px;
    font-weight:850;
    cursor:pointer;
  }
  #ignite-offers-v7 .mobile-detail-toggle:after{content:'  +';color:var(--green)}
  #ignite-offers-v7 .mobile-detail-toggle.open:after{content:'  −'}

  /* 90d / 6mo / 12mo become swipe cards instead of three tall stacked cards. */
  #ignite-offers-v7 .calc-projections{
    display:flex!important;
    gap:10px;
    overflow-x:auto;
    scroll-snap-type:x mandatory;
    scrollbar-width:none;
    margin-right:-15px;
    padding:0 15px 4px 0;
  }
  #ignite-offers-v7 .calc-projections::-webkit-scrollbar{display:none}
  #ignite-offers-v7 .projection-card{
    flex:0 0 86%;
    scroll-snap-align:start;
    min-width:0;
  }

  /* Foundation: headline stays visible, mini calculator expands only when wanted. */
  #ignite-offers-v7 .foundation-mini{padding:16px}
  #ignite-offers-v7 .foundation-mini-head{margin-bottom:8px}
  #ignite-offers-v7 .foundation-mini-grid.mobile-compact-hidden,
  #ignite-offers-v7 .foundation-stats.mobile-compact-hidden,
  #ignite-offers-v7 .foundation-sources.mobile-compact-hidden{display:none!important}

  /* Payment selector in one compact row instead of three full-width rows. */
  #ignite-offers-v7 .billing-wrap{padding:15px;gap:12px}
  #ignite-offers-v7 .billing-toggle{
    display:grid;
    grid-template-columns:repeat(3,minmax(0,1fr));
    gap:6px;
    width:100%;
  }
  #ignite-offers-v7 .bill-btn{
    min-width:0;
    width:100%;
    padding:10px 5px;
    font-size:12px;
    line-height:1.15;
  }
  #ignite-offers-v7 .bill-btn .save{font-size:9px;line-height:1.2}

  /* Pricing cards show the decision-making info first. Full deliverables expand. */
  #ignite-offers-v7 .plan-inner{padding:18px}
  #ignite-offers-v7 .plan .divider.mobile-compact-hidden,
  #ignite-offers-v7 .plan .includes-title.mobile-compact-hidden,
  #ignite-offers-v7 .plan .features.mobile-compact-hidden,
  #ignite-offers-v7 .plan .positioning.mobile-compact-hidden{display:none!important}
  #ignite-offers-v7 .plan-desc{margin-bottom:4px}
  #ignite-offers-v7 .mobile-plan-toggle{margin:14px 0 2px}

  /* Comparison remains available without occupying the page by default. */
  #ignite-offers-v7 .compare .rows.mobile-compact-hidden{display:none!important}
  #ignite-offers-v7 .compare-head{padding:16px;align-items:flex-start;flex-direction:column;gap:10px}
  #ignite-offers-v7 .compare .mobile-detail-toggle{margin:0}

  /* Compact lower-page informational sections. */
  #ignite-offers-v7 .ownership{padding:15px;gap:10px}
  #ignite-offers-v7 .care{padding:16px;gap:12px}

  /* Sticky jump keeps pricing one tap away without forcing extra scrolling. */
  #ignite-mobile-invest-jump{
    position:fixed;
    z-index:9999;
    left:12px;
    right:12px;
    bottom:max(10px,env(safe-area-inset-bottom));
    min-height:48px;
    border:1px solid rgba(255,40,72,.55);
    border-radius:14px;
    background:rgba(10,12,15,.92);
    box-shadow:0 14px 40px rgba(0,0,0,.5),0 0 0 1px rgba(255,40,72,.12) inset;
    backdrop-filter:blur(16px);
    -webkit-backdrop-filter:blur(16px);
    color:#fff;
    display:flex;
    align-items:center;
    justify-content:center;
    text-decoration:none;
    font-size:14px;
    font-weight:900;
  }
  #ignite-mobile-invest-jump span{color:var(--green);margin-left:7px}
  #ignite-offers-v7 .shell{padding-bottom:max(92px,calc(env(safe-area-inset-bottom) + 82px))}
}

@media (min-width:761px){
  #ignite-mobile-invest-jump,
  #ignite-offers-v7 .mobile-detail-toggle{display:none!important}
}
'''

js = r'''
<script>
(function(){
  const mq = window.matchMedia('(max-width:760px)');
  if(!mq.matches) return;
  const root = document.getElementById('ignite-offers-v7');
  if(!root || root.dataset.compactMobile === '1') return;
  root.dataset.compactMobile = '1';

  function makeToggle(labelClosed,labelOpen,targets,extraClass){
    const b=document.createElement('button');
    b.type='button';
    b.className='mobile-detail-toggle'+(extraClass?' '+extraClass:'');
    b.textContent=labelClosed;
    b.setAttribute('aria-expanded','false');
    targets.forEach(el=>el && el.classList.add('mobile-compact-hidden'));
    b.addEventListener('click',function(){
      const opening=b.getAttribute('aria-expanded')!=='true';
      b.setAttribute('aria-expanded',opening?'true':'false');
      b.classList.toggle('open',opening);
      b.textContent=opening?labelOpen:labelClosed;
      targets.forEach(el=>el && el.classList.toggle('mobile-compact-hidden',!opening));
    });
    return b;
  }

  // Main calculator details.
  const output=root.querySelector('.calc-output-panel');
  const hero=output&&output.querySelector('.calc-hero-results');
  const metrics=output&&output.querySelector('.calc-metrics');
  const recovery=output&&output.querySelector('.calc-recovery');
  if(output&&hero&&(metrics||recovery)){
    const btn=makeToggle('See full 90-day breakdown','Hide full 90-day breakdown',[metrics,recovery]);
    hero.insertAdjacentElement('afterend',btn);
  }

  // Foundation mini calculator.
  const foundation=root.querySelector('.foundation-mini');
  if(foundation){
    const head=foundation.querySelector('.foundation-mini-head');
    const grid=foundation.querySelector('.foundation-mini-grid');
    const stats=foundation.querySelector('.foundation-stats');
    const sources=foundation.querySelector('.foundation-sources');
    if(head&&(grid||stats)){
      const btn=makeToggle('Calculate Foundation recovery','Hide Foundation breakdown',[grid,stats,sources]);
      head.insertAdjacentElement('afterend',btn);
    }
  }

  // Plan deliverables.
  root.querySelectorAll('.plan').forEach(function(plan){
    const desc=plan.querySelector('.plan-desc');
    const divider=plan.querySelector('.divider');
    const includes=plan.querySelector('.includes-title');
    const features=plan.querySelector('.features');
    const positioning=plan.querySelector('.positioning');
    const targets=[divider,includes,features,positioning].filter(Boolean);
    if(desc&&targets.length){
      const btn=makeToggle('See everything included','Hide full deliverables',targets,'mobile-plan-toggle');
      desc.insertAdjacentElement('afterend',btn);
    }
  });

  // Comparison table.
  const compare=root.querySelector('.compare');
  if(compare){
    const head=compare.querySelector('.compare-head');
    const rows=compare.querySelector('.rows');
    if(head&&rows){
      const btn=makeToggle('Compare the plans','Hide comparison',[rows]);
      head.appendChild(btn);
    }
  }

  // Sticky jump to investment selector.
  const billing=root.querySelector('.billing-wrap');
  if(billing){
    if(!billing.id) billing.id='ignite-investment-options';
    const jump=document.createElement('a');
    jump.id='ignite-mobile-invest-jump';
    jump.href='#'+billing.id;
    jump.innerHTML='View investment options <span>↓</span>';
    jump.addEventListener('click',function(e){
      e.preventDefault();
      billing.scrollIntoView({behavior:'smooth',block:'start'});
    });
    document.body.appendChild(jump);

    const io=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){ jump.style.display=entry.isIntersecting?'none':'flex'; });
    },{threshold:.15});
    io.observe(billing);
  }
})();
</script>
'''

# Add CSS before the final style close and JS before the end of the file.
pos = s.rfind('</style>')
if pos == -1:
    raise SystemExit('No </style> found')
s = s[:pos] + css + '\n' + s[pos:]
s = s + '\n' + js
p.write_text(s)
print('compact mobile experience applied')
