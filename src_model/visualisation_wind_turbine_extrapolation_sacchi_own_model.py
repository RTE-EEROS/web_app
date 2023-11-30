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
df1 = pd.read_excel("Data_extrapolation_mass_windturbines_v4_non_confid.xlsx",sheet_name='extract data non confid')
df1

#print the name of the columns
columns=df1.columns.tolist()
columns

#Define variables based on the name of the columns
power='Power (MW)'
diameter='Rotor Diameter (m)'
hub_height='Hub height (m)'
three_blades_mass= '3 blades mass (t)'
tower_mass='Tower mass (t)'
rotor_mass='Rotor mass (t)'
rotor_mass_with_hub='Rotor mass with hub (t)'
nacelle_mass='Nacelle mass (t)'
nacelle_mass_without_hub='Nacelle mass without hub (t)'
nacelle_mass_with_hub='Nacelle mass with hub (t)'
rotor_nacelle_mass='Rotor nacelle assembly mass (t)'
wind_turbine_mass='Total mass - without painting (t)'


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


# # Sacchi 2019 mass model

# ## Scaling functions
# No changes in the equations provided by [Sacchi 2019](https://github.com/romainsacchi/LCA_WIND_DK/blob/master/LCA_parameterized_model_Eolien_public.ipynb), just renaming and reorganizing the code to adapt it to our use

# ### Equations

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

# ### offshore or onshore
# Automatic change from offshore to onshore

# +
#Sacchi's model can switch from offshore to onshore data

p_rotor_power=[]
p_height_power=[]
p_nacelle_weight_power=[]
p_rotor_weight_rotor_diameter=[]

def switch_offshore_onshore(value):
    if value == 'onshore' :
        p_rotor_power.clear()
        p_rotor_power.extend(p_rotor_power_ON)
        
        p_height_power.clear()
        p_height_power.extend(p_height_power_ON)
        
        p_nacelle_weight_power.clear()
        p_nacelle_weight_power.extend(p_nacelle_weight_power_ON)
        
        p_rotor_weight_rotor_diameter.clear()
        p_rotor_weight_rotor_diameter.extend(p_rotor_weight_rotor_diameter_ON)
       
        #p_tower_weight_d2h=p_tower_weight_d2h
        
    elif value == 'offshore' :
        p_rotor_power.clear()
        p_rotor_power.extend(p_rotor_power_OFF)
        
        p_height_power.clear()
        p_height_power.extend(p_height_power_OFF)
        
        p_nacelle_weight_power.clear()
        p_nacelle_weight_power.extend(p_nacelle_weight_power_OFF)
        
        p_rotor_weight_rotor_diameter.clear()
        p_rotor_weight_rotor_diameter.extend(p_rotor_weight_rotor_diameter_OFF)
        
        #p_tower_weight_d2h=p_tower_weight_d2h
    
    else:
        print('there is a mistake')



# -

# ### Generating data for plots (offshore)

# +
#We use the offshore model
switch_offshore_onshore('offshore')

#Generate data from Sacchi's offshore model for plot
P=np.linspace(4,16, 13)
rotor_diameter_off=[rotor_diameter_m_power_MW(x,*p_rotor_power) for x in P]
hub_height_off=[hub_height_m_power_MW(x,*p_height_power) for x in P]
mass_nacelle_off=[nacelle_weight_kg_power_MW(x,*p_nacelle_weight_power)/1000 for x in P]
mass_rotor_off=[rotor_weight_kg_power_MW(x,*p_rotor_power,*p_rotor_weight_rotor_diameter)/1000 for x in P]
mass_tower_off=[tower_weight_kg_power_MW(x, *p_rotor_power, *p_height_power, *p_tower_weight_d2h)/1000 for x in P]
mass_tot_wind_turbine_off=[total_wind_turbine_weight_kg_power_MW(x, *p_rotor_power, *p_height_power, *p_nacelle_weight_power, *p_rotor_weight_rotor_diameter, *p_tower_weight_d2h)/1000 for x in P]

#Sum of mass of rotor and mass of nacelle
mass_rotor_nacelle_off=[]
for i in range(len(mass_nacelle_off)):
    mass_rotor_nacelle_off.append(mass_rotor_off[i]+mass_nacelle_off[i])
# -


# # Plot mass model data

# ## Rotor diameter = f(power)

# +
#Fit the power and rotor diameter based on the input data (excel file)
rotor_diameter_m_power_MW_2=polynomial_fit(power, diameter, 1)
#Print the equation
print(rotor_diameter_m_power_MW_2)
#Print the graph with input data and fit model
polynomial_fit_plot(power, diameter, 1)
#Print Sacchi's model
plt.plot(P, rotor_diameter_off, label='Sacchi 2019 offshore model')

plt.legend()
plt.show()
# -

correlation_coefficient(power,diameter)

# ## Hub height = f(power)

