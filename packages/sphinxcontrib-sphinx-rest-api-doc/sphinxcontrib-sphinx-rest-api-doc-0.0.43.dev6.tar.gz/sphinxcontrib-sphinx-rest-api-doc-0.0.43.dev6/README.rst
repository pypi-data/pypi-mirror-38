=====================================
sphinxcontrib-sphinx-rest-api-doc
=====================================

.. image:: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-rest-api-doc.svg?branch=master
    :target: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-rest-api-doc

.. image:: https://badge.fury.io/py/sphinxcontrib-sphinx-rest-api-doc.svg
    :target: https://badge.fury.io/py/sphinxcontrib-sphinx-rest-api-doc


a tools for sphinx gen doc from json api

Overview
--------

Add a longer description here.

INSTALL
--------------------

.. code-block:: bash

    pip install sphinxcontrib-sphinx-rest-api-doc

Basic usage
----------------------

.. code-block:: rst

   .. rest: path_to_model.json


example in model file
----------------------



.. code-block:: json

   {
  "title": "测试资源",
  "desc": "测试测试测试",
  "method": {
    "get": {
      "list": false,
      "path": "/api/xx/xx/xx",
      "params": {
        "id":"ddede"
      },
      "desc": "dwdwedewfeferferferferfewr",
      "headers": {
        "auth":"auth"
      },
      "codes": {
        "400":"de",
        "200":"2"
      }
    }
  },
  "model": {
    "id":"",
    "desc":"dede"
  }
   }



CONFIG
----------


in config.py

.. code-block:: py
    
   extensions += ['sphinxcontrib.SphinxRest',]
   rest_api_source_root = os.path.join(PROJECT_DIR, "_static", "models")
   rest_api_domain = "timger.com.cn"
   rest_api_http_request_example_title = "Request Example"
   rest_api_http_response_example_title = "Response Example"


Links
-----

- Source: https://github.com/yishenggudou/sphinxcontrib-sphinx-rest-api-doc
- Bugs: https://github.com/yishenggudou/sphinxcontrib-sphinx-rest-api-doc/issues
- BLOG: http://www.timger.com.cn/
