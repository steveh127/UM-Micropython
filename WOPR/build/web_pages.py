#defines web_pages used in dashboard
from web_builder import Web_page,Body,Form,Button,Text_input,Radio_buttons,Checkbox,Link,Text_area,Label,Action,Header,Paragraph

from actions import Actions

#action map 
act=Actions()
actions_map={
		'set_colours':act.show_colour,
		'flash_colour':act.flash_colour,
		'show_message':act.show_message,
		'start_clock':act.start_clock,
		'stop_clock':act.stop_clock,
		'do_beep':act.beep_now,
		'clear_all':act.clear_all,
		'show_ip':act.show_ip,
		'set_time':act.time_set,
		'toggle24':act.toggle_24,
		'toggle_ds':act.toggle_Summer
		}
		
#Web Page Definitions

#home page
wopr_dashboard = Web_page(
	title='Display Dashboard',
	body=Body(
		display_list = [
			Header('Display Control',header=2,ID='title'),
			Link('Send Message',link='message'),
			Link('Clock',link='clock'),
			Link('RGB control',link='rgb_control')
		],		
		form=Form(
			[
			Button(label='Clear All',command='clear_all'),
			Button(label='Show IP address',command='show_ip')
			],
			cols=1
		),
	cols=3
	),
	css_file='dash.css',
	action_map=actions_map
)

#send message page
				
send_message=Web_page(
	title='Send Message',
	body = Body(
		display_list = [
			Header('Send Message',header=2,ID='title'),
			Link('Home',link='home'),
			Paragraph('Text can be typed in any case, </br>'
					'Unrecognised characters display as a . ')
					
		],
		form = Form(
			[
			Label('Enter your message:'),
			Text_area(label='',command='show_message',button_label='Send the Message'),
			Button(label='Beep',command='do_beep')
			],
			cols=1
		),
		cols=1
	),
	css_file   = 'dash.css',
	action_map = actions_map
)

#clock page

clock_control = Web_page(
	title='Clock Control',
	body=Body(
		display_list = [
			Header('Clock Control',header=2,ID='title'),
			Paragraph('Current Clock is $$ ',variables=[act.get_24]),
			Paragraph('Current Time is $$ ',variables=[act.get_DS]),
			Link('Home',link='home')		
		],
		form=Form(
			[
			Paragraph('Clock Buttons'),Paragraph(''),
			Button(label='Show Clock',command='start_clock'),
			Button(label='Hide Clock',command='stop_clock'),
			Action('24 or 12 hour clock',command='toggle24'),
			Action('Toggle Summertime',command='toggle_ds'),
			Action('Set Time',command='set_time')
			],
			cols=2
		),
	cols=1
	),
	css_file='dash.css',
	action_map=actions_map
)

RGB = Web_page(
	title='RGB Control',
	body=Body(
		display_list = [
			Header('RGB Control',header=2,ID='title'),
			Link('Home',link='home')		
		],
		form=Form(
			[
			Checkbox(['White','Green','Blue','Yellow','Red'],label='Select Colours',command='set_colours',button_label='Show'),
			Radio_buttons(['White','Green','Blue','Yellow','Red'],label='Flash',command='flash_colour',value='',button_label='Flash')
			],
			cols=2
		),
	cols=1
	),
	css_file='dash.css',
	action_map=actions_map
)

#links - matches commands to web pages, a 'home' page must be defined. 

links = {'home':wopr_dashboard,'message':send_message,'clock':clock_control,'rgb_control':RGB}
