"""

"""
import wcc



def main():
    # url = 'http://www.baidu.com'
    url = 'http://stockpage.10jqka.com.cn/000063/funds'
    url2 = 'https://zhuanlan.zhihu.com/p/47777088'
    url3 = 'http://www.ip138.com/'
    url4 = 'https://ip.cn/'
    cookie_str = wcc.get_cookie("http://stockpage.10jqka.com.cn/000063/")
    print (cookie_str)
    resp_text = wcc.getpage(url, use_proxy=False, use_browser=False,use_cookie=cookie_str)
    print (resp_text)




if __name__ == "__main__":
    main()
