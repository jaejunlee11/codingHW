import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client=MongoClient('localhost',27017)
db=client.dbsparta
headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
data=requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713',headers=headers)

soup=BeautifulSoup(data.text, 'html.parser')
trs=soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr')
for tr in trs :
    rank_tag=tr.select_one('td.number')
    if rank_tag is None:
        continue
    rank=rank_tag.text[0:2].strip()

    title_tag=tr.select_one('td.info > a')
    if title_tag is None:
        continue
    title=title_tag.text.strip()

    singer_tag=tr.select_one('td.info > a.artist.ellipsis')
    if title_tag is None:
        continue
    singer=singer_tag.text
    song={
        'rank': rank,
        'title': title,
        'singer': singer

    }

    print(rank,title,singer)
    db.song.insert_one(song)

