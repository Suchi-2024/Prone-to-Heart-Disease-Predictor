import streamlit as st

def know():
    # Define the medical features and their explanations
    health_data_description = """
    1. **Age**: The age of the person in years.

    2. **Sex**: The gender of the person. Typically represented as 1 for male and 0 for female.

    3. **Chest Pain Type**:
        - **Type 0**: Typical angina (chest pain due to reduced blood flow to the heart)
        - **Type 1**: Atypical angina (chest pain not related to heart)
        - **Type 2**: Non-anginal pain (chest pain not related to the heart or its function)
        - **Type 3**: Asymptomatic (no chest pain)

    4. **Resting Blood Pressure**: The blood pressure of the person while at rest (measured in mm Hg).(measured in mm Hg). (Typical range: 94-200 mm Hg)

    5. **Serum Cholesterol**: The total cholesterol level in the blood (measured in mg/dL).(Typical range: 126-564 mg/dL)

    6. **Fasting Blood Sugar**:
        - **1**: If fasting blood sugar is greater than 120 mg/dL
        - **0**: If fasting blood sugar is less than or equal to 120 mg/dL

    7. **Resting Electrocardiographic Results**:
        - **0**: Normal
        - **1**: Having ST-T wave abnormality (indicates potential issues with heart's electrical activity)
        - **2**: Showing probable or definite left ventricular hypertrophy (enlarged heart muscle)

    8. **Maximum Heart Rate Achieved**: The highest heart rate the person reaches during exercise.(Typical range: 71-202 bpm)

    9. **Exercise Induced Angina**:
        - **1**: Yes, if exercise causes chest pain
        - **0**: No, if exercise does not cause chest pain

    10. **Oldpeak**: ST depression induced by exercise relative to rest (a measurement used to evaluate heart health).(Typical range: 0-6.2)

    11. **Slope of the Peak Exercise ST Segment**:
        - **0**: Upsloping (considered normal)
        - **1**: Flat (could indicate potential heart problems)
        - **2**: Downsloping (more likely to indicate heart problems)

    12. **Number of Major Vessels Colored by Fluoroscopy**: The number of major heart blood vessels (ranging from 0 to 3) visible via fluoroscopy (an imaging technique).

    13. **Thalassemia (Thal)**:
        - **0**: Normal blood flow
        - **1**: Fixed defect (defect in the heart that doesn't change)
        - **2**: Reversible defect (defect in the heart that can improve with treatment)
    """

    # Display the health data description on the Streamlit app
    st.markdown(health_data_description)
