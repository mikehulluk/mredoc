

srcs := $(wildcard *.py)
outputs := $(patsubst %.py,%.py.out,$(srcs))



all: $(outputs)

clean:
	rm -rf *.out _output/
	

%.py.out: %.py
	python $< > $@ 2>&1








