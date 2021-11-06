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
#import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
matplotlib.use("Qt5Agg")
import matplotlib.gridspec as gridspec
#******************************************************************
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import diff
import math
from colorama import Fore, Style




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

plt.figure(1,figsize=(12, 11))
#plt.ion()
plt.loglog(x_Pc, y_Pc  , 'g-*', linewidth=1, label='HPMI Data' )
plt.xlim(50.0,  0.1)
plt.ylim(1, 100000)
plt.grid(True)
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

plt.figure(1,figsize=(12, 11))

plt.loglog(x_Pc, y_Pc  , 'b-*', linewidth=1, label='HPMI Data' )
plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
plt.xlim(50.0,0.1)
plt.ylim(1, 100000)
plt.grid(True)
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

plt.figure(1,figsize=(12, 11))

plt.loglog(x_Pc, y_Pc  , 'r-*', linewidth=1, label='HPMI Data' )
plt.loglog(Closure, Pd1  , 'k-o', linewidth=1, label='Closure Correction and Pd1 Estimate' )
plt.loglog(BV1, Pd2  , 'k-o', linewidth=1, label='BV1 and Pd2 Estimate' )
plt.xlim(50.0,0.1)
plt.ylim(1, 100000)
plt.grid(True)
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


#popt, pcov = curve_fit(func, ydata, xdata, bounds=([1, 0.01, 0.0], [30000., 3., 100.]))
popt, pcov = curve_fit(func, ydata, xdata, bounds=([Pd1*0.5, 0.01, BV1*0.5], [Pd1*1.5, 3., BV1*2]))

Pd1_solve=popt[0]
G1_solve=popt[1]
BV1_solve=popt[2]

print('Pd1 or popt[0]=',popt[0],', G1 or popt[1]=',popt[1],', BV1 or popt[2]=',popt[2])
print('Pd1 or popt[0]=',Pd1_solve,', G1 or popt[1]=',G1_solve,', BV1 or popt[2]=',BV1_solve)
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

print('Pd2 or popt[0]=',popt[0],', G2 or popt[1]=',popt[1],', BV2 or popt[2]=',popt[2])
print('Pd2 or popt[0]=',Pd2_solve,', G2 or popt[1]=',G2_solve,', BV2 or popt[2]=',BV2_solve)
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
#             kNN usaed to predict Pc curve from poro-perm location
#               Define Porosity from BVtotal and Perm from Pd1
# =============================================================================
Perm = 10**(3.33016 - 1.71092*math.log10(Pd1))
Por = BVtotal*1.25/100
print()
print('Porosity =', Por, ' and Permeability =', Perm)
print()


# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #                Read Reference Data Spreadsheet 
# # #  Read mapinv_reference_data_carbonates_calculatedMode_Rosetta data 
# # #                which is the Rosetta Stone reference data per Clerke
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
#read the file
file = r'mapinv_reference_data_carbonates_calculatedMode_Rosetta.xlsx'
Thomeer_core_data = pd.read_excel(file,index_col=False)
# ------------------------------------------------------------------ 
#    read in maininv_reference2 data which is just Rosetta Stone 
#                     this is reference data
#                       DATA WILL BE LOADED
# ------------------------------------------------------------------

Permeability = Thomeer_core_data['PERMEABILITY']
Porosity = Thomeer_core_data['POROSITY']
G1 = Thomeer_core_data['G1']
PD1 = Thomeer_core_data['PD1']
BV1 = Thomeer_core_data['BV1']
G2 = Thomeer_core_data['G2']
PD2 = Thomeer_core_data['PD2']
BV2 = Thomeer_core_data['BV2']
Rock_Index = Thomeer_core_data['ROCK_INDEX']

Perm_max = 4
Perm_min = -4
Por_max = .35
Por_min = 0

x4=np.array(Porosity)
y4=np.array(Permeability)
# =============================================================================
# # ===========================================================================
# # #------------------------------------------------------------ 
# # #               
# # #     End of reading in mapinv reference data
# # #------------------------------------------------------------
# # ===========================================================================
# =============================================================================






        

# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# ##
# ##            This is the beginnin of KNN
# ##
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
#normalized Porosity and Permeability inputs
por = (Por-Por_min)/(Por_max - Por_min)
perm= (math.log10(Perm) - Perm_min)/(Perm_max - Perm_min)
# =============================================================================
# #---------------------------------------------------------------------------- 
# #           
# #              ESTIMATE THOMEER PARAMETERS FOR BOTH PORE SYSTEMS
# #                   
# #----------------------------------------------------------------------------
# =============================================================================

dist_inv = []
dist_phi = []
dist_lperm = []
G1_weight = []
PD1_weight = []
BV1_weight = []
G2_weight = []
PD2_weight = []
BV2_weight = []
#Rock_Index_weight = []


dist_inv_total=0
G1_total  = 0
PD1_total = 0
BV1_total = 0
G2_total  = 0
PD2_total = 0
BV2_total = 0

inv_dist_array = []
#distance_knn_array = [rows,columns]
distance_knn_array = []

#------------------------------------------------------------------ 
#               Estimate all Thomeer Parameters for *_est values
#-------------------------------------------------------------------

Porosity_norm     = []
Permeability_norm = []


#this is the mapinv_reference_data being used 
for i in range(0,len(Thomeer_core_data),1):

        Porosity_norm.append((Porosity[i] - Por_min) / (Por_max - Por_min))
        Permeability_norm.append((math.log10(Permeability[i]) - Perm_min) / (Perm_max - Perm_min))
        
        #Euclidian Distance
        dist_phi.append(   abs(por  - Porosity_norm[i]    ))  
        dist_lperm.append( abs(perm - Permeability_norm[i]))
        dist_inv.append( 1  /  math.sqrt(  dist_phi[i]**2 + dist_lperm[i]**2)  )

        
        #calculalte weights for each
        G1_weight.append(dist_inv[i]  * G1[i])
        PD1_weight.append(dist_inv[i] * PD1[i])
        BV1_weight.append(dist_inv[i] * BV1[i])
        G2_weight.append(dist_inv[i]  * G2[i])
        PD2_weight.append(dist_inv[i] * PD2[i])
        BV2_weight.append(dist_inv[i] * BV2[i])
        #Rock_Index_weight.append(dist_inv[i] * Rock_Index[i])
        


        inv_dist_array.append(dist_inv[i]);  # add items

# =============================================================================
###                    KNN Array
# # ===========================================================================
# # #--------------------------------------------------------------------------
        distance_knn_array = [dist_inv, G1_weight, PD1_weight, BV1_weight, G2_weight, PD2_weight, BV2_weight,Rock_Index]
#        distance_knn_array = [Permeability, Porosity, G1, PD1, BV1, G2, PD2, BV2]
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================
xnorm=np.array(Porosity_norm)
ynorm=np.array(Permeability_norm)


# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #               Transpose and Sort new kNN array
# # #                   
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

#knn_array = np.transpose array
knn_array = np.transpose(distance_knn_array)
#print(knn_array)

#Sort array from large to low by column 0 which is dist_inv 
#xknn=np.array(knn_array)

#matsor x[x[:,column].argsort()[::-1]] and -1 us reverse order
mat_sort = knn_array[knn_array[:,0].argsort()[::-1]] #firt column reverse sort (-1)
#mat_sort = x[x[:,1].argsort()[::-1]]
#mat_sort = x[x[:,2].argsort()[::-1]

# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #               Calculate knn Thomeer Parameters
# # #                   
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================


#------------------------------------------------------------------------------
#    Number of nearest Neighbors
#------------------------------------------------------------------------------
n_neighbors = 3
#------------------------------------------------------------------------------

dist_inv_total_knn = 0
G1_total_knn = 0
PD1_total_knn = 0
BV1_total_knn = 0
G2_total_knn = 0
PD2_total_knn = 0
BV2_total_knn = 0

