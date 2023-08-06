import base64
import requests
import ybc_config
from io import BytesIO
from PIL import Image

__FONT = 'NotoSansCJK-Bold.ttc'
__PREFIX = ybc_config.config['prefix']
__CUT_URL = __PREFIX + ybc_config.uri + '/jieba'
__WC_URL = __PREFIX + ybc_config.uri + '/wordCloud'


def cut(text):
    """
    返回分词之后的列表
    :param text: 用于进行分词的文本
    :return:
        success: list划分的分词后文本
        failed: -1 包括传入空串的情况
    """
    if text:
        data = {'text': text}
        url = __CUT_URL

        for i in range(3):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                res = r.text.split('/')
                return res
        print("程序运行遇到错误，请检查参数无误后重试")
        return -1
    else:
        print("文本分析遇到错误，请检查你的文本文件")
        return -1


def cut2str(text):
    """
    返回切分之后的字符串
    :param text: 用于进行分词的文本
    :return:
        success: string，分词使用空格划分
        failed: -1 包括传入空串的情况
    """
    if text:
        res = cut(text)
        return ' '.join(res)
    else:
        print("文本分析遇到错误，请检查你的文本文件")
        return -1


def wordcloud(text, bgfile='', bgcolor='white'):
    """
    生成词云，返回词云图片对象
    :param text: 用与进行分词的文本，要求之前使用 cut 或者 cut2str 预处理
    :param bgfile: 指定词云图片的mask模板
    :param bgcolor: 指定词云图片的背景颜色
    :return:
        success: PIL.image 类型的图片对象
        failed: -1 包括传入空串的情况
    """
    if text == '':
        print("文本分析遇到错误，请检查你的文本文件")
        return -1
    if isinstance(text, list):
        text = ' '.join(text)

    font = __FONT

    if bgfile:
        try:
            with open(bgfile, 'rb') as f:
                bg_mask = base64.b64encode(f.read())
        except:
            print("图片生成遇到错误，请检查你的图片文件")
            return -1
    else:
        bg_mask = 'None'

    data = {
        'text': text,
        'font': font,
        'file': bg_mask,
        'color': bgcolor
    }
    url = __WC_URL

    for i in range(3):
        r = requests.post(url, data=data)
        if r.status_code == 200:
            if r.text != '':
                base64_data = bytes(r.text, encoding="utf8")
                byte_data = base64.urlsafe_b64decode(base64_data)
                img = Image.open(BytesIO(byte_data))
                return img
            else:
                print("程序运行遇到错误，请检查参数无误后重试")
                return -1
    print("程序运行遇到错误，请检查参数无误后重试")
    return -1


def main():
    f = open('text.txt', 'r', encoding='utf-8')
    text = f.read()
    f.close()

    print(cut(text))
    print(cut2str(text))
    print(cut(""))
    print(cut2str(""))

    wordcloud(cut(text), bgfile='test.jpg').show()
    wordcloud(cut(text)).show()


if __name__ == '__main__':
    main()
