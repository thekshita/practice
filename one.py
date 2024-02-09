#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:17:21 2024

@author: deekshitadoli
"""

import streamlit as st
from query_service import QueryService
import os
from dotenv import load_dotenv
st.title('🦜🔗 EquityEngine')

query_service = QueryService()

load_dotenv()
os.environ['OPENAI_API_KEY'] = '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'

def generate_response(question):
    resp = query_service.ask_agent(question=question)
    st.info(resp)

with st.form('my_form'):
    text = st.text_area('AMA about UW\'s DSO', 'What is the DSO and where is it located?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)
        
        