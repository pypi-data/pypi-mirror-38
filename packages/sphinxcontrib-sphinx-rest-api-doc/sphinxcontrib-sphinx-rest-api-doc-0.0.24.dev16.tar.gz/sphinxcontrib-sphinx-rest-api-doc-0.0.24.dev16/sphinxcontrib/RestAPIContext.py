#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib, codecs, json
from jinja2 import Template, FileSystemLoader, Environment
import os

DIRPATH = os.path.dirname(os.path.abspath(__file__))


class RestAPIContext(object):
    """
    
    """
    
    def __init__(self,
                 _domain,
                 _model_path,
                 **kwargs):
        self.kwargs = kwargs
        self.kwargs['http_domain'] = _domain
        self.domain = _domain
        self.model_path = _model_path
    
    @property
    def context(self):
        _ = {
            "base": {},
            "context": {}
        }
        _['base'] = self.kwargs
        import codecs
        with codecs.open(self.model_path, 'rb', 'utf-8') as fr:
            _["context"] = json.loads(fr.read())
        
        for http_method, http_desc in _['context']['method'].items():
            if _['context']['method'].get("list"):
                _['context']['method'][http_method]['response'] = json.dumps([_["context"]['model'], ], indent=4)
            else:
                _['context']['method'][http_method]['response'] = json.dumps(_["context"]['model'], indent=4)
            if http_method.upper() in ['POST', 'PUT']:
                _['context']['method'][http_method]['request'] = json.dumps(_["context"]['model'],indent=4)
            if not http_desc.get("codes"):
                _['context']['method'][http_method]['codes'] = {}
                _['context']['method'][http_method]['codes'].update(_['base']['global_codes'])
            if not http_desc.get("headers"):
                _['context']['method'][http_method]['headers'] = {}
                _['context']['method'][http_method]['headers'].update(_['base']['global_headers'])
        return _
    
    def get_rst_content(self):
        templateLoader = FileSystemLoader(searchpath=DIRPATH)
        templateEnv = Environment(loader=templateLoader,lstrip_blocks=True,trim_blocks=True)
        TEMPLATE_FILE = "api.jinja2.1.txt"
        template = templateEnv.get_template(TEMPLATE_FILE)
        template.globals.update(clever_function=lambda x: x)
        #print(self.context)
        return template.render(**self.context)


if __name__ == "__main__":
    o = RestAPIContext("test",
                       "/Volumes/data/github/sphinx-rest-api-doc/model.test.json",
                       **{
                           "response_example_title": "response_example_title",
                           "request_example_title": "request_example_title"
                       })
    print(o.context)
    s = o.get_rst_content()
    print(type(s))
    print(s)
