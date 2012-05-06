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
from mredoc.objects import ImageTypes, Languages
from mredoc.visitors import VisitorBase

doc_header = r"""
\documentclass[8pt]{scrartcl}   % list options between brackets
\usepackage[margin=0.5in]{geometry}
\usepackage{amsmath}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{hyperref}
\setcounter{secnumdepth}{-1} 

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

\usepackage{bera}
\renewcommand*\familydefault{\sfdefault} %% Only if the base font of the document is to be sans serif
\usepackage[T1]{fontenc}
\begin{document}
"""


doc_footer = r"""
\end{document}

"""



heading_by_depth = {
    2:"section",
    3:"subsection",
    4:"subsubsection",
    5:"paragraph",
    }






class LatexWriter(VisitorBase):

    _working_dir = "/tmp/ltxwriter/"

    @classmethod
    def _compile_pdf(cls, tex_str, output_filename):
        #working_dir = working_dir or "/tmp"
        if not os.path.exists(cls._working_dir):
            os.makedirs(cls._working_dir)
        tex_file = cls._working_dir + "/eqnset.tex"
        tex_pdf = cls._working_dir + "/eqnset.pdf"
        # Write to disk and compile:
        with open(tex_file,'w') as f:
            f.write(tex_str)
        os.system("pdflatex -output-directory %s %s"%(cls._working_dir, tex_file))
        os.system("pdflatex -output-directory %s %s"%(cls._working_dir, tex_file))
        os.system("pdflatex -output-directory %s %s"%(cls._working_dir, tex_file))
        os.system("cp %s %s"%(tex_pdf,output_filename) )
        if not os.path.exists(output_filename):
            raise ValueError("Something went wrong building pdf")

    @classmethod
    def BuildPDF(cls, doc, filename):
        writer = LatexWriter(doc)
        tex_str = writer.output_tex
        print tex_str
        cls._compile_pdf(tex_str, filename)
        print 'Build pdf:', filename


    def __init__(self, doc):
        self.hierachy_depth=0
        self.output_tex = self.Visit(doc)


    
    def _VisitFigure(self, n, **kwargs):
        if len( n.subfigs) == 1:
            pass

        return "\n".join([ 
            r"""\begin{figure}[htb]""",
            r"""\centering""",
            "\n".join( [ self.Visit(s) for s in n.subfigs] ),
            r"""\caption{%s}"""%self.Visit(n.caption),
            r"""\label{%s}"""%n.reflabel if n.reflabel else "",
            r"""\end{figure}""",
            ]) 
        
       

    def _VisitImage(self, n, **kwargs):
        return r"""\includegraphics{%s}"""%( n.get_filename(type=ImageTypes.PDF) )

    def _VisitSubfigure(self, n, **kwargs):
        return self.Visit(n.img)
        


    def _VisitTableOfContents(self, n, **kwargs):
        return r"\tableofcontents"

    # Visit the tree:
    def _VisitDocument(self, n, **kwargs):
        return doc_header + self.Visit(n.hierachy_root,**kwargs)  + doc_footer

    def _VisitHierachyScope(self, n, **kwargs):
        self.hierachy_depth += 1
        r = "\n".join( [ self.Visit(c) for c in n.children])
        self.hierachy_depth -= 1
        return r

    def _VisitHeading(self, n, **kwargs):
        heading_type = heading_by_depth[self.hierachy_depth]
        return "\%s{%s}\n"%(heading_type, self.Visit(n.heading) )

    def _VisitRichTextContainer(self, n, **kwargs):
        return "".join( [ self.Visit(c) for c in n.children])

    def _VisitParagraph(self, n, **kwargs):
        return self.Visit(n.contents)

    def _VisitText(self, n, **kwargs):
        return n.text.replace("&","\&").replace("_","\_")

    def _VisitTable(self, n, **kwargs):
        buildline = lambda line: " & ".join( [self.Visit(l) for l in line ]) + r" \\"
        
        header_line = buildline( n.header)
        contents = "\n".join( [buildline(c) for c in n.data] )
        alignment = "c"*len(n.header)

        return "\n".join( [
            r"""\begin{table}[h]""",
            r"""\begin{longtable}{%s}"""%alignment,
            r"""\toprule""",
            header_line,
            r"""\midrule""",
            contents,
            r"""\bottomrule""",
            r"""\end{longtable}""",
            r"""\caption{%s}"""%n.caption if n.caption else "",
            r"""\label{%s}"""%n.reflabel if n.reflabel else "",
            r"""\end{table}""",
        ])
        
        
        

        

    def _VisitEquationBlock(self, n, **kwargs):
        if  not n.equations: return  ""
        return "\n".join([ 
            r"""\begin{align*}""",
            "\n".join( [ self.Visit(s) + r"\\" for s in n.equations] ),
            r"""\end{align*}""",
            ]) 

    def _VisitEquation(self, n, **kwargs):
        return n.eqn


    def _VisitPageBreak(self,n, **kwargs):
        return r"""\newpage""" + "\n\n"
    
    
    def _VisitCodeBlock(self,n, **kwargs):
        language = {
            Languages.Python:'python',
            Languages.Bash:'bash',
            Languages.Verbatim:'', #Listings package uses empty language
            }[n.language]
       
        options = {
            'caption':'{%s}'%self.Visit(n.caption) if n.caption else "",
            'label': n.reflabel
            }
        # Only include values with value:
        opt_str = ",".join( '%s=%s'%(k,v) for k,v in options.iteritems() if v)
        opt_str = "[%s]"% opt_str if opt_str else ""
    
        return "\n".join([ 
            r"""\lstset{language=%s}"""%language,
            r"""\begin{lstlisting}%s""" % opt_str,
            n.contents,
            r"""\end{lstlisting}""",
            ]) 
    
    def _VisitList(self,n, **kwargs):
        if not n.children:
            return
        return "\n".join([
            r"\begin{itemize}",
            "\n".join([self.Visit(c) for c in n.children]),
            r"\end{itemize}",
        ])
    def _VisitListItem(self,n, **kwargs):
        return r"\item %s"%self.Visit(n.para)
    
    def _VisitInlineEquation(self,n, **kwargs):
        return "$%s$"%self.Visit(n.eqn)

    def _VisitLink(self, n, **kwargs):
        return "\href{%s}{%s}"%(n.target, n.get_link_text() )
    def _VisitRef(self, n, **kwargs):
        return r"%s \ref{%s}"%(n.target.get_type_str(), n.target.reflabel)
