

all: examples doc

.PHONEY: force_look


doc: examples force_look
	cp -Rv src/testing/_output/ doc/generated_src/
	cp -Rv src/testing/*.py doc/generated_src/
	make -C doc/


examples: force_look
	make -C src/testing/ 

lint: force_look
	pylint --output-format=html --disable='C0301,C0111,W0142' src/mredoc/ > pylint_out.html
	# C0301 - long lines
	# C0111 - 
	# W0142 'Used * or ** magic'



force_look: 
	

clean:
	make -C src/testing/ clean
	make -C doc/ clean
	rm -rf *.pyc
	rm -f pylint_out.html
