# Source Code Folder
This is a collection of database code used for the new search methods.

 SearchAPI: Takes fetch calls from searcher.js and queries the database.
 
 searcher.js: Constructs webpage that allows the user to search and display data from the database. 
 
 Database Conversion Files:

 Prerequisites:
 Python 3.6 or higher
 No other external libraries are required, only uses Python standard library

 Repository Structure:

├── txtconverter.py         # Cleans and normalizes raw .txt database dump

├── final_converter.py      # Imports cleaned CSV into SQLite database

├── clean_database.csv      # (generated) Tab‑delimited CSV of cleaned records

├── reptile_database_2024_08.txt  # (provided) Raw database file

├── reptile_bibliography_2024_08.txt  # (provided) Raw bibliography file

├── reptile_bibliography_2024_08_cleaned.csv # (generated) Cleaned bibliography csv

└── reptile_database.db     # (generated) SQLite database file

Scripts:

txtconverter.py

Purpose:
Reads a raw text dump containing reptile data.
Normalizes all line endings to Unix-style (\n).
Removes extraneous Unicode control characters (retaining only newlines and tabs).
Strips leading/trailing whitespace from each line.
Writes the cleaned output in UTF‑8 encoding.

Usage:
python3 txtconverter.py <input_raw.txt> <cleaned_output.txt>
<input_raw.txt>: Path to the original raw database file.
<cleaned_output.txt>: Desired path for the cleaned text output.

Example:
python3 txtconverter.py raw_reptiles.txt cleaned_reptiles.txt

final_converter.py

Purpose:
Defines helper functions to parse species, synonyms, distribution, and diagnosis data.
Creates four tables in SQLite:
species
synonyms
distribution
bibliography

Imports a cleaned, tab‑delimited CSV (clean_database.csv) into the species table.
Imports bibliography entries from reptile_bibliography_2024_08_cleaned.csv into a bibliography table.
Links synonyms and distribution records to their parent species by foreign keys.
Outputs a final reptile_database.db file.

Usage:
python3 final_converter.py

Ensure that the following files are present in the working directory:
clean_database.csv
reptile_bibliography_2024_08_cleaned.csv

After running, reptile_database.db will contain the processed data in normalized tables.

Notes
The functions parse_synonyms and parse_distribution are placeholders; customize them as needed to match your data format.
Adjust file paths or hard‑coded names inside final_converter.py if you wish to use different filenames.

Contributing
Feel free to open issues or submit pull requests to:
Improve parsing logic for synonyms, distribution, or diagnosis.
Enhance error handling and logging.
