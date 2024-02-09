#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 00:08:55 2024

@author: deekshitadoli
"""

#from dotenv import load_dotenv


import pickle
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter

#load_dotenv()

OPENAI_API_KEY = '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'


def create_pkl(category: str, urls: list):
    loaders = UnstructuredURLLoader(urls=urls)
    data = loaders.load()
    text_splitter = CharacterTextSplitter(separator='\n', 
                                      chunk_size=1000, 
                                      chunk_overlap=200)

    docs = text_splitter.split_documents(data)

    embeddings = OpenAIEmbeddings()
    vectorStore_openAI = FAISS.from_documents(docs, embeddings)
    
    with open(f"{category}_vectors.pkl", "wb") as f:
        pickle.dump(vectorStore_openAI, f)
    
    with open(f"{category}_vectors.pkl", "rb") as f:
        vectorStore = pickle.load(f)
        
urls = [
    "https://hr.uw.edu/dso/",
    "https://hr.uw.edu/dso/services/",
    "https://hr.uw.edu/dso/services/services-for-faculty-and-staff/",
    "https://hr.uw.edu/dso/services/managersrole/",
    "https://hr.uw.edu/dso/services/uw-job-applicants/",
    "https://hr.uw.edu/dso/services/matriculated-students/",
    "https://hr.uw.edu/dso/services/services-for-students/",
    "https://hr.uw.edu/dso/services/services-for-the-public/",
    "https://hr.uw.edu/dso/deaf-or-hard-of-hearing/overview/",
    "https://hr.uw.edu/dso/deaf-or-hard-of-hearing/faculty-guide-for-zoom-classes-with-interpreters-captioners/",
    "https://hr.uw.edu/dso/deaf-or-hard-of-hearing/faculty-guide-zoom-small-group-or-1-to-1-interpreted-meetings/",
    "https://hr.uw.edu/dso/deaf-or-hard-of-hearing/interpreter-guide-for-zoom-classes/",
    "https://hr.uw.edu/dso/deaf-or-hard-of-hearing/student-guide-for-working-with-interpreters-in-zoom-classes/",
    "https://hr.uw.edu/dso/disability-parking/students/",
    "https://hr.uw.edu/dso/disability-parking/employees/",
    "https://hr.uw.edu/dso/disability-parking/visitors/",
    "https://hr.uw.edu/dso/service-animals/",
    "https://hr.uw.edu/dso/ergonomics/",
    "https://hr.uw.edu/dso/contacts/",
    "https://hr.uw.edu/dso/additional-resources/deaf-and-hard-of-hearing-service-providers/",
    "https://hr.uw.edu/dso/additional-resources/accommodation-event-notice/",
    "https://hr.uw.edu/dso/additional-resources/dso-flyer/",
    "https://hr.uw.edu/dso/additional-resources/resources-from-dso-partners/"
    ]


create_pkl("dso", urls)
           
