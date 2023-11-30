# -*- coding: utf-8 -*-
#from math import exp
from utils import values_table
import pandas as pd
import numpy as np
from sympy import exp
import matplotlib.pyplot as plt


# # Sacchi 2019 model
#
# https://github.com/romainsacchi/LCA_WIND_DK/blob/master/LCA_parameterized_model_Eolien_public.ipynb

# +
##Scaling model: Rotor diameter (m) - Rated power (MW)
def rotor_diameter_m_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d):
    y = coeff_a - coeff_b*exp(-(x*1e3-coeff_d)/coeff_c)
    return y
p_rotor_power_ON = [152.66222073,   136.56772435,  2478.03511414,    16.44042379]
p_rotor_power_OFF = [191.83651588,   147.37205671,  5101.28555377,   376.62814798]

#Scaling model: Hub height (m) - Rated power (MW)
def hub_height_m_power_MW(x, coeff_e, coeff_f, coeff_g):
    y = coeff_e - coeff_f*exp(-(x*1e3)/coeff_g)
    return y
p_height_power_ON = [116.43035193, 91.64953366, 2391.88662558] 
p_height_power_OFF = [120.75491612, 82.75390577, 4177.56520433]


#Scaling model: Nacelle weight (kg) - Rated power (MW)
def nacelle_weight_kg_power_MW(x, coeff_h, coeff_i):
    y = coeff_h * (x*1e3)**2 + coeff_i*x*1e3
    return 1e3 * y 
p_nacelle_weight_power_ON = [  1.66691134e-06,   3.20700974e-02] 
p_nacelle_weight_power_OFF = [  2.15668283e-06,   3.24712680e-02]

#Scaling model: Rotor weight (kg) - Rated power (MW)
def rotor_weight_kg_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d, coeff_j, coeff_k):
    rotor_diameter= rotor_diameter_m_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d)
    y = coeff_j * rotor_diameter**2 + coeff_k*rotor_diameter
    return 1e3 * y
p_rotor_weight_rotor_diameter_ON  = [ 0.00460956,  0.11199577] 
p_rotor_weight_rotor_diameter_OFF = [ 0.0088365,  -0.16435292]

#Scaling model: Tower weight (kg) - Rated power (MW)
def tower_weight_kg_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d, coeff_e, coeff_f, coeff_g, coeff_l, coeff_m):
    rotor_diameter= rotor_diameter_m_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d)
    hub_height=hub_height_m_power_MW(x, coeff_e, coeff_f, coeff_g)
    y = coeff_l * rotor_diameter**2*hub_height + coeff_m
    return 1e3 * y
p_tower_weight_d2h = [3.03584782e-04, 9.68652909e+00]

#Scaling model: Total wind turbine weight (kg) - Rated power (MW)
def total_wind_turbine_weight_kg_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d, coeff_e, coeff_f, coeff_g, coeff_h, coeff_i, coeff_j, coeff_k, coeff_l, coeff_m):
    nacelle_weight = coeff_h * (x*1e3)**2 + coeff_i*x*1e3
    rotor_diameter= rotor_diameter_m_power_MW(x, coeff_a, coeff_b, coeff_c, coeff_d)
    hub_height=hub_height_m_power_MW(x, coeff_e, coeff_f, coeff_g)
    rotor_weight = coeff_j * rotor_diameter**2 + coeff_k*rotor_diameter
    tower_weight = coeff_l * rotor_diameter**2*hub_height + coeff_m
    y = nacelle_weight + rotor_weight + tower_weight
    return 1e3 * y


# -

# # Wind turbine mass and rotor diameter model

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


# +
#Import data collected in an excel file
df1 = pd.read_excel("Data_extrapolation_mass_windturbines_v4_non_confid.xlsx",sheet_name='extract data non confid')

#Data to be fited
power='Power (MW)'
diameter='Rotor Diameter (m)'
tower_mass='Tower mass (t)'
three_blades_mass= '3 blades mass (t)'
nacelle_mass_with_hub='Nacelle mass with hub (t)'
wind_turbine_mass='Total mass - without painting (t)'

#Fit the power and rotor diameter based on the input data (excel file)
rotor_diameter_m_power_MW_2=polynomial_fit(power, diameter, 1)
tower_mass_t_power_MW_2=polynomial_fit(power, tower_mass, 1)
three_blades_mass_t_power_MW_2=polynomial_fit(power, three_blades_mass, 1)
nacelle_with_hub_mass_t_power_MW_2=polynomial_fit(power, nacelle_mass_with_hub, 1)
wind_turbine_mass_t_power_MW_2=polynomial_fit(power, wind_turbine_mass, 1)

# -



# # Foundations mass diameter model
#

# +
#Import data collected in an excel file
df1 = pd.read_excel("Data_extrapolation_mass_foundations_v2_non_confid.xlsx",sheet_name='extract data jacket')

#Data to be fited
power= 'Power capacity (MW)'
jacket_mass_per_length='Mass / length (t/m)'

#Fit the power and rotor diameter based on the input data (excel file)
jacket_mass_per_length_tperm_power_MW=polynomial_fit(power, jacket_mass_per_length, 1)
