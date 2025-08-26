from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Valid fields for dynamic search
VALID_FIELDS = [
    'species_id', 'higher_taxa', 'genus', 'species', 'authority', 'year',
    'valid', 'synonyms', 'common_names', 'distribution_raw', 'notes',
    'diagnosis_raw', 'type_specimens', 'media_links', 'identifier',
    'etymology', 'catalog_number', 'external_id', 'reproduction'
]

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
        'identifier': request.args.get('identifier', '').strip().lower(),
        'etymology': request.args.get('etymology', '').strip().lower(),
        'catalog_number': request.args.get('catalog_number', '').strip().lower(),
        'external_id': request.args.get('external_id', '').strip().lower(),
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)