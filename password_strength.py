
# Advance password generator and checker 

# --- Required Libraries Import ---
import streamlit as st  # Streamlit is used for building the web app interface
import re, random, string, math, requests  # These are useful libraries for various utilities
from streamlit_lottie import st_lottie  # This helps to add Lottie animations to the app
from fpdf import FPDF  # This library is used for generating PDFs
from datetime import datetime  # For working with date and time

# --- Web Page Setup ---
# This sets up the page's title, icon, and layout. We choose centered layout here.
st.set_page_config(page_title="🔐 Password Power Tool", page_icon="🔐", layout="centered")

# --- Session State Initialization ---
# This initializes session state for storing history and controlling intro animation.
if 'history' not in st.session_state: 
    st.session_state.history = []  # Create an empty list for history if it doesn't exist
if 'show_intro' not in st.session_state: 
    st.session_state.show_intro = True  # Show intro animation once

# --- Load Lottie Animations ---
# Function to load Lottie animations from the URL
def load_lottie(url):
    r = requests.get(url)  # Fetch the animation data
    return r.json() if r.status_code == 200 else None  # Return JSON data if successful

# URLs for the intro and action animations
lottie_intro = load_lottie("https://assets10.lottiefiles.com/packages/lf20_ydo1amjm.json")
lottie_action = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jtbfg2nb.json")
lottie_lock = load_lottie("https://assets2.lottiefiles.com/packages/lf20_7wkc7spn.json")

# --- Intro Animation ---
# Display the intro animation once when the app is first loaded
if st.session_state.show_intro:
    if lottie_intro:
        # Display a welcome message and animation
        st.markdown("<h2 style='text-align:center;'>Welcome to Password Power Tool 🛡️</h2>", unsafe_allow_html=True)
        st_lottie(lottie_intro, height=250, key="intro_strength")  # Show intro animation
        st.toast("🔐 Welcome! Let's secure your digital world.", icon="🤖")  # Show a toast notification
    st.session_state.show_intro = False  # Set to False so intro doesn't show again

# --- Title & Description ---
# Display the app title and a brief description
st.markdown("<h1 style='text-align: center;'>🔐 Password Power Tool</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>🧠 Generate strong passwords & analyze their strength!</div>", unsafe_allow_html=True)
st.divider()  # Add a divider line for a clean layout

# --- Lock Animation ---
# Show a lock animation below the title
if lottie_lock:
    st_lottie(lottie_lock, height=200, key="lock_anim")

# --- Password Generator Section ---
# Display the password generator section with options
st.subheader('🛠️ Password Generator')

# Slider to choose password length between 8 and 32 characters
length = st.slider('🔢 Length', 8, 32, 12)
# Checkboxes to choose whether to include uppercase, lowercase, numbers, and symbols
upper = st.checkbox('🔠 Uppercase (A-Z)', True)
lower = st.checkbox('🔡 Lowercase (a-z)', True)
numbers = st.checkbox('🔢 Numbers (0-9)', True)
symbols = st.checkbox('🔣 Symbols (!@#$%^&*)', True)

# Button to generate a password
if st.button('✨ Generate Password'):
    chars = ''  # Initialize an empty string for characters that will form the password
    # Add characters based on the selected options
    if upper: chars += string.ascii_uppercase
    if lower: chars += string.ascii_lowercase
    if numbers: chars += string.digits
    if symbols: chars += '!@#$%^&*()_+'

    # Generate a random password of selected length
    new_pw = ''.join(random.choices(chars, k=length)) if chars else ''
    # Store the generated password and add it to the history
    st.session_state.generated_password = new_pw
    st.session_state.history.append(f'🔧 Generated: {new_pw}')

    # Display action animation and success message
    if lottie_action: 
        st_lottie(lottie_action, height=120, key='gen_anim')
        st.success('✅ Password Generated!')  # Success message
        st.toast("🎉 Great! A strong password is created.", icon="🔒")  # Toast notification
        st.balloons()  # Display balloons for fun

# Display the generated password (readonly)
if 'generated_password' in st.session_state:
    st.text_input('🔑 Your Password', value=st.session_state.generated_password, disabled=True)

st.divider()  # Divider for visual separation

# --- Password Strength Analyzer Section ---
# Section to analyze password strength
st.subheader('🔍 Password Analyzer')

# Input for user to enter a password for analysis
user_pw = st.text_input('🔎 Enter Password to Analyze', type='password')

