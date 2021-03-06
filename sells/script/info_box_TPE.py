import re
import sys
sys.path.append("lib/")
from myio import read_excel, save
from bs4 import BeautifulSoup
from wb import get_web_page
from progress_bar import progress, showProgess

DETAIL_URL = "https://sale.591.com.tw/home/house/detail/2/"
urlJumpIp = 1


def get_info_box(dom, post_id):
    info_boxes = []

    soup = BeautifulSoup(dom, "html.parser")
    info_box = soup.find("div", "info-box")

    # ********************** floor data ***********************
    floor_attr = ["樓層", "屋齡", "權狀坪數"]
    floor_data = [None] * 3

    try:
        keys = info_box.find_all("div", "info-floor-key")
        values = info_box.find_all("div", "info-floor-value")

        counts = 0
        while counts < len(values):
            for i in range(3):
                regex = r"(.*)" + re.escape(str(floor_attr[i])) + r"(.*)" #regular expression string
                if re.match(regex, values[counts].string):
                    floor_data[i] = keys[counts].get_text()
                    break
            counts += 1
    except:
        pass
    # ********************* addr data ***************************
    addr_attr = ["型態", "社區", "地址"]
    addr_data = [None] * 3

    try:
        keys = info_box.find_all("span", "info-addr-key")
        values = info_box.find_all("span", "info-addr-value")

        counts = 0
        while counts < len(values):
            for i in range(3):
                regex = r"(.*)" + re.escape(str(addr_attr[i])) + r"(.*)"
                if re.match(regex, keys[counts].string): #key and values are oppsite to floor's data
                    addr_data[i] = values[counts].get_text()
                    break
            counts += 1
    except:
        pass
    # return info and get price
    # handle unexpected string of numbers
    regex = re.escape(soup.find("span", "info-price-num").get_text())
    match = re.findall(r"[0-9]", regex)
    price = int("".join(map(str, match)))

    #handling unexpected string of area to eval
    match = re.findall(r"[0-9]+\.*[0-9]*", floor_data[2])
    area = eval("".join(map(str, match)))

    info_boxes.append({
        "post_id": post_id,
        "price": price,
        "floor": floor_data[0],
        "age": floor_data[1],
        "area": area,
        "form": addr_data[0],
        "community": addr_data[1],
        "addr": addr_data[2]
    })
    return info_boxes

def INFO_BOX_TPE_INIT():
    row_data = read_excel("sells/data/TPE/info/total_rows_TPE.xlsx") # get the excel info

    info_boxes = []
    for data in row_data:
        page = get_web_page(DETAIL_URL + data["url"], urlJumpIp)
        info_boxes += get_info_box(page, data["post_id"])
        showProgess(__file__)

    save(info_boxes, "sells/data/TPE/info/info_box_TPE")
    print(str(__file__) + " complete")
