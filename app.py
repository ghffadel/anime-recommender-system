from flask import Flask, jsonify, request, render_template
import preprocessing, recommendation

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template("index.html")

@app.route("/recommendations", methods = ["POST"])
def get_recommendations ():
    global animes, vectors

    username = request.form["username"]

    recommendations = recommendation.get_recommendations(username, animes, vectors)

    return jsonify({ "recommendations": recommendations })


if __name__ == "__main__":
    animes = preprocessing.load_animes()
    vectors = preprocessing.get_vectors(animes)

    app.run(debug = True)