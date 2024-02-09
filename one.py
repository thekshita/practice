#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 15:17:21 2024

@author: deekshitadoli
"""

import streamlit as st
import os
from dotenv import load_dotenv
from query_service import QueryService

st.title('🦜🔗 Quickstart App')
\

#load_dotenv()
#os.environ['OPENAI_API_KEY'] = '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'
#openai_api_key = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = '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'
query_service = QueryService()

def generate_response(question):
    resp = query_service.ask_agent(question=question)
    st.info(resp)

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        generate_response(text)
        
        