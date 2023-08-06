"""

"""
import requests

def get_proxy():
    """
    从虎头代理获取一个代理ip和端口
    :return:一个元组(ip, port), 其中ip是个字符串，port是个整型数字
    """
    url2 = 'http://257656416044421866.standard.hutoudaili.com/?num=1&area_type=1&scheme=1'
    url = 'http://266521123748421866.standard.hutoudaili.com/?num=1&area_type=1&scheme=1'
    response = requests.get(url).text
    iport= response.split(":")
    ip = str(iport[0])
    port = int(iport[1])
    return ip, port

def get_proxy_other():
    pro = requests.get('http://dynamic.goubanjia.com/dynamic/get/2bd6fa04ff7a708cdbcbaab207602c6e.html?sep=3')
    ip = str(pro.text.split(":")[0])
    port = int(pro.text.split(":")[1])
    return ip, port


def main():
    ip, port = get_proxy()
    print ("ip:" + ip + ", port:" + str(port))
    

if __name__ == "__main__":
    main()

