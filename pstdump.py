#! /usr/bin/python
import pypff
import email
import re

nodenr=0
edgenr=0
nodes = {}
edges = {}
nrmsgs = 0

import logging
logger = logging.getLogger(__name__)

def walk_folder(tab, folder, handler):
	n = folder.get_number_of_sub_folders()
	for i in range(0,n):
		subfolder = folder.get_sub_folder(i)
		foldername = subfolder.get_name()

		if foldername is None:
			logger.debug("Foldername = None")
			foldername = "None"
		else:
			foldername = foldername.encode('ascii', 'replace')
			logger.debug(tab + "Folder " + foldername + 
			"(" + str(subfolder.get_number_of_sub_messages()) +
			" messages)")

		walk_messages(subfolder, handler)
		ntab = tab + ":" 
		walk_folder( ntab, subfolder, handler )
	
def walk_messages(folder, handler):
	global nrmsgs
	nr_msgs = folder.get_number_of_sub_messages()
	for i in range(1, nr_msgs):
		msg = folder.get_sub_message(i)	
		handler(msg)
		nrmsgs = nrmsgs + 1

def print_nodes():
	i = 0
	with open( "nodes.csv","w" ) as f:
		f.write( "id,node\n" )
		for node in nodes:
			f.write( str(i) + "," + node + "\n" )
			i = i + 1
	i = 0
	with open( "edges.csv","w" ) as f:
		f.write( "source,target,id,weight\n" )
		for edge in edges:
			f.write( str(edge[0]) + "," + 
				 str(edge[1]) + "," + 
				 str(i) + "," + 
				 str(edges[edge]) + "\n"
			 )
	
def msg_dump(m):
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
	
	#python3: msg = email.message_from_bytes(headers)
	##print "mst = ", msg
	msglist = {}
	for key in ['from', 'to', 'cc']:
		if msg[key] is None:
			msglist[key] = ['None']
		else:
			msglist[key] =  re.findall("<([^@]*@\S+)>", msg[key])
		logger.debug("msg ", key, msglist[key] )

	print "subject ", subject
	##print "plain_text_body", plain_text_body

def walk_and_dump(fn):
	pst = pypff.file()
	pst.open(fn)
	root = pst.get_root_folder()

	walk_folder("", root, msg_dump)

	print "nrmsgs processed = ", nrmsgs

def walk_and_handle(fn, ms):
	pst = pypff.file()
	pst.open(fn)
	root = pst.get_root_folder()

	walk_folder("", root, ms.msg_handle)

	return nrmsgs

if __name__ == "__main__":
	walk_and_dump("./testpst.pst")
