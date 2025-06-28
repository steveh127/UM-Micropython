#utility method
def submit_button(command,button_label):	
	return '<button type="submit" name="item" value="' + command + '">' + button_label + '</button><br /><br />\n'

class Widget():
	def __init__(self):
		self.value=''
		
	def write(self):
		return '<p></p>'
	
	def get(self):
		return self.value()

	def save(self,item,values):
		pass

class Label(Widget):
	def __init__(self,text,*,ID=''):
		self.text=text
		self.id = ID
	
	def write(self):
		label = '<label'
		if self.id:
			text += 'id="' + self.id + '" '
		label += '>' + self.text + '</label>\n'
		return label

class Button(Widget):
	def __init__(self,*,label='',command=' '):
		self.button=submit_button(command,label)
	
	def write(self):
		return self.button

#actions should supply a single'submit' method if this is used
class Submit(Widget):
	def __init__(self,*,label='',fields=None):
		self.fields=fields
		self.button='<button type="submit" name="submit" value="submit">' + label + '</button><br /><br />\n'
	
	def write(self):
		return self.button
	
	def save(self,item,extracted):
		if self.fields is None:
			return
		if extracted:
			for field in self.fields:
				field.value = extracted[field.type_name][0]
		
			
#create widget for text or integer input
class Text_input(Widget):
	def __init__(self,*,label='',command='text_input',size=4,value='',button=True,button_label='',integer=False,ID=''):
		self.label=label
		self.type_name=command
		self.value=value
		self.size=size
		self.button=button
		self.button_label=button_label
		self.integer=integer
		if integer:
			self.cls = 'integer_input'
		else:
			self.cls = 'text_input'
		self.id = ID
				
	def write(self):
		text = '<div class="' + self.cls + '" '
		if self.id:
			text += 'id="' + self.id + '" '
		text +=  '>\n\t<label>' + self.label + '</label>\n'
		text += '\t<input type="text" name="' + self.type_name + '" size="' + str(self.size)
		text += '" value="' + self.value + '" /><br />\n\t'
		if self.button:
			text +=	submit_button(self.type_name,self.button_label)
		text += '</div>\n'
		return text
	
	def save(self,item,values):
		if item == self.type_name:
			if self.integer:
				try:
					int(values[0])
					self.value=values[0]
				except ValueError:
					self.value='Integer Required'
			else:
				self.value=values[0]

#create radio buttons widget
class Radio_buttons(Widget):
	#just save state of properties
	def __init__(self,choices,*,label='Select one',command='radio',value='',button_label='Submit',ID='',button=True):
		self.choices=choices
		self.value=value
		self.label=label
		self.type_name=command
		self.button=button
		self.button_label=button_label
		self.id = ID
		
	#element needs rebuilding on every access to maintain selection		
	def write(self):
		#div simplifies code and styling
		radio =  '<div class="radio" '
		if self.id:
			radio += 'id="' + self.id + '" '
		radio += '>\n\t<h4>' + self.label + '</h4>\n\t'
		for choice in self.choices:
			radio += '\t<input type="radio" name="' + self.type_name + '" value="' + choice 
			if choice == self.value:
				radio += '" checked="checked '
			radio += '" />'
			radio += '<label >' + choice + '</label><br />\n\t' 
		if self.button:                                                                                                                                                                                                                                                                                                                                                                      
			radio += submit_button(self.type_name,self.button_label)
		radio += '</div>\n'
		return radio
	
	def save(self,item,values):
		if item == self.type_name:
			self.value=values[0]
			
#create check box widget
class Checkbox(Widget):
	#just save state of properties
	def __init__(self,choices,*,label='Select some',command='check',value='no selections',button_label='Submit',ID=''):
		self.choices=choices
		if value=='no selections':
			self.value=[]
		self.label=label
		self.type_name=command
		self.button_label=button_label
		self.id = ID
		
	#element needs rebuilding on every access to maintain selection		
	def write(self):
		check = '<div class="check" '
		if self.id:
			check += 'id="' + self.id + '" '
		check +='>\n\t<h4>' + self.label + '</h4>\n\t'
		for choice in self.choices:
			check += '\t<input type="checkbox" name="' + self.type_name + '" value="' + choice + '" '
			if choice in self.value:
				check += ' checked="checked" '
			check += '><label >' + choice +'<label><br>\n\t'                                                                                                                                                                                                                                                                                                                                                                         
		check += submit_button(self.type_name,self.button_label)
		check += '</div>\n'
		return check
				
	def save(self,item,values):
		if item == self.type_name:
			self.value=[]
			for value in values:
				self.value.append(value)
			print(item)

#class for internal links
class Link(Widget):
	def __init__(self,link_label,*,link='',ID='int_link'):
		self.link = '<p'
		if ID:
			self.link += ' id="' + ID + '" '	
		self.link += '><a href="?item=' + link + '" >' + link_label + '</a></p>\n'
	
	def write(self):
		return self.link

