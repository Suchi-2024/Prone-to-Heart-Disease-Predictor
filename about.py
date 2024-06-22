import streamlit as st

def about():
    # Set page title
    st.title(":orange[About Our Heart Disease Detector]")

    # Add introductory text
    st.write("Welcome to our Heart Disease Detector – Your Pathway to Heart Health Excellence!")

    # Add main content using markdown for styling
    st.markdown("""
    At our website, we are dedicated to transforming the way you think about heart health. We leverage cutting-edge machine learning algorithms to predict the probability of an individual being prone to heart disease. Our platform considers a comprehensive array of factors, including age, gender, chest pain type, resting blood pressure, cholesterol levels, fasting blood sugar, electrocardiographic results, and more, to provide you with a detailed and accurate assessment.

    Our commitment to accuracy and reliability is unwavering. We understand the importance of early detection and intervention in preventing heart disease, which is why our model is meticulously designed and rigorously tested to deliver results you can trust.

    But our mission goes beyond prediction – we aim to empower you with knowledge and insights. By understanding your risk factors, you can take proactive steps towards a heart-healthy lifestyle. Whether you're looking to assess your own risk, support a loved one, or simply curious about the fascinating world of machine learning in healthcare, our website is your gateway to valuable information and resources.

    Join us on this journey to better heart health. Together, we can make a difference – one heartbeat at a time.
    """)

   

    # Add an image or visual element
    st.image("pic.png", caption="Good Health, Good Life", use_column_width=True)

    # Add a contact section with custom CSS
    # Add a contact section with custom CSS
    st.markdown("""
    <div class="contact-section">
        <h2>Let's Connect</h2>
        <form>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" placeholder="Your name..">
            <label for="email">Email-id:</label>
            <input type="text" id="name" name="Email-id" placeholder="Your email-id..">
            <button class="my-button" type="button">Subscribe for News Letter</button>

    </div>
    """, unsafe_allow_html=True)
    # Add custom CSS for styling
    st.markdown("""
    <style>
        /* Contact Form Styles */
        .contact-section {
            background-color: #E2EAF4;
            padding: 20px;
            margin-top: 20px;
            border-radius: 5px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .contact-section h2 {
            color: #333;
        }
        .contact-section form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .contact-section label {
            margin-bottom: 5px;
        }
        .contact-section input[type="text"],
        .contact-section input[type="email"],
        .contact-section textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }
        .contact-section input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .my-button {
            background-color: #7A84FC; /* Green background */
            border: none; /* Remove border */
            color: white; /* White text */
            padding: 15px 32px; /* Padding */
            text-align: center; /* Center text */
            text-decoration: none; /* Remove underline */
            display: inline-block; /* Display as inline block */
            font-size: 16px; /* Font size */
            margin: 4px 2px; /* Margin */
            cursor: pointer; /* Cursor pointer */
            border-radius: 10px; /* Rounded corners */
        }

        /* Change button color on hover */
        .my-button:hover {
            background-color: #272B56;
        }
        /* Responsive Styles */
        @media (max-width: 768px) {
            .contact-section {
                padding: 10px;
            }
            .contact-section h2 {
                font-size: 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)