from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None  # To hold the result to be displayed in the template
    bmi_result = None  # To hold the BMI result and weight status
    bmi_class = None  # To hold the BMI category class
    
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height']) / 100  # Convert cm to meters
        age = float(request.form['age'])
        gender = request.form['gender']
        activity_level = request.form['activity']
        
        # BMR calculation based on gender
        if gender == "1":
            bmr = 66.47 + (13.75 * weight) + (5.003 * height * 100) - (6.755 * age)
        elif gender == "2":
            bmr = 655.1 + (9.563 * weight) + (1.85 * height * 100) - (4.676 * age)
        else:
            result = "Invalid gender selected."
            return render_template('index.html', result=result)
        
        # Activity factors based on activity level
        activity_factors = {
            "1": 1.2,
            "2": 1.375,
            "3": 1.55,
            "4": 1.725,
            "5": 1.9
        }
        
        # Calculate Total Daily Energy Expenditure (TDEE)
        if activity_level in activity_factors:
            total = bmr * activity_factors[activity_level]
            result = f"Your Total Daily Energy Needed: {total:.2f} calories/day"
        else:
            result = 'Enter a correct activity level (1 to 5).'
        
        # BMI Calculation
        bmi = weight / (height ** 2)
        
        # BMI Classification and adding classes for styling
        if bmi < 18.5:
            bmi_result = f"Your BMI is: {bmi:.2f} (Underweight)"
            bmi_class = "underweight"
        elif 18.5 <= bmi < 24.9:
            bmi_result = f"Your BMI is: {bmi:.2f} (Normal weight)"
            bmi_class = "normal"
        elif 25 <= bmi < 29.9:
            bmi_result = f"Your BMI is: {bmi:.2f} (Overweight)"
            bmi_class = "overweight"
        else:
            bmi_result = f"Your BMI is: {bmi:.2f} (Obese)"
            bmi_class = "obese"
    
    return render_template('index.html', result=result, bmi_result=bmi_result, bmi_class=bmi_class)

if __name__ == '__main__':
    app.run(debug=True)
