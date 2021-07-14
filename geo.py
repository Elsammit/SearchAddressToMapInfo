# -*- coding: utf-8 -*-

import csv
import sys
import urllib.parse # pip3 install urllib3
import json         # https://note.com/masato1230/n/nba86746179ca
import requests     # pip3 install requests
import time
import os
import sqlite3

def main():
    args = sys.argv     # 実行時の引数取得
    if len(args) < 2:   # 実行時にcsvファイルを指定していなかった場合はエラーとする
        print("[Error] csvファイルを引数に与えてください")
        return

    if os.path.exists(args[1]) == False:        # 指定したファイルが存在しない場合にはエラーとする
        print("[Error] 指定したファイルがみつかりませんでした")
        return        

    fileName = os.path.splitext(args[1])        # 指定したファイルがcsvファイルでなければエラーとする
    if fileName[1] != ".csv":
        print("拡張子はcsvファイルにしてください")
        return

    i = 0               # ヘッダーとbody切り替え用
    AddressNum = -1     # 住所 or Addressが書かれた番号
    MapLists = []       # csvから読み出しかつ緯度・経度を追加する用変数

    # 国土地理院URL
    # APIの使用方法等は下記を参考のこと
    # https://libraries.io/github/gsi-cyberjapan/internal-search
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="    
    with open(args[1],encoding='utf-8') as f:   # 引数に与えたcsvファイル読み込み
        reader = csv.reader(f)
        for line in reader:                     # 各行読み取り
            buf = []
            if i == 0:                          # ヘッダーの場合
                j = 0                           # 列番号カウント用変数
                for item in line:               # 列読み取り
                    if item == "住所" or item == "Address" or item == "address":
                        AddressNum = j          # 住所を見つけたらその時の番号を変数に格納
                    j+=1                        # 列番号カウンタをインクリメント
                    buf.append(item)            # 取得した列をbufに格納
                if AddressNum < 0:              # 住所やアドレスがなかったらエラーとして修了
                    print("[Error] 住所もしくはAddressが項目にありません")
                    return

                buf.append("latitude")          # ヘッダーの列にlatitudeを追加
                buf.append("longitude")         # ヘッダーの列にlongitudeを追加
                MapLists.append(buf)            # ヘッダー行をMapListsに格納
            else:                               # body側の各行情報
                for item in line:               # 各行ごとのカラムを取得
                    buf.append(item)            # 取得したカラムを変数に格納
                print(line[AddressNum])
                s_quote = urllib.parse.quote(line[AddressNum])          # 住所の文字列をURLエンコード
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
                MapLists.append(buf)            # 各行ごとの情報をMapListsに格納                                    
                time.sleep(1)                   # 国土地理院APIに負荷を掛けないように
            i+=1

    with open("output.csv", mode='w',newline='',encoding='shift_jis') as f: # データをcsvファイルへ格納
        writer = csv.writer(f)
        for maplist in MapLists:                # 各行の情報を格納した変数を読み出す
            writer.writerow(maplist)            # 読み出したデータをcsvへ書き込み
    print("Write Finish !!")
            
if __name__ == "__main__":
    print("start")
    print("=========================================")
    main()
    print("=========================================")
    print("end")