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

#  ====================================================================

import itertools
import pylab
import os
import matplotlib.text as text
import collections
#from matplotlib.figure import Figure

import matplotlib
from types import NoneType




""" MReDoc is a simple object model representing simple documents composed of
text, images, tables, equations and code listings. It is designed as a simple
interface for generating out summaries of simulations of models in
computational neuroscience. Other libraries, (e.g. Reportlab, Sphinx), have
more comprehensive APIs for fonts customisation, MRedoc is more focused on a
simple set of objects that can be simply embedded within each other.


A Document is a tree of elements. Once the tree has been built, it can be
converted into LaTeX (pdf) or HTML.

.. code-block:: python

    Exanmple::



"""





class ImageTypes:
    SVG = 'svg'
    PNG = 'png'
    PDF = 'pdf'
    EPS = 'eps'

class Languages:
    Verbatim = "Verbatim"
    Python = "Python"
    Bash = "Bash"







def ensure_Paragraph(obj):
    if isinstance(obj, RichTextObject):
        return RichTextContainer(obj)
    elif isinstance(obj,Equation):
        return RichTextContainer(obj)
    elif isinstance(obj,  RichTextContainer):
        return obj
    elif isinstance(obj, basestring):
        return RichTextContainer( Text(obj) )
    else:
        print obj, type(obj)
        assert False






class InvalidDocumentTree(Exception):
    pass



def isiterable(e):
    return isinstance(e, collections.Iterable)

def flatten(objs):
    r = []
    for o in objs:
        if isinstance(o,DocumentObject):
            r.append(o)
        elif isinstance(o,basestring):
            r.append(o)
        elif isiterable(o):
            r.extend(o)
        else:
            raise InvalidDocumentTree("Unexpected argument: %s (type:%s"%(o, type(o)))

    return r





def check_type(o,t):
    if not isinstance(o,t):
        raise InvalidDocumentTree("Unexpected argument type: %s Expected: %s"%(type(o), t))
    return o

def check_seq_type(seq,t):
    seq = list(seq)
    for s in seq:
        check_type(s,t)
    return seq




def wrap_type_seq(objs, T, wrapper):
    assert isiterable(objs)
    assert not isinstance(objs,basestring)

    objsOut = []
    for o in objs:
        if isinstance(o,T):
            objsOut.append( wrapper(o))
        else:
            objsOut.append( o )
    return objsOut


def wrap_type(obj, T, wrapper):
    if isinstance(obj,T):
        return wrapper(obj)
    else:
        return obj



def get_kwargs(kw, *names):
    for k in kw:
        assert k in names, "Can't find name: %s in %s"%(k,names)
    return [ kw.get(n,None) for n in names]



class DocumentObject(object):


    def _AcceptVisitor(self, v, **kwargs):
        raise NotImplementedError()


