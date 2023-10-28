from flask import Flask, render_template, request
import xgboost as xg
import pandas as pd
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        location = request.form['location']
        subscription_months = int(request.form['subscription_months'])
        monthly_bill = float(request.form['monthly_bill'])
        total_usage_gb = float(request.form['total_usage_gb'])

        subscription_length_years = float(request.form['subscription_length_years'])
        total_monthly_cost = float(request.form['total_monthly_cost'])
        monthly_usage_per_year = float(request.form['monthly_usage_per_year'])

        data = pd.DataFrame({
            'Age': [age],
            'Gender': [gender],
            'Location': [location],
            'Subscription_Length_Months': [subscription_months],
            'Monthly_Bill': [monthly_bill],
            'Total_Usage_GB': [total_usage_gb],
            'Subscription_Length_Years': [subscription_length_years],
            'Total_Monthly_Cost': [total_monthly_cost],
            'Monthly_Usage_Per_Year': [monthly_usage_per_year]
        })

        predictions = model.predict(data)
        return render_template('result.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
