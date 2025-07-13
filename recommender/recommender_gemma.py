import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from intake import fetch_intake
import sqlite3
import json

model_id = "google/medgemma-4b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, device_map="auto", torch_dtype="auto")

llm = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device_map="auto",
    model_kwargs={"torch_dtype": "auto"}
)

def get_intake_text():
    intake_data = fetch_intake()
    return "\n".join([
        f"{name}, {dosage}, {frequency}, Purpose: {purpose}"
        for name, dosage, frequency, purpose, _ in intake_data
    ])

def generate_recommendation_prompt(intake_text):
    return f"""
    Here is the intake history:
    {intake_text}

    You are a structured data assistant for experienced dietician.

    Based on the following supplement intake history, recommend 3–5 additional supplements that are beneficial, avoiding overdose or conflict.

    Return exactly one JSON object. No explanations, no extra output.
    DO NOT put it inside markdown ```json ```. NEVER.

    Only return output in this format:
    {{
    "recommendations": [
        {{"name": "Supplement Name", "reason": "Reason for recommending it"}},
        ...
    ]
    }}
    """.strip()

def extract_recommendations(json_text):
    # decoder = json.JSONDecoder()
    # json_text = json_text.lstrip()
    # Even with prompt to not return Markdown, Gemma still ALWAYS return Markdown.
    cleaned = json_text.replace("```json", "").replace("```", "").strip()
    cleaned = cleaned.replace("``", "")

    try:
        # obj, _ = decoder.raw_decode(json_text)
        # json_text = clean_json_text(json_text)
        return json.loads(cleaned)["recommendations"]
        # return obj["recommendations"]
    except Exception as e:
        print("Failed JSON:\n", json_text)
        print("\n\nEnd Failed JSON:\n")

        raise ValueError("Failed to parse LLM JSON output")

def fetch_prices(names):
    conn = sqlite3.connect("./db/health.db")
    cursor = conn.cursor()
    like_clauses = [f"LOWER(commercial_name) LIKE ?" for _ in names]
    query = f"SELECT commercial_name, price FROM medications WHERE {' OR '.join(like_clauses)}"
    cursor.execute(query, [f"%{name.lower()}%" for name in names])
    results = cursor.fetchall()
    conn.close()

    price_map = {name: None for name in names}
    for commercial_name, price in results:
        for name in names:
            if name.lower() in commercial_name.lower():
                price_map[name] = price
                break
    return price_map

def build_price_lines(recommendations, price_map):
    lines = []
    for item in recommendations:
        name = item["name"]
        reason = item["reason"]
        price = price_map.get(name)
        price_str = f"${price:.2f}" if price is not None else "Price not found"
        lines.append(f"{name}: {price_str} — {reason}")
    return lines

def generate_cost_prompt(price_lines):
    return (
        "Here are supplement recommendations and their prices:\n\n" +
        "\n".join(price_lines) +
        "\n\nEstimate total monthly cost and suggest optimal usage duration. Keep it practical and short."
    )

def run_llm(prompt, max_new_tokens=512):
    raw = llm(
        prompt,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.9
    )[0]["generated_text"]

    gen = raw[len(prompt):]

    end_idx = gen.find("```\n")
    if end_idx != -1:
        gen = gen[:end_idx + 2]

    return gen.strip()

import time

def recommend_supplements():
    start = time.perf_counter()
    try:
        intake_text = get_intake_text()
        prompt_1 = generate_recommendation_prompt(intake_text)
        json_text = run_llm(prompt_1)
        recommendations = extract_recommendations(json_text)

        names = [r["name"] for r in recommendations]
        price_map = fetch_prices(names)
        price_lines = build_price_lines(recommendations, price_map)

        prompt_2 = generate_cost_prompt(price_lines)
        cost_summary = run_llm(prompt_2)

        result = "\n".join(price_lines) + "\n\nCost Estimate:\n" + cost_summary
    except Exception as e:
        result = f"Error: {e}"

    duration = time.perf_counter() - start

    minutes = int(duration // 60)
    seconds = int(duration % 60)

    timelapse = f"\n\nTime elapsed: {minutes}:{str(seconds).zfill(2)}"
    return result + timelapse
