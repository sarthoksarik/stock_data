from requests_html import HTMLSession, user_agent
import json
import csv

import concurrent.futures

chrome_header = {"User-Agent": user_agent()}
DEFAULT_PARAMS = {
    "lang": "en-US",
    "corsDomain": "finance.yahoo.com",
    ".tsrc": "finance",
}
url = "https://query1.finance.yahoo.com/v7/finance/quote"
session = HTMLSession()

# tickers or symbols
# symbols = ["NFLX"]


# params = {"symbols": symbols[0]}
# params.update(DEFAULT_PARAMS)

# # session
# session = HTMLSession()
# response = session.get(url, headers=chrome_header, params=params)

# resp["quoteResponse"]["result"][0]["marketCap"] is the market capital
# resp["quoteResponse"]["result"][0]["symbol"] is the symbor or ticker
input_file = "all_tickers.csv"
sym_list = []
with open(input_file) as inputcsv:
    symreader = csv.reader(inputcsv)
    for row in symreader:
        sym_list.append(row[0])

sym_cap_list = []
for sym in sym_list:
    symbols = sym
    params = {"symbols": symbols}
    params.update(DEFAULT_PARAMS)
    response = session.get(url, headers=chrome_header, params=params)
    resp = json.loads(response.text)
    try:
        c1 = resp["quoteResponse"]["result"][0]["marketCap"]
        c2 = resp["quoteResponse"]["result"][0]["symbol"]
    except KeyError:
        c1 = ""
        c2 = symbols
    sym_cap_list.append([c2, c1])
