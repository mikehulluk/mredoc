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







from mredoc.objects import VisitorBase
#from mredoc.objects import Heading, HierachyScope

from mhlibs.mredoc.objects import Heading, HierachyScope

class EmptySectionRemover(VisitorBase):
    """Each section should return False if it should be removed
    or True to be kept"""

    def _VisitDocument(self, n, **kwargs):
        return self.Visit(n.hierachy_root)

    def _VisitHierachyScope(self, n, **kwargs):
        new_children = [ c for c in n.children if self.Visit(c) ]
        
        print "NewChildren", new_children
        
        if len(new_children) == 0:
            return False
        if len(new_children) == 1 and isinstance( new_children[0] , Heading):
            #l = new_children[0]
            #print type(l)
            #print Heading
            #assert False
            
            return False

        print " - Keeping"
        
        n.children = new_children
        return True


    def _VisitFigure(self, n, **kwargs):
        if not n.subfigs:
            return False
        return True

    def _VisitImage(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitSubfigure(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitTableOfContents(self, n, **kwargs):
        return True
        raise NotImplementedError()

    def _VisitHeading(self, n, **kwargs):
        return True
        raise NotImplementedError()

    def _VisitRichTextContainer(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitText(self, **kwargs):
        raise NotImplementedError()

    def _VisitTable(self, n, **kwargs):
        return True
        raise NotImplementedError()

    def _VisitEquationBlock(self, n, **kwargs):
        if len(n.equations) == 0:
            return False
        return True
        raise NotImplementedError()

    def _VisitEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitPageBreak(self,n, **kwargs):

        return True
        raise NotImplementedError()

    def _VisitInlineEquation(self, n, **kwargs):
        raise NotImplementedError()

    def _VisitCodeBlock(self, n, **kwargs):
        return True
        raise NotImplementedError()


class NormaliseHierachyScope(VisitorBase):


    def _VisitDocument(self, n, **kwargs):
        return self.Visit(n.hierachy_root)

    def _VisitHierachyScope(self, n, **kwargs):
        for c in n.children:
            if not isinstance(c, HierachyScope): 
                continue
            self.Visit(c,**kwargs)

        if len(n.children) == 1 and isinstance( n.children[0], HierachyScope):
            n.children = n.children[0].children
