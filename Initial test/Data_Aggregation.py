
import pandas as pd
from comtradeapicall import previewFinalData

# https://unstats.un.org/unsd/methodology/m49/overview/ M49 Country codes and names
# https://comtradedeveloper.un.org/api-details#api=comtrade-v1&operation=get-get API Website of comtrade


# Subscription key for the UN Comtrade API
subscription_key = '8fc360c30644453f810f1efb9b888dc2'


def fetch_data(reporter_code, partner_code, year, month):
    """
    Fetch trade data for a specific reporter, partner, and year.
    """
    year_month = str(year) + month

    try:
        print(f"Calling API: Reporter={reporter_code}, Partner={partner_code}, Year={year}")

        # Fetch data using the Comtrade API
        data = previewFinalData(
            typeCode="C",  # Commodity data
            freqCode="M",  # Monthly frequency
            clCode="HS",  # Harmonized System classification
            period=f"{year_month}",  # Specify the period (e.g., May 2022)
            reporterCode=str(reporter_code),  # Reporter country code
            cmdCode="8542",  # HS Code 91 (replace as needed)
            flowCode="M",  # Imports
            partnerCode=str(partner_code) if partner_code else None,  # Partner country
            partner2Code=None,  # No secondary partner
            customsCode=None,  # No customs filter
            motCode=None,  # No mode of transport filter
            maxRecords=500,  # Limit to 500 records
            format_output="JSON",  # JSON output
            aggregateBy=None,  # No aggregation
            breakdownMode="classic",  # Classic breakdown
            countOnly=None,  # Retrieve full data
            includeDesc=True,  # Include descriptions
        )

        # Convert the response to a DataFrame
        df = pd.DataFrame(data)

        # Check if the DataFrame is empty
        if df.empty:
            print(f"No data returned for Reporter={reporter_code}, Partner={partner_code}, Year={year}.")
        else:
            print(f"Data fetched successfully for Reporter={reporter_code}, Partner={partner_code}, Year={year}.")
        return df
    except Exception as e:
        print(f"Error fetching data for Reporter={reporter_code}, Partner={partner_code}, Year={year}: {e}")
        return pd.DataFrame()



months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
reporter_code = 756
year = 2018

# Path to your CSV file
file_path = "UNSD — M49.csv"  # Replace with the actual path to your file
output_file = "data.csv"
# Load the CSV file
m49_df = pd.read_csv(file_path, delimiter=';')

# Extract the column with M49 codes (replace 'M49 Code' with the actual column name if different)
if 'M49 Code' in m49_df.columns:
    m49_codes = m49_df['M49 Code'].tolist()
    print(f"Extracted M49 codes: {m49_codes}")
else:
    print("The 'M49 Code' column was not found in the file.")

for partner_code in m49_codes:
    for month in months:
        data = fetch_data(reporter_code, partner_code, year, month)
        # Convert the DataFrame to a string
        data_string = data.to_csv(index=False, header=False)  # Convert without index and header

        # Append the string to the CSV file
        with open(output_file, "a") as file:
            file.write(data_string)  # Append the string to the file





