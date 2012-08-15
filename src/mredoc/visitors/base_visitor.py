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


class VisitorBase(object):
    def visit(self, node, **kwargs):
        print node
        return node._accept_visitor(self, **kwargs)

    def visit_document(self, node, **kwargs):
        raise NotImplementedError()

    def visit_hierachyscope(self, node, **kwargs):
        raise NotImplementedError()

    def visit_figure(self, node, **kwargs):
        raise NotImplementedError()

    def visit_image(self, node, **kwargs):
        raise NotImplementedError()

    def visit_subfigure(self, node, **kwargs):
        raise NotImplementedError()

    def visit_tableofcontents(self, node, **kwargs):
        raise NotImplementedError()

    def visit_heading(self, node, **kwargs):
        raise NotImplementedError()

    def visit_richtextcontainer(self, node, **kwargs):
        raise NotImplementedError()

    def visit_paragraph(self, node, **kwargs):
        raise NotImplementedError()

    def visit_text(self, node, **kwargs):
        raise NotImplementedError()

    def visit_table(self, node, **kwargs):
        raise NotImplementedError()

    def visit_equationblock(self, node, **kwargs):
        raise NotImplementedError()

    def visit_equation(self, node, **kwargs):
        raise NotImplementedError()

    def visit_inlineequation(self, node, **kwargs):
        raise NotImplementedError()

    def visit_codelisting(self, node, **kwargs):
        raise NotImplementedError()

    def visit_link(self, node, **kwargs):
        raise NotImplementedError()

    def visit_ref(self, node, **kwargs):
        raise NotImplementedError()
