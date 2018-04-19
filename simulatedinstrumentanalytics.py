# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
import argparse
import os
from dotenv import load_dotenv

#initalize Simulated Instrument Analytics service credentials
if 'VCAP_SERVICES' in os.environ:
    #load vcap service data from the app env
    vcap_services_data = json.loads(os.environ['VCAP_SERVICES'])

    #log the fact that we successfully found some service information.
    print("Got vcap_services_data\n")

    #look for the Simulated Instrument Analytics service instance
    access_token=vcap_services_data['fss-scenario-analytics-service'][0]['credentials']['accessToken']
    uri=vcap_services_data['fss-scenario-analytics-service'][0]['credentials']['uri']

    # Log the fact that we successfully found credentials
    print("Got SIA credentials\n")
else:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    access_token=os.environ.get("CRED_SIMULATED_INSTRUMENT_ANALYTICS_ACCESSTOKEN")
    uri=os.environ.get("CRED_SIMULATED_INSTRUMENT_ANALYTICS_URL")

def compute_simulated_analytics(instrument_id, scenario_file = "output_PMS.csv"):
    """
    Retreives the Simulated Instrument Analytics service data, pass the instrument_id and scernario file
    """
    #print for logging purpose
    print ("Compute Simulated Analytics")
    print("Instrument ID: " + instrument_id)
    print("Scenario File: " + scenario_file)

    #call the url
    baseurl = 'https://fss-analytics.mybluemix.net/api/v1/scenario/instrument/'  + instrument_id
    headers = {
        'enctype': "multipart/form-data",
        'x-ibm-access-token': access_token
        }
    files = {'scenario_file': open(scenario_file, 'rb')}
    get_data = requests.post(baseurl, headers=headers, files=files)
    print("Simulated Instrument Analytics status: " + str(get_data.status_code))

    #return json data
    data = get_data.json()
    print(data)
    return data

def main():
    """
    Can run this script to test Simulated Instrument Analytics service
    """
    compute_simulated_analytics(instrument_id="CX_US035242AJ52_USD")

if __name__=="__main__":
    main()
