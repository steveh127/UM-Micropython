#defines web_pages used in dashboard
from web_builder import Button,Text_input,Radio_buttons,Checkbox,Link,Label,Action,Header,Paragraph,Web_page,Body,Form
from setup_actions import Actions

#action map 
act=Actions()
#if a form has a Submit widget only one method is required.
actions_map={
	'save_config':act.save_config
	}

NAME = 'ORAC'
#home page
setup = Web_page(
	title=NAME + '_Setup',
	body=Body(
		display_list = [
			Header(NAME + ' Setup',header=2,ID='title'),
			Paragraph('This is a one shot setup page for WiFi. Be careful to set things up correctly.'),
			Paragraph('An attempt is made to detect the best WiFi network. If this is not yours please correct.'),
			Paragraph('Once setup complete restart the WOPR')		
		],		
		form=Form(
			[
			Label('Change if SSID incorrect:'),
			Text_input(label='',command='SSID',size=20,value=act.get_best_net,button=False),
			
			Label('Enter PASSWORD:'),
			Text_input(label='',command='PSWD',value=act.get_PSWD,size=20,button_label='',button=False),
				
			Radio_buttons(('12hr','24hr'),command='HR12OR24',value=act.get_1224,label='12hr or 24hr',button=False),
			Paragraph(''),
			
			Radio_buttons(('On','Off'),command='DS',value=act.get_ds,label='Daylight Saving',button=False),
			Paragraph(''),
			
			Label('UTC offset:'),
			Text_input(label='',command='UTC_offset',size=5,value=act.get_offset,button=False,integer=True),
			
			Button(label='Save Setup',command='save_config'),			
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
