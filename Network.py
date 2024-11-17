from comtradeapicall import getFinalData
import pandas as pd


# https://unstats.un.org/unsd/methodology/m49/overview/ M49 Country codes and names
# https://comtradedeveloper.un.org/api-details#api=comtrade-v1&operation=get-get API Website of comtrade


# Subscription key for the UN Comtrade API
subscription_key = '8fc360c30644453f810f1efb9b888dc2'

# Define the selection criteria
SelectionCriteria = {
    "cmdCode": '8541',       # HS Code for semiconductors
    "flowCode": 'M',      # Imports and Exports
    "includeDesc": "true"   # Include descriptions
}

def fetch_data (country, year):
    """Fetch trade data for a specific year."""
    try:
        data = getFinalData(
            subscription_key=subscription_key,
            typeCode='C',                # Commodity data
            freqCode='M',                # Monthly frequency
            clCode='HS',                 # Harmonized System classification
            period=year,                 # Year to fetch
            reporterCode=country,
            cmdCode=SelectionCriteria['cmdCode'],
            flowCode=SelectionCriteria['flowCode'],
            partnerCode=None,
            partner2Code=None,
            customsCode=None,
            motCode=None
        )
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching data for year {year}: {e}")
        return pd.DataFrame()

# Fetch data for a range of years
# Path to the CSV file
file_path = 'UNSD — M49.csv'

# Load the CSV file
m49_df = pd.read_csv(file_path, delimiter=";")

# Extract the M49 codes as a list of integers
m49_numbers = m49_df['M49 Code'].tolist()
years = range(2015,2016)  # Adjust range as needed
all_data = pd.DataFrame()



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



for year in years:
    print(f"Fetching data for {year}...")
    for country_nr in m49_numbers:
        country_name = get_country_name(country_nr)
        print(f"Fetching data for {country_name}...")
        data = fetch_data(int(country_nr), str(year))
    if not data.empty:
        all_data = pd.concat([all_data, data], ignore_index=True)

# Save the combined dataset to a CSV file
if not all_data.empty:
    all_data.to_csv("un_comtrade_free_api_data.csv", index=False)
    print("Data saved to 'un_comtrade_free_api_data.csv'.")
else:
    print("No data retrieved.")