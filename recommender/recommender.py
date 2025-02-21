
from llama_cpp import Llama
from intake import fetch_intake

llm = Llama(model_path="./models/Med-LLaMA3-8B.Q8_0.gguf", n_ctx=512)

def recommend_supplements():
    intake_data = fetch_intake()
    intake_text = "\n".join([f"{name}, {dosage}, {frequency}, Purpose: {purpose}" for name, dosage, frequency, purpose, _ in intake_data])

    prompt = (
        "Based on the following supplement intake history, recommend additional supplements "
        "that could be beneficial, ensuring there are no conflicts or overdoses. "
        "Provide reasoning for each recommendation. Also, calculate the estimated cost and duration "
        "for the suggested supplements given their standard packaging and dosage recommendations.\n\n"
        f"Current intake:\n{intake_text}\n\n"
        "Recommendations:"
    )

    # max_tokens 300 and temperature 0.2 is not enough to generate output.
    # It always return empty response in Med-LLaMa3-8B
    response = llm(
        prompt,
        max_tokens=3000,
        temperature=0.3,
        stop=["\n\n"]
    )

    recommendation = response["choices"][0]["text"].strip()
    return recommendation
