from flask import Flask,render_template,request,make_response,jsonify,session,redirect,url_for
app = Flask(__name__)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import pickle
import numpy as np
model = pickle.load(open("model_pkl", "rb"))


#-----------------------------------------------DATABASE-------------------------------------------------------------------
import sqlite3
conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS register
             (username text,email text,password text)''')			
conn.commit()
conn.close()
#----------------------------------------------------------------------------------------------------------------------------




@app.route('/',methods=['GET','POST'])
def First():
    return render_template("index.html")


@app.route('/deside',methods=['GET','POST'])
def Second():
    return render_template("form.html")

@app.route('/Signin',methods=['GET','POST'])
def Signin():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        re_password = request.form.get("re_password")
        
        if username !="" and password !="" and email !="" and re_password!="":
            if password==re_password:
                conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
                c = conn.cursor()
                c.execute("SELECT * FROM register")
                for query_result in c.fetchall():
                    if username in query_result:
                        return jsonify("already exists")
                    else:  
                        pass   
                password = bytes(password, 'utf-8')
                password = hashing(password)
                c.execute("""INSERT INTO register (username,email,password) values (?,?,?)""",(username,email,password))
                conn.commit()
                return redirect(url_for('Login'))
            else:
                return jsonify("password dosent match ") 
        else:
           return jsonify("enter all fields") 
        
    return render_template("form.html")



@app.route('/login',methods=['GET','POST'])
def Login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username !="" and password !="":
            conn = sqlite3.connect('mysqlite.db',check_same_thread=False)
            c = conn.cursor()
            c.execute("SELECT * FROM register WHERE username=?", ( username,))
            result = c.fetchall()
            if len(result)==0:     
                return jsonify("no user found")
            for i in result:
                if verify_pass(i[2],password):
                    return redirect(url_for('Home'))
                else:
                    return jsonify("invalid user")
        else:
            return jsonify("enter all fields")

    return render_template("form.html")


@app.route('/home',methods=['GET','POST'])
def Home():

    Fuel_Type_Diesel=0
    
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0

        prediction=model.predict(np.array([[Year, 
                                            Present_Price, 
                                            Kms_Driven,
                                            Owner, 
                                            Fuel_Type_Diesel, 
                                            Fuel_Type_Petrol, 
                                            Seller_Type_Individual, 
                                            Transmission_Mannual]]))
        output=round(prediction[0],2)
        if output<0:
            return render_template('home.html',prediction_texts="Sorry you cannot sell this car")
        else:
            print(output)
            return render_template('home.html',prediction_text="You can sell the Car at {} lakhs".format(output))
    else:
        return render_template("home.html")




def hashing(password):
    pw_hash = bcrypt.generate_password_hash(password)
    return pw_hash
def verify_pass(password,password1):
    return bcrypt.check_password_hash(password,password1)


if __name__=="__main__":
    app.run()
    app.run(debug=True)