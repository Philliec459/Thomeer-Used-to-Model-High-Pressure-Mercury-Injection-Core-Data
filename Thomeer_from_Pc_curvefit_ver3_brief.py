# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 09:50:53 2019

@author: craig
"""
#import sys

#from IPython import get_ipython
#get_ipython().magic('reset -sf')


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
#from PyQt5.QtCore import QTimer
#******************************************************************
import matplotlib

import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")
import matplotlib.gridspec as gridspec
#******************************************************************
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
from numpy import diff






# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #                Read Pc Data Spreadsheet 
# # #  
# # #             
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
#read the file
#file = r'Pc_data_fmin.xlsx'
file = r'Pc_data_dual_porosity.xlsx'

Thomeer_Pc_data = pd.read_excel(file,index_col=False)

Pc_r = Thomeer_Pc_data['Pc']
BVocc_r = Thomeer_Pc_data['BVocc']

x_Pc=np.array(BVocc_r)
y_Pc=np.array(Pc_r)
# =============================================================================
# # ===========================================================================
# # #------------------------------------------------------------ 
# # #               
# # #     End of reading in Pc data
# # #------------------------------------------------------------
# # ===========================================================================
# =============================================================================








# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# ##
# ##            Graphical Input of User Porosity and Pereability 
# ##
# # #--------------------------------------------------------------------------
# =============================================================================
# =============================================================================
# =============================================================================
#             Graphical Input for Closure Correction and Pd1 
# =============================================================================
def tellme(s):
    print(s)
    plt.title(s, fontsize=16, color = 'blue')
    plt.draw()


plt.clf()   #clear plot of other things

plt.figure(num=2, figsize=(10, 10))
#plt.ion()
plt.loglog(x_Pc, y_Pc  , 'g-*', linewidth=1, label='HPMI Data' )
plt.xlim(50.0,  0.1)
plt.ylim(1, 100000)
plt.grid(True, which="both",ls="-")
plt.legend()

#Use pts array to store selected points
pts = []

while len(pts) < 1:
    tellme('Select Closure Correction and Pd1')
    pts = np.asarray(plt.ginput(1, timeout=3))

Closure = pts.item(0)
Pd1 = pts.item(1)

print()
print('Closure Correction =', Closure, ' and Pd1 =', Pd1)
print()

plt.close('all')
# =============================================================================
#             End of Graphical Input for Closure Correction and Pd1 
# =============================================================================



# =============================================================================
#           Closure Correction of Pc data
# =============================================================================
x_Pc_nocc = np.array(BVocc_r)
for i in range(0,len(Thomeer_Pc_data),1):
    
    BVocc_r[i]=BVocc_r[i]-Closure
    
    if BVocc_r[i] < 0:
        BVocc_r[i] = 0.001
    else:
        BVocc_r[i] = BVocc_r[i]

x_Pc=np.array(BVocc_r)
#print(x_Pc_nocc)
#print(x_Pc)
# =============================================================================
#          End of Closure Correction for Pc data
# =============================================================================



# =============================================================================
#             Graphical Input for Pd2 and BV1
# =============================================================================
def tellme(s):
    print(s)
    plt.title(s, fontsize=16, color = 'blue')
    plt.draw()

plt.clf()   #clear plot of other things

plt.figure(num=2, figsize=(10, 10))

plt.loglog(x_Pc, y_Pc  , 'b-*', linewidth=1, label='HPMI Data' )
plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
plt.xlim(50.0,0.1)
plt.ylim(1, 100000)
plt.grid(True, which="both",ls="-")
plt.legend()

pts = []


while len(pts) < 1:
    tellme('Select BV1 and Pd2')
    pts = np.asarray(plt.ginput(1, timeout=3))

BV1 = pts.item(0)
Pd2 = pts.item(1)

print()
print('BV1 =', BV1, ' and Pd2 =', Pd2)
print()

plt.close('all')  
# =============================================================================
#             End of Graphical Input for Pd2 and BV1
# =============================================================================



# =============================================================================
#             Graphical Input for BVtotal
# =============================================================================

def tellme(s):
    print(s)
    plt.title(s, fontsize=16, color = 'blue')
    plt.draw()

plt.clf()   #clear plot of other things

plt.figure(num=2, figsize=( 10, 10))

plt.loglog(x_Pc, y_Pc  , 'r-*', linewidth=1, label='HPMI Data' )
plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
plt.loglog(BV1, Pd2  , 'k-o', linewidth=1, label='BV1 and Pd2 Estimate' )
plt.xlim(50.0,0.1)
plt.ylim(1, 100000)
plt.grid(True, which="both",ls="-")
plt.legend()

#Use pts array to store selected points
pts = []


while len(pts) < 1:
    tellme('Select BVtotal')
    pts = np.asarray(plt.ginput(1, timeout=3))

BVtotal = pts.item(0)
junk = pts.item(1)

print()
print('BVtotal =', BVtotal)
print()


plt.close('all')  
# =============================================================================
#             End of Graphical Input of BVtotal
# =============================================================================










# =============================================================================
#             Scipy for Curve_fit of Pd1, G1 and BV1
# =============================================================================
from scipy.optimize import curve_fit


bvarray_pore1 = []; #make list of 0 length
pcarray_pore1 = []

for i in range(1, 118, 1):
    if Pc_r[i] > Pd1 and Pc_r[i] < Pd2 :
        BVOCC = (BVocc_r[i])

        bvarray_pore1.append(BVocc_r[i]); #add items 
        pcarray_pore1.append(Pc_r[i]); #add items     

    
ydata=np.array(bvarray_pore1)
xdata=np.array(pcarray_pore1)

def func(xdata, a, b, c):
    return a*10**((-0.434*b)/np.log10(xdata/c))


#popt, pcov = curve_fit(func, ydata, xdata, bounds=([Pd1*0.5, 0.01, BV1*0.5], [Pd1*1.5, 3., BV1*2]))
popt, pcov = curve_fit(func, ydata, xdata, bounds=([Pd1*0.9, 0.01, BV1*0.5], [Pd1*2, 3., BV1*2]))
#popt, pcov = curve_fit(func,ydata,xdata,p0=[Pd1,0.1,BV1], bounds=(-np.inf,np.inf))


#Pd1_solve = Pd1
Pd1_solve=popt[0]
G1_solve=popt[1]
BV1_solve=popt[2]
BV2 = BVtotal - BV1


print('      Pd1 pick =',Pd1,', G1 or popt[1] =',popt[1],',      BV1 pick =',BV1)
print('Pd1 or popt[0] =',popt[0],', G1 or popt[1] =',popt[1],', BV1 or popt[2] =',popt[2])
print('Pd1 or popt[0] =',Pd1_solve,', G1 or popt[1] =',G1_solve,', BV1 or popt[2] =',BV1_solve)
print()
# =============================================================================
#             Scipy for Curve_fit of Pd2, G2 and BV2
# =============================================================================
bvarray_pore2 = []; #make list of 0 length
pcarray_pore2 = []

for i in range(1, 118, 1):
    if Pc_r[i] > Pd2 :
        BVOCC = (BVocc_r[i])

        bvarray_pore2.append(BVocc_r[i]); #add items 
        pcarray_pore2.append(Pc_r[i]); #add items     

    
ydata2=np.array(bvarray_pore2)
xdata2=np.array(pcarray_pore2)

def func(xdata2, a, b, c):
    return a*10**((-0.434*b)/np.log10(xdata2/c))


#popt, pcov = curve_fit(func, ydata2, xdata2, bounds=([1, 0.01, 0.0], [30000., 3., 100.]))
popt, pcov = curve_fit(func, ydata, xdata, bounds=([Pd2*0.5, 0.01, (BVtotal-BV1)*0.5], [Pd2*1.5, 0.5, (BVtotal-BV1)*2]))

Pd2_solve=popt[0]
G2_solve=popt[1]
BV2_solve=popt[2]


print('      Pd2 pick =',Pd2,', G1 or popt[1] =',popt[1],', BV2 pick       =',BV2)
print('Pd2 or popt[0] =',popt[0],', G2 or popt[1] =',popt[1],', BV2 or popt[2] =',popt[2])
print('Pd2 or popt[0] =',Pd2_solve,', G2 or popt[1] =',G2_solve,', BV2 or popt[2] =',BV2_solve)
print()



# =============================================================================
#             Create Pc Curves for curve fit Thomeer parameters
# =============================================================================
Pc = 0.5
bvarray_pred = []; #make list of 0 length
pcarray_pred = []

for j in range(1, 105, 1):
    if Pc > Pd1_solve:
        BVOCC1 = BV1_solve * 10**((-0.434 * G1_solve) / np.log10(Pc / Pd1_solve))
    else:
        BVOCC1 = 0.001

    if Pc >= Pd2:
        BVOCC2 = (BVtotal-BV1) * 10**((-0.434 * G1_solve) / np.log10(Pc / Pd2))
    else:
        BVOCC2 = 0.001


    BVOCC = BVOCC1 + BVOCC2

    bvarray_pred.append(BVOCC); #add items 
    pcarray_pred.append(Pc); #add items 
    
    Pc = Pc * 1.12

   
x_solve=np.array(bvarray_pred)
y_solve=np.array(pcarray_pred)
# =============================================================================
#             End of Scipy for Curve_fit of Pd1, G1 and BV1
# =============================================================================

# =============================================================================
#             Pc Curve GUI Picks
# =============================================================================
Pc = 0.5
bvarray_gui = []; #make list of 0 length
pcarray_gui = []

G1=.6

for j in range(1, 105, 1):
    if Pc > Pd1:
        BVOCC1 = BV1 * 10**((-0.434 * G1) / np.log10(Pc / Pd1))
    else:
        BVOCC1 = 0.001

    if Pc >= Pd2:
        BVOCC2 = (BVtotal-BV1) * 10**((-0.434 * .1) / np.log10(Pc / Pd2))
    else:
        BVOCC2 = 0.001


    BVOCC = BVOCC1 + BVOCC2

    bvarray_gui.append(BVOCC); #add items 
    pcarray_gui.append(Pc); #add items 
    
    Pc = Pc * 1.12

   
x_gui=np.array(bvarray_gui)
y_gui=np.array(pcarray_gui)












# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #                
# # #               Qt GUI Plots made here
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

#Define Canvas
class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 50
        self.top = 100
        self.title = 'Carbonate Petrophysical Analysis'
        self.width = 1000
        self.height = 1000
        self.initUI()




    #Define Canvas and Pushbutton
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # this defines the width and height of canvas 
        m = PlotCanvas(self, width=10, height=10)
        m.move(0,0)



        button = QPushButton('Quit Window', self)
        button.setDefault(True)
        button.setToolTip('Push this button to quit')
        #Botton starts at 500 and 0
        button.move(400,0)
        #Botton starts at 500 and goes +140 to 640 to cover canvas
        button.resize(100,30)

#        def on_button_clicked():
#            alert = QMessageBox()
#            alert.setText('You clicked the button!')
#            alert.exec_()
        def on_button_clicked():
            sys.exit(app.exec_())



        button.clicked.connect(on_button_clicked)


        self.show()


class PlotCanvas(FigureCanvas):

#what is this???
    def __init__(self, parent=None, width=5, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
#            self.axes = fig.add_subplot(211)  apparently not needed now

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plot()
        #self.plot2()
        #self.plot3()
        #self.plot4()


# Pc Plot across top 0 to 3
    def plot(self):

        gs = gridspec.GridSpec(nrows=3, 
                               ncols=3, 
#                               figure=fig, 
                               width_ratios= [1, 1, 1],
                               height_ratios=[1, 1, 1],
                               wspace=0.3,
                               hspace=0.3)
#wspace = 0.2   # the amount of width reserved for blank space between subplots
#hspace = 0.2   # the amount of height reserved for white space between subplots 

       
#        ax = self.figure.add_subplot(411) 
        ax = self.figure.add_subplot(gs[0:3, 0:3]) 
        
        
        #ax.loglog(x2, y2, 'r-'  , linewidth=3 , label='Nearest Pc Curve')
        ax.loglog(x_Pc_nocc, y_Pc, 'k--' , linewidth=1 ,markersize = 1, label='Actual Pc Curve')
        #ax.loglog(x5, y5, 'b--' , linewidth=3 , label='kNN Pc Curve')
        ax.loglog(x_Pc, y_Pc, 'g-' , linewidth=4 , label='Closure Corrected Pc Curve')
        #ax.loglog(x_gui  , y_gui,   'b--' , linewidth=1 , label='Pc from GUI Picks')
        ax.loglog(x_solve, y_solve, 'r-' , linewidth=2 , label='Curve Fit Pc Curve')
       
        ax.set_xlim(50, 0.1)
        #ax.gca().invert_xaxis()
        ax.set_ylim(1, 100000)
        #ax.set_title("Pc Curves from Scipy Curve_fit", fontname="Times New Roman", size=24,fontweight="bold", color='blue')            
        ax.set_title("Pc Curves from Scipy Curve_fit", size=24,fontweight="bold", color='blue')            

        ax.set_ylabel('Pc Hg', fontsize=16, fontweight="bold", color = 'blue')
        ax.set_xlabel('BVOCC', fontsize=16, fontweight="bold", color = 'blue')
        ax.grid(True, which="both",ls="-")
        ax.legend()

        ax.text(50,8,' h = 2.4ft',horizontalalignment='left', fontsize=10, fontweight="bold",color='green')
        ax.text(50,80,' h = 24.5ft',horizontalalignment='left', fontsize=10,fontweight="bold", color='green')
        ax.text(50,800,' h = 245ft',horizontalalignment='left', fontsize=10,fontweight="bold", color='green') 
        ax.text(50,Pd1,'------- height @ Pd',horizontalalignment='left', fontsize=15, fontweight="bold", color='blue', fontstyle='italic') 
#        ax.text(50,9000,' h = 4544ft',horizontalalignment='left')       

        ax.text(.1,Pd1,' Pd1',horizontalalignment='left', size=14, fontweight="bold", color='blue')
        ax.text(max(diff(x_Pc)) + 1,    Pd1 + 6*Pd1,'    G1',horizontalalignment='right',  size=14,fontweight="bold", color='blue')
        ax.text(BV1_solve + BV2_solve +4,  14000,'  BV_infinite',horizontalalignment='right',  size=14,fontweight="bold", color='blue')
        ax.axvline(x= BVtotal+1, color='blue' , linestyle='--')  #vertical line        
#        ax.annotate('Pd', fontsize=10, color='green', xy=(.1, PD1_est), xytext=(.5, 2),
#            arrowprops=dict(facecolor='green', shrink=0.01),
#            )
        ax.annotate('            ', fontsize=14, color='blue', xy=(BV1_solve + BV2_solve +0, 10000), xytext=(40,12000),
            arrowprops=dict(facecolor='blue', shrink=0.01),
            )
#        ax.annotate('G1', fontsize=10, color='green', xy=(1, 100), xytext=(1,100),
##            arrowprops=dict(facecolor='green', shrink=1),
#            )


 
        self.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
    
    
    #    timer = QTimer()
#    timer.timeout.connect(lambda: None)
#    timer.start(100)
#    win = QMainWindow()
#    win.show()
#    ok = win.login()
#    if ok:
#        sys.exit(app.exec_())

    
    #time.sleep(6)
    #quit
#    time.sleep(5.5)    # pause 5.5 seconds            
#    sys.exit()
#    time.sleep(5.5)    # pause 5.5 seconds
#    exit

