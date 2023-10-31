from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flaskext.mysql import MySQL
from flask_session import Session
import pandas as pd
import joblib

model = joblib.load('trainedModel.pkl')


app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hackathon'
mysql = MySQL(app)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Configure the session secret key
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        username = request.form.get('username')
        gender = request.form.get('gender')
        salary = request.form.get('salary')
        password = request.form.get('password')

        try:
            cursor = mysql.get_db().cursor()
            cursor.execute("INSERT INTO hackathon.user_register (Name, Phonenumber, Username, Gender, Salary, Password) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, phone, username, gender, salary, password))

            mysql.get_db().commit()
            cursor.close()
            
            # Redirect to the login page after successful registration
            return redirect(url_for('login'))
        except Exception as e:
            return "Error: " + str(e)

    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM hackathon.user_register WHERE Username = %s AND Password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            
            session['name'] = user[0]
            session['phone'] = user[1]  
            session['gender'] = user[3] 
            session['username'] = user[2]  
            session['salary'] = user[4]  
            
            # Redirect to a user dashboard or any other route
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password. Please try again."

    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.clear() 
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            try:
                # Read the uploaded dataset
                data = pd.read_csv(uploaded_file)
                # Assuming the dataset has 'earnings' and 'earning_potential' columns
                
                # Make predictions using the model
                # Assuming 'model' is a trained machine learning model
                predictions = model.predict(data[['earnings', 'earning_potential']])
                
                # Add the predictions to the dataset
                data['preferred_spending_limit'] = predictions *30
                data['savings']=data['earnings']- data['preferred_spending_limit']
                data['ROI']=(data['earning_potential']/data['earnings'])*100

                # Convert the dataset to HTML table
                result_table = data.to_html(classes='table table-bordered table-hover', index=False)
            except Exception as e:
                result_table = str(e)
        else:
            result_table = "Please upload a valid CSV file."

        return render_template('dashboard.html', result=result_table)


    
if __name__ == '__main__':
    app.run(debug=True)
