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
        methods = []
        permissions = _["context"].get("permissions", [])
        if type(_['context']['method']) in [dict, ]:
            for http_method, http_desc in _['context']['method'].items():
                http_desc["method"] = http_method
                methods.append(http_desc)
        else:
            methods = _['context']['method'] or _['context']['endpoints']
        for http_desc in methods:
            http_method = http_desc['method']
            if http_desc.get("list"):
                http_desc['response'] = json.dumps([_["context"]['model'], ], indent=4)
            else:
                http_desc['response'] = json.dumps(_["context"]['model'], indent=4)
            if http_method.upper() in ['POST', 'PUT']:
                http_desc['request'] = json.dumps(_["context"]['model'], indent=4)
            if not http_desc.get("codes"):
                http_desc['codes'] = {}
                http_desc['codes'].update(_['base']['global_codes'])
            if not http_desc.get("headers"):
                http_desc['headers'] = {}
                http_desc['headers'].update(_['base']['global_headers'])
            if not http_desc.get("params"):
                http_desc['params'] = {}
            http_desc['permissions'] = http_desc.get("permissions", []) + permissions
        _['context']['method'] = methods
        _['context']['endpoints'] = methods
        return _
    
    def get_rst_content(self):
        templateLoader = FileSystemLoader(searchpath=DIRPATH)
        method_map = {"detail": "get"}
        templateEnv = Environment(loader=templateLoader, lstrip_blocks=True, trim_blocks=True)
        templateEnv.filters['method_wrapper'] = lambda x: method_map.get(x, x)
        TEMPLATE_FILE = "api.jinja2.1.txt"
        template = templateEnv.get_template(TEMPLATE_FILE)
        # print(self.context)
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
