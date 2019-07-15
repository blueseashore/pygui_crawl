# coding:utf-8
# author: uckendo.com

from tkinter import *
import tkinter.messagebox as mbox
import requests
from requests.exceptions import RequestException
import re
import os


class Application(Frame):
    def __init__(self, master=None):
        # 设置主窗口背景色为黑色
        Frame.__init__(self, master)
        # 设置主窗口允许展开且水平和垂直填充
        self.pack(expand=YES, fill=BOTH)
        self.title = ''
        self.website = ''
        self.video = ''
        self.window_init()
        self.widgets_init()

    def window_init(self):
        # 初始化主窗口的其他
        self.master.title('Video Collector System')
        self.master.bg = '#C4C4C4'
        width, height = self.master.maxsize()
        # width = 800
        # height = 1000
        self.master.geometry("{}x{}".format(width, height))

    def widgets_init(self):
        # LayFirst 窗口标题 顶部居中
        # 设置 LayFirst 的背景色
        lay_first = Frame(self, bg='#C4C4C4')
        # 设置 Label 的文本内容，背景色和文字颜色
        title = Label(lay_first, highlightthickness=20, text="Video Collector System", font=('微软雅黑', 64), fg="white",
                      bg='#C4C4C4', )
        title.pack()
        # 定义布局的位置，向上对齐，水平方向填充，置顶
        lay_first.pack(side=TOP, fill=X, anchor=N)

        # LaySecond
        lay_second = Frame(self, bg='#EDEDED')
        lay_second_left = Frame(lay_second, bg='#EDEDED')
        lay_second_right = Frame(lay_second, bg='#EDEDED')
        lay_second_button = Frame(lay_second, bg='#EDEDED')
        Label(lay_second_left, borderwidth=10, width=10, text='website', fg="white", bg='#C5C1AA',
              font=('微软雅黑', 28)).pack(side=LEFT)
        self.website = StringVar()
        Entry(lay_second_right, width=80, foreground='#C4C4C4', font=('微软雅黑', 28), textvariable=self.website).pack(
            side=LEFT,
            padx=10)
        # 抓取地址按钮，需绑定事件
        Button(lay_second_button, width=10, text='抓取', background='white', fg='#C5C1AA', font=('微软雅黑', 28),
               command=self.get_html).pack(side=LEFT, padx=10)
        lay_second_left.pack(side=LEFT)
        lay_second_right.pack(side=LEFT)
        lay_second_button.pack(side=LEFT)
        lay_second.pack(side=TOP, fill=X)

        # LayThird
        lay_third = Frame(self, bg='#EDEDED')
        lay_third_left = Frame(lay_third, bg='#EDEDED')
        lay_third_right = Frame(lay_third, bg='#EDEDED')
        Label(lay_third_left, borderwidth=10, width=10, text='title', fg="white", bg='#C5C1AA', font=('微软雅黑', 28)).pack(
            side=LEFT)
        self.title_entry = Entry(lay_third_right, width=80, foreground='#C4C4C4', font=('微软雅黑', 28))
        self.title_entry.pack(side=LEFT, padx=10)

        lay_third_left.pack(side=LEFT)
        lay_third_right.pack(side=LEFT)
        lay_third.pack(side=TOP, fill=X)

        # LayFourth
        lay_fourth = Frame(self, bg='#EDEDED')
        lay_fourth_left = Frame(lay_fourth, bg='#EDEDED')
        lay_fourth_right = Frame(lay_fourth, bg='#EDEDED')
        lay_fourth_button = Frame(lay_fourth, bg='#EDEDED')
        Label(lay_fourth_left, borderwidth=10, width=10, text='video', fg="white", bg='#C5C1AA',
              font=('微软雅黑', 28)).pack(
            side=LEFT)
        video = StringVar()
        self.video_entry = Entry(lay_fourth_right, width=80, foreground='#C4C4C4', font=('微软雅黑', 28),
                                 textvariable=video)
        self.video_entry.pack(side=LEFT, padx=10)

        # 下载资源按钮，需绑定事件
        Button(lay_fourth_button, width=10, text='下载', background='white', fg='#C5C1AA', font=('微软雅黑', 28),
               command=self.download).pack(side=LEFT, padx=10)
        lay_fourth_left.pack(side=LEFT)
        lay_fourth_right.pack(side=LEFT)
        lay_fourth_button.pack(side=LEFT)
        lay_fourth.pack(side=TOP, fill=X)

        # 文件列表
        lay_fifth = Frame(self, bg='#EDEDED', width=1080, height=1780)
        lay_fifth_refresh = Frame(lay_fifth, bg='#EDEDED', width=1080, height=1780)
        # Label(lay_fifth_refresh, borderwidth=10, width=10, text='refresh', fg="white", bg='#C1CDC1',
        #       font=('微软雅黑', 28)).pack(side=TOP,fill=X)
        Button(lay_fifth_refresh, text='refresh', fg="#8B4513", bg='#C1CDC1', font=('微软雅黑', 28), highlightthickness=0,
               command=self.show_list).pack(side=TOP, fill=X)

        self.lay_fifth_box = Listbox(lay_fifth, bg='#E0E0E0', font=('微软雅黑', 28), width=1080, height=1780)
        lay_fifth_refresh.pack(side=TOP, fill=X)
        self.lay_fifth_box.pack(side=TOP, fill=X, padx=50)
        lay_fifth.pack(side=TOP, fill=X)

    def get_html(self):
        try:
            # 获取页码内容
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'  # 代理浏览器
                              + 'Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
            }
            response = requests.get(self.website.get(), headers=headers)
            # 通过状态判断是否获取成功
            if response.status_code == 200:
                pattern = re.compile('<title>(.*?)</title>', re.S)
                items = re.findall(pattern, response.text)
                if len(items) > 0:
                    self.title_entry.delete(0, END)
                    self.title = items[0]
                    self.title_entry.insert(0, items[0])

                pattern = re.compile('<iframe src="http:\/\/player.jfrft.net\/index.php\?url=(.*?)"', re.S)
                items = re.findall(pattern, response.text)
                if len(items) > 0:
                    self.video_entry.delete(0, END)
                    self.video = items[0]
                    self.video_entry.insert(0, items[0])
            else:
                mbox.showinfo('网页地址', '抓取页面内容失败，HTTPCODE:' + response.status_code)
        except RequestException:
            mbox.showinfo('网页地址', '请求异常')

    """
    下载视频
    过滤标题里特殊字符，用标题做文件名
    """

    def download(self):
        output = os.system('which ffmpeg2')
        if output == '':
            mbox.showinfo('插件丢失', '请先安装ffmpeg')
        else:
            title = self.title_entry.get().replace('丨', '')
            title = title.replace('|', '')
            title = title.replace('&', '')
            title = title.replace(' ', '')
            file = title + '.mp4'
            mbox.showinfo('正在执行命令', 'ffmpeg -i ' + self.video + ' -y /Users/kendo/Desktop/dm/' + file)
            os.system('ffmpeg -i ' + self.video + ' -y /Users/kendo/Desktop/dm/' + file)

    def refresh(self):
        self.show_list()

    def show_list(self):
        self.lay_fifth_box.delete(0, END)
        base_path = '/Users/kendo/Desktop/dm/'
        files = os.listdir(base_path)
        files.sort()
        for file in files:
            if file != '.DS_Store':
                if os.path.isdir(base_path + file):
                    pass
                    # mbox.showinfo('提示', file + '是文件加')
                else:
                    self.lay_fifth_box.insert(END, base_path + file)


if __name__ == '__main__':
    app = Application()
    app.mainloop()
