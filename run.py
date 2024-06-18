import sys
import os
import datetime
import pandas as pd 

FILES_PATH = os.getenv('SLCSP_FILES_PATH')
OUTPUT_FINAL_SLCSP_FILE = False

def load_data(slcsp_path, plans_path, zips_path):
    # We coerce the 'zipcode' column to a string to avoid losing leading zeros when reading the CSV file.
    slcsp_df = pd.read_csv(slcsp_path, dtype={'zipcode': str})
    zips_df = pd.read_csv(zips_path, dtype={'zipcode': str})
    plans_df = pd.read_csv(plans_path)

    return slcsp_df, plans_df, zips_df

def filter_plans(plans_df, metal_level='Silver'):
    return plans_df[plans_df['metal_level'] == metal_level]

# To resolve rate area ambiguities for ZIP codes, we first need to count how many unique rate areas exist per ZIP code
def resolve_rate_areas(zips_df):
    # Count how many unique rate areas exist per ZIP code. The operation takes zips_df and creates a DataframeGroupBy object, then selects the 'rate_area' to create a SeriesGroupBy object, and finally calls nunique() to count the number of unique rate areas per ZIP code and returns a Series where the index is the ZIP code and the value is the number of unique rate areas.
    zip_rate_area_counts = zips_df.groupby('zipcode')['rate_area'].nunique()

    # Filter out ZIP codes that map to exactly one rate area. It returns an IndexObject with the ZIP codes that map to exactly one rate area.
    single_rate_area_zips = zip_rate_area_counts[zip_rate_area_counts == 1].index

    # Create a new DataFrame with the ZIP code entries that map to exactly one rate area. .isin returns a boolean Series that filters the rows of zips_df.
    return zips_df[zips_df['zipcode'].isin(single_rate_area_zips)]

def calculate_second_lowest_rate(zip_to_silver_plans):

    def second_lowest_rate(group):
        rates = group['rate'].unique()
        if len(rates) > 1:
            return sorted(rates)[1]
        else:
            return None

    return zip_to_silver_plans.groupby('zipcode').apply(second_lowest_rate).reset_index()

def update_slcsp_with_rates(slcsp_df, second_lowest_rates):
    final_slcsp = pd.merge(slcsp_df, second_lowest_rates, on='zipcode', how='left')
    final_slcsp['rate'] = final_slcsp['rate_y']
    final_slcsp.drop(columns=['rate_x', 'rate_y'], inplace=True)
    final_slcsp['rate'] = final_slcsp['rate'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else '')
    return final_slcsp

def save_output(final_slcsp, output_path):
    final_slcsp.to_csv(output_path, index=False)

def main():
    slcsp_df, plans_df, zips_df = load_data(FILES_PATH + 'slcsp.csv', FILES_PATH + 'plans.csv', FILES_PATH + 'zips.csv')
    resolved_zips = resolve_rate_areas(zips_df)
    silver_plans = filter_plans(plans_df, metal_level='Silver')
    zip_to_silver_plans = pd.merge(resolved_zips, silver_plans, on=['state', 'rate_area'])
    second_lowest_rates = calculate_second_lowest_rate(zip_to_silver_plans)
    second_lowest_rates.columns = ['zipcode', 'rate']
    final_slcsp = update_slcsp_with_rates(slcsp_df, second_lowest_rates)

    final_slcsp.to_csv(sys.stdout, index=False) 

    if (OUTPUT_FINAL_SLCSP_FILE):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = FILES_PATH + 'out/slscp_final_' + timestamp + '.csv'
        save_output(final_slcsp, output_path)

if __name__ == '__main__':
    main()
