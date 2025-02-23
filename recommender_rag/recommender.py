from llama_cpp import Llama
from retriever import retrieve_supplements
from intake import fetch_intake

llm = Llama(model_path="./models/codellama-7b.Q8_0.gguf", n_ctx=512)

def recommend_supplements():
    intake_data = fetch_intake()
    intake_text = "\n".join([f"{name}, {dosage}, {frequency}, Purpose: {purpose}" for name, dosage, frequency, purpose, _ in intake_data])

    retrieved_supplements = retrieve_supplements(intake_text)
    retrieved_text = "\n".join([f"{supp[0]}: {supp[1]} Benefits: {supp[2]}" for supp in retrieved_supplements])

    prompt = (
        "Based on the following supplement intake history, recommend additional supplements "
        "that could be beneficial, ensuring there are no conflicts or overdoses. "
        "Provide reasoning for each recommendation. Also, calculate the estimated cost and duration "
        "for the suggested supplements given their standard packaging and dosage recommendations.\n\n"
        f"Current intake:\n{intake_text}\n\n"
        f"Relevant Supplements:\n{retrieved_text}\n\n"
        "Recommendations:"
    )

    response = llm(
        prompt,
        max_tokens=3000,
        temperature=0.3,
        stop=[]
    )

    return response["choices"][0]["text"].strip()
