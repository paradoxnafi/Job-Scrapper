import pandas as pd
import json


def read_jsonl(file_path):
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]
    return pd.DataFrame(data)


file1 = '../data/cleaned/LinkedIn_jobs_29-08-2024.jsonl'
file2 = '../data/cleaned/UNJobs_jobs_29-08-2024.jsonl'
file3 = '../data/cleaned/Vagaservisu_jobs_29-08-2024.jsonl'

df1 = read_jsonl(file1)
df2 = read_jsonl(file2)
df3 = read_jsonl(file3)

# Get unique columns from each DataFrame
columns_set = set(df1.columns) | set(df2.columns) | set(df3.columns)
unique_columns = sorted(columns_set)

# Create a DataFrame for the output
output_df = pd.DataFrame(index=unique_columns, columns=['Linkedin', 'UN Jobs', 'Vagaservisu'])

# Fill the DataFrame with 'yes' or 'no'
for column in unique_columns:
    output_df.at[column, 'Linkedin'] = 'yes' if column in df1.columns else 'no'
    output_df.at[column, 'UN Jobs'] = 'yes' if column in df2.columns else 'no'
    output_df.at[column, 'Vagaservisu'] = 'yes' if column in df3.columns else 'no'

# Export to Excel
output_df.to_excel('../data/cleaned/columns.xlsx', sheet_name='Columns')

print("Excel file 'job_posting_columns.xlsx' has been created.")
