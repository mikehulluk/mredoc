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

#  ====================================================================

import itertools
import pylab
import os
import collections

import matplotlib

from mredoc.errors import InvalidDocumentTree
from mredoc.constants import ImageTypes, Languages

# Since we have 'fake' class wrappers, we let functions look like classes:
# pylint: disable-msg=C0103 


def isiterable(obj):
    return isinstance(obj, collections.Iterable)

def flatten(objs):
    res = []
    for obj in objs:
        if isinstance(obj, _DocumentObject):
            res.append(obj)
        elif isinstance(obj, basestring):
            res.append(obj)
        elif obj is None:
            continue
        elif isiterable(obj):
            res.extend(flatten(obj))
        else:
            raise InvalidDocumentTree('Unexpected argument: %s (type:%s'
                     % (obj, type(obj)))
    return res


def check_type(obj, exp_type):
    if not isinstance(obj, exp_type):
        raise InvalidDocumentTree('Unexpected argument type: %s Expected: %s'
                                   % (type(obj), exp_type))
    return obj

def check_seq_type(seq, exp_type):
    seq = list(seq)
    for obj in seq:
        check_type(obj, exp_type)
    return seq




def _get_kwargs(kw, *names):
    for kwarg in kw:
        assert kwarg in names, "Can't find name: %s in %s" % (kwarg, names)
    return [kw.get(name, None) for name in names]







def DocumentObject(*args, **kwargs):
    return _DocumentObject(*args, **kwargs)

def DocumentRoot(*args, **kwargs):
    return _DocumentRoot(*args, **kwargs)

def ContentBlock(*args):
    if len(args) == 1:
        arg0 = args[0]
        if isinstance(arg0, _ContentBlock):
            return arg0
        elif isinstance(arg0, (_Link, _Ref, basestring)):
            return Paragraph(arg0)
        else:
            raise ValueError('Unexpected object passed to ContentBlock: %s (%s)'
                              % (type(arg0), arg0))
    else:
        return flatten([ContentBlock(arg) for arg in args])

def HierachyScope(*args, **kwargs):
    if len(args) == 1 and isinstance(args[0], _HierachyScope):
        return args[0]

    # Concatenate consecutive 'RichTextContainer'
    # objects into a larger 'Paragraph'
    blocks = []
    current_para_block = None
    for child in args:
        if not isinstance(child, _ContentBlock):
            if current_para_block is None:
                current_para_block = []
            current_para_block.append(child)
        else:
            if current_para_block:
                blocks.append(Paragraph(*flatten(current_para_block)))
                current_para_block = None
            blocks.append(child)
    return _HierachyScope(*blocks, **kwargs)


def Section(heading, *children):
    """ Creates a new Section, with a heading given by the first parameter. Set
    the first parameter to ``None`` to suppress the heading"""

    children = flatten(children)
    if heading:
        children = itertools.chain([Heading(heading)], children)
    return HierachyScope(*children)

# Syntactic Sugar:
def SectionNewPage(heading, *children):
    return HierachyScope( *itertools.chain([Heading(heading)], flatten(children)), new_page=True )


def Heading(heading):
    return _Heading(heading)

def Paragraph(*args, **kwargs):
    """Creates a new Paragraph, which can contain RichTextObjects."""
    return _Paragraph(*args, **kwargs)

def RichTextContainer(*args, **kwargs):
    if len(args) == 1 and isinstance(args[0], _RichTextContainer):
        return args[0]
    return _RichTextContainer(*args, **kwargs)




def _rich_text_from_string(src_str):
    src_str = src_str.strip()
    if not src_str:
        return None
    if src_str[0] == '$' and src_str[-1] == '$':
        return InlineEquation(src_str[1:-1])
    else:
        return PlainText(src_str)


