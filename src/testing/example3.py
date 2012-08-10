
from mredoc import Document, Section
from mredoc import LatexWriter
from mredoc import HTMLWriter
import os


summary = Document(

    Section("Simulation Results",

    Section(  "Overview",
        Section( "Overview Diagram", ),
        Section("Key Traces", ),
        ),
    Section( "Simulation Setup",
        Section( "Population Overview"),
        Section( "Cells"),
        Section( "Synapses"),
        Section( "Gap Junctions"),
        Section( "Stimulations"),
        Section( "Simulation Junctions"),
        ),
    Section( "Mechanism Dynamics",
        Section( "Channel"),
        Section( "Synapses"),
        ),
    Section( "Platform Details"),
    )
)


LatexWriter.BuildPDF(summary, filename=os.path.expanduser("~/Desktop/f1.pdf"))
HTMLWriter.BuildHTML(summary, output_dir=os.path.expanduser("~/Desktop/test_html_out/"))

