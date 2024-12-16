import streamlit as st
import numpy as np


def render_sidebar():
    r = st.sidebar.number_input("Внутренний радиус (см)", value=2.0)
    R = st.sidebar.number_input("Внешний радиус (см)", value=5.0)
    V = st.sidebar.number_input("Начальная скорость V (м/с)", value=8e6)
    L = st.sidebar.number_input("Длина конденсатора L (см)", value=13.0)

    return r, R, V, L


def display_information(deltaV_min, t, x, y, vy):
    t_final = t[-1]
    v_final = np.abs(vy[-1])

    st.markdown(
        f"""
        <div style="background-color: #f0f8e2; padding: 15px; border-radius: 10px;">
            <h3 style="color: #2f5d62;">🔋 Минимальная разность потенциалов:</h3>
            <p style="font-size: 24px; text-align: center; color: #000000;">{deltaV_min:.2f} В</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<p></p>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #cceeff; color:#000000;">
            <h3 style="color: #007acc;">🔍 Результаты движения:</h3>
            <h4>Время полета:</h4> <p>{t_final:.6e} с</p>
            <h4>Конечная вертикальная скорость:</h4> <p>{v_final:.6e} м/с</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
