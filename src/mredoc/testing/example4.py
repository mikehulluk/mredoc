
import os

from mredoc import Document, Section, VerbatimBlock, Paragraph, VerticalColTable

code = """
In a simulation lasting 350.0ms
Create a single compartment neuron 'cell1' with area  and initialvoltage  and capacitance 
Add Leak channels to cell1 with conductance  and reversalpotential 
Inject step-current of  into cell1 from t=100ms until t=250ms
Record cell1.V as $V
Run the simulation
"""

notes = """Although it is possible to voltage clamp the cells above 0mV, the errors in the currents recorded by the voltage clamp become very large. 
If we look at the IV curve for this channel, with these levels of concentrations, there will be very small outward currents, which means 
that the voltage-clamp is having to generating huge amounts of currents to drive the voltages up, which I think brings in large errors.
(Mike Hull)"""


table1 = VerticalColTable(
" -             | NEURON        | morphforge    | mfcuke",
[
"scenario001    | Run           | Run           | Run",
"scenario020    | Run           | Run           | Run",
"scenario021    | Run           | Run           | Run",
"scenario022    | Not Supported | Run           | Not Supported",
"scenario030    | Run           | Not Supported | Not Supported",
"scenario031    | Run           | Not Supported | Not Supported",
"scenario035    | Not Supported | Run           | Not Supported",
"scenario075    | Run           | Run           | Run",
],
caption='Simulator Support'
)



#A	C	EREV	GLK	I	VS	V.max	V.min	V[102]	V[240:249].mean	V[90:99].mean
#10000	1.0	-51	0.3	0	-51	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-51	0.3	0	-31	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-31	0.3	0	-51	OK -31.000000 (-31.0 [eps:eps: 0.005 ])	OK -51.000000 (-51.0 [eps:eps: 0.005 ])	OK -31.000000 (-31.0 [eps:eps: 0.005 ])	OK -31.000000 (-31.0 [eps:eps: 0.005 ])	OK -31.000000 (-31.0 [eps:eps: 0.005 ])
#10000	1.0	-31	0.3	0	-31	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-51	0.3	120	-51	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-31	0.3	120	-31	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-51	1.3	120	-51	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-51	0.3	200	-51	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-31	0.3	200	-31	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***
#10000	1.0	-51	1.3	200	-51	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***	 *** MISSING! ***




s = Section('Scenario001 - Response of passive cell to step current injection',
        Section('Overview',
            Section('Description', VerbatimBlock(code, caption='Machine Readble Desc.')  ),
            Section('Notes', Paragraph(notes) ),
            Section('At a glance',  table1 ),
            ),
        )

#s.to_pdf(filename=os.path.expanduser("~/Desktop/f1.pdf"))
s.to_html(output_dir=os.path.expanduser("~/Desktop/test_html_out/"))
