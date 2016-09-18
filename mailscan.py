#! /usr/bin/python
import pypff
import re
pst = pypff.file()
pst.open("/media/sf_Mailboxes/archive_2012.pst")
root = pst.get_root_folder()

nodenr=0
edgenr=0
nodes = {}
edges = {}

def process_headers(headers):
	global nodenr, edgenr, nodes, edges
	fromstring = "onbekend";
	tostring = "";
	ccstring = "";
	m = re.search( "From:.*?(<.*>).*:",  
		headers, flags=re.M|re.S )
	if m:
		fromstring = m.group(1)
	m = re.search( "To:.*?(<.*>).*:",  
		headers, flags=re.M|re.S )
	if m:
		tostring = m.group(1)
	m = re.search( "Cc:.*?(<.*>).*:",  
		headers, flags=re.M|re.S )
	if m:
		ccstring = m.group(1)
	fromlist = re.findall("<([^@]*@\S+)>", fromstring)
	if len(fromlist) > 0:
		frm = fromlist[0]
	else:
		frm = "UNKNOWN@UNKNOWN.ORG"
	tolist = re.findall("<([^@]*@\S+)>", tostring)
	cclist = re.findall("<([^@]*@\S+)>", ccstring)
	if not (frm in nodes):
		nodes[frm] = nodenr
		nodenr = nodenr + 1
	frmnr = nodes[frm]
	for to in tolist:
		if not ( to in nodes):
			nodes[to] = nodenr
			nodenr = nodenr + 1
		tonr = nodes[to]
		if not ((frmnr,tonr) in edges): 
			edges[(frmnr,tonr)] = 0
		edges[(frmnr,tonr)] = edges[(frmnr,tonr)] + 1
			
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

def list_folder(tab, folder):
	n = folder.get_number_of_sub_folders()
	for i in range(0,n):
		subfolder = folder.get_sub_folder(i)
		print tab + subfolder.get_name(), subfolder.get_number_of_sub_messages()
		list_messages(subfolder)
		ntab = tab + ":" 
		list_folder( ntab, subfolder )
	
def list_messages(folder):
	nr_msgs = folder.get_number_of_sub_messages()
	for i in range(1, nr_msgs):
		m = folder.get_sub_message(i)	
		headers = m.get_transport_headers()
		if not (headers is None):
			process_headers( headers.encode('ascii', 'replace') )
	
list_folder("", root)

print_nodes()

