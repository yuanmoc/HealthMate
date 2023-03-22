import requests


class Session(requests.Session):
    """
    http 请求工具类
    """

    def __init__(self):
        # 会话session
        self.session = requests.session()
        # 请求前处理函数
        self.beforeFun = lambda **kwargs: kwargs
        # 请求后处理函数
        self.afterFun = lambda res: None

    def before(self, fun):
        self.beforeFun = fun

    def after(self, fun):
        self.afterFun = fun

    def get(self, url, **kwargs):
        kwargs = self.beforeFun(**kwargs)
        res = self.session.get(url, **kwargs)
        self.afterFun(res)
        return res

    def post(self, url, **kwargs):
        kwargs = self.beforeFun(**kwargs)
        res = self.session.post(url, **kwargs)
        self.afterFun(res)
        return res

    def formPost(self, url, **kwargs):
        kwargs = self.beforeFun(**kwargs)
        headers = kwargs.get('headers')
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        kwargs['headers'] = headers
        res = self.session.post(url, **kwargs)
        self.afterFun(res)
        return res

    def put(self, url, **kwargs):
        kwargs = self.beforeFun(**kwargs)
        res = self.session.put(url, **kwargs)
        self.afterFun(res)
        return res

    def delete(self, url, **kwargs):
        kwargs = self.beforeFun(**kwargs)
        res = self.session.delete(url, **kwargs)
        self.afterFun(res)
        return res

    def getCookies(self):
        return self.session.cookies
