from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)



def query_db(query, args=(), one=False):
    conn = sqlite3.connect('reptile_database.db')
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    conn.close()
    if not result:
        return None
    if one:
        return result[0]
    return result

@app.route('/api/search', methods=['GET'])
def search():
    
    query = request.args.get('query', '')
    print(query.lower())
    #results = [item for item in data if query.lower() in item.lower()]
    reptile = query_db('SELECT * FROM species WHERE LOWER(common_names) LIKE LOWER(?)', ['%' + query.lower() + '%'])
    if reptile:
        print(type(reptile))
        print(f"Found reptiles: {reptile}")
        reptiles_data = [dict(r) for r in reptile]
        print("Returned reptiles:", reptiles_data)
        return jsonify([dict(r) for r in reptile]), 200
    else:
        print("No reptiles found")
        return jsonify({"error": "Reptile not found"}), 404
    #print(f"Found: {results}")
    #return jsonify(results=results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)