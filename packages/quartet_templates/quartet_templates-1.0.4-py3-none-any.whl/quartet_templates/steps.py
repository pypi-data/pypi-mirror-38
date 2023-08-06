# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.

import sys
import random
from uuid import uuid4
from time import time
from datetime import datetime

from jinja2.environment import Environment
from quartet_templates.models import Template
from quartet_capture.rules import Step, RuleContext


class TemplateStep(Step):
    """
    Will load a template based on the step parameter "Template Name" and
    render it using a combination of rule data, context variables and
    the template variables.
    """

    def execute(self, data, rule_context: RuleContext):
        self.info('Looking for Step Parameter with name "Template Name"...')
        template_name = self.get_parameter(
            'Template Name',
            raise_exception=True
        )
        context_key = self.get_parameter("Context Key")
        self.info("Template Name parameter value found: %s.  "
                  "Looking up Template...", template_name)
        template = Template.objects.get(name=template_name)
        self.info("Found template...rendering...")
        environment = Environment(
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=self.get_boolean_parameter('Auto Escape', True)
        )
        ret = template.render({'data': data, 'rule_context': rule_context,
                               'step_parameters': self.parameters,
                               'task_parameters': self.get_task_parameters(
                                   rule_context
                               ),
                               'epoch': time(),
                               'random': random.randint(1, sys.maxsize),
                               'UUID': str(uuid4()),
                               'datetime': datetime.isoformat(datetime.now())
                               }, environment=environment)
        self.info("Template response summary %s:", ret[:10000])
        if context_key:
            self.info("Placing rendered content into context key %s.",
                      context_key)
            rule_context.context[context_key] = ret
        else:
            self.info("Returning rendered content to the rule.")
            data = ret
        return data

    @property
    def declared_parameters(self):
        return {
            "Template Name": "The name of the template to load and render.",
            "Context Key": "The context key to place the output into.  If "
                           "none is specified, the output will be returned to "
                           "the rule in place of the inbound data.",
            "Auto Escape": "Whether or not the jinja2 template should be "
                           "auto escaped.  Default is True, set to False if "
                           "you are embedding XML within XML, etc."
        }

    def on_failure(self):
        pass
