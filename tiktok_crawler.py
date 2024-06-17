# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @file : tiktok_crawler
# @Email : huiwennear@163.com
# @Time : 2024/5/23 16:59

"""
    Tiktok评论爬取
"""
from utils.common_utils import CommonUtils, get_web_id_last_time

import requests
from urllib.parse import urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TiktokComment:

    def __init__(self):
        self.common_utils = CommonUtils()
        self.comment_list_headers = {
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': self.common_utils.user_agent,
            'sec-ch-ua-platform': '"Windows"',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }

    def get_comment_list(self, req_url):
        aweme_id = urlparse(req_url).path.split("/")[-1]
        ms_token = self.common_utils.get_ms_token()
        print(f"aweme_id={aweme_id}, ms_token={ms_token}")
        web_id_last_time = get_web_id_last_time()
        cursor = 0
        req_url2 = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime={web_id_last_time}&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id={aweme_id}&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F126.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&current_region=US&cursor={cursor}&device_id=7376606050684241409&device_platform=web_pc&enter_from=tiktok_web&focus_state=false&fromWeb=1&from_page=video&history_len=3&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&os=mac&priority_region=AU&referer=&region=US&screen_height=982&screen_width=1512&tz_name=Asia%2FShanghai&webcast_language=zh-Hans&msToken=N_sorU4n2DcwJnzKhZ7c2VCX-xOHWT4iyfemIBNiphSs6Wi5TW2gy0y8XMxo7BIGrK-TLgzIVoALVlD3LAS41vDCWDJy98dm256zHR9lk6KdGUH3KtWi96dLpGwJEw7aOOR6UVzXknDcuwJmgK0VIl32zA=="

        xbogus = self.common_utils.get_xbogus(req_url2, self.common_utils.user_agent)
        req_url2 = req_url2 + f'&X-Bogus={xbogus}&_signature=_02B4Z6wo00001czZRNQAAIDCniZkzecDtjHM2UBAABVaad'
        print(f"req_url2={req_url2}")
        response = requests.request("GET", req_url2, headers=self.comment_list_headers, verify=False, timeout=10)
        if response.text:
            req_json = response.json()
            total = req_json.get('total')
            print(f"total={total}")
            comments = req_json.get('comments')
            if comments:
                for comment_index in range(len(comments)):
                    comment_item = comments[comment_index]
                    print(f"爬取成功：{comment_item.get('user').get('nickname')}：{comment_item.get('text')}")
            while int(req_json.get('has_more'))==1:
                cursor = req_json.get('cursor')
                req_url2 = f"https://www.tiktok.com/api/comment/list/?WebIdLastTime={web_id_last_time}&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id={aweme_id}&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F126.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&current_region=US&cursor={cursor}&device_id=7376606050684241409&device_platform=web_pc&enter_from=tiktok_web&focus_state=false&fromWeb=1&from_page=video&history_len=3&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&os=mac&priority_region=AU&referer=&region=US&screen_height=982&screen_width=1512&tz_name=Asia%2FShanghai&webcast_language=zh-Hans&msToken=N_sorU4n2DcwJnzKhZ7c2VCX-xOHWT4iyfemIBNiphSs6Wi5TW2gy0y8XMxo7BIGrK-TLgzIVoALVlD3LAS41vDCWDJy98dm256zHR9lk6KdGUH3KtWi96dLpGwJEw7aOOR6UVzXknDcuwJmgK0VIl32zA=="
                xbogus = self.common_utils.get_xbogus(req_url2, self.common_utils.user_agent)
                req_url2 = req_url2 + f'&X-Bogus={xbogus}&_signature=_02B4Z6wo00001czZRNQAAIDCniZkzecDtjHM2UBAABVaad'
                print(f"req_url2={req_url2}")
                response=requests.request("GET", req_url2, headers=self.comment_list_headers, verify=False, timeout=10)
                if response.text:
                    req_json = response.json()
                    comments = req_json.get('comments')
                    if comments:
                        for comment_index in range(len(comments)):
                            comment_item = comments[comment_index]
                            print(f"爬取成功：{comment_item.get('user').get('nickname')}：{comment_item.get('text')}")
            else:
                print(f"爬取结束：评论数={total}")
        else:
            print(f"爬取失败或没有评论")


if __name__ == '__main__':
    req_url = "https://www.tiktok.com/@leethefoodie1005/video/7250555540592676142"
    tiktok_comment = TiktokComment()
    tiktok_comment.get_comment_list(req_url)
