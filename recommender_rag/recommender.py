from llama_cpp import Llama
from retriever import retrieve_supplements
import sqlite3
from intake import fetch_intake

# llm = Llama(model_path="./models/codellama-7b.Q8_0.gguf", n_ctx=512)
llm = Llama(model_path="./models/Med-Qwen2-7B.Q8_0.gguf", n_ctx=512)

def get_supplement_costs(supplements):
    """Fetch price and stock quantity for recommended supplements."""
    conn = sqlite3.connect("./db/recommender_rag.db")
    cursor = conn.cursor()

    cost_data = []
    for supp in supplements:
        cursor.execute("SELECT price, stock_quantity FROM medications WHERE commercial_name = ?", (supp[0],))
        result = cursor.fetchone()
        if result:
            price, stock_quantity = result
            cost_data.append((supp[0], price, stock_quantity))

    conn.close()
    return cost_data

def recommend_supplements():
    intake_data = fetch_intake()
    intake_text = "\n".join([f"{name}, {dosage}, {frequency}, Purpose: {purpose}" for name, dosage, frequency, purpose, _ in intake_data])

    retrieved_supplements = retrieve_supplements(intake_text)

    if not retrieved_supplements:
        retrieved_text = "No relevant supplements found in the database."
        cost_summary = "Cost estimation is not available."
    else:
        retrieved_text = "\n".join([f"{supp[1]}: {supp[2]} THB, lasts for {supp[3]} days." for supp in retrieved_supplements])

        total_cost = sum(supp[2] for supp in retrieved_supplements)
        cost_summary = f"Estimated total cost: {total_cost} THB\n{retrieved_text}"

    prompt = (
        "Based on the following supplement intake history, recommend additional supplements "
        "that could be beneficial, ensuring there are no conflicts or overdoses. "
        "Provide reasoning for each recommendation. Also, calculate the estimated cost and duration "
        "for the suggested supplements given their standard packaging and dosage recommendations.\n\n"
        f"Current intake:\n{intake_text}\n\n"
        f"Relevant Supplements:\n{retrieved_text}\n\n"
        f"Cost Estimation:\n{cost_summary}\n\n"
        "Recommendations:"
    )

    response = llm(
        prompt,
        max_tokens=3000,
        temperature=0.3,
        stop=[]
    )

    return response["choices"][0]["text"].strip()
