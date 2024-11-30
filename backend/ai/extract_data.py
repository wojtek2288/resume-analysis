import math
import re
import PyPDF2
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from ai.models import vectorizer, ranking_model, summarizer, tfidf_vectorizer, classifier, classifier_label_encoder
import xgboost as xgb
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load('en_core_web_lg')
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
    phone_pattern = re.compile(r'(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,4}\)?[\s\-]?)?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4}(?=\s|$)')
    email_pattern = re.compile(r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])')

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

    y_pred_probs = classifier.predict(xgb.DMatrix(X_new))
    predicted_class_index = np.argmax(y_pred_probs, axis=1)[0]
    predicted_category = classifier_label_encoder.inverse_transform([predicted_class_index])[0]

    return predicted_category

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
    good_fit_probablility = max(0, prediction[0, 0] - prediction[0, 1])
    print(prediction)

    score = (
        (prediction[0, 0] * 1.0) +  # good fit  
        (prediction[0, 1] * -1.0) + # no fit
        (prediction[0, 2] * 0.7)    # potencial fit
    )
    
    score = max(0, min(1, score))

    return score, summary, category, full_name, phone_number, email
