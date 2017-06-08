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

#Predictive Market Scenario credentials
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
access_token=os.environ.get("CRED_PREDICTIVE_MARKET_SCENARIO_ACCESSTOKEN")
uri=os.environ.get("CRED_PREDICTIVE_MARKET_SCENARIO_URL")

def Generate_Scenario(risk_factor_id, shock_value):
    """
    Creates the 'output_PMS.csv' file with the scenario by calling the Predictive Market Service service, pass the risk_factor_id and shock_value
    """
    #print for logging purpose
    print ("Generate Scenario")
    print ("Risk factor: " + risk_factor_id)
    print ("Shock Value: " + str(shock_value))
    #call the url
    BASEURL = uri
    headers = {
        'X-IBM-Access-Token': access_token,
        'Content-Type': "application/json"
        }
    data = {
        'market_change': {
            'risk_factor': risk_factor_id,
            'shock': shock_value
            }
        }
    get_data = requests.post(BASEURL, headers=headers, data=json.dumps(data))
    status = get_data.status_code
    print("Predictive Market Scenario status: " + str(status))

    #if the status is not success, return with status
    if status != 200:
        return status

    #create csv file
    data = get_data.text
    #print(data)
    f = open("output_PMS.csv", "w")
    f.write(data)
    f.close()

    #print for logging purpose, return the status
    print (os.path.exists("output_PMS.csv"))
    print("Created output_PMS.csv")
    return status

def main():
    """
    Can run this script to test Predictive Market Scenario service
    """
    risk_factor_id = "CX_EQI_SPDJ_USA500_BMK_USD_LargeCap_Price"
    shock_value = 1.5
    Generate_Scenario(risk_factor_id,shock_value)

if __name__=="__main__":
    main()
