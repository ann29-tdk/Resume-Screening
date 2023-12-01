# README.md

## main.py

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
import streamlit as st
import pickle
import re
import nltk
import os
import base64
import pandas as pd
```
`streamlit`: A Python library for creating web applications.

`pickle`: Used for serializing and deserializing Python objects.

`re`: Regular expression module for string manipulation.

`nltk`: Natural Language Toolkit for text processing.

`os`: Operating system module for interacting with the operating system.

`base64`: Module for encoding and decoding base64 data.

`pandas`: Library for data manipulation and analysis.
## nltk
Downloads NLTK resources for tokenization and stopwords.

```bash
nltk.download('punkt')
nltk.download('stopwords')

```

## Loading model
Loads machine learning models (clf and tfidfd) using pickle.
```
# Loading models
clf = pickle.load(open('clf.pkl', 'rb'))
tfidfd = pickle.load(open('tfidf.pkl', 'rb'))
```

## clean_resume()
Defines a function clean_resume to preprocess resume text by removing URLs, mentions, special characters, and extra whitespaces.
```
def clean_resume(resume_text):
    clean_text = re.sub('http\S+\s*', ' ', resume_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', '', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

```

## get_resume_link()
Defines a function get_resume_link to create a download link for a resume file.
```
def get_resume_link(uploaded_file):
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode()
    file_link = f'<a href="data:file/txt;base64,{base64_file}" download="{uploaded_file.name}">Download {uploaded_file.name}</a>'
    return file_link

```
## def main()
Sets up the main Streamlit web application, including a title and file upload widget for resumes.
```
def main():
    st.title("Resume Screening App")
    uploaded_files = st.file_uploader('Upload Resumes', type=['txt', 'pdf'], accept_multiple_files=True)

```
## Dictionaries and Dataframes
Initializes dictionaries and a DataFrame for tracking category counts and storing candidate details. Also, defines a mapping of category IDs to category names.
```
    category_counts = {}
    candidate_details = pd.DataFrame(columns=['Candidate Name', 'Category', 'Resume Link'])
    category_mapping = { ... }  # Mapping category IDs to category names

```
## Reading contents of resume
Iterates over uploaded resume files, extracts candidate names, and reads the content of each resume file.
```
    if uploaded_files:
        for uploaded_file in uploaded_files:
            candidate_name = os.path.splitext(uploaded_file.name)[0]
            try:
                resume_bytes = uploaded_file.read()
                resume_text = resume_bytes.decode('utf-8')
            except UnicodeDecodeError:
                resume_text = resume_bytes.decode('latin-1')

```
## Cleaning Resume
Cleans the resume text, transforms it using TF-IDF, and makes a prediction using the loaded machine learning model. Maps the predicted category ID to a category name.
```
                cleaned_resume = clean_resume(resume_text)
                input_features = tfidfd.transform([cleaned_resume])
                prediction_id = clf.predict(input_features)[0]
                category_name = category_mapping.get(prediction_id, "Unknown")

```
## Updates category counts, generates resume links, and appends candidate details to the DataFrame.
```
                if category_name in category_counts:
                    category_counts[category_name] += 1
                else:
                    category_counts[category_name] = 1

                resume_link = get_resume_link(uploaded_file)

                candidate_details = candidate_details.append({
                    'Candidate Name': candidate_name,
                    'Category': category_name,
                    'Resume Link': resume_link,
                }, ignore_index=True)

```
## Displays the category counts and candidate details in the Streamlit web application.
```
        st.write("Category Counts:")
        st.table(category_counts)

        st.write("Candidate Details:")
        st.markdown(candidate_details.to_html(escape=False, index=False), unsafe_allow_html=True)
```
## Executing main function
Executes the main function if the script is run as the main module.
```
if __name__ == "__main__":
    main()

```
## Installation
In the app.py file install
```
pip install streamlit pandas nltk

```
- Run the app.py in your environment
![Running app.py in VS Code](https://i.imgur.com/szpOnd6.png)

- After Running the app.py in VS Code
run the following command in your integrated VS Code terminal
![Streamlit Run Command](https://i.imgur.com/sRfeOzS.png)
- After running this command you will see streamlit application running on your default browser.
![Application](https://i.imgur.com/3Q1O7bB.png) 
