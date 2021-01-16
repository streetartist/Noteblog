'''
Noteblog插件功能：
访问链接默认是/tool/您的文件名
您需要定义类Main,并且拥有方法main，程序会在访问链接调用main函数
'''

class Main:
    def __init__(self):
        pass

    def main(self):
        return "这是一个测试插件!"
