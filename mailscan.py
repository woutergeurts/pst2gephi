#! /usr/bin/python
#
# This is the mail filter. A set of call backs to run from a pstwalk
#
# process_body
# process_subject
# process_to_from
#
# behaviour is controlled by config file
#
import email
import re
import logging
logger = logging.getLogger(__name__)

class mailscan:
	def __init__(self,config):
		self.config = config
		self.nrmsg = 0

	def process_body(self,body):
		logger.debug("processing body: " + body)

	def process_subject(self,subject):
		logger.debug("processing subject: " + subject)

	def process_to_from(self,to,frm):
		print to;
		print frm;

	def msg_handle(self, m):
		headers = m.get_transport_headers()
		msg = {key: "" for key in ['from','to','cc']}
		if not headers is None:
			headers = headers.encode('ascii', 'replace')
			msg = email.message_from_string(headers)
		else:
			msg = {key: "<None@Nowhere>" for key in ['from','to','cc']}

		subject = m.get_subject()
		if not subject is None:
			subject = subject.encode('ascii', 'replace')
		else:
			subject = "None"

		plain_text_body = m.get_plain_text_body()
		
		msglist = {}
		for key in ['from', 'to', 'cc']:
			if msg[key] is None:
				msglist[key] = ['None']
			else:
				msglist[key] =  re.findall("<([^@]*@\S+)>", msg[key])

		self.process_subject(subject)
		self.process_body(plain_text_body)

#nodenr=0
#edgenr=0
#nodes = {}
#edges = {}

if __name__ == "__main__":
	import unittest

	class TestMailScan(unittest.TestCase):
		def test_process_subject(self):
			cnfg = ""
			ms=mailscan(cnfg)
			ms.process_subject("aap")

    	unittest.main()
