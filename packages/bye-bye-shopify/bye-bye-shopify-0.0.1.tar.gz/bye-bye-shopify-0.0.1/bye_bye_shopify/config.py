import logging
import sys

from wr_profiles import envvar_profile_cls


def configure_logging():
    log_handler = logging.StreamHandler(stream=sys.stderr)
    log_handler.setFormatter(logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(message)s'))
    root_logger = logging.getLogger('')
    root_logger.handlers[:] = []
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)


@envvar_profile_cls(profile_root="bye_bye")
class ByeByeProfile:
    api_key: str
    api_password: str
    api_hostname: str = "yourshopname.myshopify.com"

    local_loader_base_dir: str = None

    product_path_template: str = "products/{product.id}/{product.id}"
    custom_collection_path_template: str = "custom_collections/{custom_collection.id}"


profile = ByeByeProfile()


class ByeByeConfig(ByeByeProfile):
    profile_delegate = profile

    @property
    def app_name(self):
        return f"bye-bye@{self.api_hostname}"


config = ByeByeConfig()

log = logging.getLogger(__name__)
