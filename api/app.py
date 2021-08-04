from flask import Flask, request
from recommender import Recommender

app = Flask(__name__)


@app.route('/recommend', methods=["POST"])
def recommend_item():
    recommender = Recommender()
    item = request.get_json()
    return recommender.recommend(item["productid"])


if __name__ == '__main__':
    app.run()
