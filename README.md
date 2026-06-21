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
