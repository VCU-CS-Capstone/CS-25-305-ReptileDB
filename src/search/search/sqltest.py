from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Function to query the database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('dummyreptile.db')
    conn.row_factory = sqlite3.Row  # Changes to dictionary for JSON output
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    return result[0] if result else None if one else result

# By common name (like "Green Iguana")
@app.route('/showcase/common_name/<common_name>', methods=['GET'])
def get_reptile_by_common_name(common_name):
    print(f"Searching for common name: {common_name}")
    reptile = query_db('SELECT * FROM taxonomy WHERE LOWER(common_names) LIKE LOWER(?)', ['%' + common_name + '%'])
    if reptile:
        print(type(reptile))
        print(f"Found reptiles: {reptile}")
        return jsonify([dict(reptile) for r in reptile]), 200
    else:
        print("No reptiles found")
        return jsonify({"error": "Reptile not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0")