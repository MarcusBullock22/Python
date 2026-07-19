import win32com.client
import pandas as pd
from datetime import datetime

# Load Excel file, you'll want to link the excel file in this folder
file_path = "your_file.xlsx" 
df = pd.read_excel(file_path)

# Ensure date columns are datetime
df["Updated Date"] = pd.to_datetime(df["Updated Date"], errors="coerce")

# Filter rows where Updated Date is older than a year
one_year_ago = datetime.now() - pd.DateOffset(years=1)
df_filtered = df[df["Updated Date"] <= one_year_ago]

# Group by email to concatenate multiple Data Sources
grouped = df_filtered.groupby("Email")["Data Source"].apply(lambda x: "\n".join(x)).reset_index()

# Initialize Outlook application
outlook = win32com.client.Dispatch("Outlook.Application")

# Prepare current timestamp
now_str = datetime.now().strftime("%Y-%m-%d")

# Ensure the 'EmailSent' column exists in the original DataFrame
if "EmailSent" not in df.columns:
    df["EmailSent"] = pd.NaT

# Send emails and update original DataFrame with sent date
for _, row in grouped.iterrows():
    email = row["Email"]
    data_sources = row["Data Source"]

    # Create new email
    mail = outlook.CreateItem(0)
    mail.To = email
    mail.Subject = "Your subject here"
    mail.Body = f"Hello,\n\nYour topic here:\n{data_sources}\n\nBest Regards,\nYour Team"
    
    # Send email
    mail.Send()

    # Update EmailSent column in original df (all matching email rows)
    df.loc[df["Email"] == email, "EmailSent"] = now_str

# Save updated Excel
df.to_excel(file_path, index=False)

print("Emails sent successfully and Excel updated.")

