
import os
import pylab





from mredoc import Document, HeadedScope
from mredoc import Figure, ImageFile, Equation

from mredoc import LatexWriter
from mredoc import HTMLWriter
from mredoc import EquationBlock, PythonBlock, VerbatimBlock, Paragraph, Link
from mredoc.objects.core import ListItem, List, ParagraphBlock
from mredoc import HeadedScopeNewPage, Ref
from mredoc.visitors import BlockNumberer




 
local_path = os.path.abspath(__file__)

test_file_path = os.path.abspath( os.path.join(os.path.dirname(local_path), "../test_data") )


# Generate the figure:
import numpy as np
x = np.linspace(-5,5,100)
y1 = np.sin(x)
y2 = np.sin(2*x)
fig = pylab.figure()
pylab.plot(x,y1, label="y=sin(x)")
pylab.plot(x,y2, label="y=sin(2x)")
pylab.legend()



code1 = """
import numpy as np
x = np.linspace(-5,5,100)
y1 = np.sin(x)
y2 = np.sin(2*x)
fig = pylab.figure()
pylab.plot(x,y1, label="y=sin(x)")
pylab.plot(x,y2, label="y=sin(2x)")
pylab.legend()
"""
op1 = """Bing Bang BonG!"""





summary = Document(
    
    HeadedScope("Trigonometry from Wikipedia",
        HeadedScope("Introduction",
            """Much of this content is copied from """, Link("http://en.wikipedia.org/wiki/Trigonometry"),
            """Trigonometry is a branch of mathematics that studies triangles
            and the relationships between their sides and the angles between
            these sides. Trigonometry defines the trigonometric functions,
            which describe those relationships and have applicability to
            cyclical phenomena, such as waves. The field evolved during the
            third century BC as a branch of geometry used extensively for
            astronomical studies. It is also the foundation of the practical
            art of surveying.""",
            Figure(
                 ImageFile( os.path.join(test_file_path,"TrigonometryTriangle.svg" )),
                 caption="Angles in a triangle",
                 reflabel="L1"
                   ),
            EquationBlock(
                r""" sin A = \frac{opp}{hyp} = \frac{a}{c}""",    
                r""" cos A = \frac{opp}{hyp} = \frac{a}{c}""",
                r""" tan A = \frac{opp}{hyp} = \frac{a}{c}""",
                caption="Relations between angles and lengths of a triangle",
                reflabel="L2"
                ),
                
            ),
        HeadedScope("In python",
            """Python is awesome and lets us do lots of clever things!""",
            PythonBlock(code1, reflabel="C1", caption="Python Code Block"),
            VerbatimBlock(op1, ),
            Figure( fig , caption="Some heading for the sin figure", reflabel="O4"),
            ParagraphBlock( "We can use ", Ref("C1"), " to produce the graphs, for example, ", Ref("O4") )
            ),
        HeadedScopeNewPage("Other Functions",
            """There are some other functions that we can also use""",
            List(
                "cot",
                "arcsin",
                "arcos",
                ['cosh - where cosh = kl;kl;',Equation("x+x=45")], 
            ),
            )
        )
    )
                    


LatexWriter.BuildPDF(summary, filename="/home/michael/Desktop/f1.pdf")
HTMLWriter.BuildHTML(summary, output_dir="/home/michael/Desktop/test_html_out/")


b = BlockNumberer(summary)
for i in b:
    print i, b[i]
