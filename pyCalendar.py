#   Programmeringsteknik webbkurs KTH Prototyp P-uppgift 110 Kalender 0.3.1
#   Daniel Lindfors
#   bossebl.op@gmail.com
#   28/6 - 2012
#
#   Detta program genererar och visar alla dagar i en viss given månad, under ett visst givet år,
#   genom ett grafiskt användargränssnitt. Alla "röda" dagar samt dagens dag markeras av programmet.



# <<<<Importering>>>>


# datetime hjälper till med att hantera datum. tkinter bygger man ett grafiskt användargränssnitt med.

from datetime import *
from tkinter import *



# <<<<Klasser>>>>


# CalendarWidget är en widget klass till tkinter. Dess enda funktion är att skapa en kalender som kan visas.
# CalendarWidget är beroende av datetime, tkinter, isHoliday funktionen och vissa av de globala konstanterna

class CalendarWidget(Frame):


    #   __init__() parametrar:
    #       root: rot widget. ett tkinter objekt i vilket CalendarWidget verkar i.
    #       y: året som CalendarWidget ska visa en månad för. har nuvarande år som förinställt värde
    #       m: månaden som CalendarWidger ska visa. har nuvarande månad som förinställt värde
    #       option: parametrar kopplade till tkinter klassen Frame som CalendarWidget ärver från
    #
    #   CalendarWidget attributer:
    #       samtliga Frame attributer
    #       self.date: ett datetime objekt som förvarar den månaden som ska visas
    #
    #   CalendarWidget metoder:
    #       samtliga Frame metoder
    
    
    def __init__(self, root, y = datetime.today().year, m = datetime.today().month, **option):
        Frame.__init__(self, root, option)

        self.date = datetime(y, m, 1)

        
        # om dagens dag finns med i den angivna månaden så sätts today till dagens dag. annars förblir today 0.
        today = 0
        if self.date.year == datetime.today().year:
            if self.date.month == datetime.today().month:
                today = datetime.today().day


        # loopar genom den översta raden i kalendern och sätter ut veckodagarnas namn i tur och ordning
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = MONDAY
        for dayName in weekdays:
            Label(self, text = dayName, width = 8).grid(row = 0, column = weekday + 1)
            weekday += 1


        # loopar genom den första kolumnen i kalendern och skriver ut veckonummer
        for i in range(6):
            Label(self, text = str(self.date.isocalendar()[1]), width = 3).grid(row = i + 1, column = 0)
            self.date += timedelta(days = 7)


        # återställer datumet till ursprungs värdet
        self.date = datetime(y, m, 1)


        # skriver "W\D" i det övre vänstra hörnet på kalendern. W = Week, D = Day. 
        Label(self, text = "W\D", width = 3).grid(row = 0, column = 0)
        

        # loopar genom varje kolumn och rad i kalendern och sätter ut det motsvarande datumet. 
        calendarRow = 1
        weekday = self.date.weekday()

        while self.date.month == m:
            calendarElement = Label(self, text = str(self.date.day), bg = "black")
            
            if isHoliday(self.date):
                calendarElement.configure(fg = "red")
            else:
                calendarElement.configure(fg = "white")

            if self.date.day == today:
                calendarElement.configure(borderwidth = 2, relief = SUNKEN)

            calendarElement.grid(row = calendarRow, column = weekday + 1)

            self.date += timedelta(days = 1)
            weekday += 1

            if weekday > SUNDAY:
                calendarRow += 1
                weekday = MONDAY


        # sätter attributen date till det ursprungliga värdet igen
        self.date = datetime(y, m, 1)


        # sätter en sträng nere i högra hörnet på kalendern som visar vilket år och månad det är. monthName är en global konstant.
        Label(self, text = monthName[m] + " " + str(y), fg = "white", bg = "black").grid(row = 6, column = 6, columnspan = 2)





                    
