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
          

def single_wire(material='silicon_dioxide',half_width = 5,nx=401,ny=201):
    '''
    A model of a single wire heater sitting on either a glass or silicon nitride substrate.

    Parameters
    -----------
    material str: material choice as available in thermal_parameters.csv
    half_width int: half width of the heater in x grid spacing
    nx,ny int: number of grid points in x and y

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
    
    k_in[:,:ny//2 ] = k[material]
    c_in[:,:ny//2] = c[material]
    rho_in[:,:ny//2] = rho[material]

    
    
    #silicon dioxide membrane
    k_in[:,ny//2:] = k['air']
    c_in[:,ny//2:] = c['air']
    rho_in[:,ny//2:] = rho['air']
        
    #the heat source
    Q_in[(nx//2-half_width):(nx//2+half_width),ny//2-1:ny//2] = 1
      
    #the parabolic velocity field
    v_in = np.zeros((nx,ny))
        
    return [k_in,c_in,rho_in,Q_in,v_in,x,y,dx,dy,nx,ny]

