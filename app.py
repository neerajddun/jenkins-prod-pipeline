from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)   # this auto-registers /metrics

@app.get("/")
def hello():
    return jsonify(
        message="✨ Welcome to Cloud with NeerajB. this is master config branch.✨",
        tip="Built with Flask, shipped by Jenkins, running in Docker.",
        UI="This is my new message"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)