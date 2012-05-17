import os
import pylab

from mredoc import Document, Section, Figure, ImageFile, Equation
from mredoc import HTMLWriter, LatexWriter
from mredoc import EquationBlock, PythonBlock, Link, Ref
from mredoc import ListItem, List, Paragraph, Table, InlineEquation
from mredoc import SectionNewPage


# Setup paths relative to this file for images:
local_path = os.path.abspath(__file__)
test_file_path = os.path.abspath( os.path.join(os.path.dirname(local_path), "../test_data") )


# Generate the figure in matplolib that we will embed:
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

summary = Document(
    Section("Trigonometry from Wikipedia",
        Section("Introduction",
            """Much of this content is copied from """, Link("http://en.wikipedia.org/wiki/Trigonometry"),
            """. Trigonometry is a branch of mathematics that studies triangles and the relationships between
            their sides and the angles between these sides. Trigonometry defines the trigonometric functions,
            which describe those relationships and have applicability to cyclical phenomena, such as waves.
            The field evolved during the third century BC as a branch of geometry used extensively for
            astronomical studies. It is also the foundation of the practical art of surveying.""",

        Section("Sin,Cos & Tan",
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
            Paragraph("""If one angle of a triangle is 90 degrees and one of the other angles is known, the third is
            thereby fixed, because the three angles of any triangle add up to 180 degrees. The two acute
            angles therefore add up to 90 degrees: they are complementary angles. The shape of a triangle is
            completely determined, except for similarity, by the angles. Once the angles are known, the ratios
            of the sides are determined, regardless of the overall size of the triangle. If the length of one
            of the sides is known, the other two are determined. These ratios are given by the following
            trigonometric functions of the known angle A, where a, b and c refer to the lengths of the sides
            in """, Ref("L1"), "."),
            Section("""Useful identities""",
                Table( [r"$\theta$ (radians)",r"$\theta$ (degs)", r"$sin(\theta)$", r"$cos(\theta)$"],
                      [["0.0",      "0.0",   "0.0",     "1.0"],
                       ["$\pi/4$",  "90.0",  "1.0,",    "0.0"],
                       ["$\pi/2$",  "180.0", "0.0,",    "-1.0"],
                       ["$3\pi/2$", "270.0", "-1.0,",    "0.0"],
                       ["$2\pi$",   "360.0", "0.0,",    "1.0"] ],
                      caption="Some common values",
                      reflabel="Table1",
                      ),
                Paragraph( Ref("Table1"), """ shows some values of sin and
                cos for values of """, InlineEquation(r"""\theta"""), ".")
            ),

            ),

        Section("Investigations In Python",
            """Python is awesome and lets us do lots of clever things!""",
            PythonBlock(code1, reflabel="C1", caption="Python Code Block"),
            Figure( fig , caption="Some heading for the sin figure", reflabel="O4"),
            Paragraph( "We can use ", Ref("C1"), " to produce the graphs, for example, ", Ref("O4"), ".")
            ),

        SectionNewPage("Inverse Functions",
            """There are some other functions that we can also use""",
            List(
                ListItem("arcsin", r"$arcsin(sin(\theta)) = \theta$"),
                ListItem("arccos", r"$arccos(cos(\theta)) = \theta$"),
            ),
            ),
        ),

        Section("Hyperbolic functions",
            r"""In mathematics, hyperbolic functions are analogs of the ordinary trigonometric, or circular,
            functions. The basic hyperbolic functions are the hyperbolic sine "sinh", and the hyperbolic
            cosine "cosh", from which are derived the hyperbolic tangent "tanh", and so on, corresponding to
            the derived trigonometric functions. The inverse hyperbolic functions are the area hyperbolic sine
            "arsinh" (also called "asinh" or sometimes "arcsinh")[2] and so on. Just as the points (cos t, sin
            t) form a circle with a unit radius, the points (cosh t, sinh t) form the right half of the
            equilateral hyperbola. """,
            List(
                Equation(r""" sinh(x) = \frac{e^x-e^{-x}}{2} =\frac{e^{2x}-1}{2e^x}"""),
                Equation(r""" sinh(x) = \frac{e^x-e^{-x}}{2} =\frac{e^{2x}-1}{2e^x}"""),
                "...",
            ),
        )
    )
)


# Create the output:
summary.to_pdf( filename="./_output/example1/pdf/output.pdf")
summary.to_html( output_dir="./_output/example1/html/")


