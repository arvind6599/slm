from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Replace with a secure key for your application


# Routes
@app.route("/", methods=["GET", "POST"])
def general_details():
    if request.method == "POST":
        session["general_details"] = {
            "Name": request.form.get("name"),
            "Age": request.form.get("age"),
            "Occupation": request.form.get("occupation"),
        }
        return redirect(url_for("question_1"))
    return render_template("general_details.html")

@app.route("/question_1", methods=["GET", "POST"])
def question_1():
    if request.method == "POST":
        session["question_1"] = request.form.get("q1")
        return redirect(url_for("question_2"))
    return render_template("question.html", question="What is your favorite type of activity?",
                           choices=["Sports", "Reading", "Traveling", "Other"], q_num="1")

@app.route("/question_2", methods=["GET", "POST"])
def question_2():
    if request.method == "POST":
        session["question_2"] = request.form.get("q2")
        return redirect(url_for("question_3"))
    return render_template("question.html", question="What is your favorite time of day?",
                           choices=["Morning", "Afternoon", "Evening", "Night"], q_num="2")

@app.route("/question_3", methods=["GET", "POST"])
def question_3():
    if request.method == "POST":
        session["question_3"] = request.form.get("q3")
        return redirect(url_for("summary"))
    return render_template("question.html", question="What is your preferred mode of learning?",
                           choices=["Visual", "Auditory", "Kinesthetic", "Reading/Writing"], q_num="3")

@app.route("/summary")
def summary():
    general_details = session.get("general_details", {})
    question_1 = session.get("question_1", "Not answered")
    question_2 = session.get("question_2", "Not answered")
    question_3 = session.get("question_3", "Not answered")
    return render_template("summary.html", general_details=general_details,
                           question_1=question_1, question_2=question_2, question_3=question_3)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
