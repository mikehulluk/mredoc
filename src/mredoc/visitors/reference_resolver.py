
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

    class Mode:
        Collect = "Collect"
        Assign = "Assign"
    
    def __init__(self, doc):
        self.ref_map = {}
        self.Visit(doc, mode= RefResolver.Mode.Collect)
        self.Visit(doc, mode= RefResolver.Mode.Assign)
        
    
    def _ActionFigure(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and n.reflabel:
            self.ref_map[n.reflabel] = n

    def _ActionTable(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and n.reflabel:
            self.ref_map[n.reflabel] = n

    def _ActionEquationBlock(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and n.reflabel:
            self.ref_map[n.reflabel] = n
    
    def _ActionCodeBlock(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and n.reflabel:
            self.ref_map[n.reflabel] = n

    def _ActionList(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Collect and n.reflabel:
            self.ref_map[n.reflabel] = n

    
    def _ActionRef(self, n, mode=None, **kwargs):
        if mode == RefResolver.Mode.Assign:
            if isinstance(n.target, basestring):
                n.target = self.ref_map[n.target]
            
            
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
    
    def _ActionParagraphBlock(self, n, **kwargs):
        pass

    def _ActionText(self, **kwargs):
        pass

    def _ActionEquation(self, n, **kwargs):
        pass

    def _ActionInlineEquation(self, n, **kwargs):
        pass

    def _ActionListItem(self, n, **kwargs):
        pass
    
    def _ActionLink(self, n, **kwargs):
        pass
                
        
    
