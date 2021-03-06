import re
import sys
sys.path.append("lib/")
from myio import read_excel, save
from bs4 import BeautifulSoup
from wb import get_web_page
from progress_bar import progress, showProgess

DETAIL_URL = "https://rent.591.com.tw/"
urlJumpIp = 1

def get_house_box(dom, post_id):
    house_boxes = []
    my_list = ["post_id", "房屋資料", "生活機能", "附近交通"]
    my_dict = {}.fromkeys(my_list)
    my_dict["post_id"] = post_id

    try:
        #獲取資訊
        soup = BeautifulSoup(dom, "html.parser")
        house_li = soup.find_all("li", "clearfix") #房屋資訊
        life_p = soup.find("div", "lifeBox").find_all("p") #生活交通

        #解析資訊
        str1 = ""
        for li in house_li: #房屋資料
            key = li.find("div", "one").get_text()
            value = li.find("div", "two").get_text()
            str1 += key + value + ","
        my_dict["房屋資料"] = str1

        for p in life_p: #生活機能
            text = p.get_text().strip()
            key = text.split("：")[0]
            value = text.split("：")[1].replace("；", ",")
            my_dict[key] = value

        #回傳資料
        house_boxes.append(my_dict)
        return house_boxes
    except:
        print("post_id " + str(post_id) + ": webpage is no longer exist")
        house_boxes.append(my_dict)
        return house_boxes

def HOUSE_BOX_TPE_INIT():
    row_data = read_excel("lease/data/TPE/info/total_rows_TPE.xlsx") # get the excel info

    house_boxes = []
    for data in row_data:
        page = get_web_page(DETAIL_URL + data["url"], urlJumpIp)
        house_boxes += get_house_box(page, data["post_id"])
        showProgess(__file__)

    save(house_boxes, "lease/data/TPE/info/house_box_TPE")
    print(str(__file__) + " complete")