# En tkinter widget klass som skapar en meny,som kan placeras vart som helst i gränssnittet, med radio knappar.
# Denna meny används för att välja månad i programmet. den ärver från tkinter klassen Menubutton. är beroende av tkinter

class DropboxWidget(Menubutton):

    #   __init__() parametrar:
    #       root: rot widget. ett tkinter objekt i vilket DropboxWidget verkar i.
    #       option: attributer kopplade till tkinter klassen Menubutton som DropboxWidget ärver från
    #
    #   DropboxWidget attributer:
    #       samtliga Menubutton attributer
    #       self.var: en variabel kopplad till radio knapparna i menyn. var antar värdet av den aktiva radio knappen
    #       self.menu: ett objekt av tkinter klasse Menu. denna håller alla radio knappar som ska visas när man trycker på menyn
    #
    #   DropboxWidget metoder:
    #       samtliga Menubutton metoder
    #       addRadioButtons(textvalueList): tar en lista med namn och värden och skapar därefter radio knappar efter dessa
    #       get(): returnerar värdet på den radio knappen som är aktiverad
    #       callback(): används som komando på samtliga radio knappar. den ser till att meny knappens namn är samma som den aktiva radio knappens


    def __init__(self, root, **option):
        Menubutton.__init__(self, root, option)
        self.var = IntVar()

        self.menu = Menu(self)
        self["menu"] = self.menu


    def addRadioButtons(self, textvalueList):
        for textvalue in textvalueList:
            self.menu.add_radiobutton(label = textvalue[0], variable = self.var, value = textvalue[1], command = self.callback)

    
    def get(self):
        return self.var.get()

    
    def callback(self):
        self.configure(text = monthName[self.var.get()])





            
#   En klass som håller hela programmets grafiska användargränssnitt.   

