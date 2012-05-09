

all: examples doc

.PHONEY: force_look


doc: examples force_look
	cp -Rv src/testing/_output/ doc/generated_src/
	cp -Rv src/testing/*.py doc/generated_src/
	make -C doc/


examples: force_look
	make -C src/testing/ 



force_look: 
	

clean:
	make -C src/testing/ clean
	make -C doc/ clean
	rm -rf *.pyc
