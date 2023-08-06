===============
bye-bye-shopify
===============

If your Shopify store isn't doing too well, it's time to close it, but Shopify doesn't
provide an easy way to extract all your product catalogue. This Python utility allows
you to do that. I wrote it for and tested it only on my mom's candle store.

Features
========

* Extract products and product variations to a JSON file, one per product
* Extract product images to a local directory
* Extract custom collections

Installation
============

.. code-block:: shell

    pip install bye-bye-shopify

Configuration
-------------

In Shopify Admin, under *Apps* / *Manage private apps* (link at the very bottom
of the page), create a new private app. The name of the app doesn't matter.
Set the following environment variables by copying the values of *API key* and *Password*
displayed on the page:

.. code-block:: shell

    export BYE_BYE_API_KEY="..."
    export BYE_BYE_API_PASSWORD="..."

You will also need to set the hostname of your shop which is probably something
like ``yourshopname.myshopify.com``:

.. code-block:: shell

    export BYE_BYE_API_HOSTNAME="yourshopname.myshopify.com"

.. code-block:: shell

    bye-bye-shopify --help

    bye-bye-shopify download_all

    ls -al data/products/
    ls -al data/custom_collections/
