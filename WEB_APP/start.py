import sys
from flask import Flask, request, render_template, redirect,url_for
import string #for a list of all the alphabets
import random
import string
import numpy as np
import os
import subprocess
import json
import combined #this is the python file which does all the processing


# import test
string_entered = " "
stringg = " "

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('input.html')



@app.route("/sendstring",methods=["GET","POST"])
def send():  
        global string_entered
        string_entered = request.form['string_entered']
        ob = combined.test_class()
        result  = ob.input(string_entered)
        #NOW THIS RESULT MIGHT BE THE ERROR CATCH LIST OR THE SET OF STRINGS
        #SO LET'S CHECK
        #IF IT IS THE ERROR CATCH LIST ;  WE NEED TO GENERATE A DIFFERENT HTML PAGE TO DISPLAY THE ERRORS
        if(type(result)==tuple):
                return render_template("string_display.html", result = json.dumps(result))
        else:
                return render_template("error_display.html", result = json.dumps(result[1]))  



@app.route("/backhome",methods=["GET","POST"])
def backhome():
        return render_template("input.html")
    

@app.route("/runjflap",methods=["GET","POST"])
def runjflap():
        import subprocess
        subprocess.call(['java', '-jar', 'JFLAP7.jar'])

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='127.0.0.1', port=5000)




