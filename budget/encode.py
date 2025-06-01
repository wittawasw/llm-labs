import codecs

def convert_to_utf8_bom(input_path, output_path):
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    with codecs.open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(content)

input_file = "data/thailand_budget_2025.csv"
output_file = "data/thailand_budget_2025_utf8_bom.csv"
convert_to_utf8_bom(input_file, output_file)
