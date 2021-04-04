#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 19:48:52 2021

@author: goharshoukat
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from PyQt5.QtGui import *
#from PyQt5.QtWidgets import QFileDialog, QDialog, QComboBox
from PyQt5.QtWidgets import *
import os
import sys
from pathlib import Path
import data_import_func
from scipy.stats import norm
import matplotlib.pyplot as plt


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(0, 0, 1000, 1000)
        #window layout
        mainLayout = QtWidgets.QGridLayout()
        #File Name and loading in sublayout
        subLayout = QtWidgets.QGridLayout()
        #signal to load and plotting butons in sublayout2
        subLayout2 = QtWidgets.QGridLayout()
        subLayout3 = QtWidgets.QGridLayout()
        #Introduce widgets here
        
        
        #sublayout widgets
        self.file_label = QtWidgets.QLabel(self)
        self.file_label.setText('File Name')
        self.file_display = QtWidgets.QLineEdit(self)
        self.file_btn = QtWidgets.QPushButton('...', self)
        self.directory = self.file_btn.clicked.connect(self.openFile)
        self.load_btn = QtWidgets.QPushButton('Load Data', self)
        self.load_btn.clicked.connect(self.readFile)
        
        #sublayout2 widgets
        self.signal_label = QtWidgets.QLabel(self)
        self.signal_label.setText('Signal')
        self.combo_box = QComboBox(self) 
        self.combo_box.addItems(['Thrust', 'Torque', 'Fx1', 'Fy1', 'Mx1', 'My1', 'Mz1', 'Fx2', 'Fy2', 'Mx2', 'My2', 'Mz2', 'Fx3', 'Fy3', 'Mx3', 'My3', 'Mz3', 'Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
        self.plot_btn = QtWidgets.QPushButton('Plot', self)
        self.plot_btn.pressed.connect(self.plot) 
        self.plot_btn.pressed.connect(self.window2) 
        self.plot_btn.pressed.connect(self.window3) 
        
        #add the input options for fft windowing, run time, sampling frequency
        #Total Run Time
        self.time_label = QtWidgets.QLabel(self)
        self.time_label.setText('Total Run Time')
        self.time_lineedit = QtWidgets.QLineEdit(self)
        self.time_lineedit.setText(str(360.0))
        
        #Sampling Frequency
        self.sampl_freq_label = QtWidgets.QLabel(self)
        self.sampl_freq_label.setText('Sampling Frequency')
        self.sampl_freq_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.sampl_freq_lineedit = QtWidgets.QLineEdit(self)
        self.sampl_freq_lineedit.setText(str(256))
        
        
        #Set up bins for fft
        self.fft_label = QtWidgets.QLabel(self)
        self.fft_label.setText('Bins for FFT')
        self.fft_input = QtWidgets.QLineEdit(self)
        self.fft_input.setText('Default')
        self.fft_checkbox = QtWidgets.QCheckBox('Normalize FFT', self)
        
        #Provide input for bins for histograms
        self.bin_label = QtWidgets.QLabel(self)
        self.bin_label.setText('Histogram Bins')
        self.bin_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.bin_lineedit = QtWidgets.QLineEdit(self)
        self.bin_lineedit.setText('50')

        #horizontally stack file selection, time and sampling frequency
        subLayout.addWidget(self.file_label, 0, 0)
        subLayout.addWidget(self.file_display, 0, 1)
        subLayout.addWidget(self.file_btn, 0, 2)
        subLayout.addWidget(self.load_btn, 0, 3)        

        subLayout3.addWidget(self.time_label, 0, 0)
        subLayout3.addWidget(self.time_lineedit, 0, 1)
        subLayout3.addWidget(self.sampl_freq_label, 0, 2)
        subLayout3.addWidget(self.sampl_freq_lineedit, 0, 3)
        subLayout3.addWidget(self.signal_label, 1, 0)
        subLayout3.addWidget(self.combo_box, 1, 1)

        subLayout3.addWidget(self.bin_label, 1, 2)
        subLayout3.addWidget(self.bin_lineedit, 1, 3)
        subLayout3.addWidget(self.fft_checkbox, 1, 4)
        subLayout3.addWidget(self.plot_btn, 1, 5)
        
        
        subLayout3.addWidget(self.fft_label, 0, 4)
        subLayout3.addWidget(self.fft_input, 0, 5)

        #add figures
        figure1 = Figure()
        figure2 = Figure()
        figure3 = Figure()
        figure4 = Figure()
        self.canvas1 = FigureCanvas(figure1)
        self.canvas2 = FigureCanvas(figure2)
        self.canvas3 = FigureCanvas(figure3)
        self.canvas4 = FigureCanvas(figure4)
        self.ax1 = figure1.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax2 = figure2.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax3 = figure3.add_subplot(111,position=[0.15, 0.15, 0.75, 0.75])
        self.ax4 = figure4.add_subplot(111,position=[0.10, 0.10, 0.70, 0.70], projection='polar')
        
        
        toolbar1 = NavigationToolbar(self.canvas1, self)
        toolbar2 = NavigationToolbar(self.canvas2, self)
        toolbar3 = NavigationToolbar(self.canvas3, self)
        toolbar4 = NavigationToolbar(self.canvas4, self)
        
        mainLayout.addLayout(subLayout, 0, 0)
        mainLayout.addLayout(subLayout2, 1, 0)
        mainLayout.addLayout(subLayout3, 0, 1)
        mainLayout.addWidget(toolbar1,2,0)
        mainLayout.addWidget(toolbar2,2,1)
        mainLayout.addWidget(toolbar3,4,0)
        mainLayout.addWidget(toolbar4,4,1)
        mainLayout.addWidget(self.canvas1,3,0)
        mainLayout.addWidget(self.canvas2,3,1)
        mainLayout.addWidget(self.canvas3,5,0)
        mainLayout.addWidget(self.canvas4,5,1)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Dashboard")
    
    #allows user to search for the required file and returns the file name    
    def openFile(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, 'File')
        self.file_display.setText(str(self.filename))

        return self.filename

    #pandas reads the data file along with the sampling frequency and total runtime
    def readFile(self):
        self.sampl_freq = float(self.sampl_freq_lineedit.text())
        self.total_time = float(self.time_lineedit.text()) 
        self.df = data_import_func.access_file(self.filename, self.total_time, self.sampl_freq)
    
    
    def plot(self):
        #Figure 1 is used to plot the time series. 
        
        self.ax1.clear()
        self.content = self.combo_box.currentText() 
        std_val, mean_val, max_val, min_val = data_import_func.stats(self.df[self.content])
        #self.l3_output.setText('%.5s' % str(mean_val))
        #Add Normalisation to the statistical parameters
        #self.l4_output.setText('%.5s' % str(std_val) + '/' + '%.4s' % str(std_val/mean_val))
        #self.l5_output.setText('%.5s' % str(max_val) + '/' + '%.4s' % str(max_val/mean_val))
        #self.l6_output.setText('%.5s' % str(min_val) + '/' + '%.4s' % str(min_val/mean_val))
        mean_array = [mean_val] * len(self.df[self.content])
        upper_std = [(mean_val + std_val)]* len(self.df[self.content])
        lower_std = [(mean_val - std_val)]* len(self.df[self.content])
        self.ax1.plot(self.df[self.content], label = 'Data')
        self.ax1.plot(self.df.index,mean_array, label = 'Mean', linestyle = '--')
        self.ax1.plot(self.df.index, upper_std, label = 'Upper Standard Deviation', linestyle = '--')
        self.ax1.plot(self.df.index, lower_std, label = 'Lower Standard Deviation', linestyle = '--')
        self.ax1.set_ylabel('Force [N]')
        self.ax1.set_xlabel('Time [s]')
        self.ax1.set_title('Time Signal')
        self.ax1.grid()
        self.ax1.legend()
        self.canvas1.draw()    
        
        
        #Figure 2 will be used to plot the fft
        #read the bins provided for the fft operation
        if self.fft_input.text() == 'Default':
            self.fft_get_text = 'Default'
        else:
            self.fft_get_text = float(self.fft_input.text())
       
        #allow for normalisation using the checkbox 
        spec, freq = data_import_func.spectral_analysis(self.df,self.content, self.total_time,self.sampl_freq,  self.fft_get_text)
        self.ax2.clear()
        
        
        if self.fft_checkbox.isChecked() == True:
            rotor_freq = data_import_func.rotor_freq(self.df['RPM'])
            freq = freq/rotor_freq            
            self.ax2.loglog(freq[1:int(len(freq)/2)], spec[1:])
            self.ax2.set_xlabel(r'$\frac{F}{f_0}$ [Hz/Hz]')
            self.ax2.set_title('Normalised FFT')
           
        else:
            self.ax2.loglog(freq[1:int(len(freq)/2)], spec[1:])
            self.ax2.set_xlabel('Frequency [s]')
            self.ax2.set_title('FFT')
            
        self.ax2.set_ylabel('Force [N]')
        self.ax2.grid(True, which = 'both', ls = '--')
        self.canvas2.draw()            
        
        #read the bins for the histogram first
        self.bin_input = int(self.bin_lineedit.text())
        #Figure 3 will be used to plot a normal distribution of normalised loads
        self.ax3.clear()
        self.ax3.hist(self.df[self.content], bins = self.bin_input, density=True)
        self.ax3.set_xlabel('Force [N]')
        self.ax3.set_ylabel('PDF')
        sorted_array = self.df.sort_values(by=self.content)[self.content]
        self.ax3.plot(sorted_array, norm.pdf(sorted_array, mean_val, std_val))
        self.ax3.set_title('Probability density Function')
        self.ax3.grid()
        self.canvas3.draw()
        
        
        #Plot the polar chart with 
        #pass values to the function angle_turbine
        t = self.df.index.to_numpy()
        Fy1 = self.df['Fy1'].to_numpy()
        Fy2 = self.df['Fy2'].to_numpy()
        Fy3 = self.df['Fy3'].to_numpy()
        fr= data_import_func.rotor_freq(self.df['RPM'])
        self.theta = data_import_func.angle_turbine(t, Fy1, Fy2, Fy3, fr)
        self.ax4.clear()
        #half the samples are plotted to avoid clutter
        self.ax4.scatter(self.theta[0:(int(len(self.theta)/2))], self.df[self.content][0:(int(self.total_time/2))], s = 0.01, alpha = 0.75)
        self.ax4.set_title('Varation against Blade Angle')
        self.canvas4.draw()
        
        
        
    #Create a new window to display the statistics    
    def window2(self):                                             # <===
        self.w = Window2()
        std_val, mean_val, max_val, min_val = data_import_func.stats(self.df[self.content])
        layout = QtWidgets.QGridLayout()
        
        self.heading1 =  QtWidgets.QLabel(self)
        self.heading1.setText('Actual')
        self.heading2 = QtWidgets.QLabel(self)
        self.heading2.setText('Normalised')
        
        #display statistical information about the signal
        self.avg_label = QtWidgets.QLabel(self)
        self.avg_label.setText('Average')
        self.avg_lineedit = QtWidgets.QLineEdit(self)
        self.avg_lineedit.setText('%.5s' % str(mean_val))
        self.avg_norm_lineedit = QtWidgets.QLineEdit(self)
        self.avg_norm_lineedit.setText('-')
        
        self.std_label = QtWidgets.QLabel(self)
        self.std_label.setText('Standard Deviation')
        self.std_lineedit = QtWidgets.QLineEdit(self)
        self.std_lineedit.setText('%.5s' % str(std_val))
        self.std_norm_lineedit = QtWidgets.QLineEdit(self)
        self.std_norm_lineedit.setText('%.4s' % str(std_val/mean_val))
            
        self.max_label = QtWidgets.QLabel(self)
        self.max_label.setText('Max')
        self.max_lineedit = QtWidgets.QLineEdit(self)
        self.max_lineedit.setText('%.5s' % str(max_val))
        self.max_norm_lineedit = QtWidgets.QLineEdit(self)
        self.max_norm_lineedit.setText('%.4s' % str(max_val/mean_val))
        
        self.min_label = QtWidgets.QLabel(self)
        self.min_label.setText('Min ')
        self.min_lineedit = QtWidgets.QLineEdit(self)
        self.min_lineedit.setText('%.5s' % str(min_val))
        self.min_norm_lineedit = QtWidgets.QLineEdit(self)
        self.min_norm_lineedit.setText('%.4s' % str(min_val/mean_val))
        
        layout.addWidget(self.heading1,0,1)
        layout.addWidget(self.heading2, 0,2)
        layout.addWidget(self.avg_label, 1, 0)
        layout.addWidget(self.avg_lineedit, 1, 1)
        layout.addWidget(self.avg_norm_lineedit, 1, 2)
        layout.addWidget(self.std_label, 2,0)
        layout.addWidget(self.std_lineedit, 2,1)
        layout.addWidget(self.std_norm_lineedit, 2, 2)
        layout.addWidget(self.max_label, 3,0)
        layout.addWidget(self.max_lineedit, 3,1)
        layout.addWidget(self.max_norm_lineedit, 3,2)
        layout.addWidget(self.min_label, 4,0)
        layout.addWidget(self.min_lineedit, 4,1)
        layout.addWidget(self.min_norm_lineedit, 4,2)
        self.w.setLayout(layout)
        
        self.w.show()
     
    #Allow for better visualisation of the angular variation    
    def window3(self):
        self.w3 = Window3()
        layout_w3 = QtWidgets.QGridLayout()
        figure5 = Figure()
        self.canvas5 = FigureCanvas(figure5)
        self.ax5 = figure5.add_subplot(111,position=[0.10, 0.10, 0.70, 0.70], projection='polar')
        self.ax5.scatter(self.theta[0:(int(len(self.theta)/2))], self.df[self.content][0:(int(self.total_time/2))], s = 0.01, alpha = 0.75)
        self.ax5.set_title('Varation against Blade Angle')
        layout_w3.addWidget(self.canvas5,0,0)
        self.w3.setLayout(layout_w3)
        self.w3.show()
        

class Window2(QtWidgets.QWidget):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statistics")
        
class Window3(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Angular Variation")
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())