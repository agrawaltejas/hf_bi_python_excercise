import requests
import pandas as pd
import logging

# Configure logging to output to both console and file
logging.basicConfig(filename='recipe_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a console handler and set the level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and attach it to the console handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the root logger
logging.getLogger('').addHandler(console_handler)

def download_recipes_file(url, destination):
    """Download a file from a given URL and save it to the specified destination.

    Args:
        url (str): The URL of the file to be downloaded.
        destination (str): The path where the file will be saved.

    Returns:
        None
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(destination, 'wb') as file:
            file.write(response.content)

        logging.info(f"File downloaded successfully to {destination}")

        fix_json_format_in_place(destination)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        raise

def fix_json_format_in_place(file_path):
    """
    Formatting Downloaded JSON data for correct parsing.
    Args:
        file_path (str): The path of downloaded JSON.

    Returns:
        None
    """
    try:
        with open(file_path, 'r') as infile:
            lines = [line.strip() for line in infile]

        # Join lines into a well-formed JSON array
        json_array = '[' + ','.join(lines) + ']'

        # Write the corrected content back to the same file
        with open(file_path, 'w') as outfile:
            outfile.write(json_array)

        logging.info(f"JSON file formatted successfully: {file_path}")

    except Exception as e:
        logging.error(f"Error fixing JSON file format: {e}")
        raise

def convert_time_to_minutes(row):
    """
    Converting PT standard times to minutes.
    Args:
        row : Row of the dataframe where the function is applied.

    Returns:
        Total converted minutes.
    """
    try:
        hours = 0
        minutes = 0

        if 'H' in row:
            hours_index = row.index('H')
            hours = int(row[2:hours_index])

        if 'M' in row:
            minutes_index = row.index('M')
            if 'H' in row:
                minutes = int(row[hours_index+1:minutes_index])
            else:
                minutes = int(row[2:minutes_index])

        # Calculate total time in minutes
        total_minutes = hours * 60 + minutes
        return total_minutes

    except Exception as e:
        logging.error(f"Error extracting minutes from duration: {e}")
        return None  

def process_recipes(input_file, chilies_file, results_file):
    """Process recipes from a JSON file, extract information about chili recipes, and save the results.

    Args:
        input_file (str): The path to the input JSON file.
        chilies_file (str): The path to save the Chilies.csv file.
        results_file (str): The path to save the Results.csv file.

    Returns:
        None
    """
    try:
        recipes_df = pd.read_json(input_file)
        logging.info(f"Read {len(recipes_df)} recipes from {input_file}")

        # Extract recipes with "Chilies" in ingredients
        target = ['chilies', 'chiles', 'chili', 'chilli', 'chile']
        chilies_df = recipes_df[recipes_df['ingredients'].apply(lambda x: any(element in x.lower() for element in target))]

        # print(chilies_df[['prepTime','cookTime']])
        chilies_df['prepTime'] = chilies_df['prepTime'].apply(convert_time_to_minutes)
        chilies_df['cookTime'] = chilies_df['cookTime'].apply(convert_time_to_minutes)
        chilies_df['totalTime'] = chilies_df['prepTime'] + chilies_df['cookTime']

        # Add difficulty field
        chilies_df['difficulty'] = chilies_df['totalTime'].apply(lambda totalTime: "Hard" if totalTime > 60 else ("Medium" if 30 < totalTime <= 60 else ("Easy" if totalTime <= 30 else "Unknown")))
        # print(chilies_df[['prepTime','cookTime','totalTime','difficulty']])

        chilies_df = chilies_df.drop_duplicates()
        chilies_df.to_csv(chilies_file, sep='|', index=False)
        logging.info(f"Chilies data saved to {chilies_file}")

        # Calculate average total_time by difficulty
        results_df = chilies_df.groupby('difficulty')['totalTime'].mean().reset_index()
        results_df.columns = ['Difficulty', 'AverageTotalTime']

        # Save Results.csv
        results_df.to_csv(results_file, sep='|', index=False, header=None)
        logging.info(f"Results data saved to {results_file}")

    except Exception as e:
        logging.error(f"Error processing recipes: {e}")
        raise

if __name__ == "__main__":
    try:
        url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
        input_file = "input/bi_recipes.json"
        chilies_file = "recipes-etl/Chilies.csv"
        results_file = "recipes-etl/Results.csv"

        download_recipes_file(url, input_file)
        process_recipes(input_file, chilies_file, results_file)

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")