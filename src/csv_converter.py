import csv
import sqlite3

# Define the database table schema with column names based on your CSV fields.
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reptiles (
            id INTEGER PRIMARY KEY,
            higher_taxa TEXT,
            genus TEXT,
            species TEXT,
            authority TEXT,
            year TEXT,
            valid TEXT,
            synonyms TEXT,
            common_names TEXT,
            distribution TEXT,
            notes TEXT,
            diagnosis TEXT,
            type_specimens TEXT,
            media_links TEXT,
            identifier TEXT,
            etymology TEXT,
            catalog_number TEXT,
            external_id TEXT,
            reproduction TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def import_csv_to_sqlite(csv_file, db_file):
    # Create (or open) the SQLite database.
    conn, cursor = create_database(db_file)
    
    # Open the CSV file (assuming it is tab-delimited) and insert each row.
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            # Check that the row has the expected number of columns (18 columns)
            if len(row) < 18:
                continue  # skip incomplete rows
            
            # Map CSV columns to database fields:
            # Column 0: higher_taxa
            # Column 1: genus
            # Column 2: species
            # Column 3: authority
            # Column 4: year
            # Column 5: valid (Y/N)
            # Column 6: synonyms (or related literature)
            # Column 7: common_names
            # Column 8: distribution (and type locality info)
            # Column 9: taxonomic notes
            # Column 10: diagnosis
            # Column 11: type_specimens info
            # Column 12: media links (photo, info, map)
            # Column 13: identifier (a long numeric code)
            # Column 14: etymology
            # Column 15: catalog_number
            # Column 16: external_id
            # Column 17: reproduction
            
            cursor.execute('''
                INSERT INTO reptiles (
                    higher_taxa, genus, species, authority, year, valid, synonyms, common_names,
                    distribution, notes, diagnosis, type_specimens, media_links, identifier, etymology,
                    catalog_number, external_id, reproduction
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row[:18])
    
    conn.commit()
    conn.close()
    print("Data import completed successfully.")

if __name__ == "__main__":
    # Adjust the file paths as necessary.
    csv_file = "clean_database.csv"          # your input CSV file
    db_file = "reptile_database.db"  # the output SQLite database
    import_csv_to_sqlite(csv_file, db_file)
