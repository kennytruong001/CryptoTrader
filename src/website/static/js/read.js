// Load the AWS SDK for Node.js
f = open('config.json')
secret = json.load(f)

var AWS = require('aws-sdk');
var user = 'kenny';
// Set the region 
AWS.config.update({region: 'us-west-1'});
AWS.config.credentials = new AWS.Credentials(secret["ACCESS_KEY_ID"], secret["ACCESS_SECRET_KEY"]);

// Create the DynamoDB service object
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

var params = {
TableName: 'CryptoTrader',
Key: {
    'User' : {S: user}
},
//ProjectionExpression: 'ATTRIBUTE_NAME'
};

// Call DynamoDB to read the item from the table
ddb.getItem(params, function(err, data) {
if (err) {
    console.log("Error", err);
} else {
    console.log("Success", JSON.stringify(data.Item['Password']['S']).replace('"', '').replace('"', ''));
}
//JSON.stringify(data.Item['Password']['S']).replace('"', '').replace('"', '')
});

    