import requests
from bs4 import BeautifulSoup
import json, os, re

from Model.item import Item
class Crawler:

    def __init__(self, url, exportFileName="./export.json"):
        self.url = url
        self.exportFileName = exportFileName
        self.CollectedData = []

        self.mainRequestsHeader = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "class.ruten.com.tw",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
    
    def exec(self, pages=3):

        for pageIndex in range(pages):
        
            r = requests.get(self.url.format(pageIndex+1), headers=self.mainRequestsHeader)
            r.encoding = "utf-8"
            page = BeautifulSoup(r.text, "html.parser")
            mainBlock = page.find("div", {"class":"rt-store-goods-listing-main"})

            for item in mainBlock.findAll("div", {"class":"rt-store-goods-disp-mix"}):

                _item_url = item.find("img", {"class":"rt-product-image"})["src"]
                raw_price = item.find("div", {"class":"item-price"}).findAll("p")[0].text.strip()
                _item_price = re.findall("\d+", raw_price)[0]
                _item_title = item.find("h3", "item-name").text.strip()
                
                self.CollectedData.append(
                    # 這邊改 dict 是為了方便輸出用
                    {
                        "imgUrl":_item_url,
                        "title":_item_title,
                        "fee":_item_price
                    }
                    # Item(
                    #     imgUrl=_item_url,
                    #     title=_item_title,
                    #     fee=_item_price
                    # )
                )


        # 最後輸出
        self.export()
        

    def export(self):
        if os.path.exists(self.exportFileName):
            with open(self.exportFileName, "w", encoding="utf-8") as f:
                json.dump(self.CollectedData, f, ensure_ascii=False)
        else:
            with open(self.exportFileName, "a+", encoding="utf-8") as f:
                json.dump(self.CollectedData, f, ensure_ascii=False)