#kNN Estimates for first 3 rows
#dist_inv_total = mat_sort[0][0] + mat_sort[1][0] + mat_sort[2][0]
for i in range(0,n_neighbors,1):
    dist_inv_total_knn = dist_inv_total_knn + mat_sort[i][0]
    G1_total_knn  = G1_total_knn + mat_sort[i][1]
    PD1_total_knn = PD1_total_knn + mat_sort[i][2]
    BV1_total_knn = BV1_total_knn + mat_sort[i][3]
    G2_total_knn  = G2_total_knn + mat_sort[i][4]
    PD2_total_knn = PD2_total_knn + mat_sort[i][5]
    BV2_total_knn = BV2_total_knn + mat_sort[i][6]


#back to k values and calculate estimations now
G1_est_knn  = G1_total_knn  / dist_inv_total_knn
PD1_est_knn = PD1_total_knn / dist_inv_total_knn
BV1_est_knn = (BV1_total_knn / dist_inv_total_knn)
G2_est_knn  = G2_total_knn  / dist_inv_total_knn
PD2_est_knn = PD2_total_knn / dist_inv_total_knn
BV2_est_knn = (BV2_total_knn / dist_inv_total_knn)


print()
print(Fore.GREEN +'Estimated Thomeer Parameters from KNN =',n_neighbors,' on normlalized Poro-Perm data')
print(Fore.GREEN + '     G1 =',G1_est_knn, ',  Pd1 =',PD1_est_knn, ', BV1(%) =',BV1_est_knn) 
print(Fore.GREEN + '     G2 =',G2_est_knn, ',  Pd2 =',PD2_est_knn, ', BV2(%) =',BV2_est_knn) 
#print(Style.RESET_ALL) 
#print('back to normal now') 










# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #               Find Closest distance Pc curve in poro-perm space
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

a = np.array(inv_dist_array)
inv_dist_thresh = np.percentile(a, 99.999)
print()
#print("Inv Distance Threshold =", inv_dist_thresh)
#print()


for i in range(0, len(Thomeer_core_data), 1):
    if dist_inv[i] > inv_dist_thresh - 0.001:
        G_1 = G1[i]
        Pd1 = PD1[i]
        Bv1 = BV1[i]
        G_2 = G2[i]
        Pd2 = PD2[i]
        Bv2 = BV2[i]
        Perm_r = Permeability[i]
        Por_r = Porosity[i]
        mode_r = math.exp(-1.15*G_1)*(214/Pd1)

        Por_r_norm = (Por_r - Por_min)/(Por_max - Por_min)
        Perm_r_norm= (math.log10(Perm_r) - Perm_min)/(Perm_max - Perm_min)

#os.system("color 1") # colour can be any number between 1 to 8
print(Fore.RED +  'Thomeer Parameters Reference Set: Por_r =', Por_r,', Perm_r =', Perm_r)
print('     Pd1_r =',Pd1, '          , G1_r =',G_1, '            , BV1_r =',Bv1) 
print('     Pd2_r =',Pd2, '         , G2_r =',G_2, '            , BV2_r =',Bv2) 
#print('     Mode of PTD = ',mode_r , 'microns') 




Pc2 = 0.5
bvarray2 = []; #make list of 0 length
pcarray2 = []

for j in range(1, 105, 1):
    if Pc2 > Pd1:
        BVOCC11 = Bv1 * 10**((-0.434 * G_1) / math.log10(Pc2 / Pd1))
    else:
        BVOCC11 = 0.001

    if Pc2 > Pd2:
        BVOCC22 = Bv2 * 10 ** ((-0.434 * G_2) / math.log10(Pc2 / Pd2))
    else:
        BVOCC22 = 0.001

       
    BVOCC_r = BVOCC11 + BVOCC22
    
    bvarray2.append(BVOCC_r); #add items 
    pcarray2.append(Pc2); #add items 
    
    Pc2 = Pc2 * 1.12

   
x2=np.array(bvarray2)
y2=np.array(pcarray2)


# =============================================================================
# # ===========================================================================
# # #--------------------------------------------------------------------------
# # #           
# # #               CREATE Pc PLOTS from kNN Values of Thomeer
# # #                   
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

