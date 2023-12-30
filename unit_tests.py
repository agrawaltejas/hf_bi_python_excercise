import requests
import unittest
import os
import pandas as pd
from main import download_recipes_file, fix_json_format_in_place, convert_time_to_minutes, process_recipes

class TestRecipeProcessing(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources or configurations
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_download_recipes_file(self):
        url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
        input_file = "test_data/test_recipes.json"

        # Ensure the file is downloaded successfully
        download_recipes_file(url, input_file)
        self.assertTrue(os.path.exists(input_file))

        # Clean up the downloaded file
        os.remove(input_file)

    def test_download_recipes_file_failure(self):
        # Test failure scenario when an invalid URL is provided
        invalid_url = "https://invalid-url.com"
        invalid_input_file = "test_data/invalid_recipes.json"

        # Ensure the function raises an exception
        with self.assertRaises(requests.exceptions.RequestException):
            download_recipes_file(invalid_url, invalid_input_file)

    def test_fix_json_format_in_place(self):
        # Create a temporary test file
        test_file = "test_data/test_json_file.json"
        with open(test_file, "w") as f:
            f.write('{"name": "Test Recipe 1"},{"name": "Test Recipe 2"}')

        # Fix the JSON format in place
        fix_json_format_in_place(test_file)

        # Read the corrected file
        with open(test_file, "r") as f:
            corrected_json = f.read()

        # Ensure the corrected JSON format
        self.assertEqual(corrected_json, '[{"name": "Test Recipe 1"},{"name": "Test Recipe 2"}]')

        # Clean up the test file
        os.remove(test_file)

    def test_convert_time_to_minutes(self):
        # Test conversion of time to minutes
        test_row = "PT1H30M"
        result = convert_time_to_minutes(test_row)
        self.assertEqual(result, 90)

        # Test when 'H' is not present in the row
        test_row_without_hours = "PT45M"
        result_without_hours = convert_time_to_minutes(test_row_without_hours)
        self.assertEqual(result_without_hours, 45)

        # Test when 'M' is not present in the row
        test_row_without_minutes = "PT2H"
        result_without_minutes = convert_time_to_minutes(test_row_without_minutes)
        self.assertEqual(result_without_minutes, 120)

    def test_process_recipes(self):
        input_file = "test_data/test_recipes.json"
        chilies_file = "test_data/test_Chilies.csv"
        results_file = "test_data/test_Results.csv"

        # Create a sample DataFrame for testing
        sample_data = [{'name': 'Recipe 1', 'ingredients': 'chilies', 'prepTime': 'PT15M', 'cookTime': 'PT35M'}, {'name': 'Recipe 2', 'ingredients': 'tomatoes', 'prepTime': 'PT20M', 'cookTime': 'PT45M'}]
        sample_df = pd.DataFrame(sample_data)

        # Save the sample DataFrame to a test file
        sample_df.to_json(input_file)

        # Ensure the function runs without errors
        process_recipes(input_file, chilies_file, results_file)

        # Clean up the test files
        # os.remove(input_file)
        # os.remove(chilies_file)
        # os.remove(results_file)

if __name__ == '__main__':
    unittest.main()
