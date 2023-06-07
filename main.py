import streamlit as st
import pandas as pd
import itertools

import datetime
import numpy as np
# import io
import plotly.express as px
# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

st.title('Modulus (Slope) Tool')


# Provide dataframe example & relative url
data_ex_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQzc-xaGomUO81MiJ7lyQ__FhbPIGK4YTvUjoE76BglXWj2XLIqSc-9-Mrlq9P2iuYeqRhgRJTgn1QW/pub?gid=0&single=true&output=csv"
# st.write("Factor Format Example File [link](%s)" % factor_ex_url)
st.markdown("#### Data Format Example File [Demo File](%s)" % data_ex_url)

uploaded_csv = st.file_uploader('#### 選擇您要上傳的CSV檔')

if uploaded_csv is not None:
    df_raw = pd.read_csv(uploaded_csv, encoding="utf-8")
    st.header('您所上傳的CSV檔內容：')
    st.dataframe(df_raw)

    select_list = list(df_raw.columns)
    # select_list
    y_var = st.selectbox("### Choose y variable", select_list)
    if not y_var:
        st.error("Please select one y variable.")

    # response
    x_list = select_list.copy()
    x_list.remove(y_var)
    x_var = st.selectbox(
        "### Choose x variable", x_list)
    if not x_var:
        st.error("Please select one x variable.")

    st.markdown("----------------")  

fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    # st.markdown("#### **Choose figure type**")
    fig_type = st.selectbox(
        "### Choose figure type", 
        ["box", "violin", "scatter", "bubble", "bubble animate", "histogram"],
    )
    
with fig_col2:
    category = st.selectbox(
        "### Choose category", x_list)
    
size_col1, size_col2 = st.columns(2)
with size_col1:

    fig_width = st.number_input('Figure Width', min_value=640, value=1280, max_value=5120, step=320) 
    
with size_col2:
    fig_height = st.number_input('Figure Height', min_value=480, value=960, max_value=3840, step=240) 

st.markdown("----------------")  

if fig_type == "histogram":
    # st.markdown("##### Choose ")
    bins = st.number_input('Choose bins', min_value=5, value=10, max_value=100, step=5) 


if st.button('Plot'):
    df_plot = df_raw.copy()


    if fig_type == "box":
        fig = px.box(df_plot, x = x_var, y=y_var, color=category, points="all", 
                        # color_discrete_sequence=color_sequence, template=template, 
                        # range_y=y_range, 
                        width=fig_width, height=fig_height,
                        hover_data=df_plot.columns,
                    )

    elif fig_type == "violin":
        fig = px.violin(df_plot, x=x_var, y=y_var, color=category, points="all",
                        # box=False, color_discrete_sequence=color_sequence, 
                        # template=template, range_y=y_range, 
                        width=fig_width, height=fig_height,
                        hover_data=df_plot.columns,
                        )
        
    elif fig_type == "histogram":
        fig = px.histogram(df_plot, x=y_var, nbins=bins, color=category,
                    # color_discrete_sequence=color_sequence,
                    # range_x=x_range, range_y=y_range, template=template,       
                    width=fig_width, height=fig_height
                    )
  
    fig.update_layout(
        xaxis_title=x_var,
        yaxis_title=y_var,
        # legend_title="Legend Title",
        font=dict(
            family="Courier New, monospace",
            size=18
            # color="RebeccaPurple"
        ),
        yaxis = dict(tickfont = dict(size=25)),
        xaxis = dict(tickfont = dict(size=15))
    )
    st.plotly_chart(fig, use_container_width=True)
