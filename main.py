#By Lucas Frias
#Modules
import requests
import tkinter as tk
from tkinter import simpledialog as dialouge
import pickle
from datetime import datetime, timedelta, date
from sys import exit
#To implement
# GUI display and formatting for day
# Add and remove buttons for schedule
# Better listbox handling (graphical subclass?)
# Internet calander functionality.
#Global variables
selectedDay = date.today().strftime('%d-%m-%Y')
global globalOffset
globalOffset = 0
#print(selectedDay)
#Graphical class - handles all window properties
class graphical:
    def __init__(self, res, title):
        #Must be a lamda so the button is not immediately clicked when starting widget.
        self.dis = tk.Tk()
        self.dis.geometry(res)
        self.dis.title(title)
        self.listbox = tk.Listbox(self.dis,
                                  height=20,
                                  width=55
                                  )
        self.todayB = tk.Button(self.dis,
                                height=5,
                                width=10,
                                text="Today",
                                command=lambda: graphical.moveToday(self.dis, self.listbox), #pass off listbox element for adding.
                            )
        self.arrowLeft = tk.Button(self.dis,
                                   height=5,
                                   width=10,
                                   text="<",
                                   command=lambda: graphical.moveBack(self.dis, self.listbox),
                                   )
        self.arrowRight = tk.Button(self.dis,
                                   height=5,
                                   width=10,
                                   text=">",
                                   command=lambda: graphical.moveTo(self.dis, self.listbox),
                                   )
        self.addB = tk.Button(self.dis,
                              height=5,
                              width=10,
                              text="+",
                              command=lambda: graphical.dateSelector.create()) 
        self.removeB = tk.Button(self.dis,
                                 height=5,
                                 width=10,
                                 text="x",
                                 command=lambda: data.edit.delete(self.listbox, 0) )
        self.todayB.place(x=200,y=0)
        self.listbox.place(x=0,y=100)
        self.addB.place(x=0,y=0)
        self.arrowRight.place(x=300, y=0)
        self.arrowLeft.place(x=100,y=0)
        self.removeB.place(x=400,y=0)
    def moveBack(dis, listbox):
        global globalOffset
        globalOffset -= 1
        selectedDay = MiDateTime.getDayInFuture(globalOffset)
        graphical.updateForDay(listbox, selectedDay)
        dis.title("Student Planner: " + selectedDay)
    def moveToday(dis, listbox):
        global globalOffset
        globalOffset = 0
        graphical.updateForDay(listbox, date.today().strftime('%d-%m-%Y'))
        dis.title("Student Planner: " +date.today().strftime('%d-%m-%Y'))
    def moveTo(dis, listbox):
        global globalOffset
        globalOffset += 1
        selectedDay = MiDateTime.getDayInFuture(globalOffset)
        dis.title("Student Planner: " + selectedDay)
        graphical.updateForDay(listbox, selectedDay)
    def popup(s):
        popupRoot = tk.Tk()
        popupRoot.after(2000, popupRoot.withdraw())
        popupButton = tk.Button(popupRoot, text = s, font = ("Verdana", 12), bg = "yellow", command = exit)
        popupButton.pack()
        popupRoot.geometry('400x50+700+500')
        popupRoot.mainloop()
    class dateSelector:
        def create():
            #Create a small window for calander dialouge.
            dwin = tk.Tk()
            dwin.geometry("400x220")
            dwin.title("Congifure an event")
            monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            def submit(): #Send info
                #month = monthCounter.curselection()[0] + 1 #Because of list offset
                year = yearBox.get("1.0", tk.END).replace("\n", "")
                #print(year)
                time = timeBox.get("1.0", tk.END).replace("\n", "")
                title = titleBox.get("1.0", tk.END).replace("\n", "")
                desc = descBox.get("1.0", tk.END).replace("\n", "")
                data.edit.write(year, time, title, desc)
                dwin.destroy()
            def newDate(): #update for new date, which is date.today. Deprecated?
                yearBox.delete("1.0", "end")
                yearBox.insert(tk.INSERT, date.today().strftime('%d-%m-%Y'))
            todayB = tk.Button(dwin,
                                    height=5,
                                    width=10,
                                    text="Today",
                                    command=newDate)
            monthCounter = tk.Listbox(dwin,
                                          height=12,
                                          width=10
                                          )
            yearBox = tk.Text(dwin,
                                height=1,
                                width=10,
                                 )
            timeBox = tk.Text(dwin,
                                height=1,
                                width=10)
            yearText = tk.Label(dwin,
                                text="Date:")
            timeText = tk.Label(dwin,
                                text="Time (24 Hour):")
            titleText = tk.Label(dwin,
                                 text="Title:")
            titleBox = tk.Text(dwin,height=2, width=23)
            descText = tk.Label(dwin,
                                 text="Description:")
            descBox = tk.Text(dwin,height=4, width=20)
            submitB = tk.Button(dwin,
                                   text="Submit",
                                   height=3,
                                   width=10,
                                   command=submit)
            #Configure Month List
            i = 0
            for months in monthList:
                monthCounter.insert(i, months)
                i += 1
            #Insert text
            titleText.place(x=200, y=60)
            titleBox.place(x=200,y=80)
            descText.place(x=200, y=130)
            descBox.place(x=200,y=150)
            titleBox.insert(tk.INSERT, "Event Name")
            descBox.insert(tk.INSERT, "A short description of the event")
            yearText.place(x=200,y=5)
            timeText.place(x=200,y=30)
            submitB.place(x=00,y=150)
            yearBox.insert(tk.INSERT, date.today().strftime('%d-%m-%Y'))
            timeBox.insert(tk.INSERT, "12:25")
            todayB.place(x=0,y=0)
            #monthCounter.place(x=100,y=0)
            yearBox.place(x=260,y=6)
            timeBox.place(x=320,y=34)
    def updateForDay(listbox, dateDMY):
        listbox.delete(0, tk.END)
        data.day.setDate(dateDMY)
        eventsInDay = data.schedule.findForDay(dateDMY)
        for sel in eventsInDay:
           infoBox.addObject(listbox,sel[0], sel[1], sel[2], sel[3]) #Add data for current selected day to the listbox.
        
    def loop(self):
        self.dis.mainloop() # Main closing loop
