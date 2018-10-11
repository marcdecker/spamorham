import os
import json
import requests
import urllib3

from flask import Flask
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def Welcome():
	return render_template('index.htm')

@app.route('/score', methods=['GET', 'POST'])
def process_form_data():
	# Get the form data - result will contian all elements from the HTML form that was just submitted
	result = request.form

	#
	# The following lines are exactly the python code example form the Watson Machine Learning page
	#
	wml_credentials = {
		"apikey": "9idMYpHepBSXVnJ0h59q3E_dyks_xaadjDlDiro478Sl",
		"iam_apikey_description": "Auto generated apikey during resource-key operation for Instance - crn:v1:bluemix:public:pm-20:us-south:a/61dff0eb8c7deeb057ebafecc51289ad:13506357-3761-4c26-bb6e-7abff3efed10::",
		"iam_apikey_name": "auto-generated-apikey-a3271ca7-00ab-4e5a-a8ac-abf6df48d5ff",
		"iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
		"iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/61dff0eb8c7deeb057ebafecc51289ad::serviceid:ServiceId-ac6f1fc9-6853-4982-862a-20e8698c7fa8",
		"instance_id": "13506357-3761-4c26-bb6e-7abff3efed10",
		"password": "1ed75151-f110-48e8-a97d-6c0d3b6622a8",
		"url": "https://us-south.ml.cloud.ibm.com",
		"username": "a3271ca7-00ab-4e5a-a8ac-abf6df48d5ff"
	}

	scoring_endpoint = 'https://us-south.ml.cloud.ibm.com/v3/wml_instances/13506357-3761-4c26-bb6e-7abff3efed10/deployments/6d3042c0-1887-4ee2-8080-1f6aad0b33e1/online'

	headers = urllib3.util.make_headers(basic_auth='{username}:{password}'.format(username=wml_credentials['username'], password=wml_credentials['password']))
	url = '{}/v3/identity/token'.format(wml_credentials['url'])
	response = requests.get(url, headers=headers)

	mltoken = json.loads(response.text).get('token')

	header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

	#
	# Here the example code is slightly modified. The input from the form is send.
	# (!) No checks on data is done here.
	#
	# payload_scoring = {"values": [[result["mts2"], result["rooms"], result["distance_to_centre"], result["sauna"]]]}


	print(result)


	#	payload_scoring = {"fields": ["ID", "CHURN", "Gender", "Status", "Children", "Est Income", "Car Owner", "Age", "LongDistance", "International", "Local", "Dropped", "Paymethod", "LocalBilltype", "LongDistanceBilltype", "Usage", "RatePlan"], "values": [[ result['ID'],'T','M','S',2,60000,'Y',46,6,3,60,2,'CC','Budget','Standard',120,2]]}

	payload_scoring = {"fields": ["text"], "values": [[result["spaorham"] ]]}

	response_scoring = requests.post(scoring_endpoint, json=payload_scoring, headers=header)

	# The result is send back as JSON. 
	#
	return jsonify( json.loads(response_scoring.text)) 
	
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
