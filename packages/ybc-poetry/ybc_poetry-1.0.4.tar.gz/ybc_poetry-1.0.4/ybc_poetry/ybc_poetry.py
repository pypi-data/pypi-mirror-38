import requests
import ybc_config

__PREFIX = ybc_config.config['prefix']
__POETRY_URL = __PREFIX + ybc_config.uri + '/poetry'


def shici(title='春晓', author='孟浩然'):
    """
    功能：根据诗词标题和作者，搜索诗词内容。

    参数：title:诗词标题，默认为'春晓'
         author:诗词作者，默认为'孟浩然'

    返回：返回搜索到的诗词内容，若未搜索到返回提示"未搜索到这首诗词"
    """
    url = __POETRY_URL + '?title=%s&author=%s' % (title, author)

    for i in range(3):
        r = requests.get(url)
        if r.status_code == 200:
            res = r.json()
            content = ''.join(res)
            return content
        elif r.status_code == 404:
            return '未搜索到这首诗词'
    error_msg = "shici()方法调用失败，请稍后再试"
    print(error_msg)
    return error_msg


def main():
    res = shici()
    print(res)

    res = shici('早发白帝城', '李白')
    print(res)

    res = shici('声声慢', '李清照')
    print(res)

    res = shici('早发白帝城', '李')
    print(res)


if __name__ == '__main__':
    main()
