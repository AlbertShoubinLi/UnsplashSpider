import requests #导入requests 模块
from bs4 import BeautifulSoup  #导入BeautifulSoup 模块
import os  #导入os模块

class BeautifulPicture():

    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://unsplash.com'  #要访问的网页地址
        self.folder_path = 'D:\BeautifulPicture'  #设置图片要存放的文件目录

    def get_pic(self):
        print('开始网页get请求')
        r = self.request(self.web_url)
        print('开始获取所有a标签')
        all_a = BeautifulSoup(r.text, 'lxml').find_all('a', class_='cV68d')  #获取网页中的class为cV68d的所有a标签
        print('开始创建文件夹')
        self.mkdir(self.folder_path)  #创建文件夹
        print('开始切换文件夹')
        os.chdir(self.folder_path)   #切换路径至上面创建的文件夹

        for a in all_a: #循环每个标签，获取标签中图片的url并且进行网络请求，最后保存图片
            img_str = a['style'] #a标签中完整的style字符串
            print('a标签的style内容是：', img_str)
            first_pos = img_str.index('"') + 1
            second_pos = img_str.index('"',first_pos)
            img_url = img_str[first_pos: second_pos] #使用Python的切片功能截取双引号之间的内容
            #获取高度和宽度的字符在字符串中的位置
            width_pos = img_url.index('&w=')
            height_pos = img_url.index('&q=')
            width_height_str = img_url[width_pos : height_pos] #使用切片功能截取高度和宽度参数，后面用来将该参数替换掉
            print('高度和宽度数据字符串是：', width_height_str)
            img_url_final = img_url.replace(width_height_str, '')  #把高度和宽度的字符串替换成空字符
            print('截取后的图片的url是：', img_url_final)
            #截取url中参数前面、网址后面的字符串为图片名
            name_start_pos = img_url.index('photo')
            name_end_pos = img_url.index('?')
            img_name = img_url[name_start_pos : name_end_pos]
            self.save_img(img_url_final, img_name) #调用save_img方法来保存图片

    def save_img(self, url, name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        file_name = name + '.jpg'
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
        r = requests.get(url, headers=self.headers)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

beauty = BeautifulPicture()  #创建类的实例
beauty.get_pic()  #执行类中的方法
