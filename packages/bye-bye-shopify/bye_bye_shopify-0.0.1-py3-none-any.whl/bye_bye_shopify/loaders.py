import json
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import requests

from .config import config, log
from .models import CustomCollection, Product


class Loader(ABC):

    def load_products(self):
        for product in Product.get_all():
            self.load_product(product)

    def load_custom_collections(self):
        for custom_collection in CustomCollection.get_all():
            products = list(Product.get_all(params={"collection_id": custom_collection.id, "fields": ["id"]}))
            self.load_custom_collection(custom_collection, products=products)

    def load_all(self):
        self.load_products()
        self.load_custom_collections()

    @abstractmethod
    def load_product(self, product: Product):
        raise NotImplementedError()

    @abstractmethod
    def load_custom_collection(self, custom_collection: CustomCollection, products: List[Product]):
        raise NotImplementedError()


class LocalLoader(Loader):
    base_dir: Path

    def __init__(self):
        self.base_dir = Path(config.local_loader_base_dir) if config.local_loader_base_dir else Path("./data").resolve()

    def get_product_path_prefix(self, product: Product) -> str:
        return str(self.base_dir / config.product_path_template.format(product=product))

    def get_custom_collection_path_prefix(self, custom_collection: CustomCollection) -> str:
        return str(self.base_dir / config.custom_collection_path_template.format(custom_collection=custom_collection))

    def load_product(self, product: Product):
        log.info(f"Loading product {product.id}")

        path_prefix = self.get_product_path_prefix(product)
        dir_path = Path(path_prefix).parent
        if not dir_path.exists():
            dir_path.mkdir(parents=True)

        product_file_path = Path(path_prefix + ".json")
        with product_file_path.open("w") as f:
            json.dump(product.to_dict(), f, sort_keys=True, indent=4)

        for image in product.images:
            image_file_suffix = Path(urlparse(image.src).path).suffix
            image_file_path = Path(path_prefix + f"-{str(image.position).zfill(2)}{image_file_suffix}")
            if image_file_path.exists():
                log.debug(f"{image.src} already downloaded to {image_file_path}, doing nothing")
                continue
            log.info(f"Downloading {image.src} to {image_file_path}")
            r = requests.get(image.src, stream=True)
            with open(image_file_path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    def load_custom_collection(self, custom_collection: CustomCollection, products: List[Product]):
        log.info(f"Loading custom collection {custom_collection.id}")

        path_prefix = self.get_custom_collection_path_prefix(custom_collection)
        dir_path = Path(path_prefix).parent
        if not dir_path.exists():
            dir_path.mkdir(parents=True)

        obj_file_path = Path(path_prefix + ".json")
        with obj_file_path.open("w") as f:
            dct = custom_collection.to_dict()
            dct["_products"] = [p.id for p in products]  # Non-shopify field to preserve the product mapping.
            json.dump(dct, f, sort_keys=True, indent=4)

        if custom_collection.image:
            image_file_suffix = Path(urlparse(custom_collection.image.src).path).suffix
            image_file_path = Path(path_prefix + image_file_suffix)
            if image_file_path.exists():
                log.debug(f"{custom_collection.image.src} already downloaded to {image_file_path}, doing nothing")
            else:
                log.info(f"Downloading {custom_collection.image.src} to {image_file_path}")
                r = requests.get(custom_collection.image.src, stream=True)
                with open(image_file_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
