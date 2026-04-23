from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "HireFlow API Running"

@app.route("/add-job", methods=["POST"])
def add_job():
    data = request.get_json()
    return jsonify({"message": "Job added successfully"})

@app.route("/get-jobs", methods=["GET"])
def get_jobs():
    return jsonify([])

@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    data = request.get_json()
    return jsonify({"result": "Resume looks good!"})

if __name__ == "__main__":
    app.run()