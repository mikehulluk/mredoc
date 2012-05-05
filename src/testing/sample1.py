
from mhlibs.mredoc import Document, HeadedScope
from mhlibs.mredoc import LatexWriter
from mhlibs.mredoc import HTMLWriter


summary = Document(
    
    HeadedScope("Simulation Results",

    HeadedScope(  "Overview",
        HeadedScope( "Overview Diagram", ),
        HeadedScope("Key Traces", ),
        ),
    HeadedScope( "Simulation Setup",
        HeadedScope( "Population Overview"),
        HeadedScope( "Cells"),
        HeadedScope( "Synapses"),
        HeadedScope( "Gap Junctions"),
        HeadedScope( "Stimulations"),
        HeadedScope( "Simulation Junctions"),
        ),
    HeadedScope( "Mechanism Dynamics",
        HeadedScope( "Channel"),
        HeadedScope( "Synapses"),
        ),
    HeadedScope( "Platform Details"),
    ) 
)


LatexWriter.BuildPDF(summary, filename="/home/michael/Desktop/f1.pdf")
HTMLWriter.BuildHTML(summary, output_dir="/home/michael/Desktop/test_html_out/")

