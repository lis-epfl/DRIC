# for string operation
import re

# for listing file in a given folder
import glob

# return the final html code from all the separate file
def get_html_code(adr):
	file_to_convert = get_list_of_htmlpy_file()
	element_right = []

	ret = file('server/page/part1.html', 'r').read().format(adr, '%', '{', '}')

	# insert js files

	ret += file('server/page/part2.html', 'r').read().format('%',)

	#insert box of the left column
	for element in file_to_convert:
		(temp1, temp2) = get_html_from_file(element)

		if temp2.lower() == 'right':
			element_right.append(temp1)
		else:
			ret += temp1
			ret += "\n"

	ret += file('server/page/part3.html', 'r').read()

	#insert box of the right column
	for element in element_right:
		ret += element
		ret += "\n"

	ret += file('server/page/part4.html', 'r').read()

	return ret

# return the html converted html code from a .htmlpy file in /page/
def get_html_from_file(file_):

	#read file
	currentfile = file('server/page/' + file_)

	#separate lines
	lines = currentfile.readlines()

	#remove \n
	lines =  [re.sub('\n', '', i) for i in lines]

	#remove empty lines
	lines = filter(None, lines)

	# first check of the keyword 'BOX:'
	if lines[0][:4] != 'BOX:':
		print 'error while reading htmlpy file: keyword "BOX:" not found'
		exit()

	# adding box parameter
	result = """<div class="box box-default" """ + lines[0][4:] + ">\n"

	#check of the keyword 'BOXHEAD:'
	if lines[1][:8] != 'BOXHEAD:':
		print 'error while reading htmlpy file: keyword "BOXHEAD:" not found'
		exit()

	# adding head parameter
	result += """<div class="box-header with-border" """ + lines[1][8:] + "> \n"

	# filling head
	i = 2
	while lines[i][:8] != 'BOXBODY:':
		result+= ' ' + lines[i] + '\n'
		i+=1


	# adding lines and body parameter
	result += """
	 <div class="box-tools pull-right">\n
	  <button class="btn btn-box-tool" data-widget="collapse" data-toggle="tooltip" title="Collapse"><i class="fa fa-minus"></i></button>\n
	  <button class="btn btn-box-tool" data-widget="remove" data-toggle="tooltip" title="Remove"><i class="fa fa-times"></i></button>\n
	 </div><!-- /.box-tools -->\n
	</div><!-- /.box-header -->\n
	<div class="box-body" """ + lines[i][8:] + "> \n"
	i+=1

	# filling body
	while lines[i][:9] != 'BOXPARAM:' and i<(len(lines)):
		result+= ' ' + lines[i] + '\n'
		i+=1

	# end
	result+= """ </div><!-- /.box-body -->\n</div><!-- /.box --> \n"""

	# remove space
	lines[i] = re.sub(' ', '', lines[i])


	if len(lines[i]) >= 20 and lines[i][9:15] == 'column': #if this string contain left or right column information
		return (result,lines[i][16:])
	else:
		return (result, 'left') #default value


# return a list of string containing all the name of the file.htmlpy in the folder /page/
def get_list_of_htmlpy_file():
	# capture a list of all the file .htmlpy and cut the 'page/''
	return [re.sub('server/page/', '', i) for i in glob.glob('server/page/*.htmlpy')]

