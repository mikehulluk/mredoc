#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

class RequiredExternalToolNotFound(RuntimeError):

    pass


class ExternalToolsLinux(object):

    @classmethod
    def ConvertImage(cls, filename1, filename2):
        # Does it exist? If so then delete it
        # so we can flag if the conversion fails.
        if os.path.exists(filename2):
            assert os.path.isfile(filename2)
            os.unlink(filename2)

        ext = lambda s: os.path.splitext(s)[1]
        if ext(filename1) != ext(filename2):
            ExternalToolsChecker.check_imagemagick()
            op = subprocess.check_call("convert %s -trim %s" %(filename1, filename2), shell=True )
            if not os.path.exists( filename2 ):
                raise RuntimeError("File conversion with ImageMagick failed. I was trying to run the command: convert %s %s"%(filename1, filename2) )
        else:
            op = shutil.copy(filename1, filename2)



    @classmethod
    def RunPDFLatex(cls, texfile, working_dir=None):
         ExternalToolsChecker.check_pdflatex()


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

