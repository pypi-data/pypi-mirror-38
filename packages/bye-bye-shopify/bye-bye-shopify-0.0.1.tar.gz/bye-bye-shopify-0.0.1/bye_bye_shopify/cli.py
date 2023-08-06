from aarghparse import cli

from .config import configure_logging
from .loaders import LocalLoader


@cli
def bye_bye_cli(subcommand, loader):

    @subcommand
    def download_products():
        loader.load_products()

    @subcommand
    def download_custom_collections():
        loader.load_custom_collections()

    @subcommand
    def download_all():
        loader.load_all()


def main():
    configure_logging()
    bye_bye_cli(loader=LocalLoader()).run()


if __name__ == "__main__":
    main()
