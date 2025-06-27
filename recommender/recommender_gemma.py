from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from intake import fetch_intake

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

    response = llm(prompt, max_length=3000, temperature=0.7, top_p=0.9)

    recommendation = response[0]["generated_text"].replace(prompt, "").strip()
    return recommendation
