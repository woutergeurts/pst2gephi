#
# Makefile for pst2gephi
#
#
PSTP=./pstprocessor.py -v
all: test

test:
	$(PSTP) -c config.test
