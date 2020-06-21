import concurrent.futures
import requests
from requests_html import HTMLSession, user_agent
from bs4 import BeautifulSoup as bs
import lxml
import csv
import string


letters = list(string.ascii_uppercase)
# "http://www.eoddata.com/stocklist/NASDAQ/A.htm"
# "http://www.eoddata.com/stocklist/NYSE/A.htm"
groups = ["NYSE", "AMEX", "NASDAQ"]

chrome_header = {"User-Agent": user_agent()}
# print(chrome_header)
for group in groups:

    group_name = group
    main_url = "http://www.eoddata.com/stocklist/" + group_name + "/"

    def scrape_main(url_chunk):

        url_full = main_url + url_chunk + ".htm"

        print("Starting " + url_full)

        session = HTMLSession()

        sr = session.get(url_full, headers=chrome_header)
        # selector for table
        sel_table = "#ctl00_cph1_divSymbols > table"

        # content of the table
        t_body = sr.html.find(sel_table)[0]

        # all the rows as list
        # first row is the header we are ignoring that for a while
        #t_rows = t_body.find('tr')[1:]

        soup_table = bs(t_body.html, "lxml")

        t_rows = soup_table.find_all("tr")[1:]

        with open(group_name + "_all_ticker_list.csv", "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",")

            for row in t_rows:
                csv_row = []
                tds = row.find_all("td")
                data1 = tds[0].a.text
                csv_row.append(data1)
                data2_6 = [td.text for td in tds[1:6]]
                csv_row.extend(data2_6)
                csv_writer.writerow(csv_row)

        print("Completed: " + url_full)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_main, letters)

# scrape_main()


# print(t_body[0].text)
# with open("fpage.txt", "w") as sfile:
#     # sfile.write(t_body.html)
#     sfile.write(t_body[0].html)


# s#ctl00_cph1_divSymbols > table
# #ctl00_cph1_divSymbols > table > tbody
# #ctl00_cph1_divSymbols > table
