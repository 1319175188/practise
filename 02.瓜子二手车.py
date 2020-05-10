import time
import pymysql
from selenium import webdriver
from lxml import etree


db = pymysql.connect(host='localhost', user='root', password='123456', database='guazi')
cursor = db.cursor()


def get_list(value_list):
    if value_list:
        value = value_list[0]
    else:
        value = "None"
    return value


def parse_html(response):
    tree = etree.HTML(response)
    li_list = tree.xpath('//ul[@class="carlist clearfix js-top"]/li')
    print(len(li_list))
    for li in li_list:
        # 1.标题
        title_list = li.xpath('.//h2/text()')
        title = get_list(title_list)
        print(title)
        # 2.标签
        label_list = li.xpath('.//div[@class="t-i"]/text()')
        if label_list:
            label = "|".join(label_list)
        else:
            label = "None"
        print(label)
        # 3.价格
        price_list = li.xpath('.//div[@class="t-price"]/p//text()')
        if price_list:
            price = "".join(price_list)
        else:
            price = "None"
        print(price)
        # 详情页href
        href_list = li.xpath('./a/@href')
        href = get_list(href_list)
        if href:
            detail_url = "https://www.guazi.com"+href
        else:
            detail_url = "None"
        print(detail_url)
        driver_detail = webdriver.PhantomJS(executable_path=r'D:\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        driver_detail.get(detail_url)
        time.sleep(2)
        detail_response = driver_detail.page_source
        detail_tree = etree.HTML(detail_response)
        # 4.车源号
        car_num_list = detail_tree.xpath('//div[@class="right-carnumber"]/text()')
        car_num = get_list(car_num_list)
        print(car_num)
        # 5.包什么
        detail_labels_list = detail_tree.xpath('//h2[@class="titlebox"]/span/text()')
        if detail_labels_list:
            detail_labels = "|".join(detail_labels_list)
        else:
            detail_labels = "None"
        print(detail_labels)
        # 6.上牌时间
        shangpai_time_list = detail_tree.xpath('//ul[@class="assort clearfix"]/li[1]/span/text()')
        shangpai_time = get_list(shangpai_time_list)
        print(shangpai_time)
        # 7.里程
        licheng_list = detail_tree.xpath('//ul[@class="assort clearfix"]/li[2]/span/text()')
        licheng = get_list(licheng_list)
        print(licheng)
        # 8.排量
        pailiang_list = detail_tree.xpath('//ul[@class="assort clearfix"]/li[3]/span/text()')
        pailiang = get_list(pailiang_list)
        print(pailiang)
        # 9.变速箱
        biansuxiang_list = detail_tree.xpath('//ul[@class="assort clearfix"]/li[4]/span/text()')
        biansuxiang = get_list(biansuxiang_list)
        print(biansuxiang)
        # 10.服务保障
        service_list = detail_tree.xpath('//ul[@class="service-protect-list clearfix"]//span/text()')
        if service_list:
            service = ",".join(service_list).strip()
        else:
            service = "None"
        print(service)
        sql = "insert into cars(标题,标签,价格,车源号,包什么,上牌时间,里程,排量,变速箱,服务保障) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"\
            .format(title, label, price, car_num, detail_labels, shangpai_time, licheng, pailiang, biansuxiang, service)
        cursor.execute(sql)
        db.commit()


if __name__ == '__main__':
    url = "https://www.guazi.com/bj/buy/o33/"
    driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    driver.get(url)
    # with open("download/瓜子二手车.html", "w", encoding="utf-8") as fp:
    #     fp.write(driver.page_source)
    time.sleep(2)
    parse_html(driver.page_source)

    page = 1
    while True:
        tree = etree.HTML(driver.page_source)
        next_list = tree.xpath('//a[@class="next"]/@class')
        time.sleep(2)
        print(next_list)

        if next_list == []:
            break

        # (3).翻页：
        driver.find_element_by_class_name('next').click()
        time.sleep(3)

        # (4).解析：
        parse_html(driver.page_source)
        page += 1
        print('当前访问{}页============'.format(page))

    # 7、关闭连接
    cursor.close()
    db.close()
