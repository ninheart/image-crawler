import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
import html

num = 0
numPicture = 0
file = ''
List = []


def Find(url):
    global List
    print('Detecting Pictures...')
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url+'#id='+str(t)+'&iurl=https%3A%2F%2Fd3qvyul2tp4j8.cloudfront.net%2Fi%2FW314qVMbjd.png&action=click'
        try:
            Result = requests.get(Url)
        except BaseException:
            t = t + 60
            continue
        else:
            result = (Result.text)
            soup = BeautifulSoup(result, 'html.parser')
            #request = 200 succeed
            #pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url

            pic_url = soup.find_all('img')
            print(pic_url)
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


def recommend(url):
    Re = []
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re


def downloadPicture(html, keyword):
    global num
    # t =0
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('Found Keyword:' + keyword + 'Preparing to download...')
    for each in pic_url:
        print('Downloading' + str(num + 1) + 'picture, the adress is' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('error, cannot be downloaded')
            continue
        else:
            #string = file + r'\\' + keyword + '_' + str(num) + '.jpg'
            string = file + '/' + keyword + '_' + str(num) + '.jpg'
            print(file)
            print(string)
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':  # 主函数入口
    word = input("Enter a key word")
    # add = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%BC%A0%E5%A4%A9%E7%88%B1&pn=120'
    url = 'https://images.search.yahoo.com/search/images?p=' + word + '&tbm=isch'
    tot = Find(url)

    Recommend = recommend(url)  # 记录相关推荐
    print('After crawling there are %d %s' % (word, tot))
    numPicture = int(input('Enter the amount of pictures you want to download '))
    file = input('Name the folder you want to save the pictures to ')
    y = os.path.exists(file)
    if y == 1:
        print('Folder already exist, please name another one')
        file = input('Name the folder you want to save the pictures to ')
        os.mkdir(file)
    else:
        os.mkdir(file)
    t = 0
    tmp = url
    while t < numPicture:
        try:
            url = tmp
            result = requests.get(url)

            print(url)
        except error.HTTPError as e:
            print('网络错误，请调整网络后重试')
            t = t + 60
        else:
            downloadPicture(result.text, word)
            t = t + 60

    print("Finished!")
    for re in Recommend:
        print(re, end='  ')