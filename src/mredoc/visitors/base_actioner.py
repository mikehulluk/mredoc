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


    def _VisitDocument(self, n, **kwargs):
        self._ActionDocument(n, **kwargs)
        self.Visit(n.hierachy_root, **kwargs) 

    def _VisitHierachyScope(self, n, **kwargs):
        self._ActionHierachyScope(n, **kwargs)
        for c in n.children:
            self.Visit(c, **kwargs)
        
        

    def _VisitFigure(self, n, **kwargs):
        self._ActionFigure( n, **kwargs)
        for c in n.subfigs:
            self.Visit(c, **kwargs)

    def _VisitImage(self, n, **kwargs):
        self._ActionImage( n, **kwargs)
        
    def _VisitSubfigure(self, n, **kwargs):
        self._ActionSubfigure( n, **kwargs)
        self.Visit(n.img, **kwargs)
        
    def _VisitTableOfContents(self, n, **kwargs):
        self._ActionTableOfContents( n, **kwargs)
        
    def _VisitHeading(self, n, **kwargs):
        self._ActionHeading( n, **kwargs)
        self.Visit(n.heading, **kwargs)
        
    def _VisitRichTextContainer(self, n, **kwargs):
        self._ActionParagraph( n, **kwargs)
        for c in n.children:
            self.Visit(c, **kwargs)
    
    def _VisitParagraphBlock(self, n, **kwargs):
        self._ActionParagraphBlock( n, **kwargs)
        self.Visit(n.contents, **kwargs)
        #for c in n.children:
        #    self.Visit(c, **kwargs)
        
    def _VisitEquationBlock(self, n, **kwargs):
        self._ActionEquationBlock( n, **kwargs)
        for c in n.equations:
            self.Visit(c, **kwargs)

    def _VisitList(self, n, **kwargs):
        self._ActionList(n, **kwargs)
        for c in n.children:
            self.Visit(c, **kwargs)
        
    
    def _VisitListItem(self, n, **kwargs):
        self._ActionListItem( n, **kwargs)
        self.Visit(n.para, **kwargs)


    def _VisitText(self, n, **kwargs):
        self._ActionText( **kwargs)
        
    def _VisitTable(self, n, **kwargs):
        self._ActionTable( n, **kwargs)

    def _VisitEquation(self, n, **kwargs):
        self._ActionEquation(n, **kwargs)
        
    def _VisitInlineEquation(self, n, **kwargs):
        self._ActionInlineEquation( n, **kwargs)
        
    def _VisitCodeBlock(self, n, **kwargs):
        self._ActionCodeBlock(n, **kwargs)
        
    def _VisitLink(self, n, **kwargs):
        self._ActionLink( n, **kwargs)

    def _VisitRef(self, n, **kwargs):
        self._ActionRef( n, **kwargs)
        



    def _ActionDocument(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionHierachyScope(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionFigure(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionImage(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionSubfigure(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionTableOfContents(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionHeading(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionParagraph(self, n, **kwargs):
        raise NotImplementedError()
    
    def _ActionParagraphBlock(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionText(self, **kwargs):
        raise NotImplementedError()

    def _ActionTable(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionEquationBlock(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionInlineEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionCodeBlock(self, n, **kwargs):
        raise NotImplementedError()

    def _ActionList(self, n, **kwargs):
        raise NotImplementedError()
    def _ActionListItem(self, n, **kwargs):
        raise NotImplementedError()
    
    def _ActionRef(self, n, **kwargs):
        raise NotImplementedError()
    def _ActionLink(self, n, **kwargs):
        raise NotImplementedError()
        
