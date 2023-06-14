
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractListModel, Qt
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
from PilotFrm1 import Ui_MainWindow
from SpinBox import Ui_InputForm

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

from dataclasses import dataclass


@dataclass
class N20389:
    Ydata =[1500,1960,2550,2550,1500]    
    Xdata=[52,68,103,125,70]
    Moments=[37,73,47.8,55,95,23]
    EmtyWeight=1439

@dataclass
class N3892Q:
    Ydata =[1500,1960,2300,2300,1500]    
    Xdata=[52,68,88,109,70]
    Moments=[37,73,46,57,95,23]
    EmtyWeight=1429

@dataclass
class N58843:
     Ydata =[1800,2250,2950,2950,1800]    
     Xdata=[57,74,115,143,87]
     Moments=[37,74,97,63,115,23]
     EmtyWeight=1764


@dataclass
class N182WK:
     Ydata =[1800,2250,2950,2950,1800]    
     Xdata=[57,74,115,143,87]
     Moments=[37,74,97,65,115,23]
     EmtyWeight=1799

@dataclass
class N81673:
     Ydata =[1200,2150,2550,2550,1200]    
     Xdata=[102,178,224,237,117]
     Moments=[82,118,95,139,139,23]
     EmtyWeight=1576

clubcraft={'N20389':N20389, 'N3892Q':N3892Q,'N58843':N58843,'N182WK':N182WK,'N81673':N81673}





class WeighModel(QAbstractListModel):
    def __init__(self, *args,**kwargs):
        super(WeighModel,self).__init__(*args,**kwargs)
        
        self.a =[0,1,2,3,4]
        self.b =[10,1,20,3,40]
        self.Pilot =0
        self.Pass = 0
        self.Bagg = 0
        self.Rear = 0
        self.Fuel =0
        self.FuelWeight = 0
        self.clname =" "
        self.Ntotal=0
        self.TotalMom =0
        self.Gvw=0
        self.MomentsGross=0

class MplCanvas(FigureCanvasQTAgg):

    
    def __init__(self,selectedAC,Gvw,Mnts,parent=None,width=6,height=4,dpi=100,):
        fig=Figure(figsize=(width,height),dpi=dpi,)
        
        super().__init__(fig,)
        
        print(Gvw)
        print(Mnts)
       
        px = Mnts
        py = Gvw
        print ("incanvas")
       
        print (selectedAC)
       # print (self.selectedAC)
        ac = clubcraft[selectedAC]
        ac1 = ac
        print(ac1)
        x= ac1.Xdata
        y=ac1.Ydata
        self.axes = fig.add_subplot(111)
        self.axes.set_xlabel('Loaded Airplane Moment/1000 (pound-inches)')
        self.axes.set_ylabel('Loaded Airplane Weight(pounds)')
          
        self.axes.plot(x,y)


       
        
        Drawing_colored_circle=self.axes.scatter(px,py,10) 
        self.axes.add_artist( Drawing_colored_circle )
      
      
      
        
       
        
       

