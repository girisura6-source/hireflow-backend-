from flask import Flask, request, jsonify

app = Flask(__name__)

jobs = []

@app.route("/")
def home():
    return "API Running"

@app.route("/add-job", methods=["POST"])
def add_job():
    data = request.get_json()
    jobs.append(data)
    return {"message": "Job added"}

@app.route("/get-jobs", methods=["GET"])
def get_jobs():
    return jsonify(jobs)