# stock-data-collector
A python script that collects US stock data and outputs useful information for analytical engagement

The program uses the Alpha Vantage API to fetch financial data and tabulates it within the console. Output is
exportable to Excel. 

Only issue: data is inconsistent perhaps due to the AV infrastructure. Error messages pop up at times, while at other times, 
the script works fine. Need to look into this...

UPDATE: improved version includes more overview information ahout the company. Note that the above issue raised is mainly because 
AV has a limitation on API calls for its free services. 5 calls per minute and 500 calls per month are the allowed freemium services

