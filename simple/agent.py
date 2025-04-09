from llama_cpp import Llama
import sqlite3
import re

# llm = Llama(model_path="./models/codellama-7b.Q8_0.gguf", n_ctx=512)
llm = Llama(model_path="./models/Meta-Llama-3.1-8B-Q8_0.gguf", n_ctx=512)


def generate_sql(natural_query: str) -> str:
    prompt = (
        "You are an expert SQL generator. "
        "Generate a SQL query for the following request. "
        "The database table is named 'receipts' with the following columns: "
        "receipt_id (INTEGER), customer_name (VARCHAR), price (FLOAT), tip (FLOAT). "
        "Only return a valid SQL query. DO NOT add explanations.\n\n"
        f"Request: {natural_query}\n"
        "SQL Query:\n"
    )

    response = llm(
        prompt,
        max_tokens=150,
        temperature=0.2,
        stop=["\n\n", ";"]  # Force stopping at query completion
    )

    raw_response = response["choices"][0]["text"].strip()

    print(f"\n🔍 **Raw LLM Response:**\n{raw_response}")

    match = re.search(r"SELECT .*", raw_response, re.DOTALL | re.IGNORECASE)
    if match:
        sql_query = match.group(0).strip()
    else:
        raise ValueError(f"❌ Invalid SQL response from LLM: {raw_response}")

    return sql_query

def execute_query(sql_query: str):
    print("\n++++++++++++++++++++++++\n")
    print("Executing SQL Query:\n", sql_query)
    print("++++++++++++++++++++++++\n")

    conn = sqlite3.connect("./db/example.db")
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
    except Exception as e:
        result = f"SQL Error: {e}"
    finally:
        conn.close()

    return result

def generate_answer(sql_result, user_query: str) -> str:
    result_str = str(sql_result)

    prompt = (
        "From the query result "
        "Use the value here to answer in human language: {result_str} "
        "Question: \"{user_query}\". "
        "Answer:"
    ).format(user_query=user_query, result_str=result_str)

    print("\n++++++++++++++++++++++++\n")
    print("Promt:\n", prompt)
    print("++++++++++++++++++++++++\n")

    response = llm(
        prompt,
        max_tokens=150,
        temperature=0.2,
        stop=["\n\n"]
    )
    answer = response["choices"][0]["text"].strip()
    return answer

def main():
    print("===================\n")
    user_query = "Can you give me the name of the client who got the most expensive receipt?"
    print("Natural Language Query:", user_query)

    try:
        sql_query = generate_sql(user_query)
        print("\n===================\n")
        print("✅ Generated SQL Query:\n", sql_query)

        print("\n===================\n")
        result = execute_query(sql_query)
        print("✅ Query Result:", result)

        answer = generate_answer(result, user_query)
        print("\n===================\n")
        print("✅ Final Answer:", answer)

    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