# Button to check the strength of the entered password
if st.button('🚀 Check Strength'):
    score = 0  # Initialize score to 0
    # Calculate password strength based on different criteria
    length_val = len(user_pw)
    has_upper = bool(re.search(r'[A-Z]', user_pw))
    has_lower = bool(re.search(r'[a-z]', user_pw))
    has_digit = bool(re.search(r'\d', user_pw))
    has_symbol = bool(re.search(r'[!@#$%^&*()_+]', user_pw))

    # Update score based on password strength
    score += length_val >= 8
    score += has_upper and has_lower
    score += has_digit
    score += has_symbol

    # Log the checked password and its strength in history
    st.session_state.history.append(f'🚀 Checked: {user_pw} - Strength: {score}/4')

    # Display action animation and toast notification
    if lottie_action:
        st_lottie(lottie_action, height=120, key='check_anim')
        st.toast("🧪 Analysis complete!", icon="📊")  # Toast message
        st.snow()  # Snow effect for fun

    # Display password strength in color and progress bar
    colors = ['red','red','orange','yellowgreen','green']
    st.markdown(f"<div style='background:{colors[score]};padding:10px;border-radius:5px;text-align:center;'>💪 Strength: {score}/4</div>", unsafe_allow_html=True)
    st.progress(score/4)  # Show a progress bar

    # Display suggestions based on password weaknesses
    tips = []
    if length_val < 8: tips.append('📏 Use at least 8 characters')
    if not (has_upper and has_lower): tips.append('🔠 Mix upper and lower case')
    if not has_digit: tips.append('🔢 Add some numbers')
    if not has_symbol: tips.append('🔣 Include special characters')

    # Show tips if any weaknesses are found
    if tips:
        st.markdown('**📝 Suggestions:**')
        for tip in tips: 
            st.warning(tip)

    # --- AI-Based Password Suggestions ---
    if score < 4:
        st.markdown('**🤖 AI-Based Suggestions:**')
        ai_suggestion = ""

        if length_val < 8:
            ai_suggestion += "Use a longer password, "
        if not (has_upper and has_lower):
            ai_suggestion += "mix uppercase and lowercase, "
        if not has_digit:
            ai_suggestion += "include some digits, "
        if not has_symbol:
            ai_suggestion += "and add special symbols like !@#$. "

        ai_suggestion = ai_suggestion.rstrip(', ') + "."  # Clean the suggestion string
        st.info(f"💡 Try something like: `{user_pw + 'A1!'}`\n\n{ai_suggestion}")

st.divider()  # Divider for visual separation

# --- Activity History & PDF Export Section ---
# Display the activity history (last 5 entries)
st.subheader('📚 Activity History & Report')

for entry in st.session_state.history[-5:]:
    st.code(entry)

# Generate a PDF report of the activity history
if st.session_state.history:
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=14)
        pdf.cell(0, 10, 'Password Power Tool Report', ln=1, align='C')
        pdf.set_font('Arial', size=10)
        pdf.cell(0, 8, datetime.now().strftime('%Y-%m-%d %H:%M'), ln=1, align='C')
        pdf.ln(4)

        # Clean the text to remove non-ASCII characters like emojis
        def clean_text(text):
            return ''.join(c for c in text if ord(c) < 128)

        for rec in st.session_state.history[-5:]:
            cleaned = clean_text(rec)
            pdf.cell(0, 6, txt=cleaned, ln=1)

        return pdf.output(dest='S').encode('latin-1')

    # Generate PDF and allow the user to download it
    pdf_bytes = create_pdf()
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_bytes,
        file_name="password_power_report.pdf",
        mime="application/pdf"
    )

# --- Clear History Button ---
# Button to clear the activity history
if st.button('🧹 Clear History'):
    st.session_state.history.clear()  # Clear the history
    st.success('🧽 History cleared!')

# --- Footer ---
# Footer to display information about the creator and technologies used
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 16px;'>"
    "Made with ❤️ by <b>MUHAMMAD HAMMAD ZUBAIR</b> 👨‍💻<br>"
    "Powered by <span style='color: #FF4B4B;'>Python</span> 🐍 & <span style='color: #4F8BF9;'>Streamlit</span>"
    "</div>",
    unsafe_allow_html=True
)



# # Basic password strength checker app using Streamlit
# import streamlit as st
# import re

# # Page config
# st.set_page_config(page_title="Password Strength Checker App", page_icon="🔒")

# # Title & Description
# st.title("🔐 Password Strength Checker")
# st.markdown("""
# ## Welcome to the Ultimate Password Strength Checker! 👋🏻  
# This app helps you create passwords that are **hard to crack** 🔐 and **easy to remember** 🧠.  
# Let's make your online life safer! 🚀
# """)

# # User input
# password = st.text_input("🔑 Enter your password:", type="password")
# password_strength = st.empty()

# feedback = []
# score = 0

# if password:
#     # Password Length
#     if len(password) >= 8:
#         score += 1
#     else:
#         feedback.append("❌ Password should be **at least 8 characters** long. 📏")

#     # Upper and Lowercase letters
#     if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
#         score += 1
#     else:
#         feedback.append("❌ Use **both uppercase and lowercase letters**. 🔠")

#     # Numbers
#     if re.search(r'\d', password):
#         score += 1
#     else:
#         feedback.append("❌ Include **at least one number**. 🔢")

#     # Special Characters
#     if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
#         score += 1
#     else:
#         feedback.append("❌ Add **special characters** like !@#$% for extra security. 💥")

#     # Strength Result
#     st.markdown("### 🔍 Password Strength Result:")
#     if score == 4:
#         st.success("✅ Your password is **strong**! 💪 Great job!")
#     elif score == 3:
#         st.warning("⚠️ Your password is **medium**. Add more variety to make it stronger! 🔧")
#     elif score == 2:
#         st.warning("⚠️ Your password is **weak**. Consider adding numbers, special characters, and using upper/lowercase. 🛠️")
#     else:
#         st.error("❌ Your password is **very weak**! Please improve it. 🚫")

#     # Show suggestions
#     if feedback:
#         st.markdown("### 🛡️ Suggestions to Improve:")
#         for tip in feedback:
#             st.markdown(f"- {tip}")

# else:
#     st.info("💡 Please enter a password to check its strength.")
