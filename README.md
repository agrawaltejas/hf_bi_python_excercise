# Recipe Processing Project

## Project Overview

This project is designed to process recipe data from a JSON file, extract information about chili recipes, and save the results. The project includes functions to download a file from a given URL, format the downloaded JSON data, convert time durations to minutes, and process recipes to create CSV files with relevant information.

## Project Structure
```bash
recipe_processing/
│
├── main.py # Main script containing project functions
|
├── unit_tests.py # Unit tests for the project functions
|
├── input/ # Input JSON file
│ ├── bi_recipes.json # Input JSON file
|
│── recipes-etl # Output files for results
│ └── Results.csv # Output file for results    
| └── Results.csv # Output file for results           
|
├── test_data/ # test data files (if any)
│
├── requirements.txt # List of project dependencies
|
├── recipe_processing.log # Logs will be saved in this log file as well.
│
└── README.md # Project documentation
```

## Technologies Used

- **Python**: The main programming language used for the project.
- **Pandas**: Used for data manipulation and analysis, especially for working with DataFrames.
- **Requests**: Used for making HTTP requests to download the recipe data.

## How to Run

1. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run unit tests:

    ```bash
    python -m unittest unit_tests.py
    ```

3. Run the main function:

    ```bash
    python recipe_processing.py
    ```

## Functionality

### `download_recipes_file(url, destination)`

Downloads a file from a given URL and saves it to the specified destination.

### `fix_json_format_in_place(file_path)`

Formats downloaded JSON data for correct parsing.

### `convert_time_to_minutes(row)`

Converts PT standard times to minutes.

### `process_recipes(input_file, chilies_file, results_file)`

Processes recipes from a JSON file, extracts information about chili recipes, and saves the results.
