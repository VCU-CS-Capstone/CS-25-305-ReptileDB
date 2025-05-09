from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Valid fields for dynamic search
VALID_FIELDS = [
    'species_id', 'higher_taxa', 'genus', 'species', 'authority', 'year',
    'valid', 'synonyms', 'common_names', 'distribution_raw', 'notes',
    'diagnosis_raw', 'type_specimens', 'media_links', 'identifier',
    'etymology', 'reproduction'
]

#get species ID
@app.route("/")
def index():
    species_id = request.args.get("species_id")
    return render_template("index.html", species_id=species_id)

def get_species_by_id(species_id):
    conn = sqlite3.connect('reptile_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT genus, species FROM species WHERE species_id = ?", (species_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        genus, species = row
        return f"{genus} {species}"
    return None


def query_db(query, args=(), one=False):
    conn = sqlite3.connect('reptile_database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    if not result:
        return None
    return result[0] if one else result

@app.route('/api/search_dynamic', methods=['GET'])
def search_dynamic():
    query = request.args.get('query', '')
    field = request.args.get('field', 'common_names')
    if field not in VALID_FIELDS:
        return jsonify({"error": "Invalid search field"}), 400

    sql = f'SELECT * FROM species WHERE LOWER({field}) LIKE LOWER(?)'
    reptile = query_db(sql, ['%' + query.lower() + '%'])
    if reptile:
        return jsonify([dict(r) for r in reptile]), 200
    else:
        return jsonify({"error": "No results found"}), 404

@app.route('/api/advanced_search', methods=['GET'])
def advanced_search():
    filters = {
        'common_names': request.args.get('common_name', '').strip().lower(),
        'higher_taxa': request.args.get('higher_taxa', '').strip().lower(),
        'genus': request.args.get('genus', '').strip().lower(),
        'species': request.args.get('species', '').strip().lower(),
        'authority': request.args.get('authority', '').strip().lower(),
        'year': request.args.get('year', '').strip().lower(),
        'valid': request.args.get('valid', '').strip().lower(),
        'synonyms': request.args.get('synonyms', '').strip().lower(),
        'distribution_raw': request.args.get('distribution', '').strip().lower(),
        'notes': request.args.get('notes', '').strip().lower(),
        'diagnosis_raw': request.args.get('diagnosis', '').strip().lower(),
        'type_specimens': request.args.get('type_specimens', '').strip().lower(),
        'media_links': request.args.get('media_links', '').strip().lower(),
        'etymology': request.args.get('etymology', '').strip().lower(),
        'reproduction': request.args.get('reproduction', '').strip().lower()
    }

    query = 'SELECT * FROM species WHERE 1=1'
    args = []

    for field, value in filters.items():
        if value:
            query += f' AND LOWER({field}) LIKE ?'
            args.append(f'%{value}%')

    result = query_db(query, args)
    if result:
        return jsonify([dict(r) for r in result]), 200
    else:
        return jsonify({"error": "No matching species found"}), 404

@app.route("/api/reptile/<int:species_id>") #Fetch all Species Data
def get_reptile(species_id):
    conn = sqlite3.connect("reptile_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            common_names,
            higher_taxa,
            genus,
            species,
            authority,
            year,
            valid,
            synonyms,
            distribution_raw,
            type_specimens,
            media_links,
            notes,
            etymology,
            reproduction
        FROM species
        WHERE species_id = ?
    """, (species_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        columns = [
            "common_names",
            "higher_taxa",
            "genus",
            "species",
            "authority",
            "year",
            "valid",
            "synonyms",
            "distribution_raw",
            "type_specimens",
            "media_links",
            "notes",
            "etymology",
            "reproduction"
        ]
        return jsonify(dict(zip(columns, row)))
    else:
        return jsonify({"error": "Species not found"}), 404


def get_inaturalist_images(scientific_name, limit=3):           #Sticking with first three "observation" images for now. Note that this is still citizen science, so accuracy not guaranteed
    url = "https://api.inaturalist.org/v1/observations"
    params = {
        "q": scientific_name,
        "per_page": limit,
        "photos": "true"
    }
    res = requests.get(url, params=params)
    images = []
    if res.ok:
        data = res.json()
        for obs in data.get("results", []):
            for photo in obs.get("photos", [])[:limit]:
                images.append(photo["url"].replace("square", "medium"))
                if len(images) >= limit:
                    break
    return images

def get_taxon_id(scientific_name): #Gets the taxon_id to query iNaturalist API
    url = "https://api.inaturalist.org/v1/taxa"
    params = {"q": scientific_name}
    res = requests.get(url, params=params)
    if res.ok:
        data = res.json()
        if data["results"]:
            return data["results"][0]["id"]
    return None

@app.route("/images")
def images():               #Pulls observation images/coordinates from iNaturalist
    species_id = request.args.get("species_id")
    if not species_id:
        return jsonify({"error": "species_id is required"}), 400

    species_name = get_species_by_id(species_id)
    if not species_name:
        return jsonify({"error": "Species not found"}), 404

    url = "https://api.inaturalist.org/v1/observations"
    params = {
        "q": species_name,
        "per_page": 5,
        "photos": "true"
    }

    res = requests.get(url, params=params)
    image_urls = []
    if res.ok:
        data = res.json()
        for obs in data.get("results", []):
            for photo in obs.get("photos", []):
                image_urls.append(photo["url"].replace("square", "medium"))
                if len(image_urls) >= 3:
                    break
            if len(image_urls) >= 3:
                break

    taxon_id = get_taxon_id(species_name)


    return jsonify({
        "species_name": species_name,
        "images": image_urls,
        "taxon_id": taxon_id
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)