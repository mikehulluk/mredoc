MReDoc: Modular Reduced Documentation API
===========================================


MRedoc is a minimal API for generating HTML and LaTeX documents containing
text, equations, figures and tables from Python.

It is designed as a simple interface for generating out summaries of
simulations of models in computational neuroscience. Other libraries, (e.g.
Reportlab, Sphinx), have more comprehensive APIs for fonts customisation and
page layout, MRedoc is more focused on a simple set of objects that can be
simply embedded within each other. It is provides a simple API for creating
documents containing figures from files and matplotlib objects.


A Document is a tree of elements. Once the tree has been built, it can be
converted into LaTeX (pdf) or HTML.



.. literalinclude:: ../src/testing/sample2.py 
