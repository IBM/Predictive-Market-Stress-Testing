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

from flask import Flask, jsonify, render_template, json, Response, request
import os
import requests
import csv

import investmentportfolio
import predictivemarketscenario
import simulatedinstrumentanalytics

app = Flask(__name__)

#risk factors defined to be used by the application
riskfactors = [
          {'CX_EQI_SPDJ_USA500_BMK_USD_LargeCap_Price': 'S&P 500 Index'},
          {'CX_EQI_NYSE_USA_BMK_USD_LargeCap_Price': 'NYSE MKT Composite Index'},
          {'CX_EQI_NASD_USAComposite_BMK_USD_LargeCap_Price': 'NASDAQ Composite Index'},
          {'CX_EQI_NYSE_CAC40_BMK_EUR_LargeCap_Price': 'CAC 40 Index'},
          {'CX_EQI_NIKK_Asia_BMK_JPY_LargeCap_Price':	'Nikkei 225 Index'},
          {'CX_EQI_HSNG_Asia_BMK_HKD_LargeCap_Price':	'Hang Seng Index'},
          {'CX_EQI_FTSE_UK_BMK_GBP_LargeCap_Price':	'FTSE 100 Index'},
          {'CX_FXC_EUR_USD_Spot': 'EUR/USD FX rate'},
          {'CX_FXC_JPY_USD_Spot': 'JPY/USD FX rate'},
          {'CX_FXC_CAD_USD_Spot': 'CAD/USD FX rate'},
          {'CX_FXC_GBP_USD_Spot': 'GBP/USD  FX rate'},
          {'CX_COS_EN_BrentCrude_IFEU': 'spot price of Brent Crude Oil'},
          {'CX_COS_EN_WTICrude_IFEU': 'spot price of WTI Crude Oil'},
          {'CX_COS_ME_Gold_XCEC': 'spot price of Gold'}
          ]

@app.route('/')
def run():
    """
    Load the site page
    """
    return render_template('index.html')

@app.route('/api/portfolionames',methods=['GET'])
def api_portfolionames():
    """
    Collects and returns the portfolio names
    """
    #get the portfolio names the from investmentportfolio module
    portfolio_names = []
    data = investmentportfolio.get_portfolios()
    for portfolios in data['portfolios']:
        portfolio_names.append(portfolios['name'])

    #returns the portfolio names as list
    print("Portfolio_names:" + str(portfolio_names))
    return json.dumps(portfolio_names)

@app.route('/api/getriskfactors',methods=['GET'])
def get_riskfactors():
    """
    Returns risk factors
    """
    return Response(json.dumps(riskfactors), mimetype='application/json')

@app.route('/api/analyze', methods =['GET','POST'])
def api_analyze():
    """
    Processes the user inputs to generate the scenario csv and run simulated instrument analytics on each holding in the portfolio
    """
    output = {}

    #retrieve the json from the ajax call
    json_file = ''
    if request.method == 'POST':
        json_file = request.json
        print ("post request")

    #if json_file successfully posted..
    if json_file != '':
        # check all required arguments are present:
        if not all(arg in json_file for arg in ["portfolio","riskfactor", "shockmag"]):
            print("Missing arguments in post request")
            return json.dumps({"status":"Error", "messages":"Missing arguments"}), 422
        portfolio = json_file["portfolio"]
        riskfactor = json_file["riskfactor"]
        shockmag = json_file["shockmag"]
        print("retreived data: " + str(portfolio) + " | " + str(riskfactor) + " | " + str(shockmag))

        #run Predictive Market Scenario service
        PMS_status = predictivemarketscenario.generate_scenario(riskfactor, shockmag)
        #if error in the call, return with error
        if PMS_status != 200:
            print("Unable to create csv from Predictive Market Scenario service")
            return json.dumps({'error': str(PMS_status) + " Unable to create csv from Predictive Market Scenario service"})
        print ("CREATED CSV")

        #get holdings data
        holdings_data = investmentportfolio.get_portfolio_holdings(portfolio)

        #go through each holding in the portfolio
        asset_output = []
        for holding in holdings_data["holdings"][-1]["holdings"]:

                #call the simulatedinstrumentanalytics module
                data = simulatedinstrumentanalytics.compute_simulated_analytics(instrument_id=holding["instrumentId"])

                #if returned as json would mean error, assign N/A, else assing the values from the list of objects
                if isinstance(data, dict):
                    value1 = "N/A"
                    value2 = "N/A"
                else:
                    value1 = data[0]["values"][0]["THEO/Price"]
                    value2 = data[1]["values"][0]["THEO/Price"]

                #create obj with the output values
                asset = holding["asset"]
                instrumentId = holding["instrumentId"]
                quantity = holding["quantity"]
                companyName = holding["companyName"]
                obj = {
                    'Asset': asset,
                    'InstrumentId': instrumentId,
                    'Quantity': quantity,
                    'CompanyName': companyName,
                    'BaseVal': value1,
                    'NewVal': value2
                }
                asset_output.append(obj)

        #get the market_conditions as list
        if os.path.exists("output_PMS.csv"):
            market_conditions = get_market_conditions("output_PMS.csv")

        #create the output json
        output = {"holdingsInfo": asset_output, "marketConditions": market_conditions}

    return json.dumps(output)


def get_market_conditions(filename):
    """
    Creates the market condition table from the scenario file and risk factors
    """
    market_conditions = []
    print("Generate conditions")

    #open the csv file to be read
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        #loop through each row to check with the risk factor and get the stress shift
        for row in readCSV:
            if len(row) > 14:
                risk_factor_csv = row[5]
                stress_shift_csv = row[13]

                #check risk factor and get the stress shift
                for rf in riskfactors:
                    for key in rf:
                        if risk_factor_csv == key and stress_shift_csv != '1':
                            #create the output obj with the values to return
                            obj = {"Risk_factor": rf[key], "Stress_shift": stress_shift_csv}
                            market_conditions.append(obj)
    return market_conditions

port = int(os.getenv('VCAP_APP_PORT', 3000))
host='0.0.0.0'

if __name__ == "__main__":
    app.run(host=host, port=int(port))
