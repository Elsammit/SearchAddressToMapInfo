# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup 
import csv
import sys
import urllib.parse # pip3 install urllib3
import json         # https://note.com/masato1230/n/nba86746179ca
import requests     # pip3 install requests
import time
import os
import sqlite3
import folium

#http://www.kabu-data.info/all_code/code_tosyo1_code.htm
def ReadCodeList():
    ret = []
    i = 0
    with open("Book1.csv",encoding='utf-8') as f:   # 引数に与えたcsvファイル読み込み
        reader = csv.reader(f)
        for line in reader:                     # 各行読み取り
            buf = []
            buf.append(line[0])
            buf.append(line[1])
            ret.append(buf)
    return ret

def SearchAddress(CodeNum):
    url = "https://profile.yahoo.co.jp/fundamental/"+str(CodeNum)
    print(url)
    html = urllib.request.urlopen(url.replace("\ufeff", ""))
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('div.profile > div > div > table > tr > td > table > tr > td')
    print(items[5].text)
    Address = items[5].text
    print(Address.split())
    return Address.split()[1]

def MakeMap(Address, companyName):
    s_quote = urllib.parse.quote(Address)          # 住所の文字列をURLエンコード
    print(s_quote)
    response = response = requests.get(makeUrl + s_quote)   # エンコードした文字列を国土地理院APIの引数として与えてget request
    if response.json() == []:                               # レスポンスされたjsonデータの中身を確認し空だったら
        print("[Error] 住所がよくわかりませんでした")          # 判定できなかった旨を出力し緯度・経度は空文字を格納
        buf.append("")                                      
        buf.append("")                    
    elif len(response.json()) >1:                           # 候補が複数あった場合、判定出来ないためスキップ
        print("[Error] 住所の絞り込みが出来ず複数候補が出ました \n 住所の絞り込みをおこなってください　")
        buf.append("")                                      
        buf.append("") 
    else:                                                   # レスポンスされたjsonデータが空でなかった場合
        print(response.json()[0]["geometry"]["coordinates"]) 
        buf.append(response.json()[0]["geometry"]["coordinates"][0])    # 緯度情報をbufに格納
        buf.append(response.json()[0]["geometry"]["coordinates"][1])    # 経度情報をbufに格納

        folium.Marker(location=[response.json()[0]["geometry"]["coordinates"][1], response.json()[0]["geometry"]["coordinates"][0]], popup=companyName).add_to(map)
                    
    map.save("result.html")


locationName = ""
makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="    
map = folium.Map(location=[35.681561, 139.767197], zoom_start=8)
if __name__ == "__main__":
    buf = []
    List = ReadCodeList()
    for list in List:
        Address = SearchAddress(list[0])
        time.sleep(5)                   # 国土地理院APIに負荷を掛けないように
        MakeMap(Address,list[1])
        time.sleep(5)                   # 国土地理院APIに負荷を掛けないように

