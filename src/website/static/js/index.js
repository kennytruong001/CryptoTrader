/// <reference types="aws-sdk" />
f = open('config.json')
secret = json.load(f)

var x = document.getElementById("login")
var y = document.getElementById("register");
var z = document.getElementById("btn");

function register(){
    x.style.left = "-400px";
    y.style.left = "50px";
    z.style.left = "110px";
    
}

function login(){
    x.style.left = "50px";
    y.style.left = "450px";
    z.style.left = "0px";
    
}

function read(username){
    // Load the AWS SDK for Node.js
    //var AWS = import('aws-sdk');
    // Set the region 
    AWS.config.update({region: 'us-west-1'});
    AWS.config.credentials = new AWS.Credentials(secret["ACCESS_KEY_ID"], secret["ACCESS_SECRET_KEY"]);
    
    // Create the DynamoDB service object
    var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
    
    var params = {
    TableName: 'CryptoTrader',
    Key: {
        'User' : {S: username}
    },
    //ProjectionExpression: 'ATTRIBUTE_NAME'
    };
    
    // Call DynamoDB to read the item from the table
    ddb.getItem(params, function(err, data) {
    if (err) {
        alert("ERROR");
    } else {
        return JSON.stringify(data.Item['Password']['S']).replace('"', '').replace('"', '');
    }
    });
}

function validate(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var temp = '';
    AWS.config.update({region: 'us-west-1'});
    AWS.config.credentials = new AWS.Credentials(secret["ACCESS_KEY_ID"], secret["ACCESS_SECRET_KEY"]);
    
    // Create the DynamoDB service object
    var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});
    
    var params = {
    TableName: 'CryptoTrader',
    Key: {
        'User' : {S: username}
        //'Password': '99d3fd0fa8fe115ef5983b5472cc95a88f2790a6fa89f8785da5afbe7b548bba'
    },
    //ProjectionExpression: 'ATTRIBUTE_NAME'
    };
    
    // Call DynamoDB to read the item from the table
    ddb.getItem(params, function(err, data) {
    if (err) {
        alert("ERROR");
    } else {
        temp = JSON.stringify(data.Item['Password']['S']).replace('"', '').replace('"', '');
    }
    });

    if (password == temp){
        alert("LOGIN SUCCESSFUL");
        return false;
    }
    else{
        alert("LOGIN FAILED");
    }
}

async function sha256(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder().encode(message);                    

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string                  
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashHex;
}