class Gui(Frame):

    #   __init__() parametrar:
    #       root: tkinter widget som Gui verkar i.
    #       option: attributer kopplade till tkinter klassen Frame som Gui ärver från
    #
    #   Gui attributer:
    #       samtliga attributer från Frame
    #       samtliga objekt som loadWidgets() skapar       
    #
    #   Gui metoder:
    #       samtliga metoder från Frame
    #       loadWidgets(): laddar alla element i det grafiska användargränssnittet
    #       getCalendar(): en kommando funktion som hämtar kalendern för den angivna månaden
    #       getTodayCalendar(): en kommando funktion som hämtar kalendern för den nuvarande månaden
    #       getPrevCalendar(): en kommando funktion som hämtar kalendern för månaden innan den som visas för tillfälligt
    #       getNextCalendar(): en kommando funktion som hämtar kalendern för månaden efter den som visas för tillfälligt
    #       errorMessage(strint): visar ett informations fönster med texten i string
    #       getCalendarEvent(): en kommand funktion som kopplas till ett event. Kallar på getCalendar()
    #       infoWindow(): en kommando funktion som visar ett fönster med information om programmet

    def __init__(self, root, **option):
        Frame.__init__(self, root, option)
        self.loadWidgets()


    def loadWidgets(self):


        # skapar alla element
        
        self.navigationFrame = Frame(self)
        
        self.getButton = Button(self.navigationFrame, text = "get", command = self.getCalendar)
        
        self.todayButton = Button(self.navigationFrame, text = "today", command = self.getTodayCalendar)
        
        self.yearLabel = Label(self.navigationFrame, text = "Year")
        
        self.monthLabel = Label(self.navigationFrame, text = "Month")

        self.yearEntry = Spinbox(self.navigationFrame, from_ = 1900, to = 3000, textvariable = "2000", width = 10)
        self.yearEntry.delete(0, END)
        self.yearEntry.insert(INSERT, "Year")
        
        self.monthEntry = DropboxWidget(self.navigationFrame, text = "Month", width = 10)
        textvalueList = [["January",JANUARY],["February", FEBRUARY],["March",MARCH],["April", APRIL],["May", MAY], ["June", JUNE],["July", JULY],["August", AUGUST],["September", SEPTEMBER],["October", OCTOBER],["November", NOVEMBER],["December", DECEMBER]]
        self.monthEntry.addRadioButtons(textvalueList)

        self.prevButton = Button(self.navigationFrame, text = "<Prev", command = self.getPrevCalendar)
        self.nextButton = Button(self.navigationFrame, text = "next>", command = self.getNextCalendar)

        self.infoButton = Button(self.navigationFrame, text = "Info", command = self.infoWindow)

        self.calendar = CalendarWidget(self, borderwidth = 1, relief = SUNKEN, bg = "black")


        # placerar ut alla element
        
        self.navigationFrame.grid(row = 0, sticky = W)
        self.calendar.grid(row = 1)

        self.yearLabel.grid(row = 0, column = 2)
        self.monthLabel.grid(row = 0, column = 3)
        self.getButton.grid(row = 1, column = 4)
        self.todayButton.grid(row = 1, column = 0, columnspan = 2)
        self.yearEntry.grid(row = 1, column = 2)
        self.monthEntry.grid(row = 1, column = 3)
        self.prevButton.grid(row = 2, column = 0, sticky = W)
        self.nextButton.grid(row = 2, column = 1, sticky = W)
        self.infoButton.grid(row = 0, column = 5, padx = 50)


        # binder events till funktioner
        
        self.yearEntry.bind("<Return>", self.getCalendarEvent)


    # binds till getButton. visar inmatad kalendermånad
    def getCalendar(self):

        # visar ett felmedelande i nytt fönster om användaren gör en felinmatning        
        if not(self.yearEntry.get().isdigit()):
            self.errorMessage("You must enter the year as digits.\nYou entered: " + self.yearEntry.get())
            return
        if not(1900 <= int(self.yearEntry.get()) <= 3000):
            self.errorMessage("The year must be between 1900 and 3000.\nYou entered: " + self.yearEntry.get())
            return
        if not(1 <= self.monthEntry.get() <= 12):
            self.errorMessage("You must select a month. No month is selected")
            return


        # skapar en ny kalender med värdena från inmatningen och placerar ut
        year = int(self.yearEntry.get())
        month = self.monthEntry.get()
        temporaryCalendar = CalendarWidget(self, year, month, borderwidth = 1, bg = "black")
        self.calendar.grid_forget()
        self.calendar = temporaryCalendar
        self.calendar.grid(row = 2)
        

    # binds till todayButton.visar dagens kalendermånad
    def getTodayCalendar(self):

        # skapar en ny kalender med värdena från dagens datum och placerar ut
        today = datetime.today()
        temporaryCalendar = CalendarWidget(self, today.year, today.month, borderwidth = 1, bg = "black")
        self.calendar.grid_forget()
        self.calendar = temporaryCalendar
        self.calendar.grid(row = 2)
        
        
    # binds till prevButton. hoppar bak en kalendermånad
    def getPrevCalendar(self):

        # skapar en ny kalender med värdena från en tidigare månad och placerar ut
        year = self.calendar.date.year
        month = self.calendar.date.month
        if month == JANUARY:
            year -= 1
            month = DECEMBER
        else:
            month -= 1

        temporaryCalendar = CalendarWidget(self, year, month, borderwidth = 1, bg = "black")
        self.calendar.grid_forget()
        self.calendar = temporaryCalendar
        self.calendar.grid(row = 2)
        

    # binds till nextButton. hoppar fram en kalendermånad
    def getNextCalendar(self):

        # skapar en ny kalender med värdena från en senare och placerar ut
        year = self.calendar.date.year
        month = self.calendar.date.month
        if month == DECEMBER:
            year += 1
            month = JANUARY
        else:
            month += 1

        temporaryCalendar = CalendarWidget(self, year, month, borderwidth = 1, bg = "black")
        self.calendar.grid_forget()
        self.calendar = temporaryCalendar
        self.calendar.grid(row = 2)


    # visar ett felmedelande
    def errorMessage(self, string):
        messagebox.showwarning("Error", string)


    # binds till enter knappen. kallar på funktionen bunden till getButton
    def getCalendarEvent(self, event):
        self.getButton.invoke()

    # binds till infoButton. Visar informations fönster.
    def infoWindow(self):
        string = "Welcome to the calendar program. This program is designed generate a calendar over a given month and year."
        messagebox.showinfo("info", string)






