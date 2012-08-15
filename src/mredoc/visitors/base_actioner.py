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









from mredoc.visitors import VisitorBase

class ActionerBase(VisitorBase):


    def _visit_document(self, node, **kwargs):
        self.action_document(node, **kwargs)
        self.visit(node.hierachy_root, **kwargs)

    def visit_hierachyscope(self, node, **kwargs):
        self.action_hierachyscope(node, **kwargs)
        for child in node.children:
            self.visit(child, **kwargs)



    def visit_figure(self, node, **kwargs):
        self.action_figure(node, **kwargs)
        for child in node.subfigs:
            self.visit(child, **kwargs)

    def visit_image(self, node, **kwargs):
        self.action_image(node, **kwargs)

    def visit_subfigure(self, node, **kwargs):
        self.action_subfigure(node, **kwargs)
        self.visit(node.img, **kwargs)

    def visit_tableofcontents(self, node, **kwargs):
        self.action_tableofcontents(node, **kwargs)

    def visit_heading(self, node, **kwargs):
        self.action_heading(node, **kwargs)
        self.visit(node.heading, **kwargs)

    def visit_richtextcontainer(self, node, **kwargs):
        self.action_richtextcontainer(node, **kwargs)
        for child in node.children:
            self.visit(child, **kwargs)

    def visit_paragraph(self, node, **kwargs):
        self.action_paragraph(node, **kwargs)
        self.visit(node.contents, **kwargs)

    def visit_equationblock(self, node, **kwargs):
        self.action_equationblock(node, **kwargs)
        for child in node.equations:
            self.visit(child, **kwargs)

    def visit_list(self, node, **kwargs):
        self.action_list(node, **kwargs)
        for child in node.children:
            self.visit(child, **kwargs)


    def visit_listItem(self, node, **kwargs):
        self.action_listItem(node, **kwargs)
        self.visit(node.para, **kwargs)


    def visit_text(self, node, **kwargs):
        self.action_text(**kwargs)

    def visit_table(self, node, **kwargs):
        self.action_table(node, **kwargs)

    def visit_equation(self, node, **kwargs):
        self.action_equation(node, **kwargs)

    def visit_inlineequation(self, node, **kwargs):
        self.action_inlineequation(node, **kwargs)

    def visit_codelisting(self, node, **kwargs):
        self.action_codelisting(node, **kwargs)

    def visit_link(self, node, **kwargs):
        self.action_link(node, **kwargs)

    def visit_ref(self, node, **kwargs):
        self.action_ref(node, **kwargs)




    def action_document(self, node, **kwargs):
        raise NotImplementedError()

    def action_hierachyscope(self, node, **kwargs):
        raise NotImplementedError()

    def action_figure(self, node, **kwargs):
        raise NotImplementedError()

    def action_image(self, node, **kwargs):
        raise NotImplementedError()

    def action_subfigure(self, node, **kwargs):
        raise NotImplementedError()

    def action_tableofcontents(self, node, **kwargs):
        raise NotImplementedError()

    def action_heading(self, node, **kwargs):
        raise NotImplementedError()

    def action_richtextcontainer(self, node, **kwargs):
        raise NotImplementedError()

    def action_paragraph(self, node, **kwargs):
        raise NotImplementedError()

    def action_text(self, **kwargs):
        raise NotImplementedError()

    def action_table(self, node, **kwargs):
        raise NotImplementedError()

    def action_equationblock(self, node, **kwargs):
        raise NotImplementedError()

    def action_equation(self, node, **kwargs):
        raise NotImplementedError()

    def action_inlineequation(self, node, **kwargs):
        raise NotImplementedError()

    def action_codeblock(self, node, **kwargs):
        raise NotImplementedError()

    def action_list(self, node, **kwargs):
        raise NotImplementedError()
    def action_listItem(self, node, **kwargs):
        raise NotImplementedError()

    def action_ref(self, node, **kwargs):
        raise NotImplementedError()
    def action_link(self, node, **kwargs):
        raise NotImplementedError()

