#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

class RequiredExternalToolNotFound(RuntimeError):
    def __init__(self, toolname):
        errmsg = "Unable to find tool: %s" % toolname
        super(RequiredExternalToolNotFound, self).__init__(errmsg)



class ExternalToolsLinux(object):

    @classmethod
    def convert_image(cls, filename1, filename2):
        # Does it exist? If so then delete it
        # so we can flag if the conversion fails.
        if os.path.exists(filename2):
            assert os.path.isfile(filename2)
            os.unlink(filename2)

        ext = lambda s: os.path.splitext(s)[1]
        if ext(filename1) != ext(filename2):
            ExternalToolsChecker.check_imagemagick()
            subprocess.check_call("convert %s -trim %s" %(filename1, filename2), shell=True )
            if not os.path.exists( filename2 ):
                raise RuntimeError("File conversion with ImageMagick failed. I was trying to run the command: convert %s %s"%(filename1, filename2) )
        else:
            shutil.copy(filename1, filename2)



    @classmethod
    def RunPDFLatex(cls, tex_str, working_dir=None, output_filename=None):
        ExternalToolsChecker.check_pdflatex()

        if not os.path.exists(cls._working_dir):
            os.makedirs(cls._working_dir)
        tex_file = working_dir + '/eqnset.tex'
        tex_pdf = working_dir + '/eqnset.pdf'

        op_dir = os.path.dirname(output_filename)
        if not os.path.exists(op_dir):
            os.makedirs(op_dir)
        # Write to disk and compile:
        with open(tex_file, 'w') as fobj:
            fobj.write(tex_str)

        compile_cmd = 'pdflatex -output-directory %s %s' \
            % (working_dir, tex_file)
        os.system(compile_cmd)
        os.system(compile_cmd)
        os.system(compile_cmd)
        os.system(compile_cmd)

        os.system('cp %s %s' % (tex_pdf, output_filename))
        if not os.path.exists(output_filename):
            raise ValueError('Something went wrong building pdf')

class ExternalToolsCheckerLinux(object):

    pdflatex_checked = False
    imagemagick_checked = False

    @classmethod
    def check_pdflatex(cls):
        if ExternalToolsCheckerLinux.pdflatex_checked:
            return
        ExternalToolsCheckerLinux.pdflatex_checked = True

        try:
            subprocess.check_call('which pdflatex')
        except:
            raise RequiredExternalToolNotFound("Can't find pdf_latex")

    @classmethod
    def check_imagemagick(cls):
        if ExternalToolsCheckerLinux.imagemagick_checked:
            return
        ExternalToolsCheckerLinux.imagemagick_checked = True

        try:
            subprocess.check_call(['which', 'convert'])
        except:
            raise RequiredExternalToolNotFound("Can't find ImageMagick(convert)")



import platform
pl = platform.system()


ExternalTools, ExternalToolsChecker = {
    'Linux': (ExternalToolsLinux, ExternalToolsCheckerLinux)
}[pl]

