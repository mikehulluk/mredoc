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
from mredoc.constants import ImageTypes, Languages
from mredoc.visitors import VisitorBase

_DOC_HEADER = r"""
\documentclass[9pt,headsepline,openany]{scrbook}   % list options between brackets


% Make the document single page:
\usepackage[PREVIEW_SINGLE_PAGEtightpage]{preview}
\renewcommand{\PreviewBorder}{1in}

\usepackage[T1]{fontenc}
\usepackage{lmodern}

\usepackage[margin=0.75in]{geometry}
\usepackage{amsmath}
\usepackage{hyperref}

\usepackage{caption}
\captionsetup{format=hang, font=small,labelfont=bf,labelsep=endash, margin=5pt }

\usepackage[usenames,dvipsnames]{xcolor}

\hypersetup{
    bookmarks=true,         % show bookmarks bar?
    unicode=false,          % non-Latin characters in Acrobat's bookmarks
    pdftoolbar=true,        % show Acrobat's toolbar?
    pdfmenubar=true,        % show Acrobat's menu?
    pdffitwindow=false,     % window fit to page when opened
    pdfstartview={FitH},    % fits the width of the page to the window
    pdfnewwindow=true,      % links in new window
    colorlinks=true,       % false: boxed links; true: colored links
    linkcolor=Blue,          % color of internal links
    citecolor=green,        % color of links to bibliography
    filecolor=magenta,      % color of file links
    urlcolor=cyan           % color of external links
}


\usepackage{listings}
\lstset{% general command to set parameter(s)
basicstyle=\footnotesize, % print whole listing small
%basicstyle=\footnotesize, % print whole listing small
keywordstyle=\color{blue}, %\bfseries\underbar,
% underlined bold black keywords
identifierstyle=, % nothing happens
commentstyle=\color{OliveGreen}, % white comments
stringstyle=\ttfamily, % typewriter type for strings
showstringspaces=false, % no special string spaces
language=python,
frame=lines,
float=tbfh}


\usepackage{graphicx}
\usepackage{placeins}

\usepackage{afterpage}

%\usepackage{bera}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\usepackage[T1]{fontenc}

\setcounter{tocdepth}{10}


\usepackage{longtable}
\usepackage{tabu}




\begin{document}
\begin{preview}
\mainmatter

"""


_DOC_FOOTER = r"""
\end{preview}
\end{document}

"""



#_HEADING_BY_DEPTH = {
#    1: 'section',
#    2: 'subsection',
#    3: 'subsubsection',
#    4: 'paragraph',
#    5: 'subparagraph',
#    }


# For book:
_HEADING_BY_DEPTH = {
    1: 'part*',
    2: 'chapter',
    3: 'section',
    4: 'subsection',
    5: 'subsubsection',
    6: 'paragraph',
    7: 'subparagraph',
    }




