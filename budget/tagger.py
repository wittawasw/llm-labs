import pandas as pd
import numpy as np
from collections import defaultdict
from unidecode import unidecode

df = pd.read_csv("data/thailand_budget_2025.csv", encoding="utf-8-sig", low_memory=False)
df.columns = [c.strip().lower().replace("?", "").replace(" ", "_") for c in df.columns]
df.fillna("", inplace=True)

df["_item_norm"] = df["item_description"].apply(lambda x: unidecode(str(x).strip().lower()))
df["_plan_norm"] = df["budget_plan"].apply(lambda x: unidecode(str(x).strip().lower()))
df["_output_norm"] = df["project_output"] if "project_output" in df else ""
if isinstance(df["_output_norm"], pd.Series):
    df["_output_norm"] = df["_output_norm"].apply(lambda x: unidecode(str(x).strip().lower()))
else:
    df["_output_norm"] = ""

tag_rules = {
    "aggregate_cross_ministry_heavy": {
        "weight": 8.0,
        "func": lambda g: g["ministry"].nunique() > 5 and g["amount"].sum() > 1e7
    },
    "duplicated_across_units_under_500k": {
        "weight": 7.5,
        "func": lambda g: g["budgetary_unit"].nunique() >= 10 and g["amount"].max() < 5e5
    },
    "repeated_same_output_no_specifics": {
        "weight": 7.0,
        "func": lambda g: g.shape[0] >= 10 and all("ค่า" in v for v in g["item_description"])
    },
    "mass_small_fragments": {
        "weight": 6.5,
        "func": lambda g: g.shape[0] >= 30 and g["amount"].max() < 2e5
    },
    "multi_ministry_same_item_same_year": {
        "weight": 6.0,
        "func": lambda g: g["ministry"].nunique() >= 4 and g["fiscal_year"].nunique() == 1
    },
    "no_output_high_amount": {
        "weight": 5.5,
        "func": lambda g: "" in g["project_output"].values and g["amount"].max() > 5e6 if "project_output" in g else False
    },
    "budget_clustered_one_org": {
        "weight": 5.0,
        "func": lambda g: g.shape[0] > 30 and g["budgetary_unit"].nunique() == 1
    },
    "common_vague_item_mass": {
        "weight": 4.8,
        "func": lambda g: any(v in g["_item_norm"].values[0] for v in ["ค่าใช้จ่าย", "ดำเนินงาน"])
    },
    "nested_category_bloat": {
        "weight": 4.5,
        "func": lambda g: any(len(str(v).split(" ")) >= 5 for v in g["category_lv3"])
    },
    "same_item_duplicate_output": {
        "weight": 4.2,
        "func": lambda g: g["_output_norm"].nunique() > 1
    },
    "low_amount_frequent": {
        "weight": 4.0,
        "func": lambda g: g.shape[0] >= 5 and g["amount"].max() < 5e5
    },
    "duplicate_project_diff_year": {
        "weight": 3.8,
        "func": lambda g: g["fiscal_year"].nunique() > 1
    },
    "frequent_loose_label": {
        "weight": 3.5,
        "func": lambda g: any(v in g["category_lv2"].values[0] for v in ["ทั่วไป", "อื่นๆ", "เบ็ดเตล็ด"])
    },
    "multi_plan_same_output": {
        "weight": 3.2,
        "func": lambda g: g["_plan_norm"].nunique() > 1
    },
    "empty_output_with_category": {
        "weight": 3.0,
        "func": lambda g: "project_output" in g and g["project_output"].eq("").any() and g["category_lv1"].nunique() > 1
    },
    "short_item_name": {
        "weight": 2.5,
        "func": lambda g: len(g["_item_norm"].values[0]) < 10
    },
    "low_info_density": {
        "weight": 2.3,
        "func": lambda g: (g.iloc[0] == "").sum() > 10
    },
    "plan_used_across_units": {
        "weight": 2.0,
        "func": lambda g: g["budgetary_unit"].nunique() > 10
    },
    "redundant_crossfunc_flag": {
        "weight": 1.8,
        "func": lambda g: "cross_func" in g and g["cross_func"].all() and g["ministry"].nunique() == 1
    },
    "same_fiscal_redundancy": {
        "weight": 1.5,
        "func": lambda g: g["fiscal_year"].nunique() == 1
    },
    "very_low_budget_noise": {
        "weight": 1.2,
        "func": lambda g: g["amount"].max() < 1e5
    },
    "possible_copy_paste_labeling": {
        "weight": 1.0,
        "func": lambda g: g["category_lv1"].nunique() == 1 and g["category_lv2"].nunique() == 1 and g["category_lv3"].nunique() == 1
    }
}

tagged_rows = []
for key, group in df.groupby(["_item_norm", "_plan_norm", "_output_norm"]):
    tags = []
    for tag, rule in tag_rules.items():
        if rule["func"](group):
            tags.append((tag, rule["weight"]))
    for _, row in group.iterrows():
        row_tags = [tag for tag, _ in tags]
        row_score = sum(w for _, w in tags)
        tagged_rows.append({**row.to_dict(), "tags": ",".join(row_tags), "score": row_score})

tagged_df = pd.DataFrame(tagged_rows)
tagged_df.drop(columns=["_item_norm", "_plan_norm", "_output_norm"], errors="ignore").to_csv("data/thailand_budget_2025_tagged.csv", index=False, encoding="utf-8-sig")
