#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   Request.py
Author: Lijiacai (1050518702@qq.com)
Date: 2018-xx-xx
Description:
    爬虫抓取的requests请求，主要扩展了重试机制，对于代理原因造成连接失败，可以重试连接，
    并且同一个页面如果需要cookie，访问，则使用同一个spider即可。
"""
import loggin
import os
import random
import sys
import time
import requests


class Request(object):
    """Request"""

    def __init__(self, proxies=None, try_time=5, frequence=0.1, timeout=20):
        """
        :param proxies: 代理
        :param try_time: 重试次数
        :param frequence: 抓取频率
        :param timeout: 超时
        """
        self.proxies = proxies
        self.session = requests.Session()
        self.try_time = try_time
        self.frequence = frequence
        self.timeout = timeout

    def proxy(self):
        """
        get proxy
        如果有其他代理，更改此处函数
        :return: 返回一个ip：12.23.88.23:2345
        """
        if len(self.proxies) == 0:
            one_proxy = None
        elif type(self.proxies) == list:
            one_proxy = random.choice(self.proxies)
        else:
            one_proxy = None
        return one_proxy

    def request(self, method, url, response_encode="utf-8",
                params=None, data=None, headers=None, cookies=None, files=None,
                auth=None, timeout=None, allow_redirects=True, proxies=None,
                hooks=None, stream=None, verify=None, cert=None, json=None):
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
                Returns :class:`Response <Response>` object.

                :param method: method for the new :class:`Request` object.
                :param url: URL for the new :class:`Request` object.
                :param response_encode: response_encode for the new :class:`response` object.
                :param params: (optional) Dictionary or bytes to be sent in the query
                    string for the :class:`Request`.
                :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                    object to send in the body of the :class:`Request`.
                :param json: (optional) json to send in the body of the
                    :class:`Request`.
                :param headers: (optional) Dictionary of HTTP Headers to send with the
                    :class:`Request`.
                :param cookies: (optional) Dict or CookieJar object to send with the
                    :class:`Request`.
                :param files: (optional) Dictionary of ``'filename': file-like-objects``
                    for multipart encoding upload.
                :param auth: (optional) Auth tuple or callable to enable
                    Basic/Digest/Custom HTTP Auth.
                :param timeout: (optional) How long to wait for the server to send
                    data before giving up, as a float, or a :ref:`(connect timeout,
                    read timeout) <timeouts>` tuple.
                :type timeout: float or tuple
                :param allow_redirects: (optional) Set to True by default.
                :type allow_redirects: bool
                :param proxies: (optional) Dictionary mapping protocol or protocol and
                    hostname to the URL of the proxy.
                :param stream: (optional) whether to immediately download the response
                    content. Defaults to ``False``.
                :param verify: (optional) Either a boolean, in which case it controls whether we verify
                    the server's TLS certificate, or a string, in which case it must be a path
                    to a CA bundle to use. Defaults to ``True``.
                :param cert: (optional) if String, path to ssl client cert file (.pem).
                    If Tuple, ('cert', 'key') pair.
                :rtype: requests.Response
                """
        for try_time in range(self.try_time):
            try:
                response = self.session.request(method, url,
                                                params=params, data=data, headers=headers,
                                                cookies=cookies,
                                                files=files,
                                                auth=auth, timeout=timeout,
                                                allow_redirects=allow_redirects,
                                                proxies=self.proxy(),
                                                hooks=hooks, stream=stream, verify=verify,
                                                cert=cert,
                                                json=json)
                response.encoding = response_encode
                result = response.text
                return result
            except Exception as e:
                logging.exception("%s forbidden:%s" % (time.asctime(), str(e)))
            time.sleep(self.frequence)

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends a OPTIONS request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', True)
        return self.request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        r"""Sends a HEAD request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        kwargs.setdefault('allow_redirects', False)
        return self.request('HEAD', url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PUT', url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        r"""Sends a PATCH request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('PATCH', url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request. Returns :class:`Response` object.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """

        return self.request('DELETE', url, **kwargs)


def test():
    """unittest"""
    spider = Request(proxies=["a"])
    print(spider.get(url="https://www.baidu.com"))


if __name__ == '__main__':
    test()
