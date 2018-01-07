#! /usr/bin/python
#
#
#
import argparse
import ConfigParser
import logging
import logging.config
logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

import pstdump
import mailscan

def main():
	parser = argparse.ArgumentParser(
		description='This is pstprocessor the driver for pst2gephi')
	parser.add_argument('-c', action="store", dest="fn_config", 
		help="filename of the config file")
	parser.add_argument('-v', action="store_true", dest="logging_verbose", 
		help="filename of the config file", default=False)

	parsed_args = parser.parse_args()

	if parsed_args.logging_verbose:
		logging.getLogger().setLevel(logging.DEBUG)
		logger.info("DEBUG switched on via -v")
		
	config = ConfigParser.ConfigParser()
	try:
		print config.read(parsed_args.fn_config)
	except:
		quit("no config file")

	fn_pst = config.get("pst","file")

	ms = mailscan.mailscan(config)
	
	#pstdump.walk_and_dump(fn_pst)
	nrmsgs = pstdump.walk_and_handle(fn_pst,ms)
	print 'Nr of mesages', nrmsgs

main()