Pc = 0.5
bvarray_knn = []; #make list of 0 length
pcarray_knn = []

   

for j in range(1, 105, 1):
    if Pc > PD1_est_knn:
        BVOCC1 = BV1_est_knn * 10**((-0.434 * G1_est_knn) / math.log10(Pc / PD1_est_knn))
    else:
        BVOCC1 = 0.001

    if Pc > PD2_est_knn:
        BVOCC2 = BV2_est_knn * 10 ** ((-0.434 * G2_est_knn) / math.log10(Pc / PD2_est_knn))
    else:
        BVOCC2 = 0.001

       
    BVOCC = BVOCC1 + BVOCC2
    
    bvarray_knn.append(BVOCC); #add items 
    pcarray_knn.append(Pc); #add items 
    
    Pc = Pc * 1.12

   
x5=np.array(bvarray_knn)
y5=np.array(pcarray_knn)

# =============================================================================
# # ===========================================================================
# # #-------------------------------------------------------------------------- 
# # #                Read Thin Section Spreadsheet
# # #  Read CO3 thin Section data which is Arab D Carbonate Data like Rosetta Stone data
# # #--------------------------------------------------------------------------
# # ===========================================================================
# =============================================================================

print()
print(Fore.GREEN + "Representative Thin Section:")
#print()


#read the file
file = r'CO3_TS_Image.xlsx'
TS_data = pd.read_excel(file,index_col=False)


Depth = TS_data['Depth']
Porosity_TS = TS_data['Porosity']
Permeability_TS = TS_data['Permeability']
Path_TS = TS_data['TS_Path']
TS= False

  
        
        
x3=np.array(Porosity_TS)
y3=np.array(Permeability_TS)


# =============================================================================
# # ===========================================================================
# ##
# ##                   Inverse Distance for TS 
# ##
# # ===========================================================================
# =============================================================================
dist_inv = []
dist_phi = []
dist_lperm = []
inv_dist_array2 = []
dist_inv_total=0


#------------------------------------------------------------------------------ 
#          Estimate Inv Distance data
#------------------------------------------------------------------------------

Porosity_norm_ts     = []
Permeability_norm_ts = []

#this is the mapinv_reference_data being used using the mapinv Porosity and Permeability vs. por and perm
for i in range(0,len(TS_data),1):

        Porosity_norm_ts.append((Porosity_TS[i] - Por_min) / (Por_max - Por_min))
        Permeability_norm_ts.append((math.log10(Permeability_TS[i]) - Perm_min) / (Perm_max - Perm_min))

        #Euclidian Distance
        dist_phi.append(   abs(por  - Porosity_norm_ts[i]    ))  
        dist_lperm.append( abs(perm - Permeability_norm_ts[i]))
        dist_inv.append( 1  /  math.sqrt(  dist_phi[i]**2 + dist_lperm[i]**2)  )


        inv_dist_array2.append(dist_inv);  # add items


a = np.array(inv_dist_array2) 
inv_dist_thresh = np.percentile(a, 99.999)


#plt.figure(2)        
for p in range(0,len(TS_data) ,1):        
        if dist_inv[p] > inv_dist_thresh - 0.001 and dist_inv[p] > 0.001:
            TS = Path_TS[p]
            Por_TS = Porosity_TS[p]
            Perm_TS = Permeability_TS[p]
       

#            print("     Reference Data: Porosity =",Porosity[p], ", Permeability =", Permeability[p],", Inv Dist '",dist_inv[i],TS)
            print(Fore.GREEN +"     Porosity =",Porosity_TS[p], ", Permeability =", Permeability_TS[p])
            print(Fore.GREEN +"     Inv Dist '",dist_inv[p],", TS Image =", Path_TS[p])    
            img=mpimg.imread(TS)
#            imgplot = plt.imshow(img)
#            plt.show()
#        else:
#            TS = 'blank.PNG'
#            Por_TS = 0
#            Perm_TS = 0
#            img=mpimg.imread(TS)               

