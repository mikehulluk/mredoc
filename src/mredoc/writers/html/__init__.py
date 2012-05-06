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



import xmlwitch
#from mredoc.writers.latex import DocumentVisitor

import os
import shutil
from mredoc import ImageTypes


from pygments import highlight
from pygments.lexers import PythonLexer, BashLexer
from pygments.formatters import HtmlFormatter
from mredoc.objects.core import Languages, Heading

import hashlib
from mredoc.visitors import VisitorBase
from mredoc.visitors import BlockNumberer

def EnsureExists(l):
    d = os.path.dirname(l)
    if not os.path.exists(d):
        os.makedirs(d)
    return l



def string_hash(s):
    return hashlib.md5(s).hexdigest()


class HTMLWriter(VisitorBase):


    @classmethod
    def BuildHTML(cls, doc, output_dir):
        return HTMLWriter(doc=doc, output_dir=output_dir)


    def _new_html_witch_obj(self,):
        o = xmlwitch.Builder(version='1.0', encoding='utf-8', indent="")
        o.write( """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">\n""")
        return o


    def _write_htmlheader_block(self):
        with self.xml.head:
            self.xml.title("MReDoc Generated Page")

            # Using the xmlwitch style does not work for this. I don't know why! To be investigated!
            self.xml.write(r"""<script type="text/x-mathjax-config"> MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}}); </script>""")
            self.xml.write(r"""<script src='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' type='text/javascript'> </script> """)
            self.xml.write(r"""<link rel="stylesheet" type="text/css" href="defaultstyle.css"/>""")

    def _write_file(self, contents, relative_filename):
        with open(os.path.join( self.output_dir, relative_filename),"w") as f:
            f.write( contents )



    def __init__(self, doc, output_dir):
        # Assign numbers to all the objects:
        self.block_numbers = BlockNumberer(doc)


        # Output locations:
        self.output_dir = EnsureExists(output_dir)
        self.output_dir_img = EnsureExists(output_dir+"/imgs/")


        self.xmlstack = [ [self._new_html_witch_obj(), 0] ]
        self.Visit(doc)

        # Write the output:
        self._write_file( str( self.xml), "index.html" )

        # Copy accross the CSS:
        import os
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        css_file = os.path.join(dir_path,"../../../resources/defaultstyle.css")
        shutil.copy(css_file, self.output_dir)

    @property
    def xml(self):
        return self.xmlstack[-1][0]



    # Visit the tree:
    def _VisitDocument(self, n, **kwargs):
        with self.xml.html:
            self._write_htmlheader_block()

            with self.xml.body:
                self.Visit( n.hierachy_root)





    def _write_block_captiontext(self,n):
            with self.xml.span(**{'class':'captionheader'} ):
                self.xml.write( n.get_ref_str() + ( ": " if n.caption else ""))
            with self.xml.span(**{'class':'captiontext'} ):
                if n.caption:
                    self.Visit(n.caption)




    def _VisitHierachyScopeInternal(self, n):
        block_type = "hierachyblock" if self.xmlstack[-1][1] != 0 else "pageblock"
        self.xmlstack[-1][1] += 1
        with self.xml.div(**{'class':block_type}) as d:
            for c in n.children:
                self.Visit(c)
        self.xmlstack[-1][1] -= 1

    def _VisitHierachyScope(self, n, **kwargs):
        if n.is_new_page:
            self.xmlstack.append( [self._new_html_witch_obj(), 0] )
            self._write_htmlheader_block()
            with self.xml.body:
                # In either case, visit all the children
                self._VisitHierachyScopeInternal(n)

                # Write out this block and link to it:
                xml_block, hierachy_depth = self.xmlstack.pop()
                assert hierachy_depth == 0

                xml_block = str(xml_block)

                # Write the new HTML file out:
                fNameShort =  "f_%s.html"%hashlib.md5(xml_block).hexdigest()
                self._write_file( xml_block, fNameShort )

                # Create a link in the local document:
                with self.xml.a(href=fNameShort):
                    if isinstance(n,basestring):
                        self.xml.write( n.is_new_page )
                    elif n.children and isinstance( n.children[0], Heading):
                        self.Visit( n.children[0].heading )
                    else:
                        self.xml.write("Link to UNKNOWN")
        else:
            self._VisitHierachyScopeInternal(n)





    def _VisitFigure(self, n, **kwargs):

        with self.xml.div(**{'class':'figblock'}) as d:

            with self.xml.figure:
                # Subfigures:
                for sf in n.subfigs:
                    self.Visit(sf)

                # Caption:
                with self.xml.figcaption:
                    self._write_block_captiontext(n)


    def _VisitImage(self, n, **kwargs):
        base_name = n.fNameBase
        dirname, name = os.path.split(base_name)

        # Copy the files accross:
        img_locs = {}
        for ext in [ImageTypes.SVG, ImageTypes.PDF, ImageTypes.PNG]:
            old_file = n.get_filename(type=ext)
            new_file = os.path.join( self.output_dir_img, name+"."+ext)
            shutil.copyfile(old_file, new_file)
            img_locs[ext] = new_file


        #srcfile = os.path.join(self.output_dir_img, name)
        with self.xml.a(href=img_locs[ImageTypes.SVG]):
            #a( None, )
            self.xml.img(None, src=img_locs[ImageTypes.PNG], alt="ImageFile", width="200")

    def _VisitSubfigure(self, n, **kwargs):
        return self.Visit(n.img)

    def _VisitHeading(self, n, **kwargs):
        header = "h%d"%self.xmlstack[-1][1]

        with self.xml[header]:
            self.Visit(n.heading)



    def _VisitTableOfContents(self, n, **kwargs):
        pass
    def _VisitPageBreak(self,n, **kwargs):
        return



    def _VisitTable(self, n, **kwargs):

        with self.xml.div( **{'class':'tableblock'} ) as d:


            with self.xml.table:
                with self.xml.tr:
                    for h in n.header:
                        with self.xml.th:
                            self.Visit(h)
                            #self.xml.write(h)

                for row in n.data:
                    with self.xml.tr:
                        for h in row:
                            with self.xml.td:
                                self.Visit(h)
                                #self.xml.write(h)

                # Caption:
                with self.xml.caption:
                    self._write_block_captiontext(n)
                    #self.xml.write( n.get_ref_str() )
                    #if n.caption:
                    #    self.Visit(n.caption)




    def _VisitEquationBlock(self, n, **kwargs):
        with self.xml.div(**{'class':'eqnblock'} ) as dout:


            with self.xml.div(**{'class':'eqnblockcontents math-header'}):# as d:
                self.xml.write(r"\begin{align*}")
                for e in n.equations:
                    self.Visit(e)
                    self.xml.write(r"\\")
                self.xml.write(r"\end{align*}")

            with self.xml.caption:
                self._write_block_captiontext(n)

    def _VisitEquation(self, n, **kwargs):
        self.xml.write( r" %s \\" % n.eqn  )




    def _VisitInlineEquation(self, n):
        with self.xml.span( **{'class':"math-header"} ):
            self.xml.write("$")
            
            self.Visit(n.eqn)
            self.xml.write("$")

    def _VisitRichTextContainer(self, n, **kwargs):
        for c in n.children:
            self.Visit(c)

    def _VisitParagraph(self, n, **kwargs):
        with self.xml.div(**{'class':'parablock'} ) :
                self.Visit(n.contents)



    def _VisitText(self, n, **kwargs):
        self.xml.write(n.text)


    def _VisitCodeBlock(self, n, **kwargs):
        lexer_lut = {
             Languages.Bash: BashLexer,
             Languages.Python: PythonLexer,
                 }
        lexer = lexer_lut.get( n.language, None)
        html = highlight(n.contents, PythonLexer(), HtmlFormatter()) if lexer else "<pre>%s</pre>"%n.contents

        with self.xml.div(**{"class":"codeblock"}) as d:

            with self.xml.div(**{"class":"codeblockcontents"}) as d:
                self.xml.write(html)
                
            with self.xml.div(**{"class":"codeblockcaption"}) as d:
                self._write_block_captiontext(n)


    def _VisitList(self, n, **kwargs):
        with self.xml.div(**{'class':'listblock'}):
            with self.xml.ul:
                for c in n.children:
                    self.Visit(c)

    def _VisitListItem(self, n, **kwargs):
        with self.xml.li:
            if n.header:
                self.Visit(n.header)
            self.Visit(n.para)


    def _VisitLink(self, n, **kwargs):
        with self.xml.a(href=n.target):
            self.xml.write(n.get_link_text())


    def _VisitRef(self, n, **kwargs):
        with self.xml.a:
            self.xml.write(n.get_link_text())

