from flask import Blueprint, render_template, request, flash, redirect, url_for
#import key_config as keys
import boto3 
import hashlib
import json


auth = Blueprint('auth', __name__)
f = open('config.json')
secret = json.load(f)

client = boto3.client('dynamodb')
table = boto3.resource('dynamodb', aws_access_key_id=secret["ACCESS_KEY_ID"],
                    aws_secret_access_key=secret["ACCESS_SECRET_KEY"]).Table("CryptoTrader")
                    


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        sha256_pass = hashlib.sha256(password.encode())
        userInfo = table.get_item(Key={"User":user})["Item"]
        portfolio = userInfo["Portfolio"]
        balance = userInfo["Balance"]
        #if sha256_pass.hexdigest() == userRecord[input_name].getPassword():
        if userInfo:
            if password == userInfo["Password"]:
                return redirect(url_for('views.home', name=user))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user = request.form.get('user')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(user) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')
            # if request.method=='POST':

            #     userInfo = table.get_item(Key={"User":user})["Item"]
            #     items = response['Items']
            #     name = items[0]['name']
            #     print(items[0]['password'])
            #     if password == items[0]['password']:
            #         return render_template("home.html",name = name)
    return render_template("sign_up.html")
    
f.close()