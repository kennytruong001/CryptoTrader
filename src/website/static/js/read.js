// Load the AWS SDK for Node.js
var AWS = require('aws-sdk');
var user = 'kenny';
// Set the region 
AWS.config.update({region: 'us-west-1'});
AWS.config.credentials = new AWS.Credentials('AKIARTYATDA47PJGBUGN', '5vRj4J8urcgIabFKaW6Bww1WN7MNkdm7Yhxoob44');

// Create the DynamoDB service object
var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

var params = {
TableName: 'CryptoTrader',
Key: {
    'User' : {S: user}
    //'Password': {S:'99d3fd0fa8fe115ef5983b5472cc95a88f2790a6fa89f8785da5afbe7b548bba'}
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

    