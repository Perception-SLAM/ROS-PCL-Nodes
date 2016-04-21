# -*- coding: utf-8 -*-

#simple GUI units are cm



#want FK, traj functions



from Tkinter import *       #importing Tk
import Tkinter as tk
import matplotlib
matplotlib.use("TkAgg")     #importing matplotlib and backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg 
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

root = Tk()                 # creates background (establishes GUI) 
style.use("ggplot")         # nicer looking plots can also do grey scaled 

root.title("Robot GUI")     # names the GUI
root.geometry("1000x650")   # sizes the GUI, though is editable by user 
                            # place all functions and computations before the GUI work so the functions have places to

                            
#To make a quit sequence from the GUI 
#--------------------------------------------------------------------------------------
#DH parameters, though shouldn't need, just good to keep close

alpha = [0,-90,0,-90,90,-90]
a = [0,0,270,70,0,0]
#theta = [t1,t2,t3,t4,t5,t6]#
d = [290,0,0,302,0,0]

#--------------------------------------------------------------------------------------
#function for quit button (example, mostly) 
                            
def quitbut() :                                                           #Defines the function to stop the GUI, will need to be updated for safety measures
    root.destroy()
    return

quitbutton = Button(text="Quit",command=quitbut,font=100,width=10,height=3)#quit button definition
quitbutton.grid(row = 2,column=3,padx=10,pady=10,sticky="s")              #quit button location

#--------------------------------------------------------------------------------------
#Frame for Joint position mode (JPM)

def JointController(J1,J2,J3,J4,J5,J6,a,d):
    #Px = a[2]*(cos(J1)*cos(J2)*cos(J3) - d[5]*(cos(J5)*(cos(J1)*cos(J2)*sin(J3) + cos(J1)*cos(J3)*sin(J2)) + sin(J5)*(sin(J1)*sin(J4) + cos(J4)*(cos(J1)*cos(J2)*cos(J3) - cos(J1)*sin(J2)*sin(J3))) - d[3]*(cos(J1)*cos(J2)*sin(J3) + cos(J1)*cos(J3)*sin(J2)) + a(2)*cos(J1)*cos(J2)
    #Py = a3*(cos(J2)*cos(J3)*sin(J1) - sin(J1)*sin(J2)*sin(J3)) - d6*(cos(J5)
    #J1E-J6E use forward kinematic formulas to figure out ending cartesian positioning currently (though should know where you are already) and after THEN export to trajectory function(s)
    #Using the end point and the requirement of constant accel and v=0 at end and start get a trajectory
    #QUESTION: if I have a function, how do I discretize that for the robot for my traj function(s)? (just 'refresh' 10ms in time and new command until it catches up?)
    return

JointControl = LabelFrame(root, bd=3)       #establishes labelframe for the JPM

J1L = Label(JointControl,text="J1")         #labels for each joint 
J2L = Label(JointControl,text="J2")
J3L = Label(JointControl,text="J3")
J4L = Label(JointControl,text="J4")
J5L = Label(JointControl,text="J5")
J6L = Label(JointControl,text="J6")

J1L.grid(row=2,column=1,padx=13.5,pady=5)   #Locations of labels in the labelframe of JPM
J2L.grid(row=3,column=1,padx=13.5,pady=5)
J3L.grid(row=4,column=1,padx=13.5,pady=5)
J4L.grid(row=5,column=1,padx=13.5,pady=5)
J5L.grid(row=6,column=1,padx=13.5,pady=5)
J6L.grid(row=7,column=1,padx=13.5,pady=5)

J0E = Label(JointControl,text="Desired")
J1E = Entry(JointControl,width=8)           #desired angle input for each joint
J2E = Entry(JointControl,width=8)
J3E = Entry(JointControl,width=8)
J4E = Entry(JointControl,width=8)
J5E = Entry(JointControl,width=8)
J6E = Entry(JointControl,width=8)

J0E.grid(row=1,column=2,padx=5,pady=5)
J1E.grid(row=2,column=2,padx=5,pady=5)      #locations of desired angle in JPM labelframe
J2E.grid(row=3,column=2,padx=5,pady=5)
J3E.grid(row=4,column=2,padx=5,pady=5)
J4E.grid(row=5,column=2,padx=5,pady=5)
J5E.grid(row=6,column=2,padx=5,pady=5)
J6E.grid(row=7,column=2,padx=5,pady=5)


