import re
import glob

# return the final html code from all the separate file
def get_html_code(adr):
	file_to_convert = get_list_of_htmlpy_file()

	ret = file('server/page/part1.html', 'r').read().format(adr, '%', '{', '}')

	# insert js files

	ret += file('server/page/part2.html', 'r').read().format('%',)

	#insert box of the left column
	if len(file_to_convert) > 0:
		ret += get_html_from_file(file_to_convert[0])

	ret += file('server/page/part3.html', 'r').read()

	#incsert box of the right column

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

	#check keyword: rules: first line MUST be 'BOXHEAD:', and there must be in the file 'BOXHEAD:' and 'BOXBODY:'
	if lines[0][:8] != 'BOXHEAD:' or 'BOXHEAD:' not in lines or 'BOXBODY:' not in lines:
		print 'error'
		exit()

	# ### start filling the final result

	# beginning
	result = """<div class="box box-default">\n <div class="box-header with-border"> \n"""

	# filling head
	i = 1
	while lines[i][:8] != 'BOXBODY:':
		result+= ' ' + lines[i] + '\n'
		i+=1

	# mid



	result += """
	 <div class="box-tools pull-right">\n
	  <button class="btn btn-box-tool" data-widget="collapse" data-toggle="tooltip" title="Collapse"><i class="fa fa-minus"></i></button>\n
	  <button class="btn btn-box-tool" data-widget="remove" data-toggle="tooltip" title="Remove"><i class="fa fa-times"></i></button>\n
	 </div><!-- /.box-tools -->\n
	</div><!-- /.box-header -->\n
	<div class="box-body"> \n"""
	i+=1

	# filling body
	while lines[i][:9] != 'BOXPARAM:' and i<(len(lines)):
		result+= ' ' + lines[i] + '\n'
		i+=1

	# end
	result+= """ </div><!-- /.box-body -->\n</div><!-- /.box --> \n"""

	# DEBUG
	return result


# return a list of string containing all the name of the file.htmlpy in the folder /page/
def get_list_of_htmlpy_file():
	# capture a list of all the file .htmlpy and cut the 'page/''
	return [re.sub('server/page/', '', i) for i in glob.glob('server/page/*.htmlpy')]

