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


class BlockNumberer(ActionerBase, dict):

    def __init__(self, obj):
        super(BlockNumberer, self).__init__()

        self.obj_counts_figure = 0
        self.obj_counts_eqn = 0
        self.obj_counts_table = 0
        self.obj_counts_code = 0
        self.obj_counts_list = 0

        self.visit(obj)

    def action_figure(self, node, **kwargs):
        self.obj_counts_figure += 1
        node.number = self.obj_counts_figure

    def action_table(self, node, **kwargs):
        self.obj_counts_table += 1
        node.number = self.obj_counts_table

    def action_equationblock(self, node, **kwargs):
        self.obj_counts_eqn += 1
        node.number = self.obj_counts_eqn


    def action_link(self, node, **kwargs):
        pass
    def action_ref(self, node, **kwargs):
        pass

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

    def action_codelisting(self, node, **kwargs):
        self.obj_counts_code += 1
        node.number = self.obj_counts_code

    def action_list(self, node, **kwargs):
        self.obj_counts_list += 1
        node.number = self.obj_counts_list

    def action_listitem(self, node, **kwargs):
        pass