class DocumentRoot(DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitDocument(self, **kwargs)
    def __init__(self, hierachy_root):
        self.hierachy_root = check_type( hierachy_root, HierachyScope)

        # Resolve internal references:
        from mredoc.visitors.reference_resolver import RefResolver
        RefResolver(self)




class DocumentBlockObject(DocumentObject):
    def __init__(self, caption, reflabel):
        para_builder = lambda s: wrap_type(s, T=(basestring,RichTextObject, Equation), wrapper=RichTextContainer )
        self.caption = check_type( para_builder(caption), RichTextContainer) if caption else None
        self.reflabel = reflabel
        self.number = None




class HierachyScope(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitHierachyScope(self, **kwargs)
    def __init__(self, *children, **kwargs):
        DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        self.is_new_page, = get_kwargs(kwargs,'new_page')

        # Convert strings to paragrpah_objects:
        strs_to_para = lambda s: wrap_type_seq(s, T=basestring, wrapper=Text)
        children = strs_to_para( flatten(children))

        #Concatenate consecutive 'RichTextContainer' objects into a larger 'ParagraphBlock'
        blocks = []
        current_para_block = None
        for c in children:
            if isinstance(c, RichTextObject):
                if not current_para_block:
                    current_para_block = []
                current_para_block.append(c)
            else:
                if current_para_block:
                    blocks.append( ParagraphBlock(*current_para_block))
                    current_para_block = None
                blocks.append(c)

        self.children = check_seq_type(blocks, DocumentBlockObject )


class Heading(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitHeading(self, **kwargs)
    def __init__(self, heading):
        DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        str_to_para = lambda s: wrap_type(s, T=basestring, wrapper=RichTextContainer)
        self.heading=check_type( str_to_para(heading), RichTextContainer)








class ParagraphBlock(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitParagraphBlock(self, **kwargs)
    def __init__(self, *children):
        DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        strs_to_text = lambda s: wrap_type_seq(s, T=basestring, wrapper=Text)
        eqns_to_inline = lambda s: wrap_type_seq(s, T=Equation, wrapper=InlineEquation)
        self.children = check_seq_type( strs_to_text( eqns_to_inline( children) ), RichTextObject )




class RichTextContainer(DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitParagraph(self, **kwargs)
    def __init__(self, *children):
        
        strs_to_text = lambda s: wrap_type_seq(s, T=basestring, wrapper=Text)
        eqns_to_inline = lambda s: wrap_type_seq(s, T=Equation, wrapper=InlineEquation)
        self.children = check_seq_type( strs_to_text( eqns_to_inline( children) ), RichTextObject )




class RichTextObject(DocumentObject):
    pass


class Ref(RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):

        return v._VisitRef(self, **kwargs)
    def __init__(self, target, ):
        self.target = target


    def get_link_text(self):
        return self.target.get_ref_str() 

class Link(RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitLink(self, **kwargs)
    def __init__(self, target, ref_text = None):
        self.target = target
        self.ref_text = ref_text

    def get_link_text(self):
        return self.ref_text or self.target 



class Text(RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        print type(v)
        return v._VisitText(self, **kwargs)
    def __init__(self, text):
        self.text = check_type(text, basestring)


class InlineEquation(RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitInlineEquation(self,**kwargs)
    def __init__(self, eqn):
        self.eqn = check_type(eqn,Equation)



class Figure(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitFigure(self,**kwargs)

    def __init__(self, *subfigs, **kwargs):
        # Unpack kwargs:
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        subfigs = [ Subfigure(s) if not isinstance(s,Subfigure) else s for s in subfigs]
        self.subfigs = check_seq_type( subfigs, Subfigure)


        para_builder = lambda s: wrap_type(s, T=(basestring,RichTextObject, Equation), wrapper=RichTextContainer )
        self.caption = check_type(para_builder(caption), RichTextContainer)


    def get_ref_str(self,):
        return "Figure %d"%self.number

class Subfigure(DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitSubfigure(self,**kwargs)
    def __init__(self, img):
        # Switch on the type:
        if isinstance(img, matplotlib.figure.Figure):
            self.img = ImageMPL(img)
        elif isinstance(img, basestring):
            self.img = ImageFile(img)
        elif isinstance(img, Image):
            self.img = img
        else:
            assert False, "Unexpetced type: %s"%str(img)




class Table(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitTable(self,**kwargs)
    def __init__(self, header, data, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)
        self.data = data
        self.header = header

    def get_ref_str(self,):
        return "Table %d"%self.number

class EquationBlock(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitEquationBlock(self,**kwargs)
    def __init__(self, *equations, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        strs_to_eqn = lambda s: wrap_type_seq(s, T=basestring, wrapper=Equation)
        self.equations = check_seq_type( strs_to_eqn(flatten(equations)), Equation)

    def get_ref_str(self,):
        return "Eqn %d"%self.number

class Equation(DocumentObject):
    def _AcceptVisitor(self, v, **kwargs):
        return v._VisitEquation(self,**kwargs)
    def __init__(self, eqn):
        self.eqn = eqn


class List(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitList(self, **kwargs)

    def __init__(self, *children, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)
        conv_to_list_item = lambda s: wrap_type_seq(s, T=(RichTextObject, Equation, basestring), wrapper=lambda c: ListItem(c))
        self.children = check_seq_type( conv_to_list_item( flatten( children)), ListItem)

    def get_ref_str(self,):
        return "List %d"%self.number

class ListItem(DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitListItem(self, **kwargs)
    def __init__(self,  para, header=None):

        self.para = ensure_Paragraph(para)
        self.header = ensure_Paragraph(header) if header else None

        assert isinstance(self.para,(RichTextContainer, NoneType) )
        assert isinstance(self.header,(RichTextContainer, NoneType) )


class CodeBlock(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitCodeBlock(self, **kwargs)
    def __init__(self, contents, **kwargs):
        caption,reflabel,language = get_kwargs(kwargs,'caption','reflabel', 'language')
        DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        self.language = language
        self.contents = contents

    def get_ref_str(self,):
        return "Listing %d"%self.number


class TableOfContents(DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitTableOfContents(self, **kwargs)




class PythonBlock(CodeBlock):
    def __init__(self, *args,**kwargs):
        super(PythonBlock,self).__init__(*args, language=Languages.Python,**kwargs)
class VerbatimBlock(CodeBlock):
    def __init__(self, *args,**kwargs):
        super(VerbatimBlock,self).__init__(*args, language=Languages.Verbatim,**kwargs)
class BashBlock(CodeBlock):
    def __init__(self, *args,**kwargs):
        super(BashBlock,self).__init__(*args, language=Languages.BashBlock,**kwargs)






class Image(DocumentObject):
    op_loc = "/tmp/figs/"
    f_num = 0

    @classmethod
    def nextFigFilenameBase(cls):
        cls.f_num = cls.f_num + 1
        fBase = os.path.join(cls.op_loc, "opfile%04d"%cls.f_num)
        if not os.path.exists(cls.op_loc):
            os.makedirs(cls.op_loc)
        return fBase


    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitImage(self,**kwargs)

    def get_filename(self, type):
        raise NotImplementedError()


class ImageMPL(Image):



    def __init__(self, fig, auto_adjust=True):
        # The pylab object or filename. Used in Figures.
        self.fig=fig
        self.fNameBase = Image.nextFigFilenameBase()

        if auto_adjust:
            resize_image(self.fig)

        # Save the image in a variety of formats:
        pylab.savefig(self.fNameBase+".pdf")
        pylab.savefig(self.fNameBase+".png")
        pylab.savefig(self.fNameBase+".svg")

    def get_filename(self, type):
        assert type in [ ImageTypes.EPS, ImageTypes.PDF,ImageTypes.PNG, ImageTypes.SVG]
        return self.fNameBase+"."+type



def resize_image(fig):
    pylab.figure( fig.number)
    fig.set_size_inches(1.75,1.75)
    for o in fig.findobj(text.Text):
        o.set_fontsize(7)
    fig.subplots_adjust(left=0.25,right=0.95)



class ImageFile(Image):
    def __init__(self, filename):

        assert isinstance(filename, basestring)
        assert os.path.exists(filename), "Invalid filename"

        self.filename = filename
        self.fNameBase = Image.nextFigFilenameBase()


    def get_filename(self, type):
        assert type in [ ImageTypes.EPS, ImageTypes.PDF,ImageTypes.PNG, ImageTypes.SVG]

        cur_ext = os.path.splitext(self.filename)[1]
        new_filename = self.filename.replace(cur_ext, type)

        if new_filename==self.filename:
            return self.filename

        new_filename = self.fNameBase + "." + type
        os.system("convert %s %s"%(self.filename, new_filename))
        return new_filename













# Syntactic Sugar:
def HeadedScope(header, *children ):
    return HierachyScope( *itertools.chain( [Heading(header)], children) )

# Syntactic Sugar:
def HeadedScopeNewPage(header, *children):
    return HierachyScope( *itertools.chain( [Heading(header)], children), new_page=True )


def Document(*children):
    if len(children)==1 and isinstance( children[0], list):
        return DocumentRoot( HierachyScope( *children[0] ) )
    else:
        return DocumentRoot( HierachyScope( *children))

def VerticalColTable( header, data ):
    if isinstance(header, basestring):
        header = header.split("|")
        data= [ l.split("|") for l in data ]

    for line in data:
        assert len(line) ==  len( header)
    return Table( header=header, data=data )



