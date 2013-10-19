

all: examples doc

.PHONEY: force_look


doc: examples force_look
	zip -r src/mredoc/testing/_output/example1_minimal/html/html_output.zip  src/testing/_output/example1_minimal/html/*
	cp -Rv src/mredoc/testing/_output/ doc/generated_src/
	cp -Rv src/mredoc/testing/*.py doc/generated_src/
	make -C doc/


examples: force_look
	make -C src/mredoc/testing/ 

lint: force_look
	pylint --output-format=html --disable='C0301,C0111,W0142,R0904,R0903' src/mredoc/ > pylint_out.html
	# C0301 - long lines
	# C0111 - 
	# W0142 'Used * or ** magic'
	# R0903/4 are too many or too few methods in class



force_look: 
	

clean:
	make -C src/mredoc/testing/ clean
	make -C doc/ clean
	rm -rf *.pyc
	find . -name '*.pyc' -exec rm {} \;
	find . -name '*.py.new' -exec rm {} \;
	rm -f pylint_out.html
