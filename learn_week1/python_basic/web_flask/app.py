from flask import Flask, render_template, jsonify, request, redirect
from bson import ObjectId
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from my_database.my_db import get_database, get_tour_guid, get_tourist_spot


app = Flask(__name__)

@app.route('/')
def index():
    mydb = get_database()
    data = get_tourist_spot(mydb)
    return render_template('index.html', model = data)

@app.route("/detail/<id>", methods=["GET", "POST"])
def form(id):
    my_query = {"_id": ObjectId(id)}
    mydb = get_database()
    mycol = mydb["tourist_spot"]
    tour_data = get_tour_guid(mydb)
    data = mycol.find_one(my_query)
    print(data)
    if request.method == "POST":
        tour_guide_id = request.form.get("tour_guide_id")
        price = request.form.get("price")
        description = request.form.get("description")
        new_values = { "$set": { "guide_id": tour_guide_id, "price_tour": price, "description": description } }
        mycol.update_one(my_query, new_values)
        return redirect("/")  # Redirect to advoid POST form when refresh

    return render_template("detail.html", data=data, tour_data=tour_data)

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name1=name)

@app.route('/api/hello', methods=['GET'])
def hello_api():
    return jsonify({'message': 'Hello from Flask API'})

@app.route('/api/add', methods=['POST'])
def add():
    data = request.json
    result = data['a'] + data['b']
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(port=5050, debug=True) #port default: 5000