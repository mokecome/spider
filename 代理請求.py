import requests


def get_proxy():
    """获取代理的函数"""
    proxy = requests.get('http://127.0.0.1:5000/get').text
    print(proxy)

    proxies = {
        "http": "http://" + proxy,
        "https": "https://" + proxy,
    }

    return proxies


proxies = get_proxy()
headers = {
    'Host': 'wreport1.meituan.net',
    'Origin': 'https://maoyan.com',
    'Referer': 'https://maoyan.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}


response = requests.get(url='https://maoyan.com/board/4?offset=0', proxies=proxies, headers=headers)
print(response.text)