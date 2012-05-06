
from mhlibs.mredoc import Document, Section
from mhlibs.mredoc import LatexWriter
from mhlibs.mredoc import HTMLWriter


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


LatexWriter.BuildPDF(summary, filename="/home/michael/Desktop/f1.pdf")
HTMLWriter.BuildHTML(summary, output_dir="/home/michael/Desktop/test_html_out/")

