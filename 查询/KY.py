import requests
from aip import AipOcr
from bs4 import BeautifulSoup

def get_yzm(file_path):  # 处理验证码
    '''
    利用百度的识图API对简单验证码进行识别
    '''

    APP_ID = '10791852'
    API_KEY = 'xK9mmVIQNTHPURfd44DKpzBP'
    SECRET_KEY = 'U4i12gvyPXU76dpZhal9e9jzFMmKffv5'

    # 初始化AipFace对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 定义参数变量
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
    }
    with open(file_path, 'rb') as fp:
        image = fp.read()
    return client.basicGeneral(image, options)

def get_data():
    '''
    获取数据
    '''
    try:
        s = requests.Session()
        headers = {
            'Host': 'www.xjedu.gov.cn',
            'Content-Length': '99',
            'Origin': 'http://www.xjedu.gov.cn',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Referer': 'http://www.xjedu.gov.cn/webpub/bpf/cjcx/search.jsp?sea_id=11190'
        }
        yzm_url = 'http://www.xjedu.gov.cn/CheckCode.do'
        with open('yzm.png', 'wb+') as png:
            png.write(s.get(yzm_url).content)
        result = get_yzm("yzm.png")
        yzm = result['words_result'][0]['words']
        url = 'http://www.xjedu.gov.cn/webpub/bpf/cjcx/search.jsp?sea_id=11190'
        params = {
            'act': 'submit',
            'A': ID,
            'randomCode': yzm,
            'submit': '查　询',
            'commond': 'search'
        }

        html = s.post(url, data=params, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        con = soup.findAll('td', attrs={'bgcolor': '#FFFFFF'})
        for i in con:
            data = i.findAll("td", attrs={'bgcolor': '#FFFFFF'})
            for ii in data:
                print(ii.getText().strip())
    except:
        print('抱歉没有找到与检索条件相符的信息，请检查您输入的准考证号码是否正确!')

if __name__ == '__main__':
    ID = input('请输入准考证号: ')
    get_data()
