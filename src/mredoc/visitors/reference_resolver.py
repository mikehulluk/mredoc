#!/usr/bin/python
# -*- coding: utf-8 -*-

# =====================================================================
# Copyright (c) 2012, Michael Hull
# All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ====================================================================

from mredoc.visitors import ActionerBase

class RefResolver(ActionerBase):

    class Mode(object):
        Collect = 'Collect'
        Assign = 'Assign'

    def __init__(self, doc):
        super(RefResolver, self).__init__()
        self.ref_map = {}
        self.visit(doc, mode=RefResolver.Mode.Collect)
        self.visit(doc, mode=RefResolver.Mode.Assign)


    def action_figure(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and node.reflabel:
            self.ref_map[node.reflabel] = node

    def action_table(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and node.reflabel:
            self.ref_map[node.reflabel] = node

    def action_equationblock(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and node.reflabel:
            self.ref_map[node.reflabel] = node

    def action_codelisting(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and node.reflabel:
            self.ref_map[node.reflabel] = node

    def action_list(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and node.reflabel:
            self.ref_map[node.reflabel] = node


    def action_ref(self, node, mode=None, **kwargs):
        if mode == RefResolver.Mode.Assign:
            if isinstance(node.target, basestring):
                node.target = self.ref_map[node.target]


    def action_document(self, node, **kwargs):
        pass

    def action_hierachyscope(self, node, **kwargs):
        pass


    def action_image(self, node, **kwargs):
        pass

    def action_subfigure(self, node, **kwargs):
        pass

    def action_tableofcontents(self, node, **kwargs):
        pass

    def action_heading(self, node, **kwargs):
        pass

    def action_richtextcontainer(self, node, **kwargs):
        pass

    def action_paragraph(self, node, **kwargs):
        pass

    def action_text(self, **kwargs):
        pass

    def action_equation(self, node, **kwargs):
        pass

    def action_inlineequation(self, node, **kwargs):
        pass

    def action_listitem(self, node, **kwargs):
        pass

    def action_link(self, node, **kwargs):
        pass



