from flask import Flask, jsonify, request, render_template
import preprocessing, recommendation

# Number of closest neighbors in KNN
K = 3

app = Flask(__name__)

@app.route("/")
def index ():
    return render_template("index.html")

@app.route("/recommendations", methods = ["POST"])
def get_recommendations ():
    global animes, animes_data, profiles

    username = request.form["username"]

    recommendations = recommendation.get_recommendations(username, K, animes_data, profiles)

    return jsonify({ "recommendations": recommendations })


if __name__ == "__main__":
    animes = preprocessing.load_animes()
    animes_data = preprocessing.get_animes_data(animes)
    profiles = preprocessing.load_profiles()

    app.run(debug = True)