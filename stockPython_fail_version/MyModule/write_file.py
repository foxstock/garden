
def write_file(d_url,d_type,d_content):
	file=open(d_url,d_type)
	file.write(d_content)
	file.close

