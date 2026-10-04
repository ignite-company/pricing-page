from pathlib import Path

p = Path('index.html')
s = p.read_text()

# Calculator framing: keep the broader Ignite database proof, but use the real Wranglin campaign for forecasts.
s = s.replace(
'''          <p>Enter the economics of your junk removal business below. The model combines your numbers with Ignite's documented paid acquisition performance and a 90-day follow-up and reactivation model.</p>''',
'''          <p>Enter the economics of your junk removal business below. The broader Ignite database stays visible as proof, while the forecast itself is calibrated to a real completed-jobs campaign so the outputs stay grounded.</p>'''
)

s = s.replace(
'''          <p>Across Ignite's documented campaign history, we've tracked 2,000+ leads and $25,000+ in ad spend. For projections, this calculator uses a conservative $16.28 weighted historical CPL baseline from the campaign data analyzed here.</p>''',
'''          <p>Across Ignite's documented campaign history, we've tracked 2,000+ leads and $25,000+ in ad spend. The forecast below is intentionally more conservative: it is calibrated to Wranglin Wranglers' real campaign of 44 website leads from $1,463.54 in ad spend, 9 closed/completed jobs, and approximately $6,000 collected over 29.27 days.</p>'''
)

# Grounded defaults from the Wranglin campaign.
s = s.replace('id="calc-ticket" type="number" inputmode="decimal" min="50" step="25" value="500"',
              'id="calc-ticket" type="number" inputmode="decimal" min="50" step="25" value="667"')
s = s.replace('id="calc-close" type="number" inputmode="decimal" min="1" max="90" step="1" value="18"',
              'id="calc-close" type="number" inputmode="decimal" min="1" max="90" step="0.5" value="20.5"')
s = s.replace(
'''            <div class="calc-input-hint">The recovery model then estimates additional delayed, reactivated, and repeat opportunities from the same lead pool.</div>''',
'''            <div class="calc-input-hint">Wranglin Wranglers converted 9 of 44 tracked website leads into closed/completed jobs, or 20.5%. To keep the forecast conservative, the model uses the lower of your entered close rate and that measured 20.5% benchmark. No extra follow-up lift is automatically added.</div>'''
)

# Output labels and explanations.
s = s.replace('Revenue from immediate jobs plus estimated follow-up recoveries that land inside the engagement.',
              'Revenue from projected paid-lead jobs using the grounded Wranglin campaign baseline. No extra nurture or reactivation revenue is automatically added.')
s = s.replace('<span>Immediate jobs</span>', '<span>Projected paid-lead jobs</span>')
s = s.replace('<span>Follow-up / reactivation jobs</span>', '<span>Extra jobs assumed</span>')
s = s.replace('<span>Modeled cohort conversion</span>', '<span>Modeled lead-to-job conversion</span>')
s = s.replace('<h5>Revenue from customers who buy quickly</h5>', '<h5>Revenue from modeled paid-lead jobs</h5>')
s = s.replace('This is the revenue most owners see first when judging whether the ads worked.',
              'This is the base-case revenue generated from the modeled lead volume, close rate, and average job size.')
s = s.replace('<h5>Additional revenue recovered through follow-up + reactivation</h5>',
              '<h5>Additional follow-up + reactivation upside</h5>')
s = s.replace('Same lead pool. More time, trust, reminders, proof, repeat need, and continued contact before the next purchase happens.',
              'Not included in the base-case forecast. Any later jobs recovered through nurture, reactivation, repeat need, or referrals are treated as upside rather than promised revenue.')

old_disclaimer = '''        Projection model, not a guarantee. Paid acquisition uses a $16.28 weighted CPL baseline from the campaign dataset analyzed for this calculator. The proof summary above reflects 2,000+ tracked leads and $25,000+ in documented ad spend across Ignite's broader campaign history. Lead recovery uses the lifecycle model discussed on this page: a base 18% immediate conversion rate expanding to approximately 30% over the life of a cohort, scaled to the close rate entered above. The recovery lift represents delayed, reactivated, or repeat opportunity from the acquired cohort. Existing pre-Ignite database revenue is not added automatically. Actual results vary by market, service mix, pricing, lead quality, sales ability, seasonality, response speed, budget, and execution.'''
new_disclaimer = '''        Projection model, not a guarantee. The proof summary above reflects 2,000+ tracked leads and $25,000+ in documented ad spend across Ignite's broader campaign history. Forecast math is intentionally calibrated to the Wranglin Wranglers case: $1,463.54 ad spend produced 44 tracked website leads at $33.26 per lead, with 9 closed/completed jobs and approximately $6,000 collected over 29.27 days. The model uses that $33.26 CPL and will not assume a paid-lead close rate above the observed 9-of-44 rate of 20.5%; a lower close rate entered above is respected. No additional follow-up, reactivation, repeat, referral, or database revenue is automatically added. Profit uses the margin entered above, and net impact subtracts both advertising spend and the initial Scale implementation investment. Actual results vary by market, service mix, pricing, lead quality, sales ability, seasonality, response speed, budget, and execution.'''
s = s.replace(old_disclaimer, new_disclaimer)

