from pathlib import Path

p = Path('index.html')
s = p.read_text()

replacements = [
(
'''              <span class="calc-small-copy">Revenue from projected paid-lead jobs using Wranglin's measured lead-cost baseline and the close rate you enter. No extra nurture or reactivation revenue is automatically added.</span>''',
'''              <span class="calc-small-copy">Revenue from projected paid-lead jobs plus modeled follow-up and reactivation recoveries. Recovery matures conservatively from 5% of initially unclosed leads by 90 days, to 8% by 6 months and 10% by 12 months.</span>'''
),
(
'''            <div class="calc-metric"><b id="calc-immediate-jobs">0</b><span>Projected paid-lead jobs</span></div>
            <div class="calc-metric"><b id="calc-recovered-jobs">0</b><span>Extra jobs assumed</span></div>''',
'''            <div class="calc-metric"><b id="calc-immediate-jobs">0</b><span>Jobs from initial close rate</span></div>
            <div class="calc-metric"><b id="calc-recovered-jobs">0</b><span>Follow-up / reactivation jobs</span></div>'''
),
(
'''            <div class="calc-metric"><b id="calc-eventual-rate">0%</b><span>Modeled lead-to-job conversion</span></div>''',
'''            <div class="calc-metric"><b id="calc-eventual-rate">0%</b><span>Modeled total conversion</span></div>'''
),
(
'''              <h5>Revenue from modeled paid-lead jobs</h5>
              <div class="recovery-value" id="calc-immediate-revenue">$0</div>
              <p>This is the base-case revenue generated from the modeled lead volume, close rate, and average job size.</p>''',
'''              <h5>Revenue from customers who close initially</h5>
              <div class="recovery-value" id="calc-immediate-revenue">$0</div>
              <p>Revenue produced directly from the lead volume, your entered close rate, and your average job size before any later recovery is added.</p>'''
),
(
'''              <h5>Additional follow-up + reactivation upside</h5>
              <div class="recovery-value" id="calc-recovered-revenue">+$0</div>
              <p>Not included in the base-case forecast. Any later jobs recovered through nurture, reactivation, repeat need, or referrals are treated as upside rather than promised revenue.</p>''',
'''              <h5>Additional follow-up + reactivation upside</h5>
              <div class="recovery-value" id="calc-recovered-revenue">+$0</div>
              <p>Modeled from the leads that do not close initially: 5% recovered by 90 days, 8% cumulatively by 6 months, and 10% cumulatively by 12 months. This is a planning assumption, not guaranteed revenue.</p>'''
),
(
'''        Projection model, not a guarantee. The proof summary above reflects 2,000+ tracked leads and $25,000+ in documented ad spend across Ignite's broader campaign history. Forecast math is intentionally calibrated to the Wranglin Wranglers case: $1,463.54 ad spend produced 44 tracked website leads at $33.26 per lead, with 9 closed/completed jobs and approximately $6,000 collected over 29.27 days. The model uses that real $33.26 CPL to estimate lead volume, then applies the lead-to-job close rate entered above to estimate jobs. No additional follow-up, reactivation, repeat, referral, or database revenue is automatically added. Profit uses the margin entered above, and net impact subtracts both advertising spend and the initial Scale implementation investment. Actual results vary by market, service mix, pricing, lead quality, sales ability, seasonality, response speed, budget, and execution.''',
'''        Projection model, not a guarantee. The proof summary above reflects 2,000+ tracked leads and $25,000+ in documented ad spend across Ignite's broader campaign history. Forecast math is calibrated to the Wranglin Wranglers case for lead cost: $1,463.54 ad spend produced 44 tracked website leads at $33.26 per lead, with 9 closed/completed jobs and approximately $6,000 collected over 29.27 days. The model uses that real $33.26 CPL to estimate lead volume, then applies the lead-to-job close rate entered above. Follow-up and reactivation are modeled separately as a planning assumption on initially unclosed leads: 5% cumulative recovery by 90 days, 8% by 6 months, and 10% by 12 months. Those recovery percentages are not presented as observed Wranglin results or guaranteed performance. Profit uses the margin entered above, and net impact subtracts both advertising spend and the initial Scale implementation investment. Actual results vary by market, service mix, pricing, lead quality, sales ability, seasonality, response speed, budget, and execution.'''
)
]

for old, new in replacements:
    if old not in s:
        raise SystemExit('Expected markup not found:\n' + old[:180])
    s = s.replace(old, new, 1)

old_func = '''  function simulate(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){
    // Wranglin anchors lead cost. The prospect's entered close rate controls conversion.
    // No nurture, reactivation, repeat, or referral lift is automatically added.
    var modeledClose = enteredCloseRate;
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
'''