class LatexWriter(VisitorBase):


    @classmethod
    def build_pdf(cls, doc, filename, single_page=False):
        # Allow '~' in the pathname:
        filename = os.path.expanduser(filename)

        writer = LatexWriter(doc, single_page=single_page)
        tex_str = writer.output_tex
        from mredoc.util.toolchecker import ExternalTools
        ExternalTools.run_pdflatex(tex_str, output_filename=filename)
        print 'Successfully written PDF to: ', filename


    def __init__(self, doc, single_page):
        super(LatexWriter, self).__init__()
        self.hierachy_depth = 0
        self.single_page = single_page


        self.output_tex = self.visit(doc)



    def visit_figure(self, node, **kwargs):
        if len(node.subfigs) == 1:
            pass

        caption = self.visit(node.caption) if node.caption else ''
        reflabel = node.reflabel if node.reflabel else ''
        return '\n'.join([
            (r"""\begin{figure}[h!]""" if not self.single_page else ''),
            (r"""\centering""" if not self.single_page else ''),
            '\n'.join([self.visit(s) for s in node.subfigs]),
            r"""\caption{%s}""" % caption,
            (r"""\label{%s}""" % reflabel if reflabel else ''),
           ( r"""\end{figure}""" if not self.single_page else '' ),
            ])



    def visit_image(self, node, **kwargs):
        return r"""\includegraphics{%s}""" \
            % node.get_filename(file_type=ImageTypes.PDF)

    def visit_subfigure(self, node, **kwargs):
        return self.visit(node.img)

    def visit_tableofcontents(self, node, **kwargs):
        tables = []

        tables.extend([
        r'\begingroup',
        r'\tableofcontents',
        r'\let\clearpage\relax',
        r'\listoftables',
        r'\endgroup',

        ] )

        return ''.join( t+'\n' for t in tables)

    def visit_document(self, node, **kwargs):
        return _DOC_HEADER.replace('PREVIEW_SINGLE_PAGE','' if not self.single_page else 'active,') + \
               self.visit(node.hierachy_root, **kwargs)  + \
               _DOC_FOOTER

    def visit_hierachyscope(self, node, **kwargs):
        self.hierachy_depth += 1
        txt = '\n'.join([self.visit(child) for child in node.children])
        if node.is_new_page:
            txt =  "\n\\newpage\n" + txt
        self.hierachy_depth -= 1
        return txt

    def visit_heading(self, node, **_kwargs):
        # NASTY TEMP HACK TO LET MIKE FINISH SOME DOCS:
        if self.hierachy_depth > 7:
            self.hierachy_depth = 7

        assert self.hierachy_depth <= 7, \
            'Deep documents not properly handled yet. TODO FIX HERE'

        heading_type = _HEADING_BY_DEPTH[self.hierachy_depth]
        return "\FloatBarrier\n\%s{%s}\n\FloatBarrier\n" % \
                (heading_type, self.visit(node.heading))

    def visit_richtextcontainer(self, node, **_kwargs):
        return ' '.join([self.visit(child) for child in node.children])

    def visit_paragraph(self, node, **_kwargs):
        return self.visit(node.contents)

    def visit_text(self, node, **_kwargs):
        return node.text.replace('&', "\&").replace('_', "\_")

    def visit_table(self, node, **_kwargs):
        buildline = lambda line: ' & '.join([self.visit(l) for l in line]) + r" \\"
        #buildline = lambda line: ' & '.join([self.visit(l) for l in line]) + r" \tablularnewline"

        header_line = buildline(node.header)
        contents = '\n'.join([buildline(child) for child in node.data])
        alignment = 'c' * len(node.header)

        return '\n'.join([
            r'''\afterpage{\clearpage}'''
            r'''{\footnotesize ''',
            r"""\begin{table}[hbtp]""",
            r"""\tabulinesep=1.5mm""",
            r"""\caption{%s}""" % self.visit(node.caption) if node.caption else "",
            r"""\begin{longtabu}{%s}""" % alignment,
            r"""\firsthline\hline""",
            header_line,
            r"""\hline""",
            contents,
            r"""\lastline\hline""",
            r"""\end{longtabu}""",
            r"""\end{table}""",
            r'''}''',
            r'''\afterpage{\clearpage}'''
        ])






    def visit_equationblock(self, node, **_kwargs):
        if not node.equations:
            return ''
        return '\n'.join([
            r"""\begin{align*}""",
            '\n'.join([self.visit(s) + r"\\" for s in node.equations] ),
            r"""\end{align*}""",
            ])

    def visit_equation(self, node, **_kwargs):
        return node.eqn


    def visit_pagebreak(self, _node, **_kwargs):
        assert False
        return r"""""" + "\n\n"
        return r"""\newpage""" + "\n\n"


    def visit_codelisting(self, node, **kwargs):
        language = {
            Languages.Python:'python',
            Languages.Bash:'bash',
            Languages.Verbatim:'', #Listings package uses empty language
            }[node.language]

        caption = self.visit(node.caption) if node.caption else ""
        options = {
            'caption':'{%s}' % caption,
            'label': node.reflabel
            }
        # Only include values with value:
        opt_str = ",".join('%s=%s' % (key, v) for (key, v) in options.iteritems() if v)
        opt_str = "[%s]" % opt_str if opt_str else ""

        return "\n".join([
            r"""\lstset{language=%s}"""%language,
            r"""\begin{lstlisting}%s""" % opt_str,
            node.contents,
            r"""\end{lstlisting}""",
            ])

    def visit_list(self, node, **_kwargs):
        if not node.children:
            return
        return "\n".join([
            r"\begin{itemize}",
            "\n".join([self.visit(child) for child in node.children]),
            r"\end{itemize}",
        ])

    def visit_listitem(self, node, **_kwargs):
        return r"\item %s" % self.visit(node.para)

    def visit_inlineequation(self, node, **_kwargs):
        return '$%s$' % self.visit(node.eqn)

    def visit_link(self, node, **_kwargs):
        return "\href{%s}{%s}" % (node.target, node.get_link_text())
    def visit_ref(self, node, **_kwargs):
        return r"%s \ref{%s}" % (node.target.get_type_str(),
                                 node.target.reflabel)