def RichTextObject(obj, **kwargs):
    if obj is None:
        return None

    elif isinstance(obj, _RichTextObject):
        return obj
    elif isinstance(obj, basestring):
        return _rich_text_from_string(obj)
    elif isinstance(obj, (int, float)):
        return _rich_text_from_string(str(obj))
    elif isinstance(obj, _Equation):
        return InlineEquation(obj)
    elif isiterable(obj):
        return flatten([RichTextObject(child, **kwargs) for child in obj])
    else:
        raise ValueError('Unexpected object passed to RichTextObject: %s (%s)'
                          % (type(obj), obj))

def Ref(*args, **kwargs):
    return _Ref(*args, **kwargs)

def Link(*args, **kwargs):
    return _Link(*args, **kwargs)

def PlainText(*args, **kwargs):
    return _PlainText(*args, **kwargs)

def InlineEquation(eqn, **kwargs):
    return _InlineEquation(eqn, **kwargs)

def Figure(*args, **kwargs):
    """Creates a Figure. *kwargs*\ : ``caption`` and ``reflabel`` """
    return _Figure(*args, **kwargs)

def Subfigure(*args, **kwargs):
    return _Subfigure(*args, **kwargs)


def Table(*args, **kwargs):
    """Creates a Table. 

     * *args* : The first argument is the header data, and the second the 
       data for the body of the table. These should both be iterables.
     * *kwargs*\ : ``caption`` and ``reflabel`` """

    return _Table(*args, **kwargs)

def EquationBlock(*args, **kwargs):
    """Creates a EquationBlock. 

     * *args* : A list of ``Equation`` objects or strings
     * *kwargs*\ : ``caption`` and ``reflabel`` """

    return _EquationBlock(*args, **kwargs)

def Equation(eqn, **kwargs):
    if isinstance(eqn, basestring):
        return _Equation(eqn, **kwargs)
    if isinstance(eqn, _Equation):
        assert not kwargs, \
                'Equation called with kwargs, but arg is already a complete object'
        return eqn
    assert False

def List(*args, **kwargs):
    return _List(*args, **kwargs)

def ListItem(*args, **kwargs):
    if len(args) == 1:
        arg0 = args[0]
        if isinstance(arg0, _ListItem):
            return arg0
        else:
            return _ListItem(RichTextContainer(arg0))
    elif len(args) == 2:
        (arg0, arg1) = args
        return _ListItem(RichTextContainer(arg0), RichTextContainer(arg1))
    return _ListItem(arg0, **kwargs)


def CodeListing(*args, **kwargs):
    """Creates a CodeListing. 

     * *args* is a single object, with a string of the contents.
     * *kwargs*\ : ``language``, ``caption`` and ``reflabel`` 

    *language* is a string and can be ``Verbatim``\ , ``Python`` or ``Bash``\ .
     """
    return _CodeListing(*args, **kwargs)

def TableOfContents(*args, **kwargs):
    return _TableOfContents(*args, **kwargs)

def PythonBlock(*args, **kwargs):
    return _PythonBlock(*args, **kwargs)
def VerbatimBlock(*args, **kwargs):
    return _VerbatimBlock(*args, **kwargs)
def BashBlock(*args, **kwargs):
    return _BashBlock(*args, **kwargs)


def Image(img, **kwargs):
    if isinstance(img, matplotlib.figure.Figure):
        return ImageMPL(img, **kwargs)
    elif isinstance(img, basestring):
        return ImageFile(img, **kwargs)
    elif isinstance(img, _Image):
        assert not kwargs, 'Image Wrapper passed unexpected kw-arguments'
        return img
    else:
        assert False, 'Unexpected type: %s' % str(img)

def ImageMPL(*args, **kwargs):
    return _ImageMPL(*args, **kwargs)

def ImageFile(*args, **kwargs):
    return _ImageFile(*args, **kwargs)






