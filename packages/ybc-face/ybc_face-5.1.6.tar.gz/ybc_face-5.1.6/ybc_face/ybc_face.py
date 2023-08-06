import base64
import os
import tempfile
import requests
import time
from PIL import Image

import ybc_config

__BASIC_URL = ybc_config.config['prefix'] + ybc_config.uri
__FACE_URL = __BASIC_URL + '/faceDetect'
__MERGE_URL = __BASIC_URL + "/faceMerge/base64"

__MAX_SIZE = 512000
__MODE = 1


def _resize_img(file_path, temp_file=None, max_size=__MAX_SIZE):
    """
    对图片进行缩放, 如果是临时图片文件, 则必须传文件对象,
    因为在 windows 系统下 NamedTemporaryFile 不能二次打开, 但是可以直接读写

    :param file_path: 原文件路径
    :param temp_file: 临时文件对象
    :param max_size:
    :return:
        如果传入临时文件对象, 返回临时文件路径, 否则返回原文件路径
    """
    im = Image.open(file_path)
    src_w = im.size[0]
    src_h = im.size[1]
    dst_w = 500
    dst_h = (src_h / src_w) * 500
    dst_size = dst_w, dst_h

    im.thumbnail(dst_size)
    if temp_file:
        im.save(temp_file)
        temp_file.seek(0)
        return temp_file.name
    else:
        im.save(file_path)
        return file_path


def _get_info(filename='', mode=__MODE):
    """
    功能: 对图片进行人脸检测

    :param filename: 图片名
    :param mode: 检测模式: 0 - 正常模式; 1 - 大脸模式
    :return:
        成功: 返回包含人脸信息的字典
        失败: -1
    """
    if not filename:
        return -1

    if not os.path.exists(filename):
        return -1

    url = __FACE_URL
    file_path = os.path.abspath(filename)
    basename, suffix = os.path.splitext(filename)
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    _resize_img(file_path, temp_file)

    data = {
        'mode': mode
    }
    files = {
        'file': temp_file
    }

    for i in range(3):
        r = requests.post(url, data=data, files=files)

        if r.status_code == 200:
            res = r.json()
            if res['code'] == 0 and res['data']:
                res = res['data']['face'][0]
                res_dict = {
                    'age': res['age'],
                    'gender': res['gender'],
                    'beauty': res['beauty'],
                    'glass': res['glass']
                }
                temp_file.close()
                return res_dict

    temp_file.close()
    return -1


def gender1(filename=''):
    """
    功能：识别人脸图片的性别信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别信息[0(女性)~100(男性)]。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['gender']


def gender(filename=''):
    """
    功能：识别人脸图片的性别。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的性别。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return '男' if res['gender'] > 90 else '女'


def age(filename=''):
    """
    功能：识别人脸图片的年龄信息。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的年龄信息[0~100]。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['age']


def glass1(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜 [true,false]。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return bool(res['glass'])


def glass(filename=''):
    """
    功能：识别人脸图片的是否戴眼镜。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的是否戴眼镜。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['glass']


def beauty(filename=''):
    """
    功能：识别人脸图片的魅力值。

    参数 filename 是待识别的人脸图片，

    返回：图片中人脸的魅力值 [0~100]。
    """
    if not filename:
        return -1
    res = _get_info(filename)
    if res == -1:
        return '图片中找不到人哦~'
    return res['beauty']


def info(filename='', mode=__MODE):
    """
    功能：识别图片中一张人脸信息。

    参数 filename 是待识别的人脸图片，

    可选参数 mode 是识别模式，1 代表最大人脸，0 代表所有人脸，默认为 1

    返回：识别出的人脸信息。
    """
    if not filename:
        return '图片中找不到人哦~'

    res = _get_info(filename, mode)
    if res == -1:
        return '图片中找不到人哦~'

    _gender = '男性' if res['gender'] >= 50 else '女性'
    _glass = '戴' if res['glass'] else '不戴'
    res_str = '{gender}，{age}岁左右，{glass}眼镜，颜值打分：{beauty}分'.format(
        gender=_gender, age=res['age'], glass=_glass, beauty=res['beauty'])

    return res_str


def info_all(filename='', mode=0):
    """返回图片中所有人脸信息"""
    if not filename:
        return '图片中找不到人哦~'

    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceInfo.php'
    file_path = os.path.abspath(filename)
    b64img = base64.b64encode(open(file_path, 'rb').read()).rstrip().decode('utf-8')
    data = {'b64img': b64img, 'mode': mode}
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        res = res['data']['face_list']
        res_str = '图片中总共发现{face_len}张人脸：'.format(face_len=len(res)) + os.linesep
        i = 1
        for val in res:
            _gender = '男性' if val['gender'] >= 50 else '女性'
            _glass = '戴' if val['glass'] else '不戴'
            res_str += '第{i}个人脸信息：{gender}，{age}岁左右，{glass}眼镜，颜值打分：{beauty}分'.format(
                i=i, gender=_gender, age=val['age'], glass=_glass, beauty=val['beauty'])
            res_str += os.linesep
            i += 1
        return res_str
    else:
        return '图片中找不到人哦~'


def ps(filename='', decoration=21):
    """变装"""
    if not filename:
        return -1

    if decoration < 1:
        decoration = 1
    if decoration > 22:
        decoration = 22

    file_path = os.path.abspath(filename)
    basename, suffix = os.path.splitext(filename)
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    _resize_img(file_path, temp_file)
    url = 'https://www.yuanfudao.com/tutor-ybc-course-api/faceDecoration.php'

    b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
    data = {'b64img': b64img, 'decoration': decoration}
    r = requests.post(url, data=data)
    res = r.json()
    if res['ret'] == 0 and res['data']:
        new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + os.path.splitext(filename)[1]
        with open(new_file, 'wb') as f:
            f.write(base64.b64decode(res['data']['image']))
        temp_file.close()
        return new_file
    else:
        temp_file.close()
        return -1


def mofa(filename='', model=1):
    """人脸融合"""

    if not filename:
        return -1

    file_path = os.path.abspath(filename)
    basename, suffix = os.path.splitext(filename)
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix)
    _resize_img(file_path, temp_file)
    url = __MERGE_URL

    b64img = base64.b64encode(temp_file.read()).rstrip().decode('utf-8')
    data = {'image': b64img, 'model': model}

    headers = {'content-type': "application/json"}

    for i in range(3):
        r = requests.post(url, json=data, headers=headers)
        if r.status_code == 200:
            res = r.json()
            if res['ret'] == '0' and res['img_base64']:
                new_file = os.path.splitext(filename)[0] + '_' + str(int(time.time())) + '_ronghe' + '.png'
                with open(new_file, 'wb') as f:
                    f.write(base64.b64decode(res['img_base64']))
                temp_file.close()
                return _resize_img(new_file)

    temp_file.close()
    return '图片中找不到人哦~'


def main():
    # pass
    # import ybc_box as box
    print(_get_info('test.jpg'))
    print(info('rgba.png'))
    print(mofa('test.jpg'))
    ps('test.jpg')
    # filename = camera()
    # res = age(filename)
    # print(res)
    # res = gender(filename)
    # print(res)
    # res = glass(filename)
    # print(res)
    # res = beauty(filename)
    # print(res)
    # res = info('2.jpg')
    # print(res)
    # res = info_all('3.jpg')
    # print(res)
    # res = age('5.jpg')
    # print(res)
    # res = gender('5.jpg')
    # print(res)
    # res = glass('5.jpg')
    # print(res)
    # res = beauty('5.jpg')
    # print(res)


if __name__ == '__main__':
    main()
