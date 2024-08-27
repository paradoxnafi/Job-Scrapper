import sys
import json


def clean_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                # Load the line as JSON
                data = json.loads(line)

                # Remove \n from each key-value pair
                cleaned_data = {k: v.replace('\n', '') if isinstance(v, str) else v for k, v in data.items()}

                # Write cleaned data back as JSON
                json.dump(cleaned_data, outfile, ensure_ascii=False)
                outfile.write('\n')
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_jsonl.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    clean_jsonl(input_file, output_file)
