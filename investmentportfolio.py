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
from dotenv import load_dotenv
import os

#initalize Investment Portfolio Service credentials to find on Bluemix otherwise from .env file
if 'VCAP_SERVICES' in os.environ:
    #load vcap service data from the app env
    vcap_services_data = json.loads(os.environ['VCAP_SERVICES'])

    #log the fact that we successfully found some service information.
    print("Got vcap_services_data\n")

    # Look for the IP service instance.
    IP_W_USERNAME=vcap_services_data['fss-portfolio-service'][0]['credentials']['writer']['userid']
    IP_W_PASSWORD=vcap_services_data['fss-portfolio-service'][0]['credentials']['writer']['password']
    IP_R_USERNAME=vcap_services_data['fss-portfolio-service'][0]['credentials']['reader']['userid']
    IP_R_PASSWORD=vcap_services_data['fss-portfolio-service'][0]['credentials']['reader']['password']

    #log the fact that we successfully found credentials
    print("Got IP credentials\n")
else:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    IP_W_USERNAME=os.environ.get("CRED_PORTFOLIO_USERID_W")
    IP_W_PASSWORD=os.environ.get("CRED_PORTFOLIO_PWD_W")
    IP_R_USERNAME=os.environ.get("CRED_PORTFOLIO_USERID_R")
    IP_R_PASSWORD=os.environ.get("CRED_PORTFOLIO_PWD_R")

def get_portfolios():
    """
    Retreives portfolio data by calling the Investment Portfolio service
    """
    print ("Get Portfolios")

    #call the url
    baseurl = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(baseurl, auth=(IP_R_USERNAME, IP_R_PASSWORD), headers=headers)
    print("Investment Portfolio status: " + str(get_data.status_code))

    # return json data
    data = get_data.json()
    print(data)
    return data

def get_portfolio_holdings(portfolio):
    """
    Retreives holdinga data from the Investment Portfolio service for the Portfolio
    """
    print ("Get Portfolio Holdings for " + portfolio)
    #construct the url
    baseurl = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/" + portfolio + "/holdings?latest=true"

    #call the url
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(baseurl, auth=(IP_R_USERNAME, IP_R_PASSWORD), headers=headers)
    print("Investment Portfolio - Get Portfolio Holdings status: " + str(get_data.status_code))

    #return json data
    data = get_data.json()
    print(data)
    return data

def main():
    """
    Can run this script to test Investment Portfolio service
    """
    get_portfolios()
    get_portfolio_holdings("MyFixedIncomePortfolio")

if __name__=="__main__":
    main()
