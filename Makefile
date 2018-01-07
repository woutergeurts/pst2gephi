#
# Makefile for pst2gephi
#
#
PSTP=./pstprocessor.py 
all: perftest

test:
	$(PSTP) -v -c config.test

perftest:
	$(PSTP) -v -c config.perftest
