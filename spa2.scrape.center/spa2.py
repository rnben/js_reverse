import requests

from playwright.sync_api import sync_playwright


BASE_URL = "https://spa2.scrape.center"


class Spa2Api(object):

    def __init__(
        self,
    ):
        browser = sync_playwright().start().chromium.launch()
        page = browser.new_page()
        page.route(
            "**/chunk-10192a00.243cb8b7.js",
            lambda route: route.fulfill(path="js\chunk-10192a00.243cb8b7.js"),
        )

        page.goto(BASE_URL)
        self.browser = browser
        self.page = page

    def __enter__(self):
        return self

    def __exit__(self, exc_ty, exc_val, tb):
        self.page.close()
        self.browser.close()
        self.page = None
        self.browser = None

    def get_token(self, limit: int):
        token = self.page.evaluate(
            '()=> {return window.encrypt("%s", "%d")}' % ("/api/movie", limit)
        )

        return token

    def get_movies(self, page: int = 1, page_size: int = 10):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Pragma": "no-cache",
            "Referer": "https://spa2.scrape.center/page/1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }

        offset = (page - 1) * page_size
        params = (
            ("limit", page_size),
            ("offset", offset),
            ("token", self.get_token(offset)),
        )

        response = requests.get(
            "https://spa2.scrape.center/api/movie/", headers=headers, params=params
        )

        response.raise_for_status()

        return response.json()


if __name__ == "__main__":
    with Spa2Api() as api:
        print(api.get_movies())
        print(api.get_movies(page=2))
