=====================================
sphinxcontrib-sphinx-rest-api-doc
=====================================

.. image:: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-rest-api-doc.svg?branch=master
    :target: https://travis-ci.org/yishenggudou/sphinxcontrib-sphinx-rest-api-doc

a tools for sphinx gen doc from json api

Overview
--------

Add a longer description here.

INSTALL
--------------------

.. code-block::bash

    pip install sphinxcontrib-sphinx-rest-api-doc

Basic usage
----------------------
.. code-block:: rst

   .. rest: path_to_model.json



CONFIG
----------


in config.py

.. code-block::py
    
  extensions += ['sphinxcontrib.sphinxcontrib-sphinx-rest-api-doc', ]
  swagger_api_url = os.path.join(PROJECT_DIR, "_static", "api-docs.json")
  swagger_api_domain = "timger.com.cn"



Links
-----

- Source: https://github.com/yishenggudou/sphinxcontrib-sphinx-rest-api-doc
- Bugs: https://github.com/yishenggudou/sphinxcontrib-sphinx-rest-api-doc/issues
