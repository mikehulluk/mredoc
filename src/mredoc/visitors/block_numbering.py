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



from mredoc.visitors import VisitorBase, ActionerBase


class BlockNumberer(ActionerBase, dict):

    def __init__(self, obj):
        dict.__init__(self)

        self.obj_counts_figure = 0
        self.obj_counts_eqn = 0
        self.obj_counts_table = 0
        self.obj_counts_code = 0
        self.obj_counts_list = 0

        self.visit(obj)


    def _ActionFigure(self, n, **kwargs):
        self.obj_counts_figure += 1
        n.number = self.obj_counts_figure

    def _ActionTable(self, n, **kwargs):
        self.obj_counts_table += 1
        n.number = self.obj_counts_table

    def _ActionEquationBlock(self, n, **kwargs):
        self.obj_counts_eqn += 1
        n.number = self.obj_counts_eqn


    def _ActionLink(self, n, **kwargs):
        pass
    def _ActionRef(self, n, **kwargs):
        pass

    def _ActionDocument(self, n, **kwargs):
        pass

    def _ActionHierachyScope(self, n, **kwargs):
        pass

    def _ActionImage(self, n, **kwargs):
        pass

    def _ActionSubfigure(self, n, **kwargs):
        pass

    def _ActionTableOfContents(self, n, **kwargs):
        pass

    def _ActionHeading(self, n, **kwargs):
        pass

    def _ActionRichTextContainer(self, n, **kwargs):
        pass
    def _ActionParagraph(self, n, **kwargs):
        pass

    def _ActionText(self, **kwargs):
        pass

    def _ActionEquation(self, n, **kwargs):
        pass

    def _ActionInlineEquation(self, n, **kwargs):
        pass

    def _ActionCodeListing(self, n, **kwargs):
        self.obj_counts_code += 1
        n.number = self.obj_counts_code

    def _ActionList(self, n, **kwargs):
        self.obj_counts_list += 1
        n.number = self.obj_counts_list

    def _ActionListItem(self, n, **kwargs):
        pass