J1 = "J1Mvar"                               #To be REPLACED with incoming data about position
J2 = "J2Mvar"
J3 = "J3Mvar"
J4 = "J4Mvar"
J5 = "J5Mvar"
J6 = "J6Mvar"
J0M = Label(JointControl,text="Measured")  #Measured angle for each joint
J1M = Label(JointControl,width=8,text=J1,bg="grey") 
J2M = Label(JointControl,width=8,text=J2,bg="grey")
J3M = Label(JointControl,width=8,text=J3,bg="grey")
J4M = Label(JointControl,width=8,text=J4,bg="grey")
J5M = Label(JointControl,width=8,text=J5,bg="grey")
J6M = Label(JointControl,width=8,text=J6,bg="grey")

J0M.grid(row=1,column=3,padx=5,pady=5)     #locations of measured angle in JPM labelframe
J1M.grid(row=2,column=3,padx=5,pady=5)       
J2M.grid(row=3,column=3,padx=5,pady=5)
J3M.grid(row=4,column=3,padx=5,pady=5)
J4M.grid(row=5,column=3,padx=5,pady=5)
J5M.grid(row=6,column=3,padx=5,pady=5)
J6M.grid(row=7,column=3,padx=5,pady=5)

J = Label(text="Joint Position Mode")      #Section Level Title
J.grid(row=1,column=1,pady=(20,0))

JointCommandButton = Button(JointControl,text="Command",bg="green",command=JointController) #Command Joint button
JointCommandButton.grid(row=8,column=3,padx=(8,8),pady=8,sticky="N")
                              #--------------------------------------------------------
#copy measured button for the joint space control

def CopyMeasuredJoint() :                                 #Function to remove old data and input new for copy measured 
    J1E.delete(0,35)
    J1E.insert(INSERT,J1)
    J2E.delete(0,35)
    J2E.insert(INSERT,J2)
    J3E.delete(0,35)
    J3E.insert(INSERT,J3)
    J4E.delete(0,35)
    J4E.insert(INSERT,J4)
    J5E.delete(0,35)
    J5E.insert(INSERT,J5)
    J6E.delete(0,35)
    J6E.insert(INSERT,J6)
    return
    
CopyMeasured = Button(JointControl,text="Copy Measured",command=CopyMeasuredJoint)
CopyMeasured.grid(row=8,column=2)                         #Copy measured button

JointControl.grid(row=2,column=1,padx=(8,0),sticky="N")   #Location of the Joint Position mode frame

#--------------------------------------------------------------------------------------
#Frame for Cartesian Position Model(CPM)

def CartesianController():
    # use FK to get current cart position, do I NOT NEED inverse kinematics? 
    # Given knowledge of current point and end effector point, do trajectory and use trajectory functions to discretize and export to robot. 
    return

CartesianControl = LabelFrame(root, bd=3)        #establishes labelframe for the CPM

XL = Label(CartesianControl,text="X")            #labels for each joint 
YL = Label(CartesianControl,text="Y")
ZL = Label(CartesianControl,text="Z")
RollL = Label(CartesianControl,text="Roll")
PitchL = Label(CartesianControl,text="Pitch")
YawL = Label(CartesianControl,text="Yaw")

XL.grid(row=1,column=1,padx=5,pady=5)            #Locations of labels in the labelframe of CPM
YL.grid(row=2,column=1,padx=5,pady=5)
ZL.grid(row=3,column=1,padx=5,pady=5)
RollL.grid(row=4,column=1,padx=5,pady=5)
PitchL.grid(row=5,column=1,padx=5,pady=5)
YawL.grid(row=6,column=1,padx=5,pady=5)

E =  Label(CartesianControl,text="Desired")
XE = Entry(CartesianControl,width=8)             #desired angle input for each joint
YE = Entry(CartesianControl,width=8)
ZE = Entry(CartesianControl,width=8)
RollE =  Entry(CartesianControl,width=8)
PitchE = Entry(CartesianControl,width=8)
YawE =   Entry(CartesianControl,width=8)

