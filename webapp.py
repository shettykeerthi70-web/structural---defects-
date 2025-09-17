import pandas as pd
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import datetime as dt

key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')





st.sidebar.title('Upload your image here')
uploaded_img = st.sidebar.file_uploader('Here',type = ['jpeg','jpg','png'])
if uploaded_img:
    image = Image.open(uploaded_img)

    st.title('Uploaded Image')
    st.image(image)

# create main page
st.title('Structural deffects : AI assisted stuctural defect identifier in constuction business')
prompt = 'Generate '
tips=('''To use the application follow the steps below:
* Upload the image
* Click on the button to generate summary
* Click download to save the report generated''')
st.write(tips)


rep_title = st.text_input('Report Text')
prep_by = st.text_input('Report prep by')
prep_for = st.text_input('Report prep for')
date = dt.datetime.now().date()

prompt = f''' {prep_for},{rep_title},{prep_for}Assume you are a structural engineer. The user has provided an image of a structure. You need to identify the structural defects 
in the image and genarate a report. The report should contain the following
* It should start with the title, prepared by and prepare for details provided by the user.
use {rep_title} as title, {prep_by} as prepared by, {prep_for} as prepared for the same.
also mention the {date} as the date
* Identify and classify the defect for eg: crack, spalling, corrosion, honycombing, etc.
* There could more than one defects in the image, Identify all the defects seperately 
* For each measure the severity of the defect as low, medium or high. If the defects is inavitable of avoidable
* For each defect identified, provide a short description of the defect and its potential impact
on the structure
* Also mention the time before this defect leads to premanent damge to the structure. 
* Provide short term and long term solution along with there estimated cost and time to implement.
'''

if st.button('Generate Report'):
    if uploaded_img is None:
        st.error('No image')
    else:
        with st.spinner('Genrating Report...'):
            response = model.generate_content([prompt,image])   
            st.write(response.text) 
        st.download_button(
        label = 'Download Report',
        data = response.text,
        file_name = 'Structural_defect_report.txt',
        mime='text/plain'
        )