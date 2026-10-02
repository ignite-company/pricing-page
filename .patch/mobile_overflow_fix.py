from pathlib import Path

p = Path('index.html')
s = p.read_text()
marker = '/* MOBILE OVERFLOW CONTAINMENT V3 */'
if marker in s:
    print('mobile overflow fix already applied')
    raise SystemExit(0)

css = r'''

/* MOBILE OVERFLOW CONTAINMENT V3 */
@media (max-width:760px){
  /* Hard containment so calculator and pricing sections never render wider than the phone. */
  #ignite-offers-v7,
  #ignite-offers-v7 .shell,
  #ignite-offers-v7 .roi-calc,
  #ignite-offers-v7 .calc-head,
  #ignite-offers-v7 .calc-evidence,
  #ignite-offers-v7 .calc-workspace,
  #ignite-offers-v7 .calc-inputs,
  #ignite-offers-v7 .calc-output-panel,
  #ignite-offers-v7 .calc-hero-results,
  #ignite-offers-v7 .calc-metrics,
  #ignite-offers-v7 .calc-recovery,
  #ignite-offers-v7 .calc-section-title,
  #ignite-offers-v7 .foundation-mini,
  #ignite-offers-v7 .foundation-mini-head,
  #ignite-offers-v7 .foundation-mini-grid,
  #ignite-offers-v7 .foundation-mini-inputs,
  #ignite-offers-v7 .foundation-mini-results,
  #ignite-offers-v7 .foundation-stats,
  #ignite-offers-v7 .billing-wrap,
  #ignite-offers-v7 .billing-toggle,
  #ignite-offers-v7 .primary-grid,
  #ignite-offers-v7 .plan,
  #ignite-offers-v7 .plan-inner,
  #ignite-offers-v7 .ownership,
  #ignite-offers-v7 .care,
  #ignite-offers-v7 .compare,
  #ignite-offers-v7 .sales-card{
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
  }

  #ignite-offers-v7 .calc-workspace{
    display:block!important;
  }

  #ignite-offers-v7 .calc-inputs{
    margin:0 0 12px!important;
  }

  #ignite-offers-v7 .calc-workspace > *,
  #ignite-offers-v7 .calc-output-panel > *,
  #ignite-offers-v7 .foundation-mini > *,
  #ignite-offers-v7 .plan-inner > *{
    min-width:0!important;
    max-width:100%!important;
  }

  #ignite-offers-v7 .calc-evidence{
    display:grid!important;
    grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
    overflow:visible!important;
  }

  #ignite-offers-v7 .evidence-chip{
    min-width:0!important;
    max-width:100%!important;
    overflow:hidden;
  }

  #ignite-offers-v7 .evidence-chip:last-child{
    grid-column:1/-1!important;
  }

  #ignite-offers-v7 .evidence-chip strong,
  #ignite-offers-v7 .evidence-chip span,
  #ignite-offers-v7 .calc-small-copy,
  #ignite-offers-v7 .calc-kicker,
  #ignite-offers-v7 .calc-metric,
  #ignite-offers-v7 .recovery-card,
  #ignite-offers-v7 .projection-row,
  #ignite-offers-v7 .foundation-result,
  #ignite-offers-v7 .plan-desc,
  #ignite-offers-v7 .feature,
  #ignite-offers-v7 .positioning{
    overflow-wrap:anywhere;
    word-break:normal;
  }

  #ignite-offers-v7 .calc-hero-results,
  #ignite-offers-v7 .calc-metrics{
    grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;
  }

  #ignite-offers-v7 .calc-hero-card,
  #ignite-offers-v7 .calc-metric,
  #ignite-offers-v7 .recovery-card{
    min-width:0!important;
    max-width:100%!important;
  }

  #ignite-offers-v7 .calc-hero-card.primary{
    grid-column:1/-1!important;
  }

  /* Keep the intentional swipe rows inside their own viewport instead of widening the page. */
  #ignite-offers-v7 .stage-grid,
  #ignite-offers-v7 .calc-projections{
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
    margin-left:0!important;
    margin-right:0!important;
    overscroll-behavior-x:contain;
    -webkit-overflow-scrolling:touch;
  }

  #ignite-offers-v7 .calc-projections{
    padding-right:0!important;
  }

  #ignite-offers-v7 .projection-card{
    flex:0 0 88%!important;
    max-width:88%!important;
  }

  #ignite-offers-v7 .stage-card{
    max-width:84%!important;
  }

  /* Inputs and buttons should never force a wider layout on iOS. */
  #ignite-offers-v7 input,
  #ignite-offers-v7 button,
  #ignite-offers-v7 select,
  #ignite-offers-v7 textarea{
    max-width:100%!important;
    min-width:0!important;
  }

  #ignite-offers-v7 .price,
  #ignite-offers-v7 .badge,
  #ignite-offers-v7 .calc-output-top,
  #ignite-offers-v7 .projection-row{
    min-width:0!important;
  }
}
'''

pos = s.rfind('</style>')
if pos == -1:
    raise SystemExit('No </style> found')
s = s[:pos] + css + '\n' + s[pos:]
p.write_text(s)
print('mobile overflow containment applied')
