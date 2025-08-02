from flask import Flask,redirect,render_template,request,url_for
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Dummy check (you can add real auth here)
    if email == "admin@example.com" and password == "1234":
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials", 401
if __name__=="__main__":
    app.run(debug=True)
