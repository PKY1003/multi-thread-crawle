import random
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time


def get_html(urls):
    responses=[]
    user_agent=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0']
    for url in urls:
        headers = {'User-Agent': random.choice(user_agent),'Referer': 'https://pixai.art/zh?utm_source=google&utm_medium=cpc&utm_campaign=23598853575&utm_content=&utm_term=&device=m&network=x&loc_physical=1009300&placement=&gad_source=2&gad_campaignid=23598895896&gclid=CjwKCAjwrNrQBhBjEiwAoR4VO-NPJLA65Z_jqe4kAftiuyi2md_a3oKbOhOVZiaObf4D8r_P61JoChoC9UMQAvD_BwE'}
        try:
            request=urllib.request.Request(url=url,headers=headers)
            response=urllib.request.urlopen(request)
            responses.append(response.read())
        except Exception as err:
            print(f'请求失败: {url}, 错误: {err}')
    return responses

def submit_and_as_completed(responses,urls):
    full_urls=[]
    results=[]

    for i,response in enumerate(responses):
        soup=BeautifulSoup(response,'lxml')
        t1=soup.find_all('img')
        for item in t1:
            img=item.get('src')
            if img and 'images-ng' in img:
                if '/gi/orig/' in img:
                    full_url=urllib.parse.urljoin(urls[i],img)
                    full_urls.append(full_url)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures=[executor.submit(download,full_url,j) for j,full_url in enumerate(full_urls)]
        for future in as_completed(futures):
            result=future.result()
            print(result)
            results.append(result)

def download(url    ,j):
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0']
    headers = {'User-Agent': random.choice(user_agent),'Referer': 'https://pixai.art/zh?utm_source=google&utm_medium=cpc&utm_campaign=23598853575&utm_content=&utm_term=&device=m&network=x&loc_physical=1009300&placement=&gad_source=2&gad_campaignid=23598895896&gclid=CjwKCAjwrNrQBhBjEiwAoR4VO-NPJLA65Z_jqe4kAftiuyi2md_a3oKbOhOVZiaObf4D8r_P61JoChoC9UMQAvD_BwE'}
    save_path=r'S:\python项目\爬虫多线程\image\pixai\\'+str(j)+'.jpg'
    try:
        time.sleep(random.choice(range(2, 6)))
        imgdata=requests.get(url,headers=headers).content
        with open(save_path,'wb') as f:
            f.write(imgdata)
        print(f'第{j}个任务完成')
        return {'state':'成功','url':url,'save_path':save_path,'j':j}

    except requests.Timeout:
        print(f'第{j}个任务失败')
        return {'state':'Timeout','url':url,'save_path':save_path,'j':j}
    except Exception as err:
        print(f'第{j}个任务失败')
        return {'state':'Error','url':url,'save_path':save_path,'j':j,'reason':str(err)}