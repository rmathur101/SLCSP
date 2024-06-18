import pandas as pd # type: ignore
pd.set_option('display.max_rows', None)
import sys

# TODO: remove hardcoded path and put it in a config file
FILES_PATH = '/Users/rmathur101 1/SLCSP/SLCSP/files/'

# Load the CSV files to check their content and structure
slcsp_df = pd.read_csv(FILES_PATH + 'slcsp.csv')
plans_df = pd.read_csv(FILES_PATH + 'plans.csv')
zips_df = pd.read_csv(FILES_PATH + 'zips.csv')

# Display the first few rows of each dataframe and their column names
# print(slcsp_df.head(), slcsp_df.columns, plans_df.head(), plans_df.columns, zips_df.head(), zips_df.columns)

# Filter out only Silver plans from the plans.csv
silver_plans = plans_df[plans_df['metal_level'] == 'Silver']

# To resolve rate area ambiguities for ZIP codes, we first need to count how many unique rate areas exist per ZIP code
zip_rate_area_counts = zips_df.groupby('zipcode')['rate_area'].nunique()

print(zip_rate_area_counts)

sys.exit()

# Filter out ZIP codes that map to exactly one rate area
single_rate_area_zips = zip_rate_area_counts[zip_rate_area_counts == 1].index

# Extract those ZIP code entries from zips.csv
resolved_zips = zips_df[zips_df['zipcode'].isin(single_rate_area_zips)]

# Join resolved ZIP codes with silver plans to get applicable silver plans per ZIP code
zip_to_silver_plans = pd.merge(resolved_zips, silver_plans, on=['state', 'rate_area'])

# Find the second lowest silver plan rate per rate area for these resolved ZIP codes
def second_lowest_rate(group):
    rates = group['rate'].unique()
    if len(rates) > 1:
        return sorted(rates)[1]  # Return the second lowest unique rate
    else:
        return None  # If there's no second lowest rate, return None

# Calculate the second lowest rates
second_lowest_rates = zip_to_silver_plans.groupby('zipcode').apply(second_lowest_rate).reset_index()
second_lowest_rates.columns = ['zipcode', 'rate']

# Now let's preview the results
second_lowest_rates.head(), zip_to_silver_plans.head()