class _DocumentObject(object):

    # Syntactic sugar, to make it easy to dumpy any part of a
    # document to a pdf-file or html
    def to_pdf(self, filename):
        """Creates a .pdf file of the object. It does this by generating LaTeX
        code, and running ``pdflatex`` on that code twice"""
        import mredoc.writers
        return mredoc.writers.LatexWriter.build_pdf(self.as_document(),
                filename=filename)

    def to_html(self, output_dir):
        """Creates a html. It will create a file ``index.html`` in the directory 
        specified by output_dir."""
        import mredoc.writers
        return mredoc.writers.HTMLWriter.build_html(self.as_document(),
                output_dir=output_dir)
    def as_document(self):
        return Document(self)


    def _accept_visitor(self, visitor, **_kwargs):
        print 'Visitor:', visitor, type(visitor)
        print 'Target:', self, type(self)
        raise NotImplementedError()




class _DocumentRoot(_DocumentObject):
    def as_document(self):
        return self

    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_document(self, **kwargs)

    def __init__(self, hierachy_root, remove_empty_sections=True, normalise_hierachy=True):
        super(_DocumentRoot, self).__init__()

        self.hierachy_root = HierachyScope(hierachy_root)

        # Resolve internal references:
        from mredoc.visitors.reference_resolver import RefResolver
        RefResolver(self)

        if remove_empty_sections:
            from mredoc.util.removeemptysections import EmptySectionRemover
            EmptySectionRemover().visit(self)

        if normalise_hierachy:
            from mredoc.util.removeemptysections import NormaliseHierachyScope
            NormaliseHierachyScope().visit(self)

    def __str__(self):
        return '<DocumentRoot: [ %s ]>' % str(self.hierachy_root)







class _ContentBlock(_DocumentObject):
    def __init__(self, caption=None, reflabel=None):
        super(_ContentBlock, self).__init__()
        self.caption = RichTextObject(caption)
        self.reflabel = reflabel
        self.number = None

    def get_ref_str(self,):
        return "%s %d" % (self.get_type_str(), self.number)

    def get_type_str(self,):
        raise NotImplementedError()




