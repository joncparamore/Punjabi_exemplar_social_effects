import tkinter as tk # Python GUI
from easygui import * # For input

######## Initiate and stylize GUI ###########
root = tk.Tk()

#adding choices for age choicebax
years = list ()
x = 1930
while x < 2010:
  years.append(x)
  x = x+1

#adding choices for langs multichoicebox
languages = ['Punjabi', 'Urdu', 'English', 'Mankiyali', 'Pashto', 'Saraiki', 'Hindko', 'Sindhi', 'Balochi', 'Other']

#choices for gender
gender = ['male', 'female']

# Get input from user (easygui)
name = enterbox(msg="Enter your full name: ",title="", root=root)
age = choicebox(msg='In what year were you born? ',title="", choices = years) #single choice menu
sex = choicebox(msg="What is your sex: ",title="", choices = gender) #single choice menu
native_lang = choicebox('What is your native language? ', title="", choices = languages)
langlist = multchoicebox(msg='What languages do you speak? ', title='', choices = languages) #multichoice menu
birthplace = enterbox(msg='What is the name of the city/town where you were born?', title="", root=root)
currenttown = enterbox(msg='What is the name of the city/town where you currently live?', title="", root=root)

def appendinfo():
  global spkinfo
  langs = ''
  #for loop to change the list made from language choices into a string
  for choices in langlist:
    if choices == 'Other':
      otherlangs = enterbox(msg='What other languages do you speak?', title='', root=root)
      langs += '' + otherlangs + ' '
    else:
      langs += '' + choices + ' '
  spkinfo = open('pan_nasalization_demographics_exp1.txt',"a") #append mode
  spkinfo.write('\n'+name+'\t'+age+'\t'+sex+'\t'+native_lang+'\t'+langs+'\t'+birthplace+'\t'+currenttown)
  spkinfo.close()

# Start up the GUI and run the program
root.state('zoomed') # https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter
appendinfo()
root.mainloop()

##TODO
#get rid of double click moving me to the next question
