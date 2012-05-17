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
    def Visit(self, n, **kwargs):
        print n
        return n._AcceptVisitor(self, **kwargs)

    def _VisitDocument(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitHierachyScope(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitFigure(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitImage(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitSubfigure(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitTableOfContents(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitHeading(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitRichTextContainer(self, n, **kwargs):
        raise NotImplementedError()
    
    def _VisitParagraph(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitText(self,n, **kwargs):
        raise NotImplementedError()

    def _VisitTable(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitEquationBlock(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitInlineEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitCodeBlock(self, n, **kwargs):
        raise NotImplementedError()
    
    def _VisitLink(self, n, **kwargs):
        raise NotImplementedError()
    
    def _VisitRef(self, n, **kwargs):
        raise NotImplementedError()