#class for action links - pretty much identical to link but makes purpose clear
class Action(Widget):
	def __init__(self,action_label,*,command='',ID='int_link'):
		self.link = '<p'
		if ID:
			self.link += ' id="' + ID + '" '	
		self.link += '><a href="?item=' + command + '" >' + action_label + '</a></p>\n'
	
	def write(self):
		return self.link
		
#classes to display information optionally with interpolated variables.
# d = Paragraph("String to Display") - d.write() - just show string as paragraph
# d = Header("String to Display",header=1) - d.write() - just show string as header (<h1>)
# d = Paragraph("Variable $$ here or $$ here to Display",[c1,c2]) - d.write() - "Variable a here or b here to Display"
# c1 and c2 are functions returning a string.
# a final $$ must be followed by at least a space.

class Header(Widget):
	def __init__(self,content,*,header=1,ID=''):
		header = str(header)
		self.title = '<h' + header
		if ID:
			self.title += ' id="' + ID + '" '
		self.title+= '>' + content + '</h' + header + '>\n'
	
	def write(self):
		return self.title
		
	
class Paragraph(Widget):
	def __init__(self,content,variables=None,*,ID=''):
		self.content=content
		self.id = ID
		self.variables=variables
	
	def write(self):
		para = '<p' 
		if self.id:
			para += ' id="' + self.id + '" '
		para+= '>'
		if self.variables is None:
			para += self.content
		else:
			parts = self.content.split('$$')
			for i in range(len(parts)):
				if i == len(parts) - 1:
					para += parts[i]	
				else:
					#variables list consists of functions returning a string 
					para += parts[i] + self.variables[i]()
		return para
		
class External_Link(Widget):
	def __init__(self,link_label,link_address,*,ID='ext_link'):
		self.link = '<p'
		if ID:
			self.link += ' id="' + ID + '" '
		self.link+= '><a href="' + link_address + '" >' + link_label + '</a></p>\n'
	
	def write(self):
		return self.link


class Web_page():
	def __init__(self,*,title='MP Dashboard',body='',css_file='',action_map=None):
		self.title=title
		self.body=body
		self.css=css_file
		if action_map is None:
			self.action_map={}
		else:
			self.action_map=action_map
			
	def _get_styling(self,css_file=''):
		cssf = open(css_file)
		styling = ''
		while line := cssf.readline():
			styling += line
		return styling	
			
	def write(self,item,values):
		styles=self._get_styling(self.css)
		html ='<html>\n\t<head>\n' 
		html += '\t\t<title>' + self.title + '</title>\n' 
		html +=	'<style type="text/css">\n' + styles + '</style>\n'
		html +=	'\t</head>\n'	
		html += self.body.write(item,values)
		html += '</html>\n'
		return html
	
	def action(self,item,values):
		for key in self.action_map:
			if key==item:
				self.action_map[item](values)


class Body():
		def __init__(self,*,display_list,form=None,title=True,cols=2):
			self.display_list=display_list
			self.form=form
			self.title=title
			self.cols=cols
		
		def write(self,item,values):
			#save state of control
			if self.form is not None:
					for control in self.form.controls:
						control.save(item,values)
			body = '<body>\n<div id="content">\n'
			body += '<div id="info">\n<table id="data">\n'
			#title is first in display list
			if self.title:
				body += '<tr><td colspan="' + str(self.cols) +' ">' + self.display_list[0].write() + '</td></tr>\n'
				display_list = self.display_list[1:]
			else:
				display_list = self.display_list
			col=0
			body += '<tr colspan="1" >'
			for display in display_list:				
				if not isinstance(display,list):
					body += '<td>' + display.write() + '</td>'
				else:
					body += '<td>' + display[0].write(display[1]) + '</td>'
				col += 1	
				if col == self.cols:
					body += '</tr>\n<tr>'
					col = 0
			body += '</tr>\n'
			if self.form is not None:
				body += '<tr>'		
				body += '<td colspan="' + str(self.cols) +' ">' + self.form.write() + '</td><tr>\n'
			body += '</table>\n</div>\n'
			body += '</div>\n</body>\n'
			return body
			
class Form():
	#controls is a list of form control objects as defined in controls.py 
	#though any object with a 'write' method that generates HTML and a 'save' method to
	#maintain dynamic content (can be a stub) will work
	def __init__(self,controls,cols=3):
		self.controls=controls
		self.cols=cols
		
	def write(self):
		form = '<form method="get">\n'
		form += '<table id="form">\n'
		col=0
		form += '<tr>'
		for control in self.controls:
			form += '<td>'
			form += control.write()
			form += '</td>'
			col +=1
			if col == self.cols:
				form += '</tr><tr>'
				col=0
		form += '</table>\n</form>\n'
		return form
	
