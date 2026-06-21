from statsmodels.stats.proportion import proportions_ztest
import numpy as np

# Your actual numbers from the query
clicks = np.array([115, 122])          # Version A clicks, Version B clicks
impressions = np.array([5994, 3413])   # Version A impressions, Version B impressions

# Run the two-proportion z-test
z_stat, p_value = proportions_ztest(clicks, impressions)

ctr_a = clicks[0] / impressions[0] * 100
ctr_b = clicks[1] / impressions[1] * 100

print(f"Version A CTR: {ctr_a:.2f}%")
print(f"Version B CTR: {ctr_b:.2f}%")
print(f"Difference: {ctr_b - ctr_a:.2f} percentage points")
print(f"\nZ-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("\n✅ RESULT: Statistically significant (p < 0.05)")
    print("Version B's higher CTR is unlikely to be due to random chance.")
else:
    print("\n❌ RESULT: NOT statistically significant (p >= 0.05)")
    print("The CTR difference could plausibly be due to random chance — need more data before declaring a winner.")