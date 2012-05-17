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
#import matplotlib.text as text
import collections

import matplotlib
from types import NoneType




class ImageTypes:
    SVG = 'svg'
    PNG = 'png'
    PDF = 'pdf'
    EPS = 'eps'

class Languages:
    Verbatim = "Verbatim"
    Python = "Python"
    Bash = "Bash"













class InvalidDocumentTree(Exception):
    pass



def isiterable(e):
    return isinstance(e, collections.Iterable)

def flatten(objs):
    r = []
    for o in objs:
        if isinstance(o,_DocumentObject):
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







def DocumentObject(*args,**kwargs):
    return _DocumentObject(*args,**kwargs)

def DocumentRoot(*args,**kwargs):
    return _DocumentRoot(*args, **kwargs)

def DocumentBlockObject(*args, **kwargs):
    if len(args) == 1:
        a = args[0]
        if isinstance(a, _DocumentBlockObject):
            return a
        if isinstance(a, (_Link,_Ref,basestring)):
            return Paragraph(a)
        
        print type(a), a
        assert False
    
    else:
        return flatten( [DocumentBlockObject(b) for b in args] )

    #print args
    #assert False
    #return _DocumentBlockObject(*args, **kwargs)

def HierachyScope(*args, **kwargs):
    if len(args) == 1 and isinstance(args[0], _HierachyScope):
        return args[0]
    return _HierachyScope(*args, **kwargs)
    #return _HierachyScope(DocumentBlockObject)

def Heading(*args,**kwargs):
    return _Heading(*args, **kwargs)

def Paragraph(*args,**kwargs):
    return _Paragraph(*args,**kwargs)

def RichTextContainer(*args,**kwargs):
    if len(args) == 1 and isinstance(args[0], _RichTextContainer):
        return args[0]

    #    self.contents = RichTextContainer(*children)
    return _RichTextContainer(*args,**kwargs)




def rich_text_from_string(s):
    s = s.strip()
    if s[0] == "$" and s[-1] == "$":
        return InlineEquation(s[1:-1])
    else:
        return Text(s)


def RichTextObject(o,**kwargs):
    if o is None:
        return None

    if isinstance(o, _RichTextObject):
        return o
    if isinstance(o, basestring):
        return rich_text_from_string(o)
    if isinstance(o, _Equation):
        return InlineEquation( o)
    if isiterable(o):
        return flatten([ RichTextObject(a,**kwargs) for a in o])

    print type(o), o
    assert False

def Ref(*args,**kwargs):
    return _Ref(*args,**kwargs)

def Link(*args,**kwargs):
    return _Link(*args,**kwargs)



def Text(*args,**kwargs):
    return _Text(*args,**kwargs)

def InlineEquation(*args, **kwargs):
    return _InlineEquation(*args, **kwargs)



def Figure(*args, **kwargs):
    return _Figure(*args, **kwargs)

def Subfigure(*args, **kwargs):
    return _Subfigure(*args, **kwargs)


def Table(*args, **kwargs):
    return _Table(*args, **kwargs)

def EquationBlock(*args, **kwargs):
    return _EquationBlock(*args, **kwargs)

def Equation(*args, **kwargs):
    return _Equation(*args, **kwargs)


def List(*args, **kwargs):
    return _List(*args, **kwargs)

def ListItem(*args, **kwargs):
    return _ListItem(*args,**kwargs)


def CodeBlock(*args, **kwargs):
    return _CodeBlock(*args, **kwargs)

def TableOfContents(*args,**kwargs):
    return _TableOfContents(*args,**kwargs)

def PythonBlock(*args,**kwargs):
    return _PythonBlock(*args,**kwargs)
def VerbatimBlock(*args,**kwargs):
    return _VerbatimBlock(*args,**kwargs)
def BashBlock(*args,**kwargs):
    return _BashBlock(*args,**kwargs)


def Image(*args, **kwargs):
    return _Image(*args,**kwargs)

def ImageMPL(*args,**kwargs):
    return _ImageMPL(*args,**kwargs)


def ImageFile(*args,**kwargs):
    return _ImageFile(*args,**kwargs)





























class _DocumentObject(object):

    # Syntactic sugar, to make it easy to dumpy any part of a
    # document to a pdf-file or html
    def to_pdf(self, filename):
        from mredoc.writers import LatexWriter
        return LatexWriter.BuildPDF(self.as_document(), filename=filename)
    def to_html(self, output_dir):
        from mredoc.writers import HTMLWriter
        return HTMLWriter.BuildHTML(self.as_document(), output_dir=output_dir)
    def as_document(self):
        return Document(self)


    def _AcceptVisitor(self, v, **kwargs):
        print "Visitor:", v, type(v)
        print "Target:", self, type(self)
        raise NotImplementedError()




class _DocumentRoot(_DocumentObject):
    def as_document(self):
        return self

    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitDocument(self, **kwargs)
    def __init__(self, hierachy_root, remove_empty_sections=True, normalise_hierachy=True):
