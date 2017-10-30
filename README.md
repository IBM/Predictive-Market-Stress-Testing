# Predictive Market Stress Testing

In this developer journey, we will use three Bluemix finance services to create a web application which performs stress test on an investment portfolio. The Investment Portfolio service is used to load the portfolio into the interface. The Predictive Market Scenario service will create a scenario csv file using risk factor and shock magnitude from user inputs. The Simulated Instrument Analytics service uses the scenario csv file with each holding in the portfolio to create a table displaying the current and stressed price of the investment holding.

When the reader has completed this journey, they will understand how to:

* Load and retrieve data from the Investment Portfolio service
* Use the Predictive Market Scenario service to generate a scenario
* Send data along with a scenario to the Simulated Instrument Analytics service to retrieve analytics

<p align="center">
  <img width="400" height="400" src="static/images/architecture.png">
</p>

## Included Components
+ Bluemix Investment Portfolio
+ Bluemix Predictive Market Scenario
+ Bluemix Simulated Instrument Analytics

# Deploy to Bluemix

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/devops/setup/deploy?repository=https://github.com/IBM/Predictive-Market-Stress-Testing)

Be sure to [load investment portfolio](#3-load-investment-portfolio) before running the application.

# Running the Application
Follow these steps to setup and run this developer journey. The steps are described in detail below.

## Prerequisite
- [Python](https://www.python.org/downloads/)
- [curl](https://curl.haxx.se/download.html)

## Steps
1. [Clone the repo](#1-clone-the-repo)
2. [Create Bluemix services](#2-create-bluemix-services)
3. [Load Investment Portfolio](#3-load-investment-portfolio)
4. [Configure Manifest file](#4-configure-manifest)
5. [Configure .env file](#5-configure-env-file)
6. [Run Application](#6-run-application)

## 1. Clone the repo

Clone the `Predictive-Market-Stress-Testing code` locally. In a terminal, run:

  `$ git clone https://github.com/IBM/Predictive-Market-Stress-Testing.git`


## 2. Create Bluemix services

Create the following services:

* [**Investment Portfolio**](https://console.ng.bluemix.net/catalog/services/investment-portfolio)
* [**Predictive Market Scenario**](https://console.ng.bluemix.net/catalog/services/predictive-market-scenarios)
* [**Simulated Instrument Analytics**](https://console.ng.bluemix.net/catalog/services/simulated-instrument-analytics)


## 3. Load Investment Portfolio

You can load your Investment Portfolio using curl.
For all these steps:
- replace {service-user-id} the user id associated with your Investment Portfolio Service
- replace {service-user_password} with the password associated with your Investment Portfolio Service

i. Creating a portfolio entry in your Investment Portfolio service:

`curl -X POST -u "{service-user-id}":"{service-user_password}" --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{ "name":"MyFixedIncomePortfolio", "timestamp": "2017-02-22T19:53:56.830Z", "closed": false, "data": { "manager": "Will Smith" }}' 'https://investment-portfolio.mybluemix.net/api/v1/portfolios'`

ii. Creating holdings in your entry:

`curl -X POST -u "{service-user-id}":"{service-user_password}" --header 'Content-Type: application/json' --header 'Accept:application/json' -d '{ "timestamp": "2017-06-04T19:53:56.830Z", "holdings": [ { "asset": "AMGN 4.1 06/15/21", "quantity": 10, "instrumentId": "CX_US031162BG42_USD", "companyName": "AMGEN INC"}, { "asset": "AMGN 5.15 11/15/41", "quantity": 30, "instrumentId": "CX_US031162BK53_USD", "companyName": "AMGEN INC" }, { "asset": "EVHC 5.625 07/15/22", "quantity": 50, "instrumentId": "CX_US03232PAD06_USD", "companyName": "ENVISION HEALTHCARE CORP"}, { "asset": "APC 4.85 03/15/21", "quantity": 40, "instrumentId": "CX_US032511BM81_USD", "companyName": "ANADARKO PETROLEUM CORP"}, { "asset": "ADI 3.5 12/05/26", "quantity": 30, "instrumentId": "CX_US032654AN54_USD", "companyName": "ANALOG DEVICES INC"}, { "asset": "ABIBB 2.65 02/01/21", "quantity": 20, "instrumentId": "CX_US035242AJ52_USD", "companyName": "ANHEUSER-BUSCH INBEV FIN"}, { "asset": "ABIBB 3.3 02/01/23", "quantity": 10, "instrumentId": "CX_US035242AL09_USD", "companyName": "ANHEUSER-BUSCH INBEV FIN"} ] }' 'https://investment-portfolio.mybluemix.net/api/v1/portfolios/MyFixedIncomePortfolio/holdings'`

Find more information on Investment Portfolio api calls [here](https://console.ng.bluemix.net/apidocs/751-investment-portfolio?&language=node#introduction).

## 4. Configure Manifest file

Edit the `manifest.yml` file in the folder that contains your code and replace with a unique name for your application. The name that you specify determines the application's URL, such as `your-application-name.mybluemix.net`. Additionally - update the service names so they match what you have in Bluemix. The relevant portion of the `manifest.yml` file looks like the following:

  ```none
  declared-services:
    Investment-Portfolio:
      label: fss-portfolio-service
      plan: fss-portfolio-service-free-plan
    Predictive-Market-Scenarios:
      label: fss-predictive-scenario-analytics-service
      plan: fss-predictive-scenario-analytics-service-free-plan
    Simulated-Instrument-Analytics:
      label: fss-scenario-analytics-service
      plan: fss-scenario-analytics-service-free-plan
  applications:
  - path: .
    memory: 128M
    instances: 1
    name: Predictive-Market-Stress-Testing
    disk_quota: 1024M
    domain: mybluemix.net
    services:
    - Investment-Portfolio
    - Predictive-Market-Scenarios
    - Simulated-Instrument-Analytics
    buildpack: python_buildpack
  ```

## 5. Configure .env file

Create a `.env` file in the root directory of your clone of the project repository by copying the sample `.env.example` file using the following command:

  ```none
  cp .env.example .env
  ```

  **NOTE** Most files systems regard files with a "." at the front as hidden files.  If you are on a Windows system, you should be able to use either [GitBash](https://git-for-windows.github.io/) or [Xcopy](https://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/xcopy.mspx?mfr=true)

You will need to update the credentials with the Bluemix credentials for each of the services you created in [Step 2](#2-create-bluemix-services).

The `.env` file will look something like the following:

  ```none
  #Investment Portfolio
  CRED_PORTFOLIO_USERID_W=
  CRED_PORTFOLIO_PWD_W=
  CRED_PORTFOLIO_USERID_R=
  CRED_PORTFOLIO_PWD_R=
  URL_GET_PORTFOLIO_HOLDINGS=https://investment-portfolio.mybluemix.net/api/v1/portfolios/

  #Predictive Market Scenario
  CRED_PREDICTIVE_MARKET_SCENARIO_URL=https://fss-analytics.mybluemix.net/api/v1/scenario/generate_predictive
  CRED_PREDICTIVE_MARKET_SCENARIO_ACCESSTOKEN=

  #Simulated Instrument Analytics
  CRED_SIMULATED_INSTRUMENT_ANALYTICS_URL=https://fss-analytics.mybluemix.net/api/v1/scenario/instrument/
  CRED_SIMULATED_INSTRUMENT_ANALYTICS_ACCESSTOKEN=
  ```

## 6. Run Application

cd into this project's root directory
+ Run `pip install -r requirements.txt` to install the app's dependencies
+ Run `python run.py`
+ Access the running app in a browser at <http://0.0.0.0:8080/>

# Troubleshooting

* To troubleshoot your Bluemix application, use the logs. To see the logs, run:

```bash
cf logs <application-name> --recent
```

* If you are running locally - inspect your environment variables closely to confirm they match.  Try running each service as standalone:

```bash
python InvestmentPortfolio.py
python PredictiveMarketScenario.py
python SimulatedInstrumentAnalytics.py
```

## Privacy Notice

Sample web applications that include this package may be configured to track deployments to [IBM Bluemix](https://www.bluemix.net/) and other platforms. The following information is sent to a [Deployment Tracker](https://github.com/IBM/metrics-collector-service) service on each deployment:

* Python package version
* Python repository URL
* Application Name (`application_name`)
* Application GUID (`application_id`)
* Application instance index number (`instance_index`)
* Space ID (`space_id`) or OS username
* Application Version (`application_version`)
* Application URIs (`application_uris`)
* Cloud Foundry API (`cf_api`)
* Labels and names of bound services
* Number of instances for each bound service and associated plan information
* Metadata in the repository.yaml file

This data is collected from the `setup.py` and `repository.yaml` file in the sample application and the `VCAP_APPLICATION` and `VCAP_SERVICES` environment variables in IBM Bluemix and other Cloud Foundry platforms. This data is used by IBM to track metrics around deployments of sample applications to IBM Bluemix to measure the usefulness of our examples, so that we can continuously improve the content we offer to you. Only deployments of sample applications that include code to ping the Deployment Tracker service will be tracked.

## Disabling Deployment Tracking

To disable tracking, simply remove ``metrics_tracker_client.track()`` from the
``run.py`` file in the top level directory.

# License

[Apache 2.0](LICENSE)