class _HierachyScope(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_hierachyscope(self, **kwargs)

    def __init__(self, *children, **kwargs):
        _ContentBlock.__init__(self, caption=None, reflabel=None)
        (self.is_new_page, ) = _get_kwargs(kwargs, 'new_page')
        self.children = check_seq_type(children, _ContentBlock)

    def __str__(self):
        return '<HierachyScope: [ %s ]>' % ','.join([str(s) for s in
                self.children])

    def get_type_str(self,):
        errmsg = 'mredoc internal error: called_HierachyScope.get_type_str()'
        raise RuntimeError(errmsg)

class _Heading(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_heading(self, **kwargs)
    def __init__(self, heading):
        _ContentBlock.__init__(self, caption=None, reflabel=None)
        self.heading = RichTextContainer(heading)

    def get_type_str(self,):
        errmsg = 'mredoc internal error: called Heading.get_type_str()'
        raise RuntimeError(errmsg)

class _Paragraph(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_paragraph(self, **kwargs)
    def __init__(self, *children):
        _ContentBlock.__init__(self, caption=None, reflabel=None)
        self.contents = RichTextContainer(children)

    def get_type_str(self,):
        errmsg = 'mredoc internal error: called Paragraph.get_type_str()'
        raise RuntimeError(errmsg)



class _RichTextContainer(_DocumentObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_richtextcontainer(self, **kwargs)

    def __init__(self, *children):
        super(_RichTextContainer, self).__init__()
        self.children = flatten([RichTextObject(child) for child in children])
        check_seq_type(self.children, _RichTextObject)

    def get_type_str(self,):
        errmsg = 'mredoc internal error: called RichTextContainer.get_type_str()'
        raise RuntimeError(errmsg)



class _RichTextObject(_DocumentObject):
    pass


class _Ref(_RichTextObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_ref(self, **kwargs)

    def __init__(self, target):
        super(_Ref, self).__init__()
        self.target = target

    def get_link_text(self):
        return self.target.get_ref_str()

class _Link(_RichTextObject):

    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_link(self, **kwargs)

    def __init__(self, target, ref_text=None):
        super(_Link, self).__init__()
        self.target = target
        self.ref_text = ref_text

    def get_link_text(self):
        return self.ref_text or self.target

class _PlainText(_RichTextObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_text(self, **kwargs)
    def __init__(self, text):
        super(_PlainText, self).__init__()
        self.text = check_type(text, basestring)

class _InlineEquation(_RichTextObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_inlineequation(self, **kwargs)
    def __init__(self, eqn):
        super(_InlineEquation, self).__init__()
        self.eqn = Equation(eqn)



class _Figure(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_figure(self, **kwargs)

    def __init__(self, *subfigs, **kwargs):
        # Unpack kwargs:
        (caption, reflabel) = _get_kwargs(kwargs, 'caption', 'reflabel')
        #_ContentBlock.__init__(self, caption=caption, reflabel=reflabel)
        super(_Figure, self).__init__(caption=caption, reflabel=reflabel)

        subfigs = [_Subfigure(subfig) for subfig in subfigs]
        self.subfigs = check_seq_type(subfigs, _Subfigure)

        if self.caption is not None:
            self.caption = check_type(RichTextContainer(caption),
                    _RichTextContainer)


    def get_type_str(self,):
        return "Figure"

class _Subfigure(_DocumentObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_subfigure(self, **kwargs)

    def __init__(self, img):
        super(_Subfigure, self).__init__()
        self.img = Image(img)




class _Table(_ContentBlock):

    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_table(self, **kwargs)

    def __init__(self, header, data, **kwargs):
        (caption, reflabel) = _get_kwargs(kwargs, 'caption', 'reflabel')
        super(_Table, self).__init__(caption=caption, reflabel=reflabel)
        self.data = data
        self.header = header

        self.header = [_RichTextContainer(h) for h in self.header]
        self.data = [[_RichTextContainer(d) for d in line] for line in
                     self.data]

    def get_type_str(self):
        return 'Table'

class _EquationBlock(_ContentBlock):

    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_equationblock(self, **kwargs)

    def __init__(self, *equations, **kwargs):
        (caption, reflabel) = _get_kwargs(kwargs, 'caption', 'reflabel')
        #_ContentBlock.__init__(self, caption=caption, reflabel=reflabel)
        super(_EquationBlock, self).__init__(caption=caption, reflabel=reflabel)

        self.equations = [Equation(eq) for eq in equations]

    def get_type_str(self):
        return 'Eqn'

class _Equation(_DocumentObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_equation(self, **kwargs)
    def __init__(self, eqn):
        super(_Equation, self).__init__()
        self.eqn = eqn
        self.eqn = self.eqn.replace(')', r"\right)")
        self.eqn = self.eqn.replace('(', r"\left(")


class _List(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_list(self, **kwargs)

    def __init__(self, *children, **kwargs):
        (caption, reflabel) = _get_kwargs(kwargs, 'caption', 'reflabel')
        super(_List, self).__init__(caption=caption, reflabel=reflabel)
        self.children = [ListItem(li) for li in children]

    def get_type_str(self):
        return 'List'

class _ListItem(_DocumentObject):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_listitem(self, **kwargs)
    def __init__(self, para, header=None):
        super(_ListItem, self).__init__()
        self.para = RichTextContainer(para)
        self.header = (RichTextContainer(header) if header else None)



class _CodeListing(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_codelisting(self, **kwargs)
    def __init__(self, contents, **kwargs):
        (caption, reflabel, language) = _get_kwargs(kwargs, 'caption',
                'reflabel', 'language')
        super(_CodeListing, self).__init__(caption=caption, reflabel=reflabel)

        self.language = language
        self.contents = contents

    def get_type_str(self):
        return 'Listing'


class _TableOfContents(_ContentBlock):
    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_tableofcontents(self, **kwargs)

    def __init__(self,):
        super(_TableOfContents, self).__init__(caption=None, reflabel=None)

    def get_type_str(self,):
        errmsg = 'mredoc internal error: called TableOfContents.get_type_str()'
        raise RuntimeError(errmsg)

class _PythonBlock(_CodeListing):
    def __init__(self, *args, **kwargs):
        super(_PythonBlock, self).__init__(language=Languages.Python, *args, **kwargs)
class _VerbatimBlock(_CodeListing):
    def __init__(self, *args, **kwargs):
        super(_VerbatimBlock, self).__init__(*args, language=Languages.Verbatim, **kwargs)
class _BashBlock(_CodeListing):
    def __init__(self, *args, **kwargs):
        super(_BashBlock, self).__init__(*args, language=Languages.Bash, **kwargs)






class _Image(_DocumentObject):
    op_loc = '/tmp/figs/'
    f_num = 0

    @classmethod
    def nextFigFilenameBase(cls):
        cls.f_num = cls.f_num + 1
        fBase = os.path.join(cls.op_loc, 'opfile%04d' % cls.f_num)
        if not os.path.exists(cls.op_loc):
            os.makedirs(cls.op_loc)
        return fBase

    def get_filename(self, file_type):
        raise NotImplementedError()

    def _accept_visitor(self, visitor, **kwargs):
        return visitor.visit_image(self, **kwargs)


class _ImageMPL(_Image):

    def __init__(self, fig, auto_adjust=True):
        super(_ImageMPL, self).__init__()
        # The pylab object or filename. Used in Figures.
        self.fig = fig
        self.fNameBase = _Image.nextFigFilenameBase()

        if auto_adjust:
            resize_image(self.fig)

        # Save the image in a variety of formats:
        pylab.savefig(self.fNameBase + '.pdf')
        pylab.savefig(self.fNameBase + '.png')
        pylab.savefig(self.fNameBase + '.svg')

    def get_filename(self, file_type):
        assert file_type in [ImageTypes.EPS, ImageTypes.PDF, ImageTypes.PNG,
                        ImageTypes.SVG]
        return self.fNameBase + '.' + file_type



def resize_image(fig):
    pylab.figure(fig.number)
    fig.set_size_inches(1.75, 1.75)
    for obj in fig.findobj(matplotlib.text.Text):
        obj.set_fontsize(7)
    fig.subplots_adjust(left=0.25, right=0.95)



class _ImageFile(_Image):
    def __init__(self, filename):
        super(_ImageFile, self).__init__()

        assert isinstance(filename, basestring)
        assert os.path.exists(filename), 'Invalid filename'

        self.filename = filename
        self.fNameBase = _Image.nextFigFilenameBase()


    def get_filename(self, file_type):
        assert file_type in [ImageTypes.EPS, ImageTypes.PDF, ImageTypes.PNG,
                        ImageTypes.SVG]

        cur_ext = os.path.splitext(self.filename)[1]
        new_filename = self.filename.replace(cur_ext, file_type)

        if new_filename == self.filename:
            return self.filename

        new_filename = self.fNameBase + '.' + file_type
        from mredoc.util.toolchecker import ExternalTools
        ExternalTools.convert_image(self.filename, new_filename)
        return new_filename













# Syntactic Sugar:


def Document(*children, **kwargs):
    """Creates a top-level document object, containing the subchildren"""
    if len(children) == 1 and isinstance(children[0], list):
        return DocumentRoot(HierachyScope(*children[0]), **kwargs)
    else:
        return DocumentRoot(HierachyScope(*children), **kwargs)

def VerticalColTable(header, data, **kwargs):
    if isinstance(header, basestring):
        header = header.split('|')
        data = [(l.split('|') if isinstance(l, basestring) else l)
                for l in data]

    for line in data:
        assert len(line) == len(header)
    return Table(header=header, data=data, **kwargs)



