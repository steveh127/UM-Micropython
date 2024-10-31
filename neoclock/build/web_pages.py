#defines web_pages used in dashboard
from web_builder import Button,Text_input,Radio_buttons,Checkbox,Link,Label,Action,Header,Paragraph,Submit,Web_page,Body,Form
from actions import Actions

#action map 
act=Actions()
#if a form has a Submit widget only one method is required.
actions_map={
	'submit':act.submit
	}

NAME = 'Clock'
#home page
setup = Web_page(
	title=NAME + '_Setup',
	body=Body(
		display_list = [
			Header(NAME + ' Setup',header=2,ID='title'),
			Paragraph('WiFi, Display and Time Setup'),
			Paragraph('This is a one shot setup page. Be careful to set things up correctly. You can save multiple times but once clock is restarted settings are fixed.'),
			Paragraph('An attempt is made to detect the best WiFi network. If this is not yours please correct.'),
			
		],		
		form=Form(
			[
			Label('Change if SSID incorrect:'),
			SSID_input := Text_input(label='',command='SSID_input',size=20,value=act.best_net,button=False),
			Label('Enter PASSWORD:'),
			PSWD_input := Text_input(label='',command='PSWD_input',size=20,button_label='',button=False),
			Type_radio := Radio_buttons(('blocks','circles','random'),command='Type_radio',value='blocks',label='Clock Pattern',
							button_label='',button=False),
			Time_radio := Radio_buttons(('12hr','24hr'),command='Time_radio',value='24hr',label='12hr or 24hr',button=False),
			Label('UTC offset:'),
			UTC_input  := Text_input(label='',command='UTC_input',size=5,value='0',button=False,integer=True),
			Submit(label='Save Setup',fields=[SSID_input,PSWD_input,Type_radio,Time_radio,UTC_input]),
			Paragraph(''),
			Paragraph('If a UTC offset is set Daylight saving correction is disabled.')				
			],
			cols=2
		),
	cols=1
	),
	css_file='dash.css',
	action_map=actions_map
)



#links - matches commands to web pages, a 'home' page must be defined. 

links = {'home':setup}
