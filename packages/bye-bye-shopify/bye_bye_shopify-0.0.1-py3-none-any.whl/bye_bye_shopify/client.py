import json

import requests

from .config import config, log


class ShopifyApiClient(requests.Session):
    def __init__(self):
        super(ShopifyApiClient, self).__init__()

        self.hooks = {
            "response": (
                self.response_logger,
            )
        }

        self.headers = {
            "User-Agent": config.app_name,
            "Content-Type": "application/json",
        }

    @staticmethod
    def response_logger(resp, **kwargs):
        url = resp.request.url
        url = "https://{}".format(url.split("@", 1)[1])

        log.info("{method} {url} -- {status_code}".format(
            method=resp.request.method,
            url=url,
            status_code=resp.status_code,
        ))
        if resp.status_code >= 300:
            log.warning(
                "{method} {url} failed with status code {status_code}.\n"
                "Response headers: {headers}\n"
                "Response content:\n{content}".format(
                    method=resp.request.method,
                    url=url,
                    status_code=resp.status_code,
                    headers=resp.headers,
                    content=resp.content,
                )
            )

    def request(self, method, resource, payload=None, **kwargs):
        if payload is not None:
            assert not kwargs["data"]
            kwargs["data"] = json.dumps(payload)

        url = "https://{key}:{password}@{hostname}/admin/{resource}.json".format(
            key=config.api_key,
            password=config.api_password,
            hostname=config.api_hostname.rstrip("/"),
            resource=resource.lstrip("/"),
        )

        return super(ShopifyApiClient, self).request(method, url, **kwargs)

    class Descriptor:
        def __init__(self):
            self.attr_name = None

        def __set_name__(self, owner, name):
            self.attr_name = f"_shopify_api_client#{name}"

        def __get__(self, instance, owner):
            if not hasattr(owner, self.attr_name):
                setattr(owner, self.attr_name, ShopifyApiClient())
            return getattr(owner, self.attr_name)
