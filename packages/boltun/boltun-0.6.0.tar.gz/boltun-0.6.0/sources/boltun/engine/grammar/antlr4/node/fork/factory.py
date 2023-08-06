from __future__ import absolute_import, division, print_function

import attr


@attr.s
class ForkNodeFactory(object):

    def create_root_node(self):
        pass

    def create_choice_node(self):
        pass

    def create_content_node(self):
        pass
