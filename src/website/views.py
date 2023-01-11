from flask import Blueprint, render_template, request, flash, jsonify, session
import json
import boto3
from website.helpers import getConfigs

configs = getConfigs()

client = boto3.client('dynamodb')
table = boto3.resource('dynamodb', aws_access_key_id=configs["ACCESS_KEY_ID"],
                    aws_secret_access_key=configs["ACCESS_SECRET_KEY"]).Table("CryptoTrader")

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    user = request.args.get('name')
    userInfo = table.get_item(Key={"User":user})["Item"]
    portfolio = userInfo["Portfolio"]
    balance = userInfo["Balance"]

    if request.method == 'POST':
        action = request.form.get('action')
        coin = request.form.get('coin')
        amount = request.form.get('amount')
            
        table.put_item(Item={
            columns[0] : user,
            columns[1] : userInfo["Password"],
            columns[2] : userInfo["Balance"],
            columns[3] : userInfo["Portfolio"]
        })
    return render_template("home.html", name=user, accountPortfolio=portfolio, accountBalance=balance)

@views.route('/')
def index():
    return render_template("index.html")