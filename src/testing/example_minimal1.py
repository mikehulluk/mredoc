import pylab, numpy
from mredoc import Section, Figure, Table

# A simple function that returns a matplotlib Figure
def generate_figure():
    f = pylab.figure()
    t = numpy.linspace(0,10)
    pylab.plot( t, numpy.exp(-t)* numpy.sin(5*t) )
    return f

# Create the summary of the simulations
# and write to HTML and LaTeX
summary = Section("My Document",
        Section("A Sub-Section",
            "This is an introductory paragraph",
            Figure( generate_figure(), caption="$e^{-t}*sin(10t)$" ),
            Table( ['x','2x'], [('%d'%x,'%d'%2*x) for x in [0,1,2,3] ] ),
            "Some more text describing the results"
        )
    )
summary.to_pdf( filename="./_output/example1_minimal/pdf/output.pdf")
summary.to_html( output_dir="./_output/example1_minimal/html/")

