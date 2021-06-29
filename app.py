from flask import Flask
from flask import request, Response
import json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.data:
        data = None
        try:
            data = json.loads(request.data.decode("utf-8"))
        except json.JSONDecoder:
            print("bad json")

        if data:
            task = data["task"]
            bot_settings = json.loads(data["bot_settings"])

    return Response(status=200)


if __name__ == "__main__":
    app.run()
