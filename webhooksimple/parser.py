from abc import ABC, abstractmethod
import yaml
import sys
import os

from jinja2 import Template, Environment, BaseLoader

from .manager import *
from .models import Webhook

class Parser(ABC):
    def __init__(self, vars_file, hooks_file):
        cwd = os.path.abspath(os.getcwd())
        self.cwd = cwd

        vars_path = os.path.join(cwd, vars_file)
        vars = yaml.safe_load(open(vars_path, "r"))

        if "adapter" not in vars.keys():
            print("You need to provide an adapter in vars.yml")
            sys.exit(-1)
        self.vars = vars
        self.hooks_file = hooks_file

    def get_manager_instance(self):
        klass = globals()[self.vars['adapter']['name']]
        instance = klass(self.vars['adapter']['authentication'],
                         self.vars['adapter']['parameters'])

        return instance

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def export(self, webhook):
        pass

class YAMLParser(Parser):
    webhook_tpl_string = """
---
hooks:{% for hook in hooks %}
  - name: {{ hook.name }}
    resource: {{ hook.resource }}
    event: {{ hook.event }}
    target_url: {{ hook.target_url }}
{% endfor %}
"""

    def render(self):
        hooks_path = os.path.join(self.cwd, self.hooks_file)
        template = Template(open(hooks_path).read())

        return template.render(self.vars)

    def parse(self):
        hooks_descr = self.render()

        return yaml.safe_load(hooks_descr)

    def convert(self):
        hooks_dict = self.parse()

        hooks = []
        for hook_descr in hooks_dict['hooks']:
            wh = Webhook(**hook_descr)
            hooks.append(wh)

        return hooks

    def export(self, webhooks):
        tpl = Environment(loader=BaseLoader).from_string(self.webhook_tpl_string)
        rendered_tpl = tpl.render(hooks=webhooks)

        return rendered_tpl