class Custom_Class(QWidget,Ui_InputForm):
    def __init__(self, ) -> None:
        super().__init__()
        self.setupUi(self)
       

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,) -> None:
        super().__init__()
        self.setupUi(self)
        self.model = WeighModel()
        #self.comboBox.view().pressed.connect(self.Aircraft)
        self.comboBox.currentIndexChanged.connect(self.Aircraft)
                        
        self.Cmd_Pilot.clicked.connect(self.Pilot_Select)
        self.Cmd_Passenger.clicked.connect(self.Passenger_Select)
        self.Cmd_Rear.clicked.connect(self.Rear_Select)
        self.Cmd_Rear_2.clicked.connect(self.Baggage_Select)
        self.Cmd_Rear_3.clicked.connect(self.Select_Fuel)
        self.cmd_submit.clicked.connect(self.UpdateFrm)

             
        #sc = MplCanvas(self,width=5, height=4,dpi=100)
       

        

        x = self.model.a
        y= self.model.b
       
       
        #sc.axes.plot(x,y)
        #self.setCentralWidget(sc)
    def Pilot_Select(self,):
        print("in Select Pilot")
        self.win = Custom_Class()
        self.win.setWindowTitle("Pilot")
        self.mode =1
        self.win.Cmd_Dial.setRange(0, 500)
        self.win.Cmd_Dial.setSingleStep(10)
        self.win.spinBox.setSingleStep(1)
        self.win.Cmd_Accept.clicked.connect(self.AcceptValues)
        self.win.spinBox.valueChanged.connect(self.BoxChanged)
       
        self.win.show()
        
        self.win.Cmd_Dial.valueChanged.connect(self.value_changed)

    def Passenger_Select(self):
        self.win = Custom_Class()
        self.win.setWindowTitle("Passenger")

        self.win.groupBox.setTitle("Passenger Weight")
        

        self.mode = 2
        self.win.Cmd_Dial.setRange(0, 500)
        self.win.Cmd_Dial.setSingleStep(10)
        self.win.spinBox.setSingleStep(1)
        self.win.Cmd_Accept.clicked.connect(self.AcceptValues)
        self.win.spinBox.valueChanged.connect(self.BoxChanged)
        self.win.show()
        self.win.Cmd_Dial.valueChanged.connect(self.value_changed)

    def Rear_Select(self):
        self.win = Custom_Class()
        self.win.setWindowTitle("Rear Passenger")
        self.win.groupBox.setTitle("Rear Passengers Wgt")
        self.mode = 3
        self.win.Cmd_Dial.setRange(0, 500)
        self.win.Cmd_Dial.setSingleStep(10)
        self.win.spinBox.setSingleStep(1)
        self.win.Cmd_Accept.clicked.connect(self.AcceptValues)
        self.win.spinBox.valueChanged.connect(self.BoxChanged)
        self.win.show()
        self.win.Cmd_Dial.valueChanged.connect(self.value_changed)

    def Baggage_Select(self):

        self.win = Custom_Class()
        self.win.setWindowTitle("Baggage")
        self.win.groupBox.setTitle("Baggage LBS")
        self.mode = 4
        self.win.Cmd_Dial.setRange(30, 200)
        self.win.Cmd_Dial.setSingleStep(10)
        self.win.spinBox.setSingleStep(1)
        self.Lbl_Bags.setText("20")
        self.win.Cmd_Accept.clicked.connect(self.AcceptValues)
        self.win.spinBox.valueChanged.connect(self.BoxChanged)
        self.win.show()
        self.win.Cmd_Dial.valueChanged.connect(self.value_changed)
    
    def Select_Fuel(self):
        self.win = Custom_Class()
        self.win.setWindowTitle("Fuel")
        self.win.groupBox.setTitle("Fuel in Gallons")
        self.mode = 5
        self.win.Cmd_Dial.setRange(5, 100)
        self.win.Cmd_Dial.setSingleStep(1)
        self.win.spinBox.setSingleStep(1)
     
        self.win.Cmd_Accept.clicked.connect(self.AcceptValues)
        self.win.spinBox.valueChanged.connect(self.BoxChanged)
        self.win.show()
        self.win.Cmd_Dial.valueChanged.connect(self.value_changed)
    
    def UpdateFrm(self):
        print("Update")
        self.win = MplCanvas(selectedAC=self.model.clname,Gvw=self.model.Gvw,Mnts=self.model.MomentsGross)
        print(self.model.clname)
       
        self.win.setWindowTitle("WeightBallance")
        self.win.show()


    def BoxChanged(self):
        NewIntVal=self.win.spinBox.value()
        newVal = str(self.win.spinBox.value())
        if self.mode ==1:
            self.Lbl_Pilot.setText(newVal+" "+"Lbs")
            self.model.Pilot=int(newVal)
           
        elif self.mode==2:
            self.Lbl_Pass.setText(newVal+" "+"Lbs")
            self.model.Pass = int(newVal)
        elif self.mode==3:
            self.Lbl_Rear.setText(newVal+" "+"Lbs")
            self.model.Rear = NewIntVal
        elif self.mode==4:
            self.Lbl_Bags.setText(newVal+" "+"Lbs")
            self.model.Bagg = NewIntVal
        elif self.mode==5:
            intVal=self.win.spinBox.value()
            FuelWgt=intVal*6.0
            self.model.Fuel=NewIntVal
            newVal=str(FuelWgt)
            self.Lbl_Bags_2.setText(newVal+" "+"Lbs")
            self.model.FuelWeight=FuelWgt
           
       
       
    def value_changed(self,i):
        
        self.win.spinBox.setValue(i)


    def AcceptValues(self,i):
        print("inAccpet")
       
        self.model.c=self.win.spinBox.value()
        self.Ntotal = (self.model.Pilot + self.model.Pass + self.model.Bagg + self.model.Rear +self.model.FuelWeight )  
        self.Front_total = (self.model.Pilot + self.model.Pass) 
        self.CalculateValues(self.Ntotal)
        stTot=str(self.model.Gvw) 


        self.Lbl_Total.setText(stTot)
        self.Lbl_Mom.setText(self.model.TotalMom)
  
       
        self.win.close()


    def CalculateValues(self,x):
        
        ac = clubcraft[self.model.clname]
        ac1 = ac
        A=ac1.EmtyWeight
        print(A)
        b=self.Ntotal
        self.model.Gvw= (A+b)
        print(self.Ntotal)
        print(self.model.Gvw)
        Pi=ac1.Moments[0]
        Bs=ac1.Moments[4]
        R=ac1.Moments[1]
        Fu=ac1.Moments[2]
        Ept=ac1.Moments[3]
        print (Pi)
        FrontPeople = self.Front_total * Pi/1000
        RearSeat = self.model.Rear * R /1000
        Baggage = self.model.Bagg * Bs / 1000
        Fuel= self.model.FuelWeight * Fu/1000
        EM_Moment=ac1.EmtyWeight * Ept/1000
        self.totalMoments =(Fuel+Baggage+RearSeat+FrontPeople+Ept)
        self.model.MomentsGross = self.totalMoments
        self.model.TotalMom=str(self.totalMoments)



        print (FrontPeople)
        print(RearSeat)
        print(Baggage)
        print(Fuel)
        print(self.model.FuelWeight)
        print(self.totalMoments)

        


    def Aircraft(self,clname):
        
        self.air = self.comboBox.currentText()
        print(self.air)

        print(self.model.clname)
        self.model.clname = self.air
        print(self.model.clname)

        
       
        win = Custom_Class()
   
app = QtWidgets.QApplication(sys.argv)
w =  MainWindow()
w.show()
app.exec_()