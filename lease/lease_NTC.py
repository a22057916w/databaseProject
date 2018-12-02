import sys
sys.path.append("script/")
from bs4 import BeautifulSoup
from wb import get_web_page
import os
import re
import json
import pandas as pd

LEASE_URL = "https://business.591.com.tw/home/search/rsList?is_new_list=1&storeType=1&type=1&kind=5&searchtype=1&region=3"
pageRow = 30
urlJumpIp = 3

def get_info(page):
    dict1 = json.loads(page) # page is a dict of dict of list of dict

    data = dict1["data"]["data"]
    lease_data_info = []

    for d in data:
        lease_data_info.append({
            "post_id": d["post_id"],
            "price": int(d["price"].replace(",", "")),
            "area": d["area"],
            "url": "rent-detail-" + str(d["post_id"]) + ".html",
            "addr": d["region_name"] + d["section_name"] + d["street_name"]
                + d["alley_name"] + d["lane_name"] + d["addr_number_name"]
        })

    return lease_data_info

def get_total_rows(page):
    str_total = json.loads(page)["records"]
    int_total = int(str_total.replace(",", ""))

    return int_total

def save(row_data):
    os.makedirs("lease/data", exist_ok=True)

    df = pd.DataFrame.from_dict(row_data)
    writer = pd.ExcelWriter('lease/data/total_rows_NTC.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='lease_total_rows_data')
    writer.save()

    with open('lease/data/total_rows_NTC.json', 'w', encoding='utf-8') as f:
        json.dump(row_data, f, indent=2, sort_keys=True, ensure_ascii=False)

if __name__ == "__main__":
    current_page = get_web_page(LEASE_URL, urlJumpIp) # return a dict of dict of list of dict
    total_rows = get_total_rows(current_page)

    page_count = 0
    row_data = []

    while page_count <= total_rows:
        data = get_info(current_page)
        row_data += data
        page_count += pageRow
        current_page = get_web_page(LEASE_URL + "&firstRow=" + str(page_count) + "&totalRows=" + str(total_rows), urlJumpIp)

    save(row_data)
