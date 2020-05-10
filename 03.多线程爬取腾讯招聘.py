import requests
import threading
import json
import time
from queue import Queue


class Mythread(threading.Thread):
    def __init__(self, name, page_queue):
        super().__init__()
        self.name = name
        self.q = page_queue

    def run(self):
        # 防止只干一个任务就退出
        while True:
            if self.q.empty():
                break
            # (1)获取任务
            page = self.q.get()
            print('========{}开始执行任务{}========'.format(self.name, page))
            # (2)发请求
            response = self.request_html(page)
            # (3)解析页面
            post_list = self.parse_html(response)
            print('======={}完成任务{}======'.format(self.name, page))
            # print(post_list)
            # with open('tencent.json','a',encoding='utf-8')as fp:
            #     fp.write(json.dumps(post_list, ensure_ascii=False)+'\n')

    def request_html(self, page):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
        url = 'https://careers.tencent.com/tencentcareer/api/post/Query?&keyword=python&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(
            page)
        response = requests.get(url=url, headers=headers).json()
        # with open("tx.json", "w", encoding="utf-8")as fp:
        #     fp.write(response)
        return response

    def parse_html(self, response):
        posts = response.get('Data').get('Posts')
        post_list = []
        for post in posts:
            post_dict = {}
            RecruitPostName = post.get('RecruitPostName')
            CountryName = post.get('CountryName')
            LocationName = post.get('LocationName')
            BGName = post.get('BGName')
            Responsibility = post.get('Responsibility')
            LastUpdateTime = post.get('LastUpdateTime')
            PostURL = post.get('PostURL')

            post_dict['RecruitPostName'] = RecruitPostName
            post_dict['CountryName'] = CountryName
            post_dict['LocationName'] = LocationName
            post_dict['BGName'] = BGName
            post_dict['Responsibility'] = Responsibility
            post_dict['LastUpdateTime'] = LastUpdateTime
            post_dict['PostURL'] = PostURL
            post_list.append(post_dict)
        return post_list


if __name__ == '__main__':
    start_time = time.time()
    print('~~~~~~~~~~~~~~~~~~任务开始{}~~~~~~~~~~~~~~~~~~~~~'.format(start_time))

    # 1.创建任务队列
    page_queue = Queue()
    for i in range(1, 11):
        page_queue.put(i)

    # 2.起线程
    crawl_name = ['crawl1', 'crawl2', 'crawl3']
    thread_list = []
    for name in crawl_name:
        crawl = Mythread(name, page_queue)
        crawl.start()
        thread_list.append(crawl)

    # 阻塞主线程
    for thread in thread_list:
        thread.join()

    end_time = time.time()
    print('~~~~~~~~~~~~~~~~~~任务结束{}~~~~~~~~~~~~~~~~~~~~~'.format(end_time))
    print('~~~~~~~~~~~~~~~~~~任务花费时间{}~~~~~~~~~~~~~~~~~~~~~'.format(end_time - start_time))