E.grid(row=0,column=2,padx=5,pady=5)
XE.grid(row=1,column=2,padx=5,pady=5)            #locations of desired angle in CPM labelframe
YE.grid(row=2,column=2,padx=5,pady=5)
ZE.grid(row=3,column=2,padx=5,pady=5)
RollE.grid(row=4,column=2,padx=5,pady=5)
PitchE.grid(row=5,column=2,padx=5,pady=5)
YawE.grid(row=6,column=2,padx=5,pady=5)

X = "XMvar"                                       #To be REPLACED with incoming data about arm
Y = "YMvar"
Z = "ZMvar"
Roll = "RollMvar"
Pitch = "PitchMvar"
Yaw = "YawMvar"

M =  Label(CartesianControl,text="Measured",bg="grey")
XM = Label(CartesianControl,width=8,text=X,bg="grey")#Measured angle for each joint
YM = Label(CartesianControl,width=8,text=Y,bg="grey")
ZM = Label(CartesianControl,width=8,text=Z,bg="grey")
RollM =  Label(CartesianControl,width=8,text=Roll,bg="grey")
PitchM = Label(CartesianControl,width=8,text=Pitch,bg="grey")
YawM =   Label(CartesianControl,width=8,text=Yaw,bg="grey")

M.grid(row=0,column=3,padx=5,pady=5)
XM.grid(row=1,column=3,padx=5,pady=5)           #locations of measured angle in CPM labelframe
YM.grid(row=2,column=3,padx=5,pady=5)
ZM.grid(row=3,column=3,padx=5,pady=5)
RollM.grid(row=4,column=3,padx=5,pady=5)
PitchM.grid(row=5,column=3,padx=5,pady=5)
YawM.grid(row=6,column=3,padx=5,pady=5)

CartesianCommandButton = Button(CartesianControl,text="Command",bg="green",command=CartesianController) #Command Joint button
CartesianCommandButton.grid(row=7,column=3,padx=(8,8),pady=8,sticky="N")

                                   #---------------------------------------------------
#Copy Measured button for the cartesian control  AND CPM in GUI

def CopyMeasuredCartesian() :                               #Function to use copy measured removing old info and updating new
    XE.delete(0,35)
    XE.insert(INSERT,X)
    YE.delete(0,35)
    YE.insert(INSERT,Y)
    ZE.delete(0,35)
    ZE.insert(INSERT,Z)
    RollE.delete(0,35)
    RollE.insert(INSERT,Roll)
    PitchE.delete(0,35)
    PitchE.insert(INSERT,Pitch)
    YawE.delete(0,35)
    YawE.insert(INSERT,Yaw)
    return

CopyMeasured = Button(CartesianControl,text="Copy Measured",command=CopyMeasuredCartesian)
CopyMeasured.grid(row=7,column=2)                           # Copy measured button

C = Label(text="Cartesian Position Mode")                   #Section label
C.grid(row=3,column=1,pady=(10,0))

CartesianControl.grid(row=4,column=1,padx=(8,0),sticky="Ne")#Location of the Cartesian Position mode frame

#--------------------------------------------------------------------------------------
#unit selection section

var = IntVar()
UnitSelection = LabelFrame(root,bd=3)                                       #frame for the label section
LabelUnit = Label(UnitSelection, text="Units (Δ moves only)")
cmSelect = Radiobutton(UnitSelection,text="cm",value=1, variable=var)       # selection button for cm, value for the conversion is set
inSelect = Radiobutton(UnitSelection,text="in",value=2, variable=var)       # selection for in, value conversion is set to 1 since that will be the working units 

LabelUnit.pack(side = LEFT)                                                 #placing the radiobuttons
cmSelect.pack(side = LEFT)
inSelect.pack(side = LEFT)

UnitSelection.grid(row=5,column=1,sticky="NE")                              #frame on the GUI

#--------------------------------------------------------------------------------------
#Safe button

#function will force return the traj function ending the inputs to the robot and then signaling for breaks engaging

SafeButton = Button(root,activebackground="yellow",bg="red",fg="black",text="SAFE",font=100,width=25,height=5)
SafeButton.grid(row=4,column=2,sticky="NW",padx=10)

#--------------------------------------------------------------------------------------
#hold position button

#Function will force return the traj function ending the inputs to the robot ONLY

HoldPositionButton = Button(root,activebackground="grey",bg="yellow",fg="black",text="Hold Position",font=100,width=25,height=5)
HoldPositionButton.grid(row=4,column=2,sticky="NE",padx=10)