class infoBox:
        # IMPORTANT!
        # Listbox element is currently being passed to add object as ls.
        # All other functions require either self or graphical.
        # This is a dumb workaround that can and will be deprecated.
        def __init__(self, graphical): #Requires graphical for listbox
            self.listbox = graphical.listbox
        def clear(self):
            self.listbox.delete(0,tk.END)
        def addObject(ls, dateDMY, time24, title, desc):
            formattedString = str(time24) + " - " + dateDMY + ": " + title + " - " + desc
            ls.insert(0, formattedString)
#Data class, handles all back-end data formatting       
class data:
    # Here's the data format outline:
    # There is one big array with multiples small arrays
    # They aren't sorted by date.
    # Each array holds several elements
    # [dateDMY, time24, title, desc]
    # dateDMY - a date format in day month year string format, like 12-25-2006
    # time24 - the time of the event, formatted in a float, like 11.12 or 5.54
    # title - title of the event in a string, like "Buy milk for grandma"
    # desc - optional with the write command, a string defining the event with additional info.
    def __init__(self):
        pass
    class day:
        def setToday():
            selectedDay = date.today().strftime('%d-%m-%Y')
        def setDate(dateDMY):
            selectedDay = dateDMY
    class edit:
        def erase():
            pickle.dump([None], open("profile.p", "wb"))
        def write(dateDMY, time24, title, desc="No description for this event."):
            #Check each data type being fed into it
            #Uncomment if you don't trust the data the user is sending.
            #Currently this code is hanging up, want to take a look at where it's slowing down.
            #This demo we assume the userdata is properly formatted.
            #if type(dateDMY) != str or "-" not in dateDMY:
            #    raise TypeError("Invalid datetime object: Should be string type object")
            #if type(time24) != float or time24 > 24.59 or time24 < 0:
            #    return TypeError ("Invalid timestamp for time24: SHould be float")
            #if type(title) != str:
            #    return TypeError("Invalid title: Should be string")
            #elif len(title) > 50:
            #    return NotImplementedError("Can't have a length over 50")
            #if type(desc) != str:
            #    return TypeError("Invalid desc: Should be string")
            #elif len(desc) > 100:
            #    return NotImplementedError("Can't have a length over 100")
            data  = pickle.load(open("profile.p", "rb")) #Get current array 
            data.append([dateDMY, time24, title, desc]) # and then add to it
            pickle.dump(data, open("profile.p", "wb")) # and write/close the data.
        def debugDisp():
            data  = pickle.load(open("profile.p", "rb"))
            print("displayData:")
            print(data)
        def verifyDate():
            pass
        def delete(listboxObject, listBoxID):
           # print(listboxObject.get(listboxObject.curselection()))
            data = pickle.load(open("profile.p", "rb"))
            print(data)
            for items in data:
                if type(items) != type(None): #retrofitting and relatively terrible that this gets eaten up the first palce
                    #finish it first, optimise it later.
                    #print(str(items) + "$|$" + str(listboxObject.get(listboxObject.curselection())))
                    formattedString = str(items[1]) + " - " + items[0] + ": " + items[2] + " - " + items[3]
                    if formattedString == listboxObject.get(listboxObject.curselection()):
                        listboxObject.delete(listboxObject.curselection())
                        data.remove(items) #remove from local list
                        
            pickle.dump(data, open("profile.p", "wb")) #dump to file
            #graphical.moveToday()#update the screen
    class schedule:
        def findForDay(dateDMY):
            data  = pickle.load(open("profile.p", "rb"))
            accumulatedEvents = []
            for eventLog in data:
                try:
                    if eventLog[0] == dateDMY:
                        accumulatedEvents.append(eventLog)
                except TypeError: #Wrong type formatted, silently fail.
                    pass
            return accumulatedEvents
        def checkIfEmpty():
            if pickle.load(open("profile.p", "rb"))[0] == None: return True
            else: return False
