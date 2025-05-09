import csv
import sys  # added to increase CSV field size limit
csv.field_size_limit(sys.maxsize)
import sqlite3
import re

# --------------------
# Helper Parsing Functions
# --------------------
def parse_synonyms(synonyms_text, genus, species):
    # TODO: implement synonym parsing per documentation
    return []

def parse_distribution(distribution_text):
    # TODO: implement distribution parsing per documentation
    return {'type_locality': None}

def parse_diagnosis(text):
    """
    Extracts physical traits from the diagnosis text using regex.
    """
    traits = {
        'color': None,
        'pattern': None,
        'head_color_distinct': None,
        'nape': None,
        'scale_type': None,
        'ventral_color': None,
        'ventral_pattern': None,
        'max_length_mm': None
    }
    # color
    m = re.search(r'\b(red|blue|green|brown|yellow|black|white|grey|gray|orange|purple)\b', text, re.IGNORECASE)
    if m:
        traits['color'] = m.group(1).lower()
    # pattern
    m = re.search(r'\b(striped|spotted|banded|mottled|reticulated)\b', text, re.IGNORECASE)
    if m:
        traits['pattern'] = m.group(1).lower()
    # head_color_distinct
    m = re.search(r'(head[^.,;]*)', text, re.IGNORECASE)
    if m:
        traits['head_color_distinct'] = m.group(1).strip()
    # nape
    m = re.search(r'(nape[^.,;]*)', text, re.IGNORECASE)
    if m:
        traits['nape'] = m.group(1).strip()
    # scale_type
    m = re.search(r'\b(keeled|smooth)\b', text, re.IGNORECASE)
    if m:
        traits['scale_type'] = m.group(1).lower()
    # ventral_color & ventral_pattern
    m = re.search(r'(ventral[^.,;]*)', text, re.IGNORECASE)
    if m:
        vc = m.group(1).strip()
        traits['ventral_color'] = vc
        m2 = re.search(r'ventral pattern[^.,;]*', vc, re.IGNORECASE)
        if m2:
            traits['ventral_pattern'] = m2.group(0).strip()
    # max_length_mm
    m = re.search(r'(\d+(?:\.\d+)?)(?:\s*)(cm|mm)\b', text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        unit = m.group(2).lower()
        if unit == 'cm':
            val *= 10
        traits['max_length_mm'] = int(val)
    return traits

# --------------------
# Database Setup
# --------------------
def create_tables(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS species")
    cursor.execute("DROP TABLE IF EXISTS synonyms")
    cursor.execute("DROP TABLE IF EXISTS distribution")
    cursor.execute("""
    CREATE TABLE species (
        species_id INTEGER PRIMARY KEY AUTOINCREMENT,
        higher_taxa TEXT,
        genus TEXT,
        species TEXT,
        authority TEXT,
        year TEXT,
        valid TEXT,
        synonyms TEXT,
        common_names TEXT,
        distribution_raw TEXT,
        notes TEXT,
        diagnosis_raw TEXT,
        type_specimens TEXT,
        media_links TEXT,
        identifier TEXT,
        etymology TEXT,
        catalog_number TEXT,
        external_id TEXT,
        reproduction TEXT,
        family TEXT,
        color TEXT,
        pattern TEXT,
        head_color_distinct TEXT,
        nape TEXT,
        scale_type TEXT,
        ventral_color TEXT,
        ventral_pattern TEXT,
        max_length_mm INTEGER,
        venomous TEXT
    )""")
    cursor.execute("""
    CREATE TABLE synonyms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_id INTEGER,
        accepted_species TEXT,
        synonym TEXT,
        author TEXT,
        year TEXT,
        notes TEXT,
        reference TEXT,
        FOREIGN KEY(species_id) REFERENCES species(species_id)
    )""")
    cursor.execute("""
    CREATE TABLE distribution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_id INTEGER,
        subspecies TEXT,
        country TEXT,
        subdivision TEXT,
        type_locality TEXT,
        coordinates TEXT,
        FOREIGN KEY(species_id) REFERENCES species(species_id)
    )""")
    conn.commit()
    return conn, cursor

# --------------------
# Utility: pop by regex
# --------------------
def pop_pattern(parts, pattern, flags=0):
    for i in range(len(parts)-1, -1, -1):
        if re.search(pattern, parts[i], flags):
            return parts.pop(i)
    return ""

# --------------------
# Import species
# --------------------
def import_csv_to_db(csv_file, db_file):
    conn, c = create_tables(db_file)
    with open(csv_file, encoding='utf-8') as f:
        for row in csv.reader(f, delimiter='\t'):
            parts = [p.strip() for p in row]
            # venom
            venom_flag = any(re.search(r'\bvenomou[sm]!?', p, re.IGNORECASE) for p in parts)
            parts = [p for p in parts if not re.match(r'(?i)^venemous!?', p)]
            # stray blank
            if len(parts)>7 and not parts[7]: del parts[7]
            # pop labeled fields
            distribution_raw = pop_pattern(parts, r'^Distribution:.*', re.IGNORECASE)
            diagnosis_raw   = pop_pattern(parts, r'^Diagnosis:.*', re.IGNORECASE)
            # common names
            common_names = ''
            for i,p in enumerate(parts):
                if p.startswith('E: '): common_names, parts[i] = p[3:].strip(), ''
            # reproduction
            reproduction = pop_pattern(parts, r'\b(?:oviparous|viviparous|ovoviviparous|ovovivparous)\b', re.IGNORECASE)
            # other
            external_id     = pop_pattern(parts, r'^\d{1,}/\d+')
            catalog_number  = pop_pattern(parts, r'^\d{5,7}$')
            etymology       = pop_pattern(parts, r'^(?:Named after|Apparently named)')
            media_links     = pop_pattern(parts, r'https?://')
            type_specimens  = pop_pattern(parts, r'^(?:Type|Types|Syntypes|Holotype|Lectotype|Paratype|Syntype)')
            identifier      = pop_pattern(parts, r'^\d{8,}$')
            # core
            parts = (parts + ['']*11)[:11]
            (ht, gen, sp, auth, yr, val, syns, cn, dist_f, notes, dfb) = parts
            if common_names: cn = common_names
            dist_f = distribution_raw or dist_f
            notes  = re.sub(r'(?i)^venemous!?\s*', '', notes).strip()
            diag_f = diagnosis_raw or dfb
            diag_f = re.sub(r'(?i)^venemous!?\s*', '', diag_f).strip()
            traits = parse_diagnosis(diag_f)
            # insert
            c.execute("""
            INSERT INTO species (
              higher_taxa, genus, species, authority, year, valid,
              synonyms, common_names, distribution_raw, notes,
              diagnosis_raw, type_specimens, media_links, identifier, etymology,
              catalog_number, external_id, reproduction,
              family, color, pattern, head_color_distinct, nape,
              scale_type, ventral_color, ventral_pattern, max_length_mm,
              venomous
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
              ht, gen, sp, auth, yr, val,
              syns, cn, dist_f, notes,
              diag_f, type_specimens, media_links, identifier, etymology,
              catalog_number, external_id, reproduction,
              '', traits['color'], traits['pattern'], traits['head_color_distinct'], traits['nape'],
              traits['scale_type'], traits['ventral_color'], traits['ventral_pattern'], traits['max_length_mm'],
              'yes' if venom_flag else 'no'
            ))
            sid = c.lastrowid
            # insert raw synonyms text if present
            if syns:
                c.execute("""
                    INSERT INTO synonyms (species_id, accepted_species, synonym)
                    VALUES (?,?,?)
                """, (sid, f"{gen} {sp}", syns))
            # insert distribution raw into distribution table
            dist = parse_distribution(dist_f)
            c.execute("""
                INSERT INTO distribution (
                    species_id, subspecies, country, subdivision, type_locality, coordinates
                ) VALUES (?,?,?,?,?,?)
            """, (sid, None, None, None, dist['type_locality'], None))
    conn.commit()
    conn.close()
    print("Conversion complete.")


# ----------------------------------------------------------------------------
# Import Bibliography Data (single info column)
# ----------------------------------------------------------------------------
def import_bibliography(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='	')
        for row in reader:
            if len(row) < 2:
                continue
            ref_id = row[0].strip()
            if not re.match(r'^\d+$', ref_id):
                continue
            # Join all remaining columns into one info field
            info = " | ".join([col.strip() for col in row[1:] if col.strip()])
            cursor.execute("""
                INSERT OR IGNORE INTO bibliography (
                    reference_id, info
                ) VALUES (?, ?)
            """, (ref_id, info))
    conn.commit()
    conn.close()


# --------------------
# Entry Point
# --------------------
if __name__ == "__main__":
    import_csv_to_db("clean_database.csv", "reptile_database.db")
    import_bibliography("reptile_bibliography_2024_08_cleaned.csv", "reptile_database.db")