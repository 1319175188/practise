import time
from selenium import webdriver
from lxml import etree
import re


def get_list(list_value):
    if list_value:
        lis = list_value[0]
    else:
        lis = "None"
    return lis


def parse_html(response):
    tree = etree.HTML(response)
    li_list = tree.xpath('//div[@class="layout-Module-container layout-Cover ListContent"]/ul[@class="layout-Cover-list"]/li')
    print(len(li_list))
    for li in li_list:
        # 标签
        label = li.xpath('.//span[@class="DyListCover-zone"]/text()')
        label = get_list(label)
        print(label)
        # 标题
        title = li.xpath('.//h3[@class="DyListCover-intro"]/text()')
        title = get_list(title)
        print(title)
        # 详情页链接
        href = li.xpath('.//a[1]/@href')
        href = get_list(href)
        if href == "None":
            detail_url = "None"
        else:
            detail_url = "https://www.douyu.com/" + href
        print(detail_url)


if __name__ == '__main__':
    # (1)封装浏览器
    driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # (2)访问网站
    driver.get('https://www.douyu.com/directory/all')
    time.sleep(3)
    # with open("download/douyu.html", "w", encoding="utf-8") as fp:
    #     fp.write(driver.page_source)
    # 解析
    parse_html(driver.page_source)

    page = 1
    while True:
        flag_pattern = re.compile(r'<li title="下一页" .*?aria-disabled="(.*?)">')
        flag = flag_pattern.findall(driver.page_source)[0]
        time.sleep(1)
        print(flag)

        if flag == 'true':
            break

        # (3).翻页：
        driver.find_element_by_class_name(' dy-Pagination-next').click()
        time.sleep(3)

        # (4).解析：
        parse_html(driver.page_source)
        page += 1
        print('当前访问{}页============'.format(page))









