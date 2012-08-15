

all: examples doc

.PHONEY: force_look


doc: examples force_look
	cp -Rv src/testing/_output/ doc/generated_src/
	cp -Rv src/testing/*.py doc/generated_src/
	make -C doc/


examples: force_look
	make -C src/testing/ 

lint: force_look
	pylint --output-format=html --disable='C0301,C0111,W0142,R0904,R0903' src/mredoc/ > pylint_out.html
	# C0301 - long lines
	# C0111 - 
	# W0142 'Used * or ** magic'
	# R0903/4 are too many or too few methods in class



force_look: 
	

clean:
	make -C src/testing/ clean
	make -C doc/ clean
	rm -rf *.pyc
	find . -name '*.pyc' -exec rm {} \;
	rm -f pylint_out.html