# +
#Fit the power and rotor diameter based on the input data (excel file)
hub_height_m_power_MW_2=polynomial_fit(power, hub_height, 1)
#Print the equation
print(hub_height_m_power_MW_2)
#Print the graph with input data and fit model
polynomial_fit_plot(power, hub_height, 1)
#Print Sacchi's model
plt.plot(P, hub_height_off, label='Sacchi 2019 offshore model')

plt.legend()
plt.show()


# -

# ## Mass_rotor = f(power)

# ### Rotor - all data

rotor_mass_t_power_MW_2=polynomial_fit(power, rotor_mass, 1)
print(rotor_mass_t_power_MW_2)
polynomial_fit_plot(power, rotor_mass, 1)
plt.plot(P, mass_rotor_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ### Rotor with hub

rotor_with_hub_mass_t_power_MW_2=polynomial_fit(power,rotor_mass_with_hub, 1)
print(rotor_with_hub_mass_t_power_MW_2)
polynomial_fit_plot(power, rotor_mass_with_hub, 1)
plt.plot(P, mass_rotor_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ### Rotor without hub : only blades > it fits

three_blades_mass_t_power_MW_2=polynomial_fit(power, three_blades_mass, 1)
print(three_blades_mass_t_power_MW_2)
polynomial_fit_plot(power, three_blades_mass, 1)
plt.plot(P, mass_rotor_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ## Mass_nacelle = f(power)

# ### Nacelle - all data

nacelle_mass_t_power_MW_2=polynomial_fit(power, nacelle_mass, 1)
print(nacelle_mass_t_power_MW_2)
polynomial_fit_plot(power, nacelle_mass, 1)
plt.plot(P, mass_nacelle_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ### Nacelle - without hub

nacelle_without_hub_mass_t_power_MW_2=polynomial_fit(power, nacelle_mass_without_hub, 1)
print(nacelle_without_hub_mass_t_power_MW_2)
polynomial_fit_plot(power, nacelle_mass_without_hub, 1)
plt.plot(P, mass_nacelle_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ### Nacelle with hub

nacelle_with_hub_mass_t_power_MW_2=polynomial_fit(power, nacelle_mass_with_hub, 1)
print(nacelle_with_hub_mass_t_power_MW_2)
polynomial_fit_plot(power, nacelle_mass_with_hub, 1)
plt.plot(P, mass_nacelle_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ## Mass_tower = f(power)

tower_mass_t_power_MW_2=polynomial_fit(power, tower_mass, 1)
print(tower_mass_t_power_MW_2)
polynomial_fit_plot(power, tower_mass, 1)
plt.plot(P, mass_tower_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ## Mass (rotor + nacelle) = f(power)

rotor_nacelle_mass_t_power_MW_2=polynomial_fit(power, rotor_nacelle_mass, 1)
print(rotor_nacelle_mass_t_power_MW_2)
polynomial_fit_plot(power, rotor_nacelle_mass, 1)
plt.plot(P, mass_rotor_nacelle_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# ## Mass wind turbine = f(power)

wind_turbine_mass_t_power_MW_2=polynomial_fit(power, wind_turbine_mass, 1)
print(wind_turbine_mass_t_power_MW_2)
polynomial_fit_plot(power,wind_turbine_mass, 1)
plt.plot(P, mass_tot_wind_turbine_off, label='Sacchi 2019 offshore model')
plt.legend()
plt.show()

# # Value table

# +
turbine_MW=5

values_table(
    rotor_diameter_sacchi=(rotor_diameter_m_power_MW(turbine_MW,*p_rotor_power),"m"),
    rotor_diameter_data=(rotor_diameter_m_power_MW_2(turbine_MW),"m"),
    tower_height_sacchi=(hub_height_m_power_MW(turbine_MW,*p_height_power),"m"),
    tower_height_data=(hub_height_m_power_MW_2(turbine_MW),"m"),
    mass_nacelle_sacchi=(nacelle_weight_kg_power_MW(turbine_MW,*p_nacelle_weight_power)/1000 ,"t"),
    mass_nacelle_data=(nacelle_with_hub_mass_t_power_MW_2(turbine_MW),"t"),
    mass_rotor_sacchi=(rotor_weight_kg_power_MW(turbine_MW,*p_rotor_power,*p_rotor_weight_rotor_diameter) /1000,"t"),
    mass_rotor_data=(three_blades_mass_t_power_MW_2(turbine_MW),"t"),
    mass_tower_sacchi=(tower_weight_kg_power_MW(turbine_MW, *p_rotor_power, *p_height_power, *p_tower_weight_d2h)/1000,"t"),
    mass_tower_data=(tower_mass_t_power_MW_2(turbine_MW),"t"),
    mass_tot_wind_turbine_sacchi=(total_wind_turbine_weight_kg_power_MW(turbine_MW, *p_rotor_power, *p_height_power, *p_nacelle_weight_power, *p_rotor_weight_rotor_diameter, *p_tower_weight_d2h) /1000, "t"),
    mass_tot_wind_turbine_data=(wind_turbine_mass_t_power_MW_2(turbine_MW), "t"),
)
# -