# En klass som håller i hela programmet

class App():

    #   __init__() parametrar:
    #       root: rot widget. ett tkinter objekt som programmet grafiska användargränssnitt verkar i.
    #
    #   App attributer:
    #       self.gui: programmets grafiska användargränssnitt
    #
    #   App metoder:
    #       run(): kör programmet
    #       exit(): avslutar programmet
    
    def __init__(self, root):
        self.gui = Gui(root, borderwidth = 20)
        self.gui.grid()


    def run(self):
        
        # startar anvädargränssnittets huvud loop
        self.gui.mainloop()


    def exit(self):
        # gör ingenting än så länge. utvidgas endast vid behov
        return



# <<<<Global constants>>>>

# gör programmet lite mer lätt läsligt
MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

JANUARY = 1
FEBRUARY = 2
MARCH = 3
APRIL = 4
MAY = 5
JUNE = 6
JULY = 7
AUGUST = 8
SEPTEMBER = 9
OCTOBER = 10
NOVEMBER = 11
DECEMBER = 12


# spar programmet från en massa if satser då man ska ha namnet på en uträknad månad.
monthName = {1:"January" , 2:"February" , 3:"March" , 4:"April" , 5:"May" , 6:"June", 7:"July" , 8:"August" , 9:"September" , 10:"October" , 11:"November" , 12:"December"}



# <<<<Funktioner>>>>

# tar ett datetime objekt som parameter. Returnerar True om datumet är en röd dag. annars False
def isHoliday(date):
        # alla söndagar
        if date.weekday() == SUNDAY:
            return True
        # tretton dagen
        elif date.day == 6 and date.month == JANUARY:
            return True
        # första maj
        elif date.day == 1 and date.month == MAY:
            return True
        # midsommardagen
        elif date.month == JUNE and (20 <= date.day <= 26) and date.weekday() == SATURDAY:
            return True
        # alla helgons dag
        elif ( (date.month == OCTOBER and date.day == 31) or (date.month == NOVEMBER and 1 <= date.day <= 6) ) and date.weekday() == 5:
            return True
        # julens helgdagar
        elif date.month == DECEMBER and (date.day == 25 or date.day == 26):
            return True
        # nyårsdagen
        elif date.month == JANUARY and date.day == 1:
            return True
        # national dagen
        elif date.month == JUNE and date.day == 6:
            return True
        else:
            century = int(date.year/100) + 1
            G = date.year%19 + 1
            X = int(3*century/4) - 12
            Z = int((8*century + 5)/25) - 5
            
            E = (11*G + 20 + Z-X)%30
            if E == 25 and G > 11:
                E += 1
            if E == 24:
                E += 1

            N = 44 - E
            if N < 21:
                N += 30

            D = int(5*date.year/4) - X- 10
            S = N + 7 - (D + N)%7

            dS = datetime(year = date.year, month = 3, day = 1) + timedelta(days = S - 1)
            # påsk
            if date == dS:
                return True
            # annandag påsk
            if date == dS + timedelta(days = 1):
                return True
            #långfredag 
            if date == dS - timedelta(days = 2):
                return True
            # kristi himmelfärd *
            if date == dS + timedelta(days = 39):
                return True
            # pingst
            if date == dS + timedelta(days = 49):
                return True

        return False



# <<<<Initialisering>>>>

# skapar ett tkinter huvud fönster och ett App objekt
root = Tk()
root.resizable(width = False, height = False)
root.wm_title("110 Calendar")

app = App(root)



# <<<<Program loop>>>>

# kör programmet    
app.run()



# <<<<Exit>>>>

# avslutar programmet    
app.exit()
