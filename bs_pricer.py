# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 16:17:20 2026

@author: manu0
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import norm 

######################################################################

st.title("Black-Scholes-Merton Pricer")

st.subheader("Input data")
col1, col2 = st.columns(2)
option_type = col1.selectbox("Option type?", ("Call", "Put"))
S = col1.number_input("Spot:", min_value = 0.01, value = 50.0, step = 5.0)
K = col1.number_input("Strike:", min_value = 0.01, value = 60.0, step = 5.0)
r = col2.number_input("Risk-free rate:", min_value = 0.0, value = 0.05, step = 0.05)
T = col2.number_input("Maturity (years):", min_value = 0.0001, value = 1.0, step = 0.25)
sigma = col2.number_input("Volatility:", min_value = 0.0001, max_value = 1.0, value = 0.2, step = 0.05)

@st.cache_data
def calculate_d1_d2(S, K, r, T, sigma):

    d1 = (np.log(S/K) + (r + sigma**2/2) * T)/(sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    return(d1,d2)

def bs_pricer(S, K, r, T, sigma, option_type):
    
    d1, d2 = calculate_d1_d2(S, K, r, T, sigma)
    
    option_type = option_type.lower().strip()
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return(round(price, 5))

######################################################################

def parity_check(S, K, r, T, sigma):
    spread = (bs_pricer(S, K, r, T, sigma, "Call") - bs_pricer(S, K, r, T, sigma, "Put")) - (S - K * np.exp(-r * T))   
    return(spread)
        
result_parity = parity_check(S, K, r, T, sigma)

st.divider()
st.subheader("Call-put parity check")
col1, col2, col3 = st.columns(3)
col1.metric("Theoretical price", value = f"${bs_pricer(S, K, r, T, sigma, option_type):.5f}")
col2.metric("Spread", value = f"${parity_check(S, K, r, T, sigma):.5f}")

if np.abs(result_parity) < 1e-4:
    col3.write("Model holds: no arbitrage")
else:
    col3.write("Something wrong: arbitrage")

######################################################################

def bs_greeks(S, K, r, T, sigma, option_type):

    d1, d2 = calculate_d1_d2(S, K, r, T, sigma)
    
    option_type = option_type.lower().strip()
    
    gamma = norm.pdf(d1)/(S * sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * norm.pdf(d1)
    
    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-(S * norm.pdf(d1) * sigma)/(2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))/365
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)

    elif option_type == "put":
        delta = norm.cdf(d1) - 1 
        theta = (-(S * norm.pdf(d1) * sigma)/(2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))/365
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)

    return(delta, gamma, vega, theta, rho)

######################################################################
    
st.divider()
st.subheader("Greeks")

spot_range = pd.Series(np.linspace(S * 0.5, S * 1.5, 100))

option_type = option_type.lower().strip()

delta_atm, gamma_atm, vega_atm, theta_atm, rho_atm = bs_greeks(S, K, r, T, sigma, option_type)

st.markdown(f"**Current Values at Spot = {S}**")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Delta", f"{delta_atm:.4f}")
m2.metric("Gamma", f"{gamma_atm:.2e}" if gamma_atm < 0.0001 else f"{gamma_atm:.5f}")
m3.metric("Vega", f"{vega_atm:.4f}")
m4.metric("Theta", f"{theta_atm:.4f}")
m5.metric("Rho", f"{rho_atm:.4f}")

deltas_list, gammas_list, vegas_list, thetas_list, rhos_list = [], [], [], [], []
for spot_temp in spot_range:
    d, g, v, th, rh = bs_greeks(spot_temp, K, r, T, sigma, option_type)
    deltas_list.append(d)
    gammas_list.append(g)
    vegas_list.append(v)
    thetas_list.append(th)
    rhos_list.append(rh)

delta_series = pd.Series(deltas_list)
gamma_series = pd.Series(gammas_list)
vega_series = pd.Series(vegas_list)
theta_series = pd.Series(thetas_list)
rho_series = pd.Series(rhos_list)

graph_delta = px.line(x = spot_range, y = delta_series, labels = {"x":"Spot", "y":"Delta"}, title = "Delta of the option", template = "plotly_dark", height = 600)
graph_gamma = px.line(x = spot_range, y = gamma_series, labels = {"x":"Spot", "y":"Gamma"}, title = "Gamma of the option", template = "plotly_dark", height = 600)
graph_vega = px.line(x = spot_range, y = vega_series, labels = {"x":"Spot", "y":"Vega"}, title = "Vega of the option", template = "plotly_dark", height = 600)
graph_theta = px.line(x = spot_range, y = theta_series, labels = {"x":"Spot", "y":"Theta"}, title = "Theta of the option", template = "plotly_dark", height = 600)
graph_rho = px.line(x = spot_range, y = rho_series, labels = {"x":"Spot", "y":"Rho"}, title = "Rho of the option", template = "plotly_dark", height = 600)

st.plotly_chart(graph_delta, width = "stretch")
st.plotly_chart(graph_gamma, width = "stretch")
st.plotly_chart(graph_vega, width = "stretch")
st.plotly_chart(graph_theta, width = "stretch") 
st.plotly_chart(graph_rho, width = "stretch") 
    

        




