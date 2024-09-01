import pandas as pd
import json


def read_jsonl(file_path):
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    return pd.DataFrame(data)


file1 = '../data/cleaned/LinkedIn_jobs_29-08-2024.jsonl'
file2 = '../data/cleaned/unjobs_jobs_27-08-2024.jsonl'
file3 = '../data/cleaned/vagaservisu_jobs_27-08-2024.jsonl'

# Read the JSONL files
df1 = read_jsonl(file1)
df2 = read_jsonl(file2)
df3 = read_jsonl(file3)

# Add a title row for each DataFrame
df1.columns = pd.MultiIndex.from_product([['LinkedIn'], df1.columns])
df2.columns = pd.MultiIndex.from_product([['UN Jobs'], df2.columns])
df3.columns = pd.MultiIndex.from_product([['Vagaservisu'], df3.columns])

# Combine the DataFrames side by side
combined_df = pd.concat([df1, df2, df3], axis=1)

# Export to Excel
output_file = '../data/cleaned/reports/job_data.xlsx'
combined_df.to_excel(output_file)

print(f"Data has been exported to {output_file}")
