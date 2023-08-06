import os.path
import time
from random import randint
import requests
import ybc_config

__PREFIX = ybc_config.config['prefix']
__PIC_SEARCH_URL = __PREFIX + ybc_config.uri + '/picSearch'


def pic_search(keyword='', total=10):
    """
    搜索图片并下载。

    参数 keyword: 搜索关键词。
    参数 total: 本次下载图片数量，最大为 30。
    返回: 无。
    """
    if keyword == '':
        return -1

    url = __PIC_SEARCH_URL
    data = {
        'keyWord': keyword,
        'total': total
    }
    headers = {'content-type': "application/json"}

    for i in range(3):
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            pic_url = r.json()
            break
        elif i == 2:
            print('搜索不到相关图片哦~')
            return -1

    url_count = len(pic_url)
    if url_count < 1:
        return -1
    if total >= url_count:
        total = url_count

    print('找到关键词为: ' + keyword + ' 的图片，现在开始下载图片...')
    count = 0
    for key in pic_url:
        if count == total:
            break
        print('正在下载第' + str(count + 1) + '张图片，图片地址:' + str(key))
        try:
            pic = requests.get(key, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue

        dir_path = keyword
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        tag = time.strftime('%H%M%S', time.localtime(time.time())) + '.' + str(randint(1000, 9999))
        filename = dir_path + '/' + keyword + '_' + str(count) + '_' + tag + '.jpg'
        fp = open(filename, 'wb')
        fp.write(pic.content)
        fp.close()
        count += 1
    print('下载完成！')
    return 0


def main():
    pic_search('彭于晏')


if __name__ == '__main__':
    main()