new_func = '''  function recoveryRateForDays(days){
    // Cumulative recovery assumption for leads that did not close initially.
    // 5% by 90 days, 8% by 6 months, 10% by 12 months.
    if(days <= 0) return 0;
    if(days <= 90) return .05 * (days / 90);
    if(days <= 180) return .05 + (.03 * ((days - 90) / 90));
    if(days <= 365) return .08 + (.02 * ((days - 180) / 185));
    return .10;
  }

  function project(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){
    var modeledClose = enteredCloseRate;
    var adSpend = dailyBudget * days;
    var leads = adSpend / BASE_CPL;
    var immediateJobs = leads * modeledClose;
    var unclosedLeads = Math.max(0, leads - immediateJobs);
    var recoveryRate = recoveryRateForDays(days);
    var recoveredJobs = unclosedLeads * recoveryRate;
    var jobs = immediateJobs + recoveredJobs;
    var immediateRevenue = immediateJobs * avgTicket;
    var recoveredRevenue = recoveredJobs * avgTicket;
    var revenue = immediateRevenue + recoveredRevenue;
    var grossProfit = revenue * profitMargin;
    var net = grossProfit - adSpend - SCALE_FEE;
    var cac = jobs > 0 ? adSpend / jobs : 0;
    var totalConversion = leads > 0 ? jobs / leads : 0;

    return {
      days:days,
      leads:leads,
      jobs:jobs,
      immediateJobs:immediateJobs,
      recoveredJobs:recoveredJobs,
      unclosedLeads:unclosedLeads,
      recoveryRate:recoveryRate,
      revenue:revenue,
      immediateRevenue:immediateRevenue,
      recoveredRevenue:recoveredRevenue,
      grossProfit:grossProfit,
      adSpend:adSpend,
      net:net,
      cac:cac,
      eventualRate:totalConversion,
      enteredRate:enteredCloseRate,
      baselineCpl:BASE_CPL,
      baselineClose:BASE_CLOSE,
      baselineTicket:BASE_TICKET,
      baselineRoas:BASE_ROAS,
      baselineDays:WRANGLIN_DAYS
    };
  }

  function simulate(days, avgTicket, enteredCloseRate, profitMargin, dailyBudget){
    var result = project(days,avgTicket,enteredCloseRate,profitMargin,dailyBudget);
    var breakEvenDay = null;
    for(var day=1; day<=365; day++){
      if(project(day,avgTicket,enteredCloseRate,profitMargin,dailyBudget).net >= 0){
        breakEvenDay = day;
        break;
      }
    }
    result.breakEvenDay = breakEvenDay;
    return result;
  }
'''

if old_func not in s:
    raise SystemExit('Old simulate function not found')
s = s.replace(old_func, new_func, 1)

old_render = '''    setText('calc-immediate-jobs',number(r90.immediateJobs));
    setText('calc-recovered-jobs','0');
    setText('calc-total-jobs',number(r90.jobs));
    setText('calc-adspend90',money(r90.adSpend));
    setText('calc-grossprofit90',money(r90.grossProfit));
    setText('calc-cac90',money(r90.cac));
    setText('calc-eventual-rate',pct(r90.eventualRate));
    setText('calc-immediate-revenue',money(r90.immediateRevenue));
    setText('calc-recovered-revenue','$0');'''

new_render = '''    setText('calc-immediate-jobs',number(r90.immediateJobs));
    setText('calc-recovered-jobs','+'+number(r90.recoveredJobs));
    setText('calc-total-jobs',number(r90.jobs));
    setText('calc-adspend90',money(r90.adSpend));
    setText('calc-grossprofit90',money(r90.grossProfit));
    setText('calc-cac90',money(r90.cac));
    setText('calc-eventual-rate',pct(r90.eventualRate));
    setText('calc-immediate-revenue',money(r90.immediateRevenue));
    setText('calc-recovered-revenue','+'+money(r90.recoveredRevenue));'''

if old_render not in s:
    raise SystemExit('Old render metrics block not found')
s = s.replace(old_render, new_render, 1)

old_card = '''          '<div class="projection-row"><span>Projected jobs</span><b>'+number(c.data.jobs)+'</b></div>' +
          '<div class="projection-row"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +
          '<div class="projection-row"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +'''
new_card = '''          '<div class="projection-row"><span>Projected jobs</span><b>'+number(c.data.jobs)+'</b></div>' +
          '<div class="projection-row"><span>Follow-up / reactivation</span><b>+'+money(c.data.recoveredRevenue)+'</b></div>' +
          '<div class="projection-row"><span>Gross profit</span><b>'+money(c.data.grossProfit)+'</b></div>' +
          '<div class="projection-row"><span>Ad spend</span><b>'+money(c.data.adSpend)+'</b></div>' +'''
if old_card not in s:
    raise SystemExit('Projection card block not found')
s = s.replace(old_card, new_card, 1)

# Add a small note to the longer-term heading so the maturity logic is visible in the UI.
old_heading = '''          <div class="calc-section-title"><h4>Longer-term system economics</h4><span>Assumes the same budget and performance continue</span></div>'''
new_heading = '''          <div class="calc-section-title"><h4>Longer-term system economics</h4><span>Same budget + performance, with recovery maturing from 5% to 8% to 10%</span></div>'''
if old_heading not in s:
    raise SystemExit('Longer-term heading not found')
s = s.replace(old_heading, new_heading, 1)

p.write_text(s)
print('updated index.html', len(s), len(s.splitlines()))
