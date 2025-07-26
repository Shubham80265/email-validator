import pandas as pd
from email_utils import check_email

def validate_emails(input_file, output_file):
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)

    if 'Email' not in df.columns:
        raise ValueError("Input file must have an 'Email' column")

    results = []
    for email in df['Email']:
        result = check_email(str(email))
        results.append(result)

    result_df = pd.DataFrame(results)
    result_df.to_excel(output_file, index=False)
    print(f"✅ Done! Saved to {output_file}")

if __name__ == "__main__":
    validate_emails("format.xlsx", "output_validated_emails.xlsx")