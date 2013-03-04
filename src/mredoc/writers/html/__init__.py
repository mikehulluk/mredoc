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


import os
import shutil
import hashlib
import re
import string

from pygments import highlight
from pygments.lexers import PythonLexer, BashLexer
from pygments.formatters import HtmlFormatter

from mredoc.constants import ImageTypes, Languages
from mredoc.writers.html import xmlwitch
from mredoc.visitors import VisitorBase
from mredoc.visitors import BlockNumberer
from mredoc.util.misc import ensure_location_exists



class HTMLWriter(VisitorBase):

    @classmethod
    def build_html(cls, doc, output_dir, clear_dir=False):
        return HTMLWriter(doc=doc, output_dir=output_dir,clear_dir=clear_dir)


    @classmethod
    def _new_html_witch_obj(cls):
        obj = xmlwitch.Builder(version='1.0', encoding='utf-8', indent='')
        obj.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.1//EN" "http://www.w3.org/TR/xhtml-basic/xhtml-basic11.dtd">\n"""
                )
        return obj


    def _write_htmlheader_block(self):
        with self.xml.head:
            self.xml.title('MReDoc Generated Page')

            # Using the xmlwitch style does not work for this. I don't know why! To be investigated!
            self.xml.write(r"""<script type="text/x-mathjax-config"> MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}}); </script>""")
            self.xml.write(r"""<script src='http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML' type='text/javascript'> </script> """)
            self.xml.write(r"""<link rel="stylesheet" type="text/css" href="defaultstyle.css"/>""")

    def _write_file(self, contents, relative_filename):
        fname = os.path.join(self.output_dir, relative_filename)
        with open(fname, 'w') as fobj:
            fobj.write(contents)



    def __init__(self, doc, output_dir, clear_dir=False):
        assert clear_dir==False, "clear_dir enabled, but I havne't worked ou how to do this safely! (in case clear_dir = ~/ by accident for example!!"
        output_dir = os.path.expanduser(output_dir)

        super(HTMLWriter, self).__init__()
        # Assign numbers to all the objects:
        self.block_numbers = BlockNumberer(doc)

        # Output locations:
        self.output_dir = ensure_location_exists(output_dir)
        self.output_dir_img = ensure_location_exists(output_dir + '/imgs/')

        self.xmlstack = [[HTMLWriter._new_html_witch_obj(), 0]]
        self.visit(doc)

        # Write the output:
        self._write_file(str(self.xml), 'index.html')

        # Copy accross the CSS:
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        pkg_path = os.path.join(dir_path, '../../../')
        css_file = os.path.join(pkg_path, 'resources/defaultstyle.css')

        #shutil.copy(css_file, self.output_dir)
        op_css = self.output_dir+"/defaultstyle.css"
        if not os.path.exists(op_css):
            os.symlink(css_file, op_css )


    @property
    def xml(self):
        return self.xmlstack[-1][0]



    # visit the tree:
    def visit_document(self, node, **_kwargs):
        with self.xml.html:
            self._write_htmlheader_block()

            with self.xml.body:
                with self.xml.div(**{'class':'pageblock'}):

                    self.visit(node.hierachy_root)


    def _write_block_captiontext(self, node):
        with self.xml.span(**{'class':'captionheader'}):
            self.xml.write(node.get_ref_str() + (": " if node.caption else ""))
        with self.xml.span(**{'class':'captiontext'}):
            if node.caption:
                self.visit(node.caption)




    def visit_hierachyscopeinternal(self, node):
        block_type = ('hierachyblock' if self.xmlstack[-1][1]
                      != 0 else 'pageblock')
        block_type = 'hierachyblock' if self.xmlstack[-1][1]  != 0 else ''

        self.xmlstack[-1][1] += 1
        with self.xml.div(**{'class': block_type}):
            for child in node.children:
                self.visit(child)
        self.xmlstack[-1][1] -= 1

    def visit_hierachyscope(self, node, **_kwargs):
        from mredoc.objects import _Heading

        if node.is_new_page:
            self.xmlstack.append([HTMLWriter._new_html_witch_obj(), 0])
            self._write_htmlheader_block()
            with self.xml.body:
                with self.xml.div(**{'class':'pageblock'}):

                    # In either case, visit all the children
                    self.visit_hierachyscopeinternal(node)

                    # Write out this block and link to it:
                    (xml_block, hierachy_depth) = self.xmlstack.pop()
                    assert hierachy_depth == 0

                    xml_block = str(xml_block)

                    # Write the new HTML file out:
                    file_hash = hashlib.md5(xml_block).hexdigest()
                    fname_short = 'f_%s.html' % file_hash
                    self._write_file(xml_block, fname_short)

                    # Create a link in the local document:
                    with self.xml.p():
                        with self.xml.a(href=fname_short):
                            if isinstance(node, basestring):
                                self.xml.write(node.is_new_page)
                            elif node.children and isinstance(node.children[0], _Heading):
                                self.visit(node.children[0].heading)
                            else:
                                self.xml.write('Link to UNKNOWN')
        else:
            self.visit_hierachyscopeinternal(node)





    def visit_figure(self, node, **_kwargs):

        with self.xml.div(**{'class': 'figblock'}):

            with self.xml.figure:
                # Caption:
                with self.xml.figcaption:
                    self._write_block_captiontext(node)
                # Subfigures:
                for subfig in node.subfigs:
                    self.visit(subfig)



    def visit_image(self, node, **_kwargs):
        base_name = node.fNameBase
        (_dirname, name) = os.path.split(base_name)

        # Copy the files accross:
        img_locs = {}
        for ext in [ImageTypes.SVG, ImageTypes.PNG]:
            old_file = node.get_filename(file_type=ext)
            h = hashlib.new('md5')
            with open(old_file) as f:
                h.update(f.read() )

            new_filename = name + h.hexdigest() + '.' + ext
            new_file = os.path.join(self.output_dir_img, new_filename)
            shutil.copyfile(old_file, new_file)
            img_locs[ext] = new_filename

        rel_loc = os.path.relpath(self.output_dir_img, self.output_dir)

        node = lambda path: os.path.normpath(os.path.join(rel_loc, path))
        with self.xml.a(href=node(img_locs[ImageTypes.SVG])):
            self.xml.img(None, src=node(img_locs[ImageTypes.PNG]),
                         alt='ImageFile', width='200')

    def visit_subfigure(self, node, **_kwargs):
        return self.visit(node.img)

    def visit_heading(self, node, **_kwargs):
        header = 'h%d' % self.xmlstack[-1][1]
        with self.xml[header]:
            self.visit(node.heading)

    def visit_tableofcontents(self, _node, **_kwargs):
        pass

    def visit_pagebreak(self, _node, **_kwargs):
        return

    def visit_table(self, node, **_kwargs):
        with self.xml.div(**{'class': 'tableblock'}):

            with self.xml.table:
                with self.xml.thead:
                    with self.xml.tr:
                        for colheader in node.header:
                            with self.xml.th:
                                self.visit(colheader)

                for row in node.data:
                    with self.xml.tr:
                        for cell in row:
                            with self.xml.td:
                                self.visit(cell)
                # Caption:
                with self.xml.div(**{'class':'tableblockcaption'}):
                    self._write_block_captiontext(node)

    def visit_equationblock(self, node, **_kwargs):
        with self.xml.div(**{'class': 'eqnblock'}):

            with self.xml.div(**{'class': 'eqnblockcontents math-header'
                              }):
                self.xml.write(r"\begin{align*}")
                for eqn in node.equations:
                    self.visit(eqn)
                    self.xml.write(r"\\")
                self.xml.write(r"\end{align*}")

            with self.xml.caption:
                self._write_block_captiontext(node)

    def visit_equation(self, node, **_kwargs):
        self.xml.write(r" %s \\" % node.eqn)

    def visit_inlineequation(self, node):
        with self.xml.span(**{'class': 'math-header'}):
            self.xml.write('$')
            self.visit(node.eqn)
            self.xml.write('$')

    def visit_richtextcontainer(self, node, **_kwargs):
        for child in node.children:
            self.visit(child)
            self.xml.write(' ')

    def visit_paragraph(self, node, **_kwargs):
        with self.xml.div(**{'class': 'parablock'}):
            self.visit(node.contents)

    def visit_text(self, node, **_kwargs):
        # Resolves the possible ':XYZ:' tags
        # There are 2 possibilities:
        # a. ":XYZ:thequickbrownfox"
        # b. "asjdlask :XYZ:`jkl` asjdkl :XYZ:`asdsa` sdjfls "

        # If the second case applies, rewrite it as the first by enclosing
        # the entire string in `` (except the role), then apply the first:
        text = node.text
        r2 = re.compile(r"""^:(?P<role>\w+):(?P<text>.*)$""")
        m = r2.match(text)
        if m:
            text = ':%s:`%s`' % ( m.groupdict()['role'], m.groupdict()['text'] )

        r1 = re.compile(r""":(?P<role>\w+):`(?P<text>.*?)`""")

        def repl_func(m):
            role = m.groupdict()['role'] 
            assert role in ['success','warning','err'],'Unsupported role: %s' % role
            return string.Template("""<span class='mrd_${role}'>${text}</span>""").substitute(m.groupdict())
        text = r1.sub( repl_func, text)






        #

        self.xml.write(text)

    def visit_codelisting(self, node, **_kwargs):
        import cgi
        lexer_lut = {Languages.Bash: BashLexer,
                     Languages.Python: PythonLexer}
        lexer = lexer_lut.get(node.language, None)

        if lexer:
            html = highlight(node.contents,
                             PythonLexer(),
                             HtmlFormatter())
        else:
            html = '<pre>%s</pre>' % cgi.escape(node.contents)

        with self.xml.div(**{'class': 'codeblock'}):
            with self.xml.div(**{'class': 'codeblockcaption'}):
                self._write_block_captiontext(node)
            with self.xml.div(**{'class': 'codeblockcontents'}):
                self.xml.write(html)


    def visit_list(self, node, **_kwargs):
        with self.xml.div(**{'class': 'listblock'}):
            with self.xml.ul:
                for child in node.children:
                    self.visit(child)

    def visit_listitem(self, node, **_kwargs):
        with self.xml.li:
            if node.header:
                self.visit(node.header)
            self.visit(node.para)

    def visit_link(self, node, **_kwargs):
        with self.xml.a(href=node.target):
            self.xml.write(node.get_link_text())

    def visit_ref(self, node, **_kwargs):
        with self.xml.a:
            self.xml.write(node.get_link_text())

