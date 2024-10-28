import pandas as pd
import scipy.stats
import streamlit as st
import time

# Estas son variables de estado que se conservan cuando Streamlit vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Inicializa el gráfico
chart = st.line_chart([0.5])

def toss_coin(n):
    # Simula el lanzamiento de una moneda
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    outcome_no = 0
    outcome_1_count = 0
    mean = None

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])  # Agrega el promedio actual al gráfico
        time.sleep(0.05)  # Pausa para hacer el gráfico más visual

    return mean

# Control deslizante para el número de intentos
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1  # Incrementa el número del experimento
    mean = toss_coin(number_of_trials)  # Realiza el experimento
    # Actualiza los resultados del experimento en el DataFrame
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trials,
                            mean]],
                     columns=['no', 'iteraciones', 'media'])
    ], axis=0).reset_index(drop=True)

# Muestra los resultados acumulados en un DataFrame
st.write(st.session_state['df_experiment_results'])