# Replace the ROI projection script only.
start_marker = "<script>\n(function(){\n  var root = document.getElementById('ignite-roi-calculator');"
start = s.find(start_marker)
if start == -1:
    raise SystemExit('ROI script start not found')
end = s.find('</script>', start)
if end == -1:
    raise SystemExit('ROI script end not found')
end += len('</script>')

new_script = r'''<script>
(function(){
  var root = document.getElementById('ignite-roi-calculator');
  if(!root) return;

  // Grounded projection baseline: Wranglin Wranglers real campaign.
  var WRANGLIN_SPEND = 1463.54;
  var WRANGLIN_LEADS = 44;
  var WRANGLIN_REVENUE = 6000;
  var WRANGLIN_JOBS = 9;
  var WRANGLIN_DAILY_BUDGET = 50;
  var WRANGLIN_DAYS = WRANGLIN_SPEND / WRANGLIN_DAILY_BUDGET;
  var BASE_CPL = WRANGLIN_SPEND / WRANGLIN_LEADS;
  var BASE_CLOSE = WRANGLIN_JOBS / WRANGLIN_LEADS;
  var BASE_TICKET = WRANGLIN_REVENUE / WRANGLIN_JOBS;
  var BASE_ROAS = WRANGLIN_REVENUE / WRANGLIN_SPEND;

  var SCALE_FEE = 3500;
  var FOUNDATION_FEE = 1500;

  var ticket = document.getElementById('calc-ticket');
  var closeRate = document.getElementById('calc-close');
  var margin = document.getElementById('calc-margin');
  var budget = document.getElementById('calc-budget');
  var foundationOrganicLeads = document.getElementById('foundation-organic-leads');
  var foundationOrganicClose = document.getElementById('foundation-organic-close');

  function val(el, fallback){
    var n = parseFloat(el.value);
    return isFinite(n) ? n : fallback;
  }

  function clamp(n, min, max){
    return Math.min(max, Math.max(min, n));
  }

  function money(n){
    var sign = n < 0 ? '-' : '';
    return sign + '$' + Math.abs(n).toLocaleString('en-US',{maximumFractionDigits:0});
  }

  function number(n){
    return Math.round(n).toLocaleString('en-US');
  }

  function pct(n){
    return (n * 100).toFixed(n * 100 < 10 ? 1 : 0) + '%';
  }

  function simulate(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){
    // Never assume better paid-lead conversion than the measured Wranglin baseline.
    // If the prospect's real close rate is lower, honor the lower number.
    var modeledClose = Math.min(enteredCloseRate, BASE_CLOSE);
    var adSpend = dailyBudget * days;
    var leads = adSpend / BASE_CPL;
    var jobs = leads * modeledClose;
    var revenue = jobs * avgTicket;
    var grossProfit = revenue * profitMargin;
    var net = grossProfit - adSpend - SCALE_FEE;
    var cac = jobs > 0 ? adSpend / jobs : 0;

    var dailyLeads = dailyBudget / BASE_CPL;
    var dailyContribution = (dailyLeads * modeledClose * avgTicket * profitMargin) - dailyBudget;
    var breakEvenDay = dailyContribution > 0 ? Math.ceil(SCALE_FEE / dailyContribution) : null;

    return {
      days:days,
      leads:leads,
      jobs:jobs,
      immediateJobs:jobs,
      recoveredJobs:0,
      revenue:revenue,
      immediateRevenue:revenue,
      recoveredRevenue:0,
      grossProfit:grossProfit,
      adSpend:adSpend,
      net:net,
      breakEvenDay:breakEvenDay,
      cac:cac,
      eventualRate:modeledClose,
      enteredRate:enteredCloseRate,
      baselineCpl:BASE_CPL,
      baselineClose:BASE_CLOSE,
      baselineTicket:BASE_TICKET,
      baselineRoas:BASE_ROAS,
      baselineDays:WRANGLIN_DAYS
    };
  }

  function setText(id, value){
    var el = document.getElementById(id);
    if(el) el.textContent = value;
  }

  function render(){
    var avgTicket = Math.max(1, val(ticket,BASE_TICKET));
    var enteredCloseRate = clamp(val(closeRate,BASE_CLOSE*100)/100, .01, .90);
    var profitMargin = clamp(val(margin,50)/100, .01, .95);
    var dailyBudget = Math.max(1, val(budget,50));

    var r90 = simulate(90,avgTicket,enteredCloseRate,profitMargin,dailyBudget);
    var r180 = simulate(180,avgTicket,enteredCloseRate,profitMargin,dailyBudget);
    var r365 = simulate(365,avgTicket,enteredCloseRate,profitMargin,dailyBudget);

    setText('calc-revenue90',money(r90.revenue));
    setText('calc-breakeven',r365.breakEvenDay && r365.breakEvenDay <= 365 ? r365.breakEvenDay + ' days' : '365+ days');
    setText('calc-net90',money(r90.net));
    setText('calc-leads90',number(r90.leads));
    setText('calc-immediate-jobs',number(r90.immediateJobs));
    setText('calc-recovered-jobs','0');
    setText('calc-total-jobs',number(r90.jobs));
    setText('calc-adspend90',money(r90.adSpend));
    setText('calc-grossprofit90',money(r90.grossProfit));
    setText('calc-cac90',money(r90.cac));
    setText('calc-eventual-rate',pct(r90.eventualRate));
    setText('calc-immediate-revenue',money(r90.immediateRevenue));
    setText('calc-recovered-revenue','$0');

    var profitPerJob = avgTicket * profitMargin;
    var foundationJobs = profitPerJob > 0 ? Math.ceil(FOUNDATION_FEE / profitPerJob) : 0;
    var organicLeads = foundationOrganicLeads ? Math.max(0, val(foundationOrganicLeads,12)) : 0;
    var organicClose = foundationOrganicClose ? clamp(val(foundationOrganicClose,25)/100, .01, .95) : .25;
    var organicJobsPerMonth = organicLeads * organicClose;
    var organicGrossProfitPerMonth = organicJobsPerMonth * profitPerJob;
    var foundationMonths = organicGrossProfitPerMonth > 0 ? FOUNDATION_FEE / organicGrossProfitPerMonth : null;
    var foundationDays = foundationMonths !== null ? Math.max(1, Math.ceil(foundationMonths * 30.44)) : null;

    setText('calc-foundation-jobs',foundationJobs + (foundationJobs === 1 ? ' job' : ' jobs'));
    setText('calc-foundation-jobs-month',organicJobsPerMonth.toFixed(organicJobsPerMonth < 10 ? 1 : 0) + ' / mo');
    setText('calc-foundation-time',foundationDays ? foundationDays + (foundationDays === 1 ? ' day' : ' days') : '-');
    setText('calc-foundation-time-detail',foundationDays ? 'At your current organic lead pace, before assuming any lift from the new systems.' : 'Enter your current monthly organic lead flow.');

    var projections = document.getElementById('calc-projections');
    if(projections){
      var cards = [
        {label:'90 days',data:r90},
        {label:'6 months',data:r180},
        {label:'12 months',data:r365}
      ];
      projections.innerHTML = cards.map(function(c){
        return '<div class="projection-card">' +
          '<div class="period">'+c.label+'</div>' +
          '<div class="projection-revenue">'+money(c.data.revenue)+'</div>' +
          '<div class="projection-row"><span>Projected jobs</span><b>'+number(c.data.jobs)+'</b></div>' +
          '<div class="projection-row"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +
          '<div class="projection-row"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +
          '<div class="projection-row"><span>Net after ads + implementation</span><b>'+money(c.data.net)+'</b></div>' +
        '</div>';
      }).join('');
    }
  }

  [ticket,closeRate,margin,budget,foundationOrganicLeads,foundationOrganicClose].filter(Boolean).forEach(function(el){
    el.addEventListener('input',render);
    el.addEventListener('change',render);
  });

  render();
})();
</script>'''

s = s[:start] + new_script + s[end:]

# Sanity checks.
checks = [
    'WRANGLIN_SPEND = 1463.54',
    'WRANGLIN_LEADS = 44',
    'WRANGLIN_REVENUE = 6000',
    'WRANGLIN_JOBS = 9',
    'Math.min(enteredCloseRate, BASE_CLOSE)',
    '2,000+',
    '$25,000+',
    '$16.28',
    'value="20.5"',
    'value="667"',
    'No extra follow-up lift is automatically added.'
]
for x in checks:
    if x not in s:
        raise SystemExit(f'missing expected marker: {x}')

if 'RECOVERY_LIFT' in s:
    raise SystemExit('old recovery model still present')

p.write_text(s)
print('Wranglin grounded projection model applied')
