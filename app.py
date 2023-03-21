from flask import Flask, jsonify, request, render_template
from src import preprocessing, recommendation

app = Flask(__name__, static_url_path = "/static")

@app.route("/")
def index ():
    return render_template("index.html")

@app.route("/recommendations", methods = ["POST"])
def get_recommendations ():
    animes = preprocessing.load_animes()
    vectors = preprocessing.get_vectors(animes)

    username = request.form["username"]

    recommendations = recommendation.get_recommendations(username, animes, vectors)

    return jsonify({ "recommendations": recommendations })


if __name__ == "__main__":
    app.run(debug = True)