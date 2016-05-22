# for string operation
import re

# for listing file in a given folder
import glob

# to get extension
import os

#import array id
from msg_type import msg_tab, msg_tab_inv

# return the final html code from all the separate file
def get_html_code(adr):

    # some usefull array
    file_to_convert = get_list_of_htmlpy_file()
    element_right = []
    element_left = []
    element_js = []
    element_css = []
    call_back_array = []
    names = []

    # get htmlpy file content
    for element in file_to_convert:
        (items, column, js_file, cba) = get_html_from_file(element)
        names.append(os.path.splitext(element)[0]);

        if column.lower() == 'right':
            element_right.append(items)
        else:
            element_left.append(items)

        for current in js_file:
            name, extension = os.path.splitext(current)

            if extension == '.js':
                element_js.append(current)
            elif extension == '.css':
                element_css.append(current)

        call_back_array.extend(cba)

    # start filling final html :

    # read part0
    ret = file('server/page/part0.html', 'r').read()

    #insert css files
    ret += '\n\n' 
    for element in element_css:  
        ret+='<link href="/static/css/box/' + element + '" rel="stylesheet">'
        ret+='\n'
    ret += '\n\n' 

    # read part1
    ret += file('server/page/part1.html', 'r').read().format(adr)

    # insert msg_tab from python
    ret+='\n\n'
    msg_tab_it = sorted(msg_tab.items(), key= lambda msg: msg[1])

    ret+= '<script>\n  var msg_tab = {\n'
    for element in msg_tab_it:
        ret+="    '" + str(element[0]) + "' : " + str(element[1]) + ',\n'
    ret+='  };\n'

    ret+="""
  var reverse_msg_tab = {};
  for (element in msg_tab)
    reverse_msg_tab[ msg_tab[element] ] = element;\n</script>"""


    # insert js files
    ret += '\n\n'
    for element in element_js:
        ret+='<script src="/static/js/box/' + element + '"></script>'
        ret+='\n'
    ret += '\n\n'  

    # insert js call-back script
    ret += """<script>\nvar call_back_tab = {\n"""
    for (code_num, code_str) in msg_tab_inv.items():
        ret += '    ' + str( code_num ) + ' : [ '

        for element in call_back_array:
            (code_name, func_name) = element.items()[0]

            if code_str == code_name:
                ret += func_name + ','

        ret = ret[:-1] + '],\n' #removing last ',' and add \n
    ret += """}\n</script>\n"""

    # read part2
    ret += file('server/page/part2.html', 'r').read()

    for name in names:
            ret +="""
            <li class="active Box_handler" onclick="boxClick(this)" id="BOX_handler_""" + name + """">
              <a href="#Box_anchor_""" + name + """">
                <i class="fa fa-th"></i><span>""" + name + """</span>
              </a>
            </li>\n\n"""

    # read part3
    ret += file('server/page/part3.html', 'r').read()

    #insert box of the right column
    ret += '\n\n'
    for element in element_left:
        ret += element
        ret += '\n'
    ret += '\n\n'

    # read part4
    ret += file('server/page/part4.html', 'r').read()

    #insert box of the right column
    ret += '\n\n' 
    for element in element_right:
        ret += element
        ret += '\n'
    ret += '\n\n' 

    # read part5
    ret += file('server/page/part5.html', 'r').read()
    ret += '\n' 

    return ret

# return the html converted html code from a .htmlpy file in /page/
def get_html_from_file(file_):

    name, extension = os.path.splitext(file_);

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
        return

    # adding box parameter
    result = """<div class="box box-default" """ + lines[0][4:] + " id='BOX_" + name+ """'>
  <a name='Box_anchor_""" + name + "'></a>"

    #check of the keyword 'BOXHEAD:'
    if lines[1][:8] != 'BOXHEAD:':
        print 'error while reading htmlpy file: keyword "BOXHEAD:" not found'
        return

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
    result+= " </div><!-- /.box-body -->\n</div><!-- /.box --> \n"

    # remove space
    lines[i] = re.sub(' ', '', lines[i])


    if len(lines[i]) >= 20 and lines[i][9:15] == 'column': #if this string contain left or right column information
        column = lines[i][16:]
    else:
        column ='left' #default value

    i+=1

    # checking BOXSCRIPT is present
    if i>=(len(lines)):
        # NO SCRIPT or CALLBACK FOUND
        return (result, column, [], [])

    if lines[i][:8] != 'BOXFILE:' and lines[i][:12] != 'BOXCALLBACK:':
       # NO SCRIPT or CALLBACK FOUND
        return (result, column, [], [])

    if lines[i][:8] == 'BOXFILE:':
        # format of script :
        # BOXSCRIPT: filename1.js filename2.js filename3.js ...
        # on single line !

        # JS file found must be in public/js/box/
        list_js_file = [el for el in lines[i][9:].split(' ') if el != ''] # same as : filter(None, lines[i][11:].split(' '))
        i += 1
        if i>=(len(lines)):
            # NO SCRIPT FOUND
            return (result, column, list_js_file, [])

    else:
        list_js_file = []

    call_back_tab = []

    if lines[i][:12] == 'BOXCALLBACK:':
        i += 1
        all_call_back = ''

        # regrouping all lines remaining in one single
        for line in lines[i:]:
            all_call_back += ' ' + line

        all_call_back = filter(None, all_call_back.split(' '))

        if len(all_call_back) == 0: # no call back
            return (result, column, list_js_file, [])

        elif len(all_call_back) % 2 == 1: #if there is an odd number of parameter:
            del all_call_back[-1]

        # convert format from ['a', 'b', 'a', 'b',...] to [{'a':'b'}, {'a':'b'}, ...]
        call_back_tab = [{code_name:code_func} for (code_name, code_func) in zip(all_call_back[::2], all_call_back[1::2])]

    return (result, column, list_js_file, call_back_tab)


# return a list of string containing all the name of the file.htmlpy in the folder server/page/
def get_list_of_htmlpy_file():
    # capture a list of all the file .htmlpy and cut the 'page/''
    return [re.sub('server/page/', '', i) for i in glob.glob('server/page/*.htmlpy')]

