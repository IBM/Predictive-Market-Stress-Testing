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

#Investment Portfolio Service credentials
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
IP_W_username=os.environ.get("CRED_PORTFOLIO_USERID_W")
IP_W_password=os.environ.get("CRED_PORTFOLIO_PWD_W")
IP_R_username=os.environ.get("CRED_PORTFOLIO_USERID_R")
IP_R_password=os.environ.get("CRED_PORTFOLIO_PWD_R")

def Get_Portfolios():
    """
    Retreives portfolio data by calling the Investment Portfolio service
    """
    print ("Get Portfolios")
    #call the url
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/"
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)
    print("Investment Portfolio status: " + str(get_data.status_code))
    # return json data
    data = get_data.json()
    print(data)
    return data

def Get_Portfolio_Holdings(Portfolio):
    """
    Retreives holdinga data from the Investment Portfolio service for the Portfolio
    """
    print ("Get Portfolio Holdings for " + Portfolio)
    #construct the url
    BASEURL = "https://investment-portfolio.mybluemix.net/api/v1/portfolios/" + Portfolio + "/holdings"
    #call the url
    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    get_data = requests.get(BASEURL, auth=(IP_R_username, IP_R_password), headers=headers)
    print("Investment Portfolio - Get Portfolio Holdings status: " + str(get_data.status_code))
    #return json data
    data = get_data.json()
    print(data)
    return data

def main():
    """
    Can run this script to test Investment Portfolio service
    """
    Get_Portfolios()
    #Get_Portfolio_Holdings("P1")
    Get_Portfolio_Holdings("MyFixedIncomePortfolio")

if __name__=="__main__":
    main()