if not TS :
    print("     'No Representative Thin Section'")
    TS = 'blank.PNG'
    Por_TS = 0
    Perm_TS = 0
    img=mpimg.imread(TS)               
    
else:
    print(Fore.GREEN + "     Representative Thin Section is Available")
       
print(Style.RESET_ALL) 

plt.close('all')
#quit







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
        self.width = 500
        self.height = 1200
        self.initUI()




    #Define Canvas and Pushbutton
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # this defines the width and height of canvas 
        m = PlotCanvas(self, width=5, height=12)
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
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
#            self.axes = fig.add_subplot(211)  apparently not needed now

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.plot()
        self.plot2()
        self.plot3()
        self.plot4()


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
        ax = self.figure.add_subplot(gs[0, 0:3]) 
        
        
        #ax.loglog(x2, y2, 'r-'  , linewidth=3 , label='Nearest Pc Curve')
        ax.loglog(x_Pc_nocc, y_Pc, 'k--' , linewidth=1 ,markersize = 1, label='Actual Pc Curve')
        #ax.loglog(x5, y5, 'b--' , linewidth=3 , label='kNN Pc Curve')
        ax.loglog(x_Pc, y_Pc, 'g-' , linewidth=3 , label='Closure Corrected Pc Curve')
        #ax.loglog(x_gui  , y_gui,   'b--' , linewidth=1 , label='Pc from GUI Picks')
        ax.loglog(x_solve, y_solve, 'r-' , linewidth=2 , label='Curve Fit Pc Curve')
       
        ax.set_xlim(50, 0.1)
        #ax.gca().invert_xaxis()
        ax.set_ylim(1, 100000)
        ax.set_title("Pc Curves from Scipy Curve_fit", color = 'red')            
        ax.set_ylabel('Pc Hg', color = 'red')
        ax.set_xlabel('BVOCC', color = 'red')
        ax.grid(True)
        ax.legend()

        ax.text(50,8,' h = 2.4ft',horizontalalignment='left', fontsize=10, color='green')
        ax.text(50,80,' h = 24.5ft',horizontalalignment='left', fontsize=10, color='green')
        ax.text(50,800,' h = 245ft',horizontalalignment='left', fontsize=10, color='green') 
        ax.text(50,PD1_est_knn,'------- height @ Pd',horizontalalignment='left', fontsize=8, color='red', fontstyle='italic') 
#        ax.text(50,9000,' h = 4544ft',horizontalalignment='left')       

        ax.text(.1,PD1_est_knn,' Pd',horizontalalignment='left', fontsize=11, color='red')
        ax.text(max(diff(x5)) + 1,    PD1_est_knn + 6*PD1_est_knn,'    G1',horizontalalignment='right', fontsize=11, color='red')
        ax.text(BV1_est_knn + BV2_est_knn +4,  14000,'  BVinf',horizontalalignment='right', fontsize=11, color='red')
        ax.axvline(x= BV1_est_knn + BV2_est_knn, color='red' , linestyle='--')  #vertical line        
#        ax.annotate('Pd', fontsize=10, color='green', xy=(.1, PD1_est), xytext=(.5, 2),
#            arrowprops=dict(facecolor='green', shrink=0.01),
#            )
#        ax.annotate('BVinf', fontsize=10, color='green', xy=(BV1_est+BV2_est, 10000), xytext=(60,10000),
#            arrowprops=dict(facecolor='green', shrink=0.01),
#            )
#        ax.annotate('G1', fontsize=10, color='green', xy=(1, 100), xytext=(1,100),
##            arrowprops=dict(facecolor='green', shrink=1),
#            )


 
        self.draw()


#Poro_Perm xplot Thomeer Clastics dB
    def plot2(self):

        gs = gridspec.GridSpec(nrows=3, 
                               ncols=3, 
#                               figure=fig, 
                               width_ratios= [1, 1, 1],
                               height_ratios=[1, 1, 1],
                               wspace=0.3,
                               hspace=0.3)
        
        cx = self.figure.add_subplot(gs[1,0:3])        
        
        #cx = self.figure.add_subplot(412) 

        cx.plot(xnorm, ynorm  , 'b-*', linewidth=0, label='Normalized Core Data' )
        cx.plot(por, perm  , 'r-D', linewidth=0, label='User Poro-perm' )
        cx.plot(Por_r_norm, Perm_r_norm  , 'g-D', linewidth=0, label='Thomeer Nearest Sample ' )
