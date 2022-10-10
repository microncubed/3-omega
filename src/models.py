# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:19:49 2019

@author: andrew.ferguson
"""
import numpy as np
import csv
import os

path = os.getcwd()
basepath = os.path.dirname(path)

##Builds up the dictionaries of thermal parameters

k = {}
c = {}
rho = {}

filename = basepath+"/src/thermal_properties.csv"

with open(filename,'r') as f:
    csvreader = csv.DictReader(f)
    for row in csvreader:
        k[row['material']]= float(row['thermal_conductivity'])
        c[row['material']]= float(row['specific_heat'])
        rho[row['material']]= float(row['density'])
          
def test2d():    
    nx=101
    ny=101
    dx = 3e-6
    dy = 1e-6

    
    x_lim = (nx-1)*dx/2
    y_lim = (ny-1)*dy/2
    
    x = np.linspace(-x_lim,x_lim,nx)
    y = np.linspace(-y_lim,y_lim,ny)
    
    k_in = np.zeros((nx,ny))
    k_in[:,:] =k['water']
    
    Q_in = np.zeros((nx,ny))
    Q_in_val = 1
    Q_in[:,:] = Q_in_val
    
    v_in = np.zeros((nx,ny))
    c_in = np.zeros((nx,ny))
    rho_in = np.zeros((nx,ny))
    
    c_in[:,:]=c['water']
    rho_in[:,:]=rho['water']
    
    return [k_in,c_in,rho_in,Q_in,v_in,x,y,dx,dy,nx,ny]

def single_wire(glass = True, half_width = 5):
    '''
    A model of a single wire heater sitting on either a glass or silicon nitride substrate.

    Parameters
    -----------
    glass boolean: if True heater sits on glass, if False on silicon nitride
    half_width int: half width of the heater in grid spacings

    Returns
    -----------
    k_in np.ndarray : thermal conductivity
    c_in np.ndarray : heat capacity
    rho_in np.ndarray : density
    Q_in np.ndarray : heat source
    v_in np.ndarray : velocity field
    x np.ndarray : the x-axis
    y np.ndarray : the y-axis
    dx float : step-size in x
    dy float : step-size in y
    nx int : number of steps in x
    ny int : number of steps in y
    '''		

    nx=401
    ny=201
    dx = 2.5e-6
    dy = 2.5e-6
    
    x_lim = (nx-1)*dx/2
    y_lim = (ny-1)*dy/2
    
    x = np.linspace(-x_lim,x_lim,nx)
    y = np.linspace(-y_lim,y_lim,ny)
    
    k_in = np.zeros((nx,ny))
    c_in = np.zeros((nx,ny))
    rho_in = np.zeros((nx,ny))
    Q_in = np.zeros((nx,ny))       
    
    v_max=0
    
    #put some water or air in the flow cell
    if glass == True:
        k_in[:,:100 ] = k['silicon_dioxide']
        c_in[:,:100] = c['silicon_dioxide']
        rho_in[:,:100] = rho['silicon_dioxide']
    elif glass == False:
        k_in[:,:100 ] = k['silicon_nitride']
        c_in[:,:100] = c['silicon_nitride']
        rho_in[:,:100] = rho['silicon_nitride']
    
    
    #silicon dioxide membrane
    k_in[:,100:] = k['air']
    c_in[:,100:] = c['air']
    rho_in[:,100:] = rho['air']
        
    #the heat source
    Q_in[(200-half_width):(200+half_width),99:100] = 1
      
    #the parabolic velocity field
    v_in = np.zeros((nx,ny))
    for yval in range(50,101):
        v_in[:,yval] = v_max - 4*v_max/50**2*(yval-75)**2
        
    return [k_in,c_in,rho_in,Q_in,v_in,x,y,dx,dy,nx,ny]