#
        self.hierachy_root = HierachyScope( hierachy_root)

        # Resolve internal references:
        from mredoc.visitors.reference_resolver import RefResolver
        RefResolver(self)

        if remove_empty_sections:
            from mredoc.util.removeemptysections import EmptySectionRemover
            EmptySectionRemover().Visit(self)

        if normalise_hierachy:
            from mredoc.util.removeemptysections import NormaliseHierachyScope
            NormaliseHierachyScope().Visit(self)







class _DocumentBlockObject(_DocumentObject):
    def __init__(self, caption=None, reflabel=None):
        self.caption = RichTextObject(caption) 
        self.reflabel = reflabel
        self.number = None
    def get_ref_str(self,):
        return "%s %d"%(self.get_type_str(), self.number)
    def get_type_str(self,):
        raise NotImplementedError()




class _HierachyScope(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitHierachyScope(self, **kwargs)
    def __init__(self, *children, **kwargs):
        _DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        self.is_new_page, = get_kwargs(kwargs,'new_page')

        # Convert strings to paragrpah_objects:
        #strs_to_para = lambda s: wrap_type_seq(s, T=basestring, wrapper=Text)
        #children = strs_to_para( flatten(children))
        #children = flatten( [ DocumentBlockObject(a) for a in children ] )

        #Concatenate consecutive 'RichTextContainer' objects into a larger 'Paragraph'
        blocks = []
        current_para_block = None
        for c in children:
            if not isinstance(c, _DocumentBlockObject):
                if not current_para_block:
                    current_para_block = []
                current_para_block.append(c)
            else:
                if current_para_block:
                    blocks.append( Paragraph(*current_para_block))
                    current_para_block = None
                blocks.append(c)

        self.children = check_seq_type(blocks, _DocumentBlockObject )


class _Heading(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitHeading(self, **kwargs)
    def __init__(self, heading):
        _DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        #str_to_para = lambda s: wrap_type(s, T=basestring, wrapper=RichTextContainer)
        #self.heading=check_type( str_to_para(heading), RichTextContainer)
        self.heading=RichTextContainer(heading) #check_type( str_to_para(heading), RichTextContainer)








class _Paragraph(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitParagraph(self, **kwargs)
    def __init__(self, *children):
        _DocumentBlockObject.__init__(self,caption=None, reflabel=None)
        self.contents = RichTextContainer(children)

        #if len(children) == 1 and isinstance(children[0], RichTextContainer):
        #    self.contents = children[0]
        #else:
        #    self.contents = RichTextContainer(*children)








class _RichTextContainer(_DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitRichTextContainer(self, **kwargs)
    def __init__(self, *children):
        self.children = flatten( [RichTextObject(a) for a in children ] ) 
        check_seq_type( self.children, _RichTextObject)




class _RichTextObject(_DocumentObject):
    pass


class _Ref(_RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitRef(self, **kwargs)
    def __init__(self, target, ):
        self.target = target
    def get_link_text(self):
        return self.target.get_ref_str()

class _Link(_RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitLink(self, **kwargs)
    def __init__(self, target, ref_text = None):
        self.target = target
        self.ref_text = ref_text
    def get_link_text(self):
        return self.ref_text or self.target



class _Text(_RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        print type(v)
        return v._VisitText(self, **kwargs)
    def __init__(self, text):
        self.text = check_type(text, basestring)


class _InlineEquation(_RichTextObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitInlineEquation(self,**kwargs)
    def __init__(self, eqn):
        eqn_builder = lambda s: wrap_type(eqn, T=(basestring), wrapper=Equation )
        self.eqn = check_type(eqn_builder(eqn),_Equation)



class _Figure(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitFigure(self,**kwargs)

    def __init__(self, *subfigs, **kwargs):
        # Unpack kwargs:
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        _DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        subfigs = [ _Subfigure(s) if not isinstance(s,_Subfigure) else s for s in subfigs]
        self.subfigs = check_seq_type( subfigs, _Subfigure)


        #para_builder = lambda s: wrap_type(s, T=(basestring,_RichTextObject, _Equation), wrapper=_RichTextContainer )
        self.caption = check_type(RichTextContainer(caption), _RichTextContainer)


    def get_type_str(self,):
        return "Figure"

class _Subfigure(_DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitSubfigure(self,**kwargs)
    def __init__(self, img):
        # Switch on the type:
        if isinstance(img, matplotlib.figure.Figure):
            self.img = ImageMPL(img)
        elif isinstance(img, basestring):
            self.img = ImageFile(img)
        elif isinstance(img, _Image):
            self.img = img
        else:
            assert False, "Unexpetced type: %s"%str(img)




class _Table(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitTable(self,**kwargs)
    def __init__(self, header, data, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        _DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)
        self.data = data
        self.header = header

        self.header = [ _RichTextContainer(h) for h in self.header]
        self.data = [ [ _RichTextContainer(d) for d in line]  for line in self.data]

    def get_type_str(self,):
        return "Table"

class _EquationBlock(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitEquationBlock(self,**kwargs)
    def __init__(self, *equations, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        _DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        strs_to_eqn = lambda s: wrap_type_seq(s, T=basestring, wrapper=_Equation)
        self.equations = check_seq_type( strs_to_eqn(flatten(equations)), _Equation)

    def get_type_str(self,):
        return "Eqn"

class _Equation(_DocumentObject):
    def _AcceptVisitor(self, v, **kwargs):
        return v._VisitEquation(self,**kwargs)
    def __init__(self, eqn):
        self.eqn = eqn
        self.eqn=self.eqn.replace(")",r"\right)")
        self.eqn=self.eqn.replace("(",r"\left(")


class _List(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitList(self, **kwargs)

    def __init__(self, *children, **kwargs):
        caption,reflabel = get_kwargs(kwargs,'caption','reflabel')
        _DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)
        conv_to_list_item = lambda s: wrap_type_seq(s, T=(_RichTextObject, _Equation, basestring), wrapper=lambda c: _ListItem(c))
        self.children = check_seq_type( conv_to_list_item( flatten( children)), _ListItem)

    def get_type_str(self,):
        return "List"

class _ListItem(_DocumentObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitListItem(self, **kwargs)
    def __init__(self,  para, header=None):

        self.para = RichTextContainer(para)
        self.header = RichTextContainer(header) if header else None

        assert isinstance(self.para,(_RichTextContainer, NoneType) )
        assert isinstance(self.header,(_RichTextContainer, NoneType) )


class _CodeBlock(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitCodeBlock(self, **kwargs)
    def __init__(self, contents, **kwargs):
        caption,reflabel,language = get_kwargs(kwargs,'caption','reflabel', 'language')
        _DocumentBlockObject.__init__(self,caption=caption, reflabel=reflabel)

        self.language = language
        self.contents = contents

    def get_type_str(self,):
        return "Listing"


class _TableOfContents(_DocumentBlockObject):
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitTableOfContents(self, **kwargs)
    def __init__(self, *children):
        _DocumentBlockObject.__init__(self,caption=None, reflabel=None)



class _PythonBlock(_CodeBlock):
    def __init__(self, *args,**kwargs):
        super(_PythonBlock,self).__init__(*args, language=Languages.Python,**kwargs)
class _VerbatimBlock(_CodeBlock):
    def __init__(self, *args,**kwargs):
        super(_VerbatimBlock,self).__init__(*args, language=Languages.Verbatim,**kwargs)
class _BashBlock(_CodeBlock):
    def __init__(self, *args,**kwargs):
        super(_BashBlock,self).__init__(*args, language=Languages.BashBlock,**kwargs)






class _Image(_DocumentObject):
    op_loc = "/tmp/figs/"
    f_num = 0

    @classmethod
    def nextFigFilenameBase(cls):
        cls.f_num = cls.f_num + 1
        fBase = os.path.join(cls.op_loc, "opfile%04d"%cls.f_num)
        if not os.path.exists(cls.op_loc):
            os.makedirs(cls.op_loc)
        return fBase

    def get_filename(self, type):
        raise NotImplementedError()
    def _AcceptVisitor(self,v,**kwargs):
        return v._VisitImage(self,**kwargs)


class _ImageMPL(_Image):



    def __init__(self, fig, auto_adjust=True):
        # The pylab object or filename. Used in Figures.
        self.fig=fig
        self.fNameBase = _Image.nextFigFilenameBase()

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
    for o in fig.findobj(matplotlib.text.Text):
        o.set_fontsize(7)
    fig.subplots_adjust(left=0.25,right=0.95)



class _ImageFile(_Image):
    def __init__(self, filename):

        assert isinstance(filename, basestring)
        assert os.path.exists(filename), "Invalid filename"

        self.filename = filename
        self.fNameBase = _Image.nextFigFilenameBase()


    def get_filename(self, type):
        assert type in [ ImageTypes.EPS, ImageTypes.PDF,ImageTypes.PNG, ImageTypes.SVG]

        cur_ext = os.path.splitext(self.filename)[1]
        new_filename = self.filename.replace(cur_ext, type)

        if new_filename==self.filename:
            return self.filename

        new_filename = self.fNameBase + "." + type
       	from mredoc.util.toolchecker import ExternalTools
        ExternalTools.ConvertImage( self.filename, new_filename)
        return new_filename













# Syntactic Sugar:
def Section(header, *children ):
    return HierachyScope( *itertools.chain( [Heading(header)], children) )

# Syntactic Sugar:
def SectionNewPage(header, *children):
    return HierachyScope( *itertools.chain( [Heading(header)], children), new_page=True )


def Document(*children, **kwargs) :
    if len(children)==1 and isinstance( children[0], list):
        return DocumentRoot( HierachyScope( *children[0] ),**kwargs )
    else:
        return DocumentRoot( HierachyScope( *children), **kwargs)

def VerticalColTable( header, data ):
    if isinstance(header, basestring):
        header = header.split("|")
        data= [ l.split("|") for l in data ]

    for line in data:
        assert len(line) ==  len( header)
    return Table( header=header, data=data )



