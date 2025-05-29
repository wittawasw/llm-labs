import pandas as pd
import math

df = pd.read_csv("data/thailand_budget_2025_utf8_bom.csv", encoding="utf-8-sig", low_memory=False)

df.columns = [col.strip().lower().replace("?", "").replace(" ", "_") for col in df.columns]

columns_to_check = [
    "ministry", "budgetary_unit", "budget_plan",
    "category_lv1", "category_lv2", "category_lv3",
    "item_description", "amount", "fiscal_year"
]

def is_unclean(value):
    return (
        (isinstance(value, float) and (math.isnan(value) or math.isinf(value))) or
        (isinstance(value, str) and value.strip() == "")
    )

unclean_mask = df[columns_to_check].applymap(is_unclean).any(axis=1)
unclean_df = df[unclean_mask]

unclean_df.to_csv("unclean_rows.csv", index=False, encoding="utf-8-sig")
print(f"Found {len(unclean_df)} unclean rows. Written to unclean_rows.csv")
