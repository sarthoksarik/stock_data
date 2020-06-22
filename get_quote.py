from requests_html import HTMLSession, user_agent
import json
import csv

chrome_header = {"User-Agent": user_agent()}
DEFAULT_PARAMS = {
    "lang": "en-US",
    "corsDomain": "finance.yahoo.com",
    ".tsrc": "finance",
}
url = "https://query1.finance.yahoo.com/v7/finance/quote"

# tickers or symbols
symbols = ["HWM.P"]


params = {"symbols": symbols[0]}
params.update(DEFAULT_PARAMS)

# session
session = HTMLSession()
response = session.get(url, headers=chrome_header, params=params)


resp = json.loads(response.text)
# resp["quoteResponse"]["result"][0]["marketCap"] is the market capital
print(resp["quoteResponse"]["result"][0]["symbol"])
