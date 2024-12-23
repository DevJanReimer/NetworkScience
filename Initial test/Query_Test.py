from comtradeapicall import previewFinalData
import pandas as pd

# Define parameters for the query
params = {
    "typeCode": "C",  # Commodity data
    "freqCode": "M",  # Monthly frequency
    "clCode": "HS",  # Harmonized System classification
    "period": "202205",  # May 2022
    "reporterCode": "36",  # Australia
    "cmdCode": "91",  # HS code for goods starting with 91
    "flowCode": "M",  # Imports
    "partnerCode": None,  # No specific partner
    "partner2Code": None,  # No secondary partner
    "customsCode": None,  # No customs procedure filter
    "motCode": None,  # No mode of transport filter
    "maxRecords": 500,  # Limit to 500 records
    "format_output": "JSON",  # Output in JSON format
    "aggregateBy": None,  # No aggregation
    "breakdownMode": "classic",  # Classic breakdown mode
    "countOnly": None,  # Fetch full data
    "includeDesc": True  # Include descriptions
}

# Fetch data using previewFinalData
print("Fetching data for Australia's imports (May 2022, HS Code 91)...")
try:
    data = previewFinalData(**params)
    # Convert the response to a DataFrame
    df = pd.DataFrame(data)

    # Display the first few rows of the DataFrame
    if not df.empty:
        print("Data Retrieved:")
        print(df.head())
    else:
        print("No data retrieved for the specified parameters.")
except Exception as e:
    print(f"Error fetching data: {e}")