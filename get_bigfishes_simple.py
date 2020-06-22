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
output_file = "sym_marketcap_sim.csv"
sym_list = []
err_json = {}
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
    except (KeyError, IndexError):
        c1 = ""
        c2 = symbols
        err_json.update({sym: resp})
    sym_cap_list.append([c2, c1])
    with open(output_file, "w", newline="") as of:
        ofwriter = csv.writer(of)
        ofwriter.writerows(sym_cap_list)
with open("err.json", "a") as ef:
    ef.write(json.dumps(err_json))
