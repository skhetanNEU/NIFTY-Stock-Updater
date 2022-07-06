# NIFTY Stocks Updater
This is a stocks updater that fetches data from multiple sites consisting data about NIFTY Stocks, parses the data accordingly and updates the google sheets along with updating it periodically locally on Microsoft Excel.

A dyno is setup on Heroku to run this stock updater in a specified time interval.

The google sheets(that gets updated by this updater) consists of certain decision rules taking into consideration factors such as moving averages for 50 days, 100 days, 200 days, support values, resistance values, curve formation of stocks and gives out predicitions for the best performing stocks.

(This repo doesn't contain the Keys.json required since it cannot be made public.)

The requirements for running this script is mentioned in requirements.txt.

