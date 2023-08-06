import copy
from typing import Any, ClassVar, List

from strictus_dictus import sdict

from .client import ShopifyApiClient


class ShopifyResource:
    resource_name: ClassVar[str] = None
    shopify: ClassVar[ShopifyApiClient] = ShopifyApiClient.Descriptor()

    @classmethod
    def get_count(cls):
        return cls.shopify.get("{resource}/count".format(resource=cls.resource_name)).json()["count"]

    @classmethod
    def get_all(cls, limit=None, params=None, _path=None):
        page = 1
        page_limit = 50
        _path = _path or cls.resource_name

        num_returned = 0

        if params:
            params = copy.deepcopy(params)
        else:
            params = {}
        params["page"] = page
        params["limit"] = min(page_limit, limit) if limit is not None else page_limit

        while True:
            resp = cls.shopify.get(_path, params=params)
            content = resp.json()[cls.resource_name]
            for row in content:
                yield cls(row)
                num_returned += 1
                if limit is not None and num_returned >= limit:
                    return
            if len(content) < page_limit:
                return
            params["page"] += 1

    @classmethod
    def get_by_id(cls, id):
        resp = cls.shopify.get("{}/{}".format(cls.resource_name, id))
        return resp.json()[cls.resource_name[:-1]]


class ProductVariant(ShopifyResource, sdict):
    resource_name = "variants"

    id: int
    product_id: int
    title: str
    price: str
    sku: str
    position: int
    inventory_policy: str
    compare_at_price: str
    fulfillment_service: str
    inventory_management: str
    option1: str
    option2: str
    option3: str
    created_at: str
    updated_at: str
    taxable: bool
    barcode: str
    grams: int
    image_id: int
    weight: float
    weight_unit: str
    inventory_item_id: int
    inventory_quantity: int
    old_inventory_quantity: int
    requires_shipping: bool
    admin_graphql_api_id: str
    presentment_prices: List


class ProductImage(ShopifyResource, sdict):
    resource_name = "images"

    id: int
    product_id: int
    position: int
    created_at: str
    updated_at: str
    width: int
    height: int
    src: str
    variant_ids: List

    admin_graphql_api_id: str
    alt: str


class Product(ShopifyResource, sdict):
    resource_name = "products"

    id: int
    title: str
    body_html: str
    vendor: str
    product_type: str
    created_at: str
    handle: str
    updated_at: str
    published_at: str
    template_suffix: str
    tags: str
    published_scope: str
    admin_graphql_api_id: str
    variants: List[ProductVariant]
    options: List[dict]
    images: List[ProductImage]
    image: Any


class CustomCollectionImage(sdict):
    src: str
    alt: str
    width: int
    height: int
    created_at: str


class CustomCollection(ShopifyResource, sdict):
    resource_name = "custom_collections"

    id: int
    body_html: str
    handle: str
    image: CustomCollectionImage
    metafields: List[dict]
    published: bool
    published_at: str
    published_scope: str
    sort_order: str
    template_suffix: str
    title: str
    updated_at: str

    admin_graphql_api_id: str
