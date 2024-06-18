import unittest
import pandas as pd
from run import (
    load_data, 
    filter_plans, 
    resolve_rate_areas, 
    calculate_second_lowest_rate, 
    update_slcsp_with_rates,
    FILES_PATH
)

class TestSLCSP(unittest.TestCase):

    def setUp(self):
        # Load the test data
        self.slcsp_df, self.plans_df, self.zips_df = load_data(
            FILES_PATH + 'slcsp_test.csv',
            FILES_PATH + 'plans_test.csv',
            FILES_PATH + 'zips_test.csv'
        )

        # Apply the workflow
        silver_plans = filter_plans(self.plans_df, metal_level='Silver')
        resolved_zips = resolve_rate_areas(self.zips_df)
        zip_to_silver_plans = pd.merge(resolved_zips, silver_plans, on=['state', 'rate_area'])
        second_lowest_rates = calculate_second_lowest_rate(zip_to_silver_plans)
        second_lowest_rates.columns = ['zipcode', 'rate']
        final_slcsp = update_slcsp_with_rates(self.slcsp_df, second_lowest_rates)
        self.final_slcsp = final_slcsp

    def test_scenario_multiple_rates(self):
        zipcode = "78902"
        expected_rate = "189.00"  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        print(self.final_slcsp)
        self.assertEqual(actual_rate, expected_rate)

    def test_scenario_multiple_counties_single_rate_area(self):
        zipcode = "23456"
        expected_rate = "205.00"  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        self.assertEqual(actual_rate, expected_rate)

    def test_scenario_multiple_counties_multiple_rate_areas(self):
        zipcode = "34567"
        expected_rate = ""  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        self.assertEqual(actual_rate, expected_rate)

    def test_scenario_single_rate(self):
        zipcode = "545678"
        expected_rate = ""  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        self.assertEqual(actual_rate, expected_rate)

    def test_scenario_multiple_non_unique_rates(self):
        zipcode = "45678"
        expected_rate = "250.00"  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        self.assertEqual(actual_rate, expected_rate)

    def test_scenario_no_matching_rate(self):
        zipcode = "67890"
        expected_rate = ""  
        actual_rate = self.final_slcsp[self.final_slcsp['zipcode'] == zipcode]['rate'].iloc[0]
        self.assertEqual(actual_rate, expected_rate)

if __name__ == '__main__':
    unittest.main()
