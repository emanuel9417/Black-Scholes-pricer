# Black-Scholes-Merton Option Pricing & Greeks Dashboard

## Overview
An interactive financial tool developed to price European options using the **Black-Scholes-Merton model**. The application provides real-time sensitivity analysis (Greeks) and verifies the mathematical consistency of the model through Put-Call Parity.

**Live Application:** [View Web App](https://emanuel9417-black-scholes-merton-pricer-a5xaep7bhkp3yqs7pgrfgq.streamlit.app/)

## Key Features
* **Option Pricing**: Accurate calculation of Call and Put premiums.
* **Dynamic Greeks Analysis**: Visual representation of risk sensitivities:
    * **Delta**
    * **Gamma**
    * **Vega**
    * **Theta**
    * **Rho**
* **Put-Call Parity Check**: Real-time validation to ensure no-arbitrage conditions.
* **Scenario Simulation**: Interactive charts showing Greeks behavior across a $\pm 50\%$ spot price range.

## Technical Stack
Python, numpy, scipy, pandas, plotly, streamlit

## Implementation Details
The model assumes log-normal distribution of stock prices and constant volatility over the option's life. The dashboard is designed for users to visualize how Greeks evolve as the option moves In-the-Money (ITM) or Out-of-the-Money (OTM).
