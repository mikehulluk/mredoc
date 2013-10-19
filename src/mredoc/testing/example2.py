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

import os
import pylab



from mredoc import Document, Section
from mredoc import Figure, Image, Equation
from mredoc import EquationBlock, PythonBlock, VerbatimBlock, Link
from mredoc import List, Paragraph
from mredoc import SectionNewPage, Ref
from mredoc.visitors import BlockNumberer


# Generate the figure:
import numpy as np
x = np.linspace(-5, 5, 100)
y1 = np.sin(x)
y2 = np.sin(2 * x)
fig = pylab.figure()
pylab.plot(x, y1, label='y=sin(x)')
pylab.plot(x, y2, label='y=sin(2x)')
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

    Section("Trigonometry from Wikipedia",
        Section("Introduction",
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
                 Image( resource_filename(__name__, 'test_data/TrigonometryTriangle.svg') ),
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
        Section("In python",
            """Python is awesome and lets us do lots of clever things!""",
            PythonBlock(code1, reflabel="C1", caption="Python Code Block"),
            VerbatimBlock(op1, ),
            Figure( fig , caption="Some heading for the sin figure", reflabel="O4"),
            Paragraph( "We can use ", Ref("C1"), " to produce the graphs, for example, ", Ref("O4") )
            ),
        SectionNewPage("Other Related Functions",
            """There are some other functions that we can also use""",
            List(
                "cot",
                "arcsin",
                "arcos",
                ['cosh - where cosh = kl;kl;',Equation("x+x=45")],
            ),
            ),

        Section("Hyperbolic functions",
			r"""In mathematics, hyperbolic functions are analogs of
			the ordinary trigonometric, or circular, functions. The
			basic hyperbolic functions are the hyperbolic sine
			"sinh", and the hyperbolic cosine
			"cosh", from which are derived the hyperbolic
			tangent "tanh", and so on, corresponding
			to the derived trigonometric functions. The inverse
			hyperbolic functions are the area hyperbolic sine
			"arsinh" (also called "asinh" or sometimes "arcsinh")[2]
			and so on. Just as the points (cos t, sin t) form a
			circle with a unit radius, the points (cosh t, sinh t)
			form the right half of the equilateral hyperbola. """,
            List(
                ["sinh", Equation(r""" sinh(x) = \frac{e^x-e^{-x}}{2} =\frac{e^{2x}-1}{2e^x}""")],
                "cosh",
                "tanh",
                ['cosh - where cosh = kl;kl;',Equation(r"x+x^2=\frac{45}{3}")],
            ),
            )
        )
    )



summary.to_pdf(filename=os.path.expanduser("~/Desktop/f1.pdf"))
summary.to_html(output_dir=os.path.expanduser("~/Desktop/test_html_out/"))


b = BlockNumberer(summary)
for i in b:
    print i, b[i]
