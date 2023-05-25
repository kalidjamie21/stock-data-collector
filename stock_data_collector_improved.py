import requests
from tabulate import tabulate

API_KEY = 'RLZ5GE7FUOM57VUY'

def get_company_data(ticker):
    overview_url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'

    try:
        # Make API request for company overview data
        overview_response = requests.get(overview_url)

        # Check if the request is successful
        if overview_response.status_code == 200:
            # Extract required data from overview response
            company_data = overview_response.json()
            global company_name, exchange_platform, company_description, company_sector, company_industry, company_market_cap, ev_to_ebitda 
            company_name = company_data['Name']
            exchange_platform = company_data['Exchange']
            #stock_price = company_data['Price']
            company_description = company_data['Description']
            company_sector = company_data['Sector']
            company_industry = company_data['Industry']
            company_market_cap = int(company_data['MarketCapitalization'])
            ev_to_ebitda = company_data['EVToEBITDA']

            # Call the existing function to fetch and print financial data
            get_financial_data(ticker)
        else:
            print("Error: Failed to fetch company data.")
    except KeyError:
        print("Error: Company data not available for the given ticker symbol.")
    except requests.exceptions.RequestException:
        print("Error: Failed to connect to the API. Please check your internet connection.")

def get_financial_data(ticker):
    income_statement_url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={API_KEY}'
    balance_sheet_url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={API_KEY}'
    cash_flow_url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={API_KEY}'

    try:
        # Make API requests for income statement, balance sheet, and cash flow statement
        income_statement_response = requests.get(income_statement_url)
        balance_sheet_response = requests.get(balance_sheet_url)
        cash_flow_response = requests.get(cash_flow_url)

        # Check if all requests are successful
        if all(response.status_code == 200 for response in [income_statement_response, balance_sheet_response, cash_flow_response]):
            # Extract required data from income statement response
            income_data = income_statement_response.json()
            fiscal_year = income_data['annualReports'][0]['fiscalDateEnding']
            total_revenues = int(income_data['annualReports'][0]['totalRevenue'])
            cost_of_sales = int(income_data['annualReports'][0]['costOfRevenue'])
            gross_profit = int(income_data['annualReports'][0]['grossProfit'])
            operating_expenses = int(income_data['annualReports'][0]['operatingExpenses'])
            s_g_a = int(income_data['annualReports'][0]['sellingGeneralAndAdministrative'])
            net_income = int(income_data['annualReports'][0]['netIncome'])
            ebitda = int(income_data['annualReports'][0]['ebitda'])
            income_before_tax = int(income_data['annualReports'][0]['incomeBeforeTax'])
            income_tax_expense = int(income_data['annualReports'][0]['incomeTaxExpense'])
            tax_rate = income_tax_expense / income_before_tax

            # Extract required data from balance sheet response
            balance_data = balance_sheet_response.json()
            total_assets = int(balance_data['annualReports'][0]['totalAssets'])
            current_assets = int(balance_data['annualReports'][0]['totalCurrentAssets'])
            cash = int(balance_data['annualReports'][0]['cashAndCashEquivalentsAtCarryingValue'])
            prop_plant_equip = int(balance_data['annualReports'][0]['propertyPlantEquipment'])
            total_liabilities = int(balance_data['annualReports'][0]['totalLiabilities'])
            current_liabilities = int(balance_data['annualReports'][0]['totalCurrentLiabilities'])
            total_debt = int(balance_data['annualReports'][0]['shortLongTermDebtTotal'])
            total_equity = int(balance_data['annualReports'][0]['totalShareholderEquity'])
            retained_earnings = int(balance_data['annualReports'][0]['retainedEarnings'])

            # Extract required data from cash flow statement response
            cash_flow_data = cash_flow_response.json()
            operating_cash_flow = int(cash_flow_data['annualReports'][0]['operatingCashflow'])
            investing_cash_flow = int(cash_flow_data['annualReports'][0]['cashflowFromInvestment'])
            financing_cash_flow = int(cash_flow_data['annualReports'][0]['cashflowFromFinancing'])
            capex = cash_flow_data['annualReports'][0]['capitalExpenditures']
            if capex == 'None':
                capex = 0
            else:
                capex = int(capex)

            dividend_payout = cash_flow_data['annualReports'][0]['dividendPayout']
            if dividend_payout == 'None':
                dividend_payout = 0
            else:
                dividend_payout = int(dividend_payout)

            # Calculate ratios
            gross_profit_margin = gross_profit / total_revenues
            ebitda_margin = ebitda / total_revenues
            net_profit_margin = net_income / total_revenues
            current_ratio = current_assets / current_liabilities
            debt_to_equity_ratio = total_liabilities / total_equity
            return_on_equity = total_equity / total_revenues
            capex_income_ratio = capex / net_income
            dividend_income_ratio = dividend_payout / net_income

            # Prepare the data for tabulation
            headers = ['Metric', 'Value']
            data = [
                ['Stock Ticker', ticker_symbol],
                ['Exchange:', exchange_platform],
                ['Company Name:', company_name],
                ['Description:', company_description],
                ['Industry:', company_industry],
                ['Sector:', company_sector],
                ['Market Cap:', format(company_market_cap, ',')],
                ['EV/EBITDA:', ev_to_ebitda],
                ['Fiscal Year Ending', fiscal_year],
                ['', ''],
                ['Income Statement Data', ''],
                ['Total Revenues', format(total_revenues, ',')],
                ['Cost of Sales', format(cost_of_sales, ',')],
                ['Gross Profit', format(gross_profit, ',')],
                ['Operating Expenses', format(operating_expenses, ',')],
                ['SG&A', format(s_g_a, ',')],
                ['EBITDA', format(ebitda, ',')],
                ['Net Income', format(net_income, ',')],
                ['Prevailing Tax Rate (Income Tax Expense/EBT)', format(tax_rate, '.0%')],
                ['', ''],
                ['Balance Sheet Data', ''],
                ['Total Assets', format(total_assets, ',')],
                ['Current Assets', format(current_assets, ',')],
                ['Total Cash and Cash Equivalents (excluding Marketable Securities)', format(cash, ',')],
                ['PP&E', format(prop_plant_equip, ',')],
                ['Total Liabilities', format(total_liabilities, ',')],
                ['Current Liabilities', format(current_liabilities, ',')],
                ['Total Debt (short + long term debt)', format(total_debt, ',')],
                ['Total Equity', format(total_equity, ',')],
                ['Retained Earnings', format(retained_earnings, ',')],
                ['', ''],
                ['Cash Flow Statement Data', ''],
                ['Operating Cash Flow', format(operating_cash_flow, ',')],
                ['Investing Cash Flow', format(investing_cash_flow, ',')],
                ['Financing Cash Flow', format(financing_cash_flow, ',')],
                ['CapEx', format(capex, ',')],
                ['Dividend Payout', format(dividend_payout, ',')],
                ['', ''],
                ['Ratios', ''],
                ['Gross Profit Margin', format(gross_profit_margin, '.0%')],
                ['EBITDA Margin', format(ebitda_margin, '.0%')],
                ['Net Profit Margin', format(net_profit_margin, '.0%')],
                ['Current Ratio', format(current_ratio, '.2f')],
                ['Debt to Equity Ratio', format(debt_to_equity_ratio, '.2f')],
                ['Return on Equity', format(return_on_equity, '.0%')],
                ['CapEx to Net Income Ratio', format(capex_income_ratio, '.2f')],
                ['Dividend Payout to Net Income Ratio', format(dividend_income_ratio, '.2f')]
            ]

            # Print the tabulated data
            print(tabulate(data, headers, tablefmt='plain'))
        else:
            print("Error: Failed to fetch financial data.")
    except KeyError:
        print("Error: Financial data not available for the given ticker symbol.")
    except requests.exceptions.RequestException:
        print("Error: Failed to connect to the API. Please check your internet connection.")

# Prompt the user for a ticker symbol and call the function
ticker_symbol = input("Enter the ticker symbol of a publicly listed company: ").upper()
get_company_data(ticker_symbol)