#        cx.semilogy(Por_TS, Perm_TS  , 'c-^', linewidth=0, label='TS Poro-perm Point' )
        cx.set_xlim(0 , 1.0)
        #ax.gca().invert_xaxis()
        cx.set_ylim(0 , 1.0)
        cx.set_title("Normalized Core Data having Thomeer Pc Parameters", color = 'blue')            
        cx.set_ylabel('Normalized Permeability', color = 'blue')
        cx.set_xlabel('Normalized Porosity (all Carbonate Rock)', color = 'blue')
        cx.annotate('User Poro-Perm', fontsize=10, color='red', xy=(por, perm), xytext=(-0.03, 0.9),
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    )
        cx.annotate('Nearest Pc', fontsize=10, color='green' ,xy=(Por_r_norm, Perm_r_norm), xytext=(0.75, .4),
                    arrowprops=dict(facecolor='green', shrink=0.05),
                    )



        cx.grid(True)
        cx.legend()

        self.draw()


#Poro_Perm xplot of Katmai Core data
    def plot3(self):

#wspace = 0.2   # the amount of width reserved for blank space between subplots
#hspace = 0.2   # the amount of height reserved for white space between subplots         
        
        gs = gridspec.GridSpec(nrows=3, 
                               ncols=3, 
#                               figure=fig, 
                               width_ratios= [1, 1, 1],
                               height_ratios=[1, 1, 1],
                               wspace=0.0,
                               hspace=0.4)
        
        cx = self.figure.add_subplot(gs[2,0:3])        
        #cx = self.figure.add_subplot(414) 
        cx.semilogy(x4, y4  , 'y-*', linewidth=0, label='Thomeer dB Core Data' )
        cx.semilogy(x3, y3  , 'b-*', linewidth=0, label='TS Core Data' )
        cx.semilogy(Por, Perm  , 'r-D', linewidth=0, label='User Poro-perm ' )
        cx.semilogy(Por_TS, Perm_TS  , 'g-D', linewidth=0, label='TS Poro-perm ' )
        cx.set_xlim(0.0,0.35)
        #ax.gca().invert_xaxis()
        cx.set_ylim(0.0001, 10000)
        #cx.set_title("Katmai Core Analysis Database")            
        cx.set_ylabel('Permeability', color='green')
        cx.set_xlabel('Porosity (Carbonate Core Data dB with TS)', color = 'green')
        cx.grid(True)
        cx.annotate('User Poro-Perm', fontsize=10, color='red', xy=(Por, Perm), xytext=(.26, 1),
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    )
        cx.annotate('Nearest TS', fontsize=10, color='green' ,xy=(Por_TS, Perm_TS), xytext=(.065, 0.00015),
                    arrowprops=dict(facecolor='green', shrink=0.05),
                    )

        cx.annotate('Nearest TS', fontsize=10, color='green' , xy=(0.135, 1000), xytext=(.24, 20000),
                    arrowprops=dict(facecolor='green', shrink=0.1),
                    )


        cx.legend()

        self.draw()



#Thin Section plot row 1 and column 0
    def plot4(self):

#wspace = 0.2   # the amount of width reserved for blank space between subplots
#hspace = 0.2   # the amount of height reserved for white space between subplots         
        
        gs = gridspec.GridSpec(nrows=3, 
                               ncols=3, 
#                               figure=fig, 
                               width_ratios= [1, 1, 1],
                               height_ratios=[1, 1, 1],
                               wspace=-0.3,
                               hspace=-0.4)
        
        bx = self.figure.add_subplot(gs[2,0:1]) 

        bx.axes.get_xaxis().set_visible(False)
        bx.axes.get_yaxis().set_visible(False)

        bx.imshow(img)

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

