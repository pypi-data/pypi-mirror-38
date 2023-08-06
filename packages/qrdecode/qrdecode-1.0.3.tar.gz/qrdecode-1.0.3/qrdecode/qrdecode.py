import ybc_config
import requests
import os


__PREFIX = ybc_config.config['prefix']
__QRDECODE_URL = __PREFIX + ybc_config.uri + '/qrcode'


def decode(filename=''):
    """
    识别二维码
    :param filename: 待识别的图片
    :return: 识别结果信息
    """
    url = __QRDECODE_URL
    filepath = os.path.abspath(filename)
    files = {}
    with open(filepath, 'rb') as fp:
        files['file'] = fp.read()

    for i in range(3):
        r = requests.post(url, files=files)
        if r.status_code == 200:
            return r.text
        else:
            return '没有识别出二维码'


def main():
    print(decode('test1.jpg'))
    print(decode('test2.jpg'))


if __name__ == '__main__':
    main()
