# import streamlit as st
# import pickle
# import re
# import nltk
# import os

# nltk.download('punkt')
# nltk.download('stopwords')

# # Loading models
# clf = pickle.load(open('clf.pkl', 'rb'))
# tfidfd = pickle.load(open('tfidf.pkl', 'rb'))

# def clean_resume(resume_text):
#     clean_text = re.sub('http\S+\s*', ' ', resume_text)
#     clean_text = re.sub('RT|cc', ' ', clean_text)
#     clean_text = re.sub('#\S+', '', clean_text)
#     clean_text = re.sub('@\S+', '  ', clean_text)
#     clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
#     clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
#     clean_text = re.sub('\s+', ' ', clean_text)
#     return clean_text
#     # ... existing cleaning logic ...

# def main():
#     st.title("Resume Screening App")
#     uploaded_files = st.file_uploader('Upload Resumes', type=['txt', 'pdf'], accept_multiple_files=True)

#     # Dictionary to keep track of category counts
#     category_counts = {}

#     # Dictionary to store candidate names and their categories
#     candidate_categories = {}

#     # Map category ID to category name
#     category_mapping = {
#                 15: "Java Developer",
#                 23: "Testing",
#                 8: "DevOps Engineer",
#                 20: "Python Developer",
#                 24: "Web Designing",
#                 12: "HR",
#                 13: "Hadoop",
#                 3: "Blockchain",
#                 10: "ETL Developer",
#                 18: "Operations Manager",
#                 6: "Data Science",
#                 22: "Sales",
#                 16: "Mechanical Engineer",
#                 1: "Arts",
#                 7: "Database",
#                 11: "Electrical Engineering",
#                 14: "Health and fitness",
#                 19: "PMO",
#                 4: "Business Analyst",
#                 9: "DotNet Developer",
#                 2: "Automation Testing",
#                 17: "Network Security Engineer",
#                 21: "SAP Developer",
#                 5: "Civil Engineer",
#                 0: "Advocate",
#     }

#     if uploaded_files:
#         for uploaded_file in uploaded_files:
#             # Extract candidate name from the file name
#             candidate_name = os.path.splitext(uploaded_file.name)[0]

#             try:
#                 resume_bytes = uploaded_file.read()
#                 resume_text = resume_bytes.decode('utf-8')
#             except UnicodeDecodeError:
#                 resume_text = resume_bytes.decode('latin-1')

#             cleaned_resume = clean_resume(resume_text)
#             input_features = tfidfd.transform([cleaned_resume])
#             prediction_id = clf.predict(input_features)[0]

#             category_name = category_mapping.get(prediction_id, "Unknown")

#             # Increment the count for the category
#             if category_name in category_counts:
#                 category_counts[category_name] += 1
#             else:
#                 category_counts[category_name] = 1

#             # Store the candidate's name and their predicted category
#             candidate_categories[candidate_name] = category_name

#         # Display the table with category counts
#         st.write("Category Counts:")
#         st.table(category_counts)

#         # Display the candidate names and their predicted categories
#         st.write("Candidate Names:")
#         st.table(candidate_categories)

# if __name__ == "__main__":
#     main()




















import streamlit as st
import pickle
import re
import nltk
import os
import base64
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')

# Loading models
clf = pickle.load(open('clf.pkl', 'rb'))
tfidfd = pickle.load(open('tfidf.pkl', 'rb'))

def clean_resume(resume_text):
    clean_text = re.sub('http\S+\s*', ' ', resume_text)
    clean_text = re.sub('RT|cc', ' ', clean_text)
    clean_text = re.sub('#\S+', '', clean_text)
    clean_text = re.sub('@\S+', '  ', clean_text)
    clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', r' ', clean_text)
    clean_text = re.sub('\s+', ' ', clean_text)
    return clean_text

def get_resume_link(uploaded_file):
    # Convert the file to a base64 string
    base64_file = base64.b64encode(uploaded_file.getvalue()).decode()
    file_link = f'<a href="data:file/txt;base64,{base64_file}" download="{uploaded_file.name}">Download {uploaded_file.name}</a>'
    return file_link

def main():
    st.title("Resume Screening App")
    uploaded_files = st.file_uploader('Upload Resumes', type=['txt', 'pdf'], accept_multiple_files=True)

    # Dictionary to keep track of category counts
    category_counts = {}

    # DataFrame to store candidate details
    candidate_details = pd.DataFrame(columns=['Candidate Name', 'Category', 'Resume Link'])

    # Map category ID to category name
    category_mapping = {
        15: "Java Developer",
        23: "Testing",
        8: "DevOps Engineer",
        20: "Python Developer",
        24: "Web Designing",
        12: "HR",
        13: "Hadoop",
        3: "Blockchain",
        10: "ETL Developer",
        18: "Operations Manager",
        6: "Data Science",
        22: "Sales",
        16: "Mechanical Engineer",
        1: "Arts",
        7: "Database",
        11: "Electrical Engineering",
        14: "Health and fitness",
        19: "PMO",
        4: "Business Analyst",
        9: "DotNet Developer",
        2: "Automation Testing",
        17: "Network Security Engineer",
        21: "SAP Developer",
        5: "Civil Engineer",
        0: "Advocate",
    }

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Extract candidate name from the file name
            candidate_name = os.path.splitext(uploaded_file.name)[0]

            try:
                resume_bytes = uploaded_file.read()
                resume_text = resume_bytes.decode('utf-8')
            except UnicodeDecodeError:
                resume_text = resume_bytes.decode('latin-1')

            cleaned_resume = clean_resume(resume_text)
            input_features = tfidfd.transform([cleaned_resume])
            prediction_id = clf.predict(input_features)[0]

            category_name = category_mapping.get(prediction_id, "Unknown")

            # Increment the count for the category
            if category_name in category_counts:
                category_counts[category_name] += 1
            else:
                category_counts[category_name] = 1

            # Create and store resume link
            resume_link = get_resume_link(uploaded_file)

            # Append candidate details to DataFrame
            candidate_details = candidate_details._append({
                'Candidate Name': candidate_name,
                'Category': category_name,
                'Resume Link': resume_link,
            }, ignore_index=True)

        # Display the table with category counts
        st.write("Category Counts:")
        st.table(category_counts)

        # Display the candidate details with resume links
        st.write("Candidate Details:")
        st.markdown(candidate_details.to_html(escape=False, index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
