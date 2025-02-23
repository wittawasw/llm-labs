from intake import fetch_intake
from recommender import recommend_supplements

def main():
    print("===================\n")
    print("📋 Current Supplement Intake:")
    intake = fetch_intake()
    for item in intake:
        print(f"- {item[0]} ({item[1]}), {item[2]}, Purpose: {item[3]}")

    print("\n===================\n")
    print("🤖 Generating Supplement Recommendations...")
    try:
        suggestions = recommend_supplements()
        print("\n✅ LLM Recommendations:")
        print(suggestions)
    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
