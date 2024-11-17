from comtradeapicall import getFinalData
import pandas as pd


# https://unstats.un.org/unsd/methodology/m49/overview/ M49 Country codes and names
# https://comtradedeveloper.un.org/api-details#api=comtrade-v1&operation=get-get API Website of comtrade


# Subscription key for the UN Comtrade API
subscription_key = '8fc360c30644453f810f1efb9b888dc2'

# Define the selection criteria
SelectionCriteria = {
    "cmdCode": '85',  # Electronics (HS Chapter 85)
    "flowCode": 'M',  # Imports and Exports
    "includeDesc": "true"  # Include descriptions
}


def fetch_data(reporter_code, partner_code, year):
    """
    Fetch trade data for a specific reporter, partner, and year.
    """
    try:
        # Fetch data using the Comtrade API
        data = getFinalData(
            subscription_key=subscription_key,
            typeCode='C',
            freqCode='M',
            clCode='HS',
            period=year,
            reporterCode=reporter_code,
            cmdCode=SelectionCriteria['cmdCode'],
            flowCode=SelectionCriteria['flowCode'],
            partnerCode=partner_code,
            partner2Code=None,
            customsCode=None,
            motCode=None
        )

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Check if the DataFrame is empty
        if df.empty:
            print(f"No data returned for Reporter={reporter_code}, Partner={partner_code}, Year={year}.")
        return df
    except Exception as e:
        print(f"Error fetching data for Reporter={reporter_code}, Partner={partner_code}, Year={year}: {e}")
        return pd.DataFrame()

def get_country_name(m49_code):
    """
    Function to get the country name corresponding to an M49 number.
    :param m49_code: The M49 code to search for.
    :return: The corresponding country name or None if not found.
    """
    try:
        # Search for the M49 code in the DataFrame
        country_name = m49_df.loc[m49_df['M49 Code'] == m49_code, 'Country or Area'].values
        if len(country_name) > 0:
            return country_name[0]
        else:
            return None
    except KeyError:
        print("The columns 'M49 Code' or 'Country or Area' do not exist in the CSV.")
        return None

def get_country_code(country_name):
    """
    Function to get the M49 code corresponding to a country name.
    :param country_name: The name of the country to search for.
    :return: The corresponding M49 code or None if not found.
    """
    try:
        # Search for the country name in the DataFrame
        country_code = m49_df.loc[m49_df['Country or Area'] == country_name, 'M49 Code'].values
        if len(country_code) > 0:
            return country_code[0]
        else:
            return None
    except KeyError:
        print("The columns 'Country or Area' or 'M49 Code' do not exist in the CSV.")
        return None

# Fetch data for a range of years
# Path to the CSV file
file_path = 'UNSD — M49.csv'

# Load the CSV file
m49_df = pd.read_csv(file_path, delimiter=";")

# Extract the M49 codes as a list of integers
m49_numbers = m49_df['M49 Code'].tolist()
years = range(2015, 2016)  # Adjust range as needed
all_data = pd.DataFrame()

# Counter for iterations
iteration_count = 0
"""
for year in years:
    print(f"Fetching data for Year: {year}...")
    for reporter_code in m49_numbers:
        reporter_name = get_country_name(reporter_code)
        for partner_code in m49_numbers:
            partner_name = get_country_name(partner_code)
            iteration_count += 1
            print(f"[Iteration {iteration_count}] Fetching data: Year={year}, Reporter={reporter_name}, Partner={partner_name}...")
            data = fetch_data(reporter_code, partner_code, year)
            if not data.empty:
                all_data = pd.concat([all_data, data], ignore_index=True)
"""

for partner_code in m49_numbers:
            partner_name = get_country_name(partner_code)
            reporter_code = 158
            iteration_count += 1
            print(f"[Iteration {iteration_count}] Fetching data: Year={2023}, Reporter=Taiwan, Partner={partner_name}...")
            data = fetch_data(reporter_code, partner_code, 2023)
            if not data.empty:
                all_data = pd.concat([all_data, data], ignore_index=True)
            if iteration_count == 200:
                break  # End the loop


# Save the combined dataset to a CSV file
if not all_data.empty:
    all_data.to_csv("un_comtrade_free_api_data.csv", index=False)
    print("Data saved to 'un_comtrade_free_api_data.csv'.")
else:
    print("No data retrieved.")
