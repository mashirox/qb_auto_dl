import time
import qbittorrentapi
import requests
from pyquery import PyQuery as pq

tv_url = "https://jpopsuki.eu/ajax.php?section=torrents&freeleech=1&tags_type=0&order_by=s3&order_way=desc&filter_cat%5B6%5D=1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

jpopsuki = requests.Session()

seed_pool = []
now_pool = []
username = ""
password = ""


def getCookie():
    jpopsuki.post("https://jpopsuki.eu/login.php", data={'username': username, 'password': password})
    cookies_dict = jpopsuki.cookies.get_dict()
    print(cookies_dict)


def checkUpdate():
    try:
        seq = jpopsuki.get(tv_url).text
        jpopsukiDoc = pq(seq)
        data = jpopsukiDoc("#torrent_table .torrent_redline").items()
        for i in data:
            pt_url = i("td:nth-child(4) > a:nth-child(3)")
            now_pool.append(pt_url.attr("href"))

        else_data = jpopsukiDoc("#torrent_table .group_torrent_redline").items()
        for i in else_data:
            pt_url = i("td:nth-child(1) > a")
            now_pool.append(pt_url.attr("href"))

        authdata = jpopsukiDoc("#torrent_table .torrent_redline td:nth-child(4) > span > a:nth-child(1)")
        url = authdata.attr("href")
        authkey = url[38:]

        for i in now_pool:
            if i not in seed_pool:
                print(i + "  NOT IN SEED POOL！！")
                seed_pool.append(i)
                qbt_client = qbittorrentapi.Client(host='127.0.0.1:8080', username='', password='')
                res = qbt_client.torrents_add(
                    urls="https://jpopsuki.eu/torrents.php?action=download&id={}".format(i[-6:]) + authkey,
                    save_path="E:/PT/",
                    cookie=jpopsuki.cookies.get_dict(),
                    is_skip_checking=False,
                    is_root_folder=True, )
    except Exception as e:
        print("遇到错误", e)
        time.sleep(300)
        getCookie()


def getTvLink():
    try:
        seq = jpopsuki.get(tv_url).text
        jpopsukiDoc = pq(seq)
        print(jpopsukiDoc)
        data = jpopsukiDoc("#torrent_table .torrent_redline").items()
        for i in data:
            pt_url = i("td:nth-child(4) > a:nth-child(3)")
            seed_pool.append(pt_url.attr("href"))

        else_data = jpopsukiDoc("#torrent_table .group_torrent_redline").items()
        for i in else_data:
            pt_url = i("td:nth-child(1) > a")
            seed_pool.append(pt_url.attr("href"))
    except Exception as e:
        print("遇到错误", e)
        time.sleep(300)
        getCookie()


def main():
    jpopsuki.headers = headers
    getCookie()
    getTvLink()
    print(seed_pool)
    while True:
        time.sleep(500)
        checkUpdate()


if __name__ == '__main__':
    main()
