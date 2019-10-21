import misaka
import os
import requests
import uuid
from bs4 import BeautifulSoup


def get_files_list(dir):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir:
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list


def get_pics_list(md_content):
    """
    获取一个markdown文档里的所有图片链接
    :param md_content:
    :return:
    """
    md_render = misaka.Markdown(misaka.HtmlRenderer())
    html = md_render(md_content)
    soup = BeautifulSoup(html, features='html.parser')
    pics_list = []
    for img in soup.find_all('img'):
        pics_list.append(img.get('src'))

    return pics_list


def download_pics(url, file):
    img_data = requests.get(url).content
    filename = os.path.basename(file)
    dirname = os.path.dirname(file)
    targer_dir = os.path.join(dirname, f'{filename}.assets')
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)

    with open(os.path.join(targer_dir, f'{uuid.uuid4().hex}.jpg'), 'w+') as f:
        f.buffer.write(img_data)


if __name__ == '__main__':
    files_list = get_files_list(os.path.abspath(os.path.join('.', 'files')))

    for file in files_list:
        print(f'正在处理：{file}')

        with open(file, encoding='utf-8') as f:
            md_content = f.read()

        pics_list = get_pics_list(md_content)
        print(f'发现图片 {len(pics_list)} 张')

        for index, pic in enumerate(pics_list):
            print(f'正在下载第 {index + 1} 张图片...')
            download_pics(pic, file)
        print(f'处理完成。')
