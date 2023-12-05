# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sympy import exp
from utils import values_table
from scipy import stats

# # Data collected in excel file

# ## Import data

#Import data collected in an excel file
df1 = pd.read_excel("Data_extrapolation_mass_foundations_v2_non_confid.xlsx",sheet_name='extract data jacket')
df1

#print the name of the columns
columns=df1.columns.tolist()
columns

#Define variables based on the name of the columns
power= 'Power capacity (MW)'
length='Length (m)'
jacket_mass='Jacket mass (t)'
jacket_mass_per_length='Mass / length (t/m)'
jacket_mass_per_length_per_power= 'Mass / length / power (t/m/MW)'
normalized_jacket_mass_per_length_per_power='Normalized Mass / length / power'


# ## Function to fit data collected

def polynomial_fit(x_axis,y_axis,degree):
    """
    Fit the input data with a polynomial function
    x_axis is a string. The name of the column with x-axis data to be fitted
    y_axis is a string. The name of the column with y-axis data to be fitted
    degree is an integrer. The degree of the polynomial function to be fitted
    """
    #Generate a dataframe with the two columns that have to be correlated
    df2=pd.concat([df1[x_axis], df1[y_axis]], axis=1, keys=[x_axis, y_axis])
    
    # Delete all the lines with NaN values
    df2=df2[(~df2.isnull()).all(axis=1)]

    #Generate two lists of data that need to be correlated                                                          
    x_list = [x for x in df2[x_axis]]
    y_list = [y for y in df2[y_axis]]

    #Fit the data 
    fit =np.polyfit(x_list, y_list, degree)
    poly = np.poly1d(fit)
    return poly


# ## Function to get correlation coefficient if the polynomial fit degree is 1

# +
# Linear regression # y=ax+b

def correlation_coefficient(x_axis,y_axis):
    #Generate a dataframe with the two columns that have to be correlated
    df2=pd.concat([df1[x_axis], df1[y_axis]], axis=1, keys=[x_axis, y_axis])
    
    # Delete all the lines with NaN values
    df2=df2[(~df2.isnull()).all(axis=1)]

    #Generate two lists of data that need to be correlated                                                          
    x_list = [x for x in df2[x_axis]]
    y_list = [y for y in df2[y_axis]]
    
    #Do the linear regression
    slope, intercept, r_value, p_value, std_error = stats.linregress(x_list,y_list)
    print ('Y= {0:.1f}'.format(slope),'x X', '+ {0:.1f}'.format(intercept))
    print ('correlation coefficient = {0:.4f}'.format(r_value))



# -

# ## Function to visualize the fit

def polynomial_fit_plot(x_axis,y_axis,degree):
    """
    Plot the fit of the input data with a polynomial function
    x_axis is a string. The name of the column with x-axis data to be fitted
    y_axis is a string. The name of the column with y-axis data to be fitted
    degree is an integrer. The degree of the polynomial function to be fitted
    """
    #Generate a dataframe with the two columns that have to be correlated
    df2=pd.concat([df1[x_axis], df1[y_axis]], axis=1, keys=[x_axis, y_axis])
    
    # Delete all the lines with NaN values
    df2=df2[(~df2.isnull()).all(axis=1)]

    #Generate two lists of data that need to be correlated                                                          
    x_list = [x for x in df2[x_axis]]
    y_list = [y for y in df2[y_axis]]

    #Fit the data 
    fit =np.polyfit(x_list, y_list, degree)
    poly = np.poly1d(fit)
    
    #plot the data
    P=np.linspace(4,16, 13)
    y=[poly(x) for x in P]
    plt.plot(x_list, y_list, label='input data', marker = 'o', markersize = 5)
    plt.plot(P, y, label='fit')
    plt.xlim(4,16)
    plt.xlabel(x_axis, fontsize=16)
    plt.ylabel(y_axis, fontsize=16)
    #plt.legend()
    
    #return plt.show


# # Plot mass model data

# ## Jacket = f(power)

# +
#Fit the power and rotor diameter based on the input data (excel file)
jacket_mass_per_length_tperm_power_MW=polynomial_fit(power, jacket_mass_per_length, 1)
#Print the equation
print(jacket_mass_per_length_tperm_power_MW)
#Print the graph with input data and fit model
polynomial_fit_plot(power, jacket_mass_per_length, 1)

plt.legend()
plt.show()
# -

correlation_coefficient(power,jacket_mass_per_length)

# # Scaling factor

turbine_MW_min=5
turbine_MW_max=15

mass_per_MW_min=jacket_mass_per_length_tperm_power_MW(turbine_MW_min)/turbine_MW_min
mass_per_MW_max=jacket_mass_per_length_tperm_power_MW(turbine_MW_max)/turbine_MW_max
scale_factor=mass_per_MW_max/mass_per_MW_min
print(format(scale_factor, '.2f'))  

# +
#Fit the power and rotor diameter based on the input data (excel file)
normalized_jacket_mass_per_length_power_MW=polynomial_fit(power, normalized_jacket_mass_per_length_per_power, 1)
#Print the equation
print(normalized_jacket_mass_per_length_power_MW)
#Print the graph with input data and fit model
polynomial_fit_plot(power, normalized_jacket_mass_per_length_per_power, 1)

plt.ylim(0,1)
plt.legend()
plt.show()
# -

# # Value table

# +
turbine_MW=5
water_depth=40
emerged_height=20

values_table(
    jacket_mass_per_length=(jacket_mass_per_length_tperm_power_MW(turbine_MW)*(water_depth+emerged_height),"t"),
)
# -