# MiDatetime, a simpler version of datetime for this project mostly. Only uses d/m/Y format, so probably not great for formatting.
class MiDateTime:
    def eventStringToDMY(eventString):
        pass
    def getDayInFuture(dayInFuture):
        #https://stackoverflow.com/questions/25120621/python-get-date-in-future-x-days-and-hours-left-to-date
        dt = date.today()
        td = timedelta(dayInFuture)
        unformatted = dt + td
        myDate = unformatted.strftime('%d-%m-%Y')
        return myDate
    def addToDate(date, extra):
        td = timedelta(extra)
        unformatted = date + td
        myDate = unformatted.strftime('%d-%m-%Y')
        return myDate
    def today():
        return date.today().strftime('%d-%m-%Y')
class saintJames:
    def __init__(self):
        pass
    def writeDateInfo(dateDMY, listbox):
        print("started")
        dateFormatted = "2022-2-16"#datetime.strptime(dateDMY, '%d-%m-%y')
        #Double split in between two text expactansies, the event name and URL
        a = requests.get("https://sjakeepingfaith.org/calendar/today/?tribe-bar-date=" +   dateFormatted)#.strftime('%Y-%m-%d'))
        if a != 200:
            return ValueError("Non-200 Response")
        #Now we format the string, which is messy
        #Cut the entire rest of the text besides the event
        #This is a messy bit of code, but basically just trim between the title to get the info.
        #This function only handles one date for now.
        print("before CPU")
        finalMessage = a.text.split('<a class="url" href="https://sjakeepingfaith.org/calendar/a-day-180/" title="A- Day" rel="bookmark">')[1].split("<!-- Event Meta -->")[0].strip().replace("", "")
        print(finalMessage)
        print(data.edit.write(dateDMY, 12.00, finalMessage))
if __name__ == "__main__":
    #data.edit.erase()
    #graphical.popup("bird")
    #print(MiDateTime.getDayInFuture(1))
    win = graphical("500x500", "Student Planner")
    data.edit.debugDisp()
    infoBox(win) #Give win object for editing of listbox
    graphical.loop(win) #Loops main window
else:
    pass #Being imported as a module