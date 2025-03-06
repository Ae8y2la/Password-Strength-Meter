import streamlit as st
import re
import random
import string

# Custom CSS for simple and clean styling
st.markdown("""
<style>
    /* Background */
    .stApp {
        background: #E5C5C1;
        color: #260101;
        font-family: 'Arial', sans-serif;
    }

    /* Card-like design for input and results */
    .card {
        background: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Simple input field */
    .stTextInput input {
        background: #ffffff;
        color: #333333;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        width: 100%;
    }

    /* Simple buttons */
    .stButton button {
        background: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: background 0.3s ease;
    }
    .stButton button:hover {
        background: #45a049;
    }

    /* Simple progress bar */
    .stProgress > div > div > div {
        background: #4CAF50;
        border-radius: 8px;
    }

    /* Simple checkbox */
    .stCheckbox label {
        font-size: 16px;
        color: #333333;
    }

    /* Simple success, warning, and error messages */
    .stSuccess {
        color: #4CAF50;
    }
    .stWarning {
        color: #FFA500;
    }
    .stError {
        color: #FF0000;
    }

    /* Simple headings */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #333333;
    }

    /* Simple slider */
    .stSlider .css-1cpxqw2 {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Function to check password strength
def check_password_strength(password):
    # Criteria for password strength
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    digit_criteria = re.search(r'[0-9]', password) is not None
    special_char_criteria = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    # Calculate strength score
    strength_score = 0
    if length_criteria:
        strength_score += 1
    if uppercase_criteria:
        strength_score += 1
    if lowercase_criteria:
        strength_score += 1
    if digit_criteria:
        strength_score += 1
    if special_char_criteria:
        strength_score += 1

    return strength_score

# Function to generate a strong password
def generate_password(length=12, include_symbols=True, include_numbers=True):
    characters = string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Main App
def main():
    st.title("Password Strength Meter 🔒")
    st.markdown("Check your password strength and generate strong passwords easily.")

    # Toggle for dark/light mode
    dark_mode = st.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown("""
        <style>
            .stApp {
                background: #1e1e1e;
                color: #ffffff;
            }
            .card {
                background: #2d2d2d;
                color: #ffffff;
            }
            .stTextInput input {
                background: #2d2d2d;
                color: #ffffff;
            }
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #ffffff;
            }
        </style>
        """, unsafe_allow_html=True)

    # Password input field with toggle to show/hide password
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        password = st.text_input("Enter your password:", type="password", placeholder="Type your password here...")
        show_password = st.checkbox("👁️ Show Password")
        if show_password:
            st.write(f"Your password is: **{password}**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Password strength analysis
    if password:
        strength_score = check_password_strength(password)
        strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
        strength_level = strength_levels[min(strength_score, len(strength_levels) - 1)]  # Cap the score

        # Display strength level
        st.subheader(f"Password Strength: **{strength_level}** {['😟', '😕', '😐', '😊', '😎'][strength_score]}")

        # Progress bar
        progress_value = (strength_score + 1) / len(strength_levels)
        st.progress(progress_value)

        # Display feedback based on strength
        if strength_score == 0:
            st.error("🚨 Your password is very weak. Consider using a longer password with a mix of characters.")
        elif strength_score == 1:
            st.warning("⚠️ Your password is weak. Add more complexity (e.g., uppercase letters, numbers, or special characters).")
        elif strength_score == 2:
            st.warning("⚠️ Your password is medium. Consider adding more complexity to make it stronger.")
        elif strength_score == 3:
            st.success("✅ Your password is strong. Good job!")
        elif strength_score == 4:
            st.success("✅ Your password is very strong. Excellent!")

        # Detailed strength analysis
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### Detailed Analysis:")
            st.markdown(f"""
            - Length: {"✅" if len(password) >= 8 else "❌"} (Minimum 8 characters)
            - Uppercase Letters: {"✅" if re.search(r'[A-Z]', password) else "❌"}
            - Lowercase Letters: {"✅" if re.search(r'[a-z]', password) else "❌"}
            - Numbers: {"✅" if re.search(r'[0-9]', password) else "❌"}
            - Special Characters: {"✅" if re.search(r'[!@#$%^&*(),.?":{}|<>]', password) else "❌"}
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # Password generator
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔑 Generate a Strong Password")
        password_length = st.slider("Password Length", min_value=8, max_value=32, value=12)
        include_symbols = st.checkbox("Include Symbols", value=True)
        include_numbers = st.checkbox("Include Numbers", value=True)
        if st.button("Generate Password"):
            with st.spinner("Generating your password..."):
                generated_password = generate_password(password_length, include_symbols, include_numbers)
                st.success(f"Your generated password is: **{generated_password}**")
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Aeyla Naseer. All rights reserved!")

# Run the app
if __name__ == "__main__":
    main()