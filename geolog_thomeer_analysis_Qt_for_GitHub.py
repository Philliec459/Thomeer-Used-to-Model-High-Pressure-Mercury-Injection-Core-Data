#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 16:14:28 2022

@author: craig
"""

#import geolog
import numpy as np
import pandas as pd
from numpy import diff
#import openpyxl



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,  QSizePolicy,  QPushButton
#from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

#from PyQt5.QtCore import QTimer
#******************************************************************
import matplotlib

import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")
import matplotlib.gridspec as gridspec
#******************************************************************
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure








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
# # #     End of reading in Pc data if required or Geolog below
# # #------------------------------------------------------------
# # ===========================================================================
# =============================================================================


# Load data from geolog
#while geolog.getrow():



# Put your code here !!!

# for Excel file you need to add the number of pore systems below:
no_pore_sys= 2  

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
    plt.title(s, fontsize=16, fontweight="bold", color = 'green')
    plt.draw()


plt.clf()   #clear plot of other things

plt.figure(num=2, figsize=(10, 10))
#plt.ion()
plt.semilogy(x_Pc, y_Pc  , 'g-*', linewidth=1, label='HPMI Data' )
plt.xlim(30.0,  0.01)
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
print('Closure Correction =', round(Closure,2), ' and Pd1 =', round(Pd1,1))
print()

plt.close('all')
# =============================================================================
#             End of Graphical Input for Closure Correction and Pd1 
# =============================================================================
#Closure = 0.5
#Pd1 = 10

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
    plt.title(s, fontsize=16, fontweight="bold", color = 'blue')
    plt.draw()

plt.clf()   #clear plot of other things

plt.figure(num=2, figsize=(10, 10))

plt.loglog(x_Pc, y_Pc  , 'b-*', linewidth=1, label='HPMI Data' )
plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
plt.xlim(50.0,0.01)
plt.ylim(1, 100000)
plt.grid(True, which="both",ls="-")
plt.legend()

pts = []


while len(pts) < 1:
    tellme('Select BV1 and Pd2')
    pts = np.asarray(plt.ginput(1, timeout=3))

BV1 = pts.item(0)
Pd2 = pts.item(1)
G1  = 0.4

print()
print('BV1 =', round(BV1,2), ' and Pd2 =', round(Pd2,1))
print()

plt.close('all')  
# =============================================================================
#             End of Graphical Input for Pd2 and BV1
# =============================================================================
#BV1=7
#Pd2=300


# =============================================================================
#             Graphical Input for BVtotal
# =============================================================================
if no_pore_sys > 1: 
    def tellme(s):
        print(s)
        plt.title(s, fontsize=16, fontweight="bold", color = 'red')
        plt.draw()
    
    plt.clf()   #clear plot of other things
    
    plt.figure(num=2, figsize=( 10, 10))
    
    plt.loglog(x_Pc, y_Pc  , 'r-*', linewidth=1, label='HPMI Data' )
    plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
    plt.loglog(BV1, Pd2  , 'k-o', linewidth=1, label='BV1 and Pd2 Estimate' )
    plt.xlim(50.0,0.01)
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
    
    BV2 = BVtotal - BV1
    print('BV2 = ',BV2)

    G2=0.2
    
    print()
    print('BVtotal =', round(BVtotal,2))
    print()
    
    
    plt.close('all')  
# =============================================================================
#             End of Graphical Input of BVtotal
# =============================================================================
#BVtotal=10






# =============================================================================
#             Scipy for Curve_fit of Pd1, G1 and BV1
# =============================================================================
from scipy.optimize import curve_fit
# =============================================================================
#             Scipy for Curve_fit for just Pd1, G1 and BV1
# =============================================================================
if no_pore_sys == 1: 
    
    bvarray_pore1 = []; #make list of 0 length
    pcarray_pore1 = []
    
    for i in range(1, len(Thomeer_Pc_data), 1):
        if Pc_r[i] > Pd1 and Pc_r[i] < Pd2 :
            BVOCC = (BVocc_r[i])
    
            bvarray_pore1.append(BVocc_r[i]); #add items 
            pcarray_pore1.append(Pc_r[i]); #add items     
    
        
    ydata=np.array(bvarray_pore1)
    xdata=np.array(pcarray_pore1)
    
    def func(xdata, a, b, c):
        return a*10**((-0.434*b)/np.log10(xdata/c))
    
    
    popt, pcov = curve_fit(func, xdata, ydata, method='trf', bounds=([1, .5, 1 ], [np.inf, np.inf, np.inf]))

    
    BV1_solve = popt[0]   
    G1_solve  = popt[1]
    Pd1_solve = popt[2]

    
    
    print('      Pd1 pick =',round(Pd1,1),', G1 or popt[1] =',round(popt[1],2),',       BV1 pick =',round(BV1,2))
    print('Pd1 or popt[2] =',round(popt[2],1),', G1 or popt[1] =',round(popt[1],2),', BV1 or popt[0] =',round(popt[0],2))
    print('Pd1 or popt[2] =',round(Pd1_solve,1),', G1 or popt[1] =',round(G1_solve,2),', BV1 or popt[0] =',round(BV1_solve,2))
    print()


    Pd2_solve = float("nan")
    G2_solve  = float("nan")
    BV2_solve = float("nan")

    BVtotal = BV1_solve 

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
    
    
        BVOCC = BVOCC1
    
        bvarray_pred.append(BVOCC); #add items 
        pcarray_pred.append(Pc); #add items 
        
        Pc = Pc * 1.12
    
       
    x_solve=np.array(bvarray_pred)
    y_solve=np.array(pcarray_pred)

# =============================================================================
#             Scipy for Curve_fit of 2 Pore Systems
# =============================================================================
elif no_pore_sys == 2  :

    bvarray_pore1 = []; #make list of 0 length
    pcarray_pore1 = []
    
    for i in range(1, len(Thomeer_Pc_data), 1):
        if Pc_r[i] > Pd1 and Pc_r[i] < Pd2 :
            BVOCC = (BVocc_r[i])
    
            bvarray_pore1.append(BVocc_r[i]); #add items 
            pcarray_pore1.append(Pc_r[i]); #add items     
    
        
    ydata=np.array(bvarray_pore1)
    xdata=np.array(pcarray_pore1)
    
    def func(xdata, a, b, c):
        return a*10**((-0.434*b)/np.log10(xdata/c))
    
    
    popt, pcov = curve_fit(func, xdata, ydata, method='trf', bounds=([1, .5, 1 ], [np.inf, np.inf, np.inf]))

    
    BV1_solve = popt[0]   
    G1_solve  = popt[1]
    Pd1_solve = popt[2]

    
    
    print('      Pd1 pick =',round(Pd1,1),', G1 or popt[1] =',round(popt[1],2),',       BV1 pick =',round(BV1,2))
    print('Pd1 or popt[2] =',round(popt[2],1),', G1 or popt[1] =',round(popt[1],2),', BV1 or popt[0] =',round(popt[0],2))
    print('Pd1 or popt[2] =',round(Pd1_solve,1),', G1 or popt[1] =',round(G1_solve,2),', BV1 or popt[0] =',round(BV1_solve,2))
    print()
    # =============================================================================
    #             Scipy for Curve_fit of Pd2, G2 and BV2
    # =============================================================================
    bvarray_pore2 = []; #make list of 0 length
    pcarray_pore2 = []
    
    for i in range(1, len(Thomeer_Pc_data), 1):
        if Pc_r[i] > Pd2 :
            
            BVOCC = (BVocc_r[i])
    
            bvarray_pore2.append(BVocc_r[i]); #add items 
            pcarray_pore2.append(Pc_r[i]); #add items     
    
        
    ydata2=np.array(bvarray_pore2)
    xdata2=np.array(pcarray_pore2)
    
    def func2(xdata2, a, b, c):
        return a*10**((-0.434*b)/np.log10(xdata2/c))
    popt, pcov = curve_fit(func2, xdata2, ydata2, method='dogbox', bounds=([0.0 , 0.1, 1.0 ], [np.inf, np.inf, np.inf]))    

  
    # try to use picks for now:
    #########popt=[BV2, G1_solve*0.7, Pd2]

    print('This is the second pore system',popt[0],popt[1])
     
    #BV2_solve = popt[0] - BV1_solve
    if  popt[0] - BV1_solve > 0:
        BV2_solve = popt[0] - BV1_solve   
    else:
        BV2_solve = 0       

    G2_solve  = popt[1]
    #Pd2_solve = popt[2]
    Pd2_solve = Pd2
    
 

    print('Pd2  =',round(Pd2_solve,1),', G2 or popt[1] =',round(G2_solve,2),', BV2 or popt[0] =',round(BV2_solve,2))
    print()
 


    # =============================================================================
    #             Create Pc Curves for curve fit Thomeer parameters
    # =============================================================================
    Pc = 0.5
    bvarray_pred = []; #make list of 0 length
    pcarray_pred = []
    bvocc2_pred  = []
    
    for j in range(1, 105, 1):
        if Pc > Pd1_solve:
            BVOCC1 = BV1_solve * 10**((-0.434 * G1_solve) / np.log10(Pc / Pd1_solve))
        else:
            BVOCC1 = 0.001
    
        if Pc > Pd2_solve:
            BVOCC2 = BV2_solve * 10**((-0.434 * G2_solve) / np.log10(Pc / Pd2_solve))
        else:
            BVOCC2 = 0.001
    
    
        BVOCC = BVOCC1 + BVOCC2
    
        bvarray_pred.append(BVOCC); #add items 
        pcarray_pred.append(Pc); #add items 
        bvocc2_pred.append(BVOCC2)  
        
        Pc = Pc * 1.12
    
       
    x_solve=np.array(bvarray_pred)
    x2_solve=np.array(bvocc2_pred)
    y_solve=np.array(pcarray_pred)
    # =============================================================================
    #             End of Scipy for Curve_fit of Pd1, G1 and BV1
    # =============================================================================
    
  


g1_solve  = G1_solve
g2_solve  = G2_solve
pd1_solve = Pd1_solve
pd2_solve = Pd2_solve
bv1_solve = BV1_solve
bv2_solve = BV2_solve
closure   = Closure

   


# # Store data into geolog
# #geolog.puttable()

# #geolog.putrow()
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

        
        ax = self.figure.add_subplot(gs[0:3, 0:3]) 
        
        
        #ax.loglog(x2, y2, 'r-'  , linewidth=3 , label='Nearest Pc Curve')
        ax.loglog(x_Pc_nocc, y_Pc, 'k--' , linewidth=1 ,markersize = 1, label='Actual HPMI Pc Curve')
        ax.loglog(Closure, Pd1, 'ko' , linewidth=10 , label='Closure Correction')        
        #ax.loglog(x5, y5, 'b--' , linewidth=3 , label='kNN Pc Curve')
        ax.loglog(x_Pc, y_Pc, 'g-' , linewidth=2 , label='Closure Corrected Pc Curve')
        #ax.loglog(x_gui  , y_gui,   'b--' , linewidth=1 , label='Pc from GUI Picks')
        ax.loglog(x_solve, y_solve, 'r-' , linewidth=3 , label='Thomeer Modeled Pc Curve')
               
        ax.set_xlim(50, 0.1)
        #ax.gca().invert_xaxis()
        ax.set_ylim(1, 100000)
        #ax.set_title("Pc Curves from Scipy Curve_fit", fontname="Times New Roman", size=24,fontweight="bold", color='blue')            
        ax.set_title("Thomeer Parameters from Scipy Curve_fit used to Model HPMI data", size=16,fontweight="bold", color='blue')            

        ax.set_ylabel('Pc Hg', fontsize=16, fontweight="bold", color = 'blue')
        ax.set_xlabel('BVOCC', fontsize=16, fontweight="bold", color = 'blue')
        ax.grid(True, which="both",ls="-")
        ax.legend()

        ax.text(50,8,' h = 2.4ft'  ,horizontalalignment='left', fontsize=10, fontweight="bold",color='green')
        ax.text(50,80,' h = 24.5ft',horizontalalignment='left', fontsize=10,fontweight="bold", color='green')
        ax.text(50,800,' h = 245ft',horizontalalignment='left', fontsize=10,fontweight="bold", color='green') 
        ax.text(50,Pd1,'---- height @ Pd',horizontalalignment='left', fontsize=12, fontweight="bold", color='blue', fontstyle='italic') 

        ax.text(.1,Pd1,' Pd1',horizontalalignment='left', size=14, fontweight="bold", color='blue')
        ax.text(max(diff(x_Pc)) + 1,    Pd1 + 6*Pd1,'    G1',horizontalalignment='right',  size=14,fontweight="bold", color='blue')
        ax.text(BV1_solve + BV2_solve +4,  14000,'  BV_infinite',horizontalalignment='right',  size=14,fontweight="bold", color='blue')
        ax.axvline(x= BVtotal+1, color='blue' , linestyle='--')  #vertical line        

        ax.annotate('            ', fontsize=14, color='blue', xy=(BV1_solve + BV2_solve +0, 10000), xytext=(40,12000),
            arrowprops=dict(facecolor='blue', shrink=0.01),
        )

        ax.text(40,3.3  , 'Thomeer Parameter Estimates from Scipy curve_fit:', horizontalalignment='left', fontsize=14, fontweight="bold",color='blue')
        ax.text(40,2.2  , 'Pd1 ='   , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')
        ax.text(24,2.2  , round(Pd1_solve,1) , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')
        ax.text(6,2.2   , 'G1 ='  , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')
        ax.text(4,2.2   , round(G1_solve,2)  , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')
        ax.text(0.8,2.2 ,'BV1 = ' , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')
        ax.text(0.5,2.2 , round(BV1_solve,2) , horizontalalignment='left', fontsize=12, fontweight="bold",color='red')

    
        if no_pore_sys > 1: 
            ax.loglog(x2_solve, y_solve, 'k--' , linewidth=1 , label='Thomeer BVOCC2')
            ax.text(40,1.5  , 'Pd2 ='   , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')
            ax.text(24,1.5  , round(Pd2_solve,1) , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')
            ax.text(6,1.5   , 'G2 ='  , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')
            ax.text(4,1.5   , round(G2_solve,2)  , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')
            ax.text(0.8,1.5 ,'BV2 = ' , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')
            ax.text(0.5,1.5 , round(BV2_solve,2) , horizontalalignment='left', fontsize=12, fontweight="bold",color='brown')





 
        self.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
    
    

