# nykaa-customer-intelligence
### Customer Segmentation (RFM Analysis)

Using Recency, Frequency, and Monetary scoring, customers were segmented 
into 5 groups. The distribution is notably polarized: 60% of customers 
fall into either "Champions" (1,420) or "Lost" (1,530), with comparatively 
few in the "Needs Attention" middle segment (210).

**Key insight:** Customers tend to either become loyal repeat buyers or 
churn early — there's little gradual drift. This suggests retention 
strategy should prioritize the early customer lifecycle (first → second 
purchase) over broad re-engagement campaigns for long-lapsed users.

**Recommended action:** Prioritize win-back campaigns for the 800 
"At Risk (High Value)" customers — proven high-spenders showing signs 
of disengagement — over the larger but lower-value "Lost" segment.


### Cohort Retention Analysis

Customers were grouped by signup month and tracked for repeat purchases 
over time. Across nearly all cohorts, retention drops sharply from 100% 
(month 0) to ~15-25% by month 1, then remains stable in that band through 
month 15-20.

**Key insight:** Customer churn risk is concentrated almost entirely in 
the first month after signup — customers who make a second purchase tend 
to keep returning at a steady ~20% monthly rate long-term, rather than 
gradually drifting away. This means retention strategy ROI is highest 
when focused on the 0-to-1-month window (e.g., a second-purchase 
incentive or onboarding sequence), rather than long-term loyalty programs.

**Note:** The most recent cohorts (Oct-Nov 2025) show unusually high 
retention (68-85%) due to small sample size — these cohorts have very 
few customers, so individual repeat purchases swing the percentage 
heavily. Cohorts with fewer than ~30 customers were excluded from 
trend conclusions.

### A/B Test: Monsoon Sale Campaign Creative

Two creative versions of the same campaign were tested:
- **Version A (Bold design):** 1.92% CTR (115 clicks / 5,994 impressions)
- **Version B (Minimal design):** 3.57% CTR (122 clicks / 3,413 impressions)

A two-proportion z-test confirmed this difference is statistically 
significant (z = -4.93, p < 0.0001) — Version B's higher CTR is not 
due to random chance.

**Recommendation:** Scale Version B as the primary creative across 
similar campaigns. The minimal design approach outperformed the bold 
design by nearly 2x in click-through rate.


## Module 2: Ad Campaign & Marketing Analytics

Simulated a realistic ad funnel (impressions → clicks → purchases) across 
10 campaigns spanning 4 channels (Search, Influencer, Email, Banner), with 
ad-driven purchases linked directly to real transaction records for 
accurate revenue attribution.

### Key Findings

**1. Channel performance varies dramatically**
- Search and Influencer campaigns deliver the strongest ROAS (2.6x–4.4x)
- Every Banner campaign has ROAS below 1.0 — actively losing money
- Email sits near breakeven (~1.5x)

**2. A/B Test: Creative Design (Monsoon Sale Campaign)**
- Version B (Minimal design): 3.57% CTR
- Version A (Bold design): 1.92% CTR
- Confirmed statistically significant via two-proportion z-test 
  (p < 0.0001) — not due to chance

**3. Channel matters more than creative**
- Even the "winning" A/B variant (Version B) remained unprofitable 
  (ROAS 0.96) because it was still a Banner campaign — reinforcing 
  that channel selection is a bigger lever than ad creative

### Recommendation
Reallocate the ₹255,000 currently spent on underperforming Banner 
campaigns toward Search and Influencer channels, which show 2-4x 
better returns.

### Visuals
![CTR by Campaign](visuals/5_ctr_by_campaign.png)
![ROAS by Campaign](visuals/6_roas_by_campaign.png)
![Overall Funnel](visuals/7_overall_funnel.png)
![A/B Test Result](visuals/8_ab_test_result.png)
