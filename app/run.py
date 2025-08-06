from flask import Flask,redirect,render_template,request,url_for
import redis
app = Flask(__name__)
app.secret_key = "pawan236007"

r = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/registration',methods=['GET','POST'])
def register():
  if request.method=="POST":  
    name = request.form.get('First')
    last = request.form.get('Last')
    email = request.form.get('Email')
    password = request.form.get('Password')
    r.hset(f"user:{email}",
      mapping={
          'first' : name,
          'last' : last,
          'password' :  password,
          'email' : email
      }
    )
    return redirect(url_for('index'))
  return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_key = f"user:{email}"
        if r.exists(user_key):
            storedpass = r.hget(user_key, 'password')
            if password == storedpass:
                return redirect(url_for('index'))
            else:
                return "Incorrect password"
        else:
            return "Email not registered"

    # For GET request, show login form
    return render_template('login.html')

if __name__=="__main__":
    app.run(debug=True)
