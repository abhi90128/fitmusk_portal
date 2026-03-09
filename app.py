from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    result = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100
        result = round(weight / (height ** 2), 2)
    return render_template('bmi.html', result=result)

@app.route('/calorie', methods=['GET', 'POST'])
def calorie():
    calories = None
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        age = int(request.form['age'])
        gender = request.form['gender']

        if gender == 'male':
            bmr = 10*weight + 6.25*height - 5*age + 5
        else:
            bmr = 10*weight + 6.25*height - 5*age - 161

        calories = round(bmr * 1.55)

    return render_template('calorie.html', calories=calories)

@app.route('/macro', methods=['GET', 'POST'])
def macro():
    protein = carbs = fats = None

    if request.method == 'POST':
        weight = float(request.form['weight'])
        goal = request.form['goal']

        # Protein calculation
        protein = round(weight * 2)

        # Calories from protein
        protein_calories = protein * 4

        if goal == 'fat_loss':
            total_calories = weight * 24
        elif goal == 'muscle_gain':
            total_calories = weight * 30
        else:
            total_calories = weight * 27

        remaining_calories = total_calories - protein_calories

        fats = round((remaining_calories * 0.25) / 9)
        carbs = round((remaining_calories - (fats * 9)) / 4)

    return render_template('macro.html',
                           protein=protein,
                           carbs=carbs,
                           fats=fats)

@app.route('/faq')
@app.route('/faq')
def faq():
    faqs = [
        {"question": "How much protein should I consume daily?",
         "answer": "You should consume around 1.6 to 2.2 grams of protein per kg of bodyweight."},

        {"question": "Is cardio necessary for fat loss?",
         "answer": "Calorie deficit is most important. Cardio helps but diet plays bigger role."},

        {"question": "How many days per week should I workout?",
         "answer": "3 to 5 days per week is ideal depending on your goal and recovery."},

        {"question": "Can I build muscle while losing fat?",
         "answer": "Yes, beginners can achieve body recomposition with proper diet and training."}
    ]

    return render_template('faq.html', faqs=faqs)


@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/choose-plan')
def choose_plan():
    return render_template('choose_plan.html')


@app.route('/experience/<bodytype>')
def experience(bodytype):
    return render_template('experience.html', bodytype=bodytype)


@app.route('/plan-result/<bodytype>/<level>')
def plan_result(bodytype, level):

    plans = {

        "lean": {
            "beginner": [
                "Ultimate Bulk 1",
                "Summer Gain 1",
                "Winter Bulk"
            ],
            "intermediate": [
                "Bulk 2",
                "Summer Gain 2"
            ],
            "advanced": [
                "Advanced Lean Athlete Plan"
            ]
        },

        "average": {
            "beginner": [
                "Lean Mode 1",
                "Body Recomp 1"
            ],
            "intermediate": [
                "Lean Mode 2",
                "Body Recomp 2"
            ],
            "advanced": [
                "Advanced Recomposition Plan"
            ]
        },

        "highbf": {
            "beginner": [
                "Ultimate Shred 1"
            ],
            "intermediate": [
                "Ultimate Shred 2"
            ],
            "advanced": [
                "Extreme Fat Loss Plan"
            ]
        }
    }

    recommended = plans.get(bodytype, {}).get(level, [])

    return render_template(
        'plan_result.html',
        plans=recommended,
        bodytype=bodytype,
        level=level
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)