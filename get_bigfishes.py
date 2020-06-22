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

def get_quote_data(symbol: str):
    # retrieves the json data from url
    # session is any HTMLsession object

    params = {"symbols": symbol}
    params.update(DEFAULT_PARAMS)

    response = session.get(url, headers=chrome_header, params=params)
    resp_json = json.loads(response.text)

    return (resp_json, symbol)


def main():
    # read the csv file and loop through the tickers

    with open("all_tickers.csv") as symcsv:
        symreader = csv.reader(symcsv)
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for row in symreader:
                f = executor.submit(get_quote_data, row[0])
                threads.append(f)

            with open("sym_marketcap.csv", "w", newline="") as resultcsv:
                result_writer = csv.writer(resultcsv, delimiter=",")
                for thread in threads:
                    # recieve json response from get request
                    (row_json, syminp) = thread.result()
                    try:
                        col1 = row_json["quoteResponse"]["result"][0]["symbol"]
                        col2 = row_json["quoteResponse"]["result"][0]["marketCap"]
                    except (KeyError, IndexError) as e:
                        col1 = syminp
                        col2 = e
                    finally:
                        result_writer.writerow([col1, col2])


main()
