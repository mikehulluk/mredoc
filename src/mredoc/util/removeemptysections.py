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
from mredoc.objects.core import _Heading, _HierachyScope

class EmptySectionRemover(VisitorBase):
    """Each section should return False if it should be removed
    or True to be kept"""

    def _visit_document(self, node, **kwargs):
        return self.visit(node.hierachy_root)

    def visit_hierachyscope(self, node, **kwargs):
        new_children = [child for child in node.children if self.visit(child)]

        if len(new_children) == 0:
            return False
        if len(new_children) == 1 and \
           isinstance(new_children[0], _Heading):
            return False

        node.children = new_children
        return True


    def visit_figure(self, node, **kwargs):
        if not node.subfigs:
            return False
        return True

    def visit_image(self, node, **kwargs):
        raise NotImplementedError()

    def visit_subfigure(self, node, **kwargs):
        raise NotImplementedError()

    def visit_tableofcontents(self, node, **kwargs):
        return True

    def visit_heading(self, node, **kwargs):
        return True

    def visit_richtextcontainer(self, node, **kwargs):
        raise NotImplementedError()

    def visit_paragraph(self, node, **kwargs):
        if not node.contents:
            return False
        return True

    def visit_list(self, node, **kwargs):
        if not node.children:
            return False
        return True

    def visit_text(self, **kwargs):
        raise NotImplementedError()

    def visit_table(self, node, **kwargs):
        return True

    def visit_equationblock(self, node, **kwargs):
        if len(node.equations) == 0:
            return False
        return True

    def visit_equation(self, node, **kwargs):
        raise NotImplementedError()

    def visit_pagebreak(self, node, **kwargs):
        return True

    def visit_inlineequation(self, node, **kwargs):
        raise NotImplementedError()

    def visit_codelisting(self, node, **kwargs):
        return True


class NormaliseHierachyScope(VisitorBase):

    def _visit_document(self, node, **kwargs):
        return self.visit(node.hierachy_root)

    def visit_hierachyscope(self, node, **kwargs):
        for child in node.children:
            if not isinstance(child, _HierachyScope):
                continue
            self.visit(child, **kwargs)

        if len(node.children) == 1 and \
           isinstance(node.children[0], _HierachyScope):
            node.children = node.children[0].children
