# import libraries 
import streamlit as st
import joblib
import numpy as np

# method to load the saved model
def load_model():
    model = joblib.load('notebook/loan_eligibility.pkl')
    return model

# load the model
model = load_model()

# method to predict loan eligibility
def show_predict_page():
    st.markdown("<h1 style='text-align: center;'>Loan Eligibility Prediction</h1>", unsafe_allow_html=True)
    
    # add image
    st.image('images/loan2.jpg', use_column_width=True)
    st.write("""#### Kindly provide the details below to verify your loan eligibility.""")
    
    Gender = ("Male", "Female")
    Married = ("Yes", "No")
    Dependents = ("0", "1", "2", "3")
    Education = ("Graduate", "Not Graduate")
    Self_Employed = ("Yes", "No")
    Property_Area = ("Rural", "Urban", "Semiurban")
    
    gender = st.selectbox("Gender", Gender)
    married = st.selectbox("Married", Married)
    dependents = st.selectbox("Dependants", Dependents)
    education = st.selectbox("Education", Education)
    self_employed = st.selectbox("Employment status", Self_Employed)
    property_area = st.selectbox("Property area", Property_Area)
    loan_amount_term = st.number_input('Loan amount tenure (months)', 1, 60)
    credit_history = st.number_input('Credit history', 0, 1, value=1)
    total_income = st.number_input('Total income', 0, 5000000)
    loan_amount = st.number_input('Loan amount', 0, 5000000)
        
    # action the button to start the prediction
    ok = st.button("Submit")
    if ok:
        # convert property area to number, since models don't accept string 
        if property_area == 'Urban':
            property_area = 0
        if property_area == 'Rural':
            property_area = 2
        if property_area == 'Semiurban':
            property_area = 1

        # convert string features to numeric values
        gender = 0 if gender == 'Male' else 1
        married = 0 if married == 'Yes' else 1
        dependents = int(dependents)
        education = 0 if education == 'Graduate' else 1
        self_employed = 0 if self_employed == 'Yes' else 1
        
        # prepare input features for prediction
        X = np.array([[gender, married, dependents, education, self_employed, 
                       loan_amount, loan_amount_term, credit_history, property_area, total_income]])      
        
        # predict loan eligibility
        loan_eligibility = model.predict(X)
        status = 'eligible' if np.round(loan_eligibility[0]) == 1.0 else 'not eligible'
        st.subheader(f"You are **{status}** for the loan.")

# run the Streamlit app
if __name__ == '__main__':
    show_predict_page()