#--------------------------------------------------------------------------------------
#Delta Cartesian Frame


def DeltaController():
    values = var.get()      #uses the radiobuttons to set a conversion to be used by the program
    if values == 1:             #it will be multiplied by inputted values before passed onto IK
        conversion = 1
    if values == 2:
        conversion = 1/2.54
    if values == 0 :
        error = Tk()
        error.title("error")
        L34 = Label(error,text="Must Choose a Unit")
        L34.grid(row=1,column=1,pady=20,padx=20)
    #Convert to in if required by taking inputs and multiplying by the current amount in the ==2 loop
    #Knowing the current position (FK) in space, and delta (so now end) find traj
        return

DeltaMoves = LabelFrame(root,bd=3)                  #Delta moves frame
DeltaLabel = Label(DeltaMoves,text="Delta Moves")
XDL = Label(DeltaMoves,text="ΔX")                   #labels for the dialog
YDL = Label(DeltaMoves,text="ΔY")
ZDL = Label(DeltaMoves,text="ΔZ")

XDE = Entry(DeltaMoves,width=8)                     #entry space fo the dialog
YDE = Entry(DeltaMoves,width=8)
ZDE = Entry(DeltaMoves,width=8)

DeltaLabel.grid(row=0,column=2)                     #placing the labels and entry fields in frame
XDL.grid(row=1,column=1,padx=5,pady=5)
YDL.grid(row=2,column=1,padx=5,pady=5)
ZDL.grid(row=3,column=1,padx=5,pady=5)
XDE.grid(row=1,column=2,padx=5,pady=5)
YDE.grid(row=2,column=2,padx=5,pady=5)
ZDE.grid(row=3,column=2,padx=5,pady=5)

DeltaMoves.grid(row=4,column=2,stick="sw")          # placing frames in the GUI

DeltaCommandButton = Button(DeltaMoves,text="Command",bg="green",command=DeltaController) #Command Joint button
DeltaCommandButton.grid(row=4,column=2,padx=(5,5),pady=5,sticky="N")

#--------------------------------------------------------------------------------------
#Force Feedback

ForceData = LabelFrame(root,bd=3)                        #Frame for force data box

XFD = Label(ForceData,text="XForcevar",bg="grey")        #the force data coming in
YFD = Label(ForceData,text="YForcevar",bg="grey")
ZFD = Label(ForceData,text="ZForcevar",bg="grey")

XFL = Label(ForceData,text="X-Force")                    #the labels for the forces 
YFL = Label(ForceData,text="Y-Force")
ZFL = Label(ForceData,text="Z-Force")

XFD.grid(row=1, column=2,pady=15,padx=8)                 #locations of info in frame
YFD.grid(row=2, column=2,pady=15,padx=8) 
ZFD.grid(row=3, column=2,pady=15,padx=8)
XFL.grid(row=1, column=1,pady=15,padx=8)
YFL.grid(row=2, column=1,pady=15,padx=8)
ZFL.grid(row=3, column=1,pady=15,padx=8)

ForceData.grid(row=2,column=3,padx=5,sticky="N")         #location of frame in GUI

#--------------------------------------------------------------------------------------
#frame including force plots

GraphFrame = LabelFrame(root)                           # establishes the frame

f = Figure(figsize=(6,2.5),dpi=100)                     # sizes the figure in the frame
a = f.add_subplot(111)                                  # adds a single plot in 1 position

def animate(i):                                         # LIVE plot updates as the file is updated with force/torque data
    pullData = open("fileofData.txt","r").read()        #reads in the plot
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList,yList)
    a.axis([0,10,0,17])                                 # axis sizing 
    a.set_ylabel("Force (N)")                           # axis title
    return

Plot = FigureCanvasTkAgg(f,root)                        #establishes the plot
Plot.show()                                             # shows it in the widget 
Plot.get_tk_widget().grid(row=2,column=2)
GraphFrameLabel = Label(root,text="Force")              #Label for graph frame 
GraphFrameLabel.grid(row=1,column=2,sticky="s")         # places into the frame 

GraphFrame.grid(row=2,column=2,padx=5)                  #places frame into the GUI

#--------------------------------------------------------------------------------------
ani = animation.FuncAnimation(f, animate, interval=100)

root.mainloop() #remains last such that it repeats and continues 
