import math
import re
import PyPDF2
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from ai.models import vectorizer, ranking_model, summarizer, tfidf_vectorizer, classifier

nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

def extract_contact_info(text):
    phone_pattern = re.compile(r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')
    email_pattern = re.compile(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$')

    phone_numbers = phone_pattern.findall(text)
    emails = email_pattern.findall(text)

    doc = nlp(text)
    full_names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']

    phone_numbers = [''.join(number).strip() for number in phone_numbers]

    phone_number = phone_numbers[0] if phone_numbers else None
    email = emails[0] if emails else None
    full_name = full_names[0] if full_names else None

    return full_name, phone_number, email

def get_summary(resume_text):
    tokenized_input = summarizer.tokenizer(resume_text, truncation=True, return_tensors="pt")
    resume_input_length = len(tokenized_input['input_ids'][0])

    if resume_input_length > 1024:
        resume_text = resume_text[:1024]
        resume_input_length = 1024

    max_length = min(math.floor(0.5 * resume_input_length), 512)
    min_length = min(math.floor(0.2 * resume_input_length), 128)

    summary = summarizer(
        resume_text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]['summary_text']

    return summary

def predict_category(resume_text):
    X_new = tfidf_vectorizer.transform([resume_text])
    return classifier.predict(X_new)[0]

def extract_data(resume_file, job_description):
    resume_text = extract_text_from_pdf(resume_file)
    
    full_name, phone_number, email = extract_contact_info(resume_text)

    summary = get_summary(resume_text)

    category = predict_category(resume_text)
    
    cleaned_resume = clean_text(resume_text)
    cleaned_job_desc = clean_text(job_description)

    vectorized_resume = vectorizer([cleaned_resume])
    vectorized_job_desc = vectorizer([cleaned_job_desc])

    prediction = ranking_model.predict([vectorized_resume, vectorized_job_desc])
    good_fit_probablility = max(0, prediction[0, 2] - prediction[0, 0])
    
    return good_fit_probablility, summary, category, full_name, phone_number, email