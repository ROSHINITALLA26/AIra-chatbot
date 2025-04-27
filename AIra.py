import time

import PyPDF2
import streamlit as st
import pandas as pd
import json
import google.generativeai as genai
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
st.set_page_config(page_title="AIra - Your Career Assistant", layout="wide", page_icon="assets/favicon.png")
st.markdown("""
    <style>
    /* Background gradient */
    body {
        background: linear-gradient(to right, #f8f9fa, #e0eafc);
        font-family: 'Poppins', sans-serif;
    }

    /* Center main titles */
    h1, h2, h3 {
        text-align: center;
        color: #5c4d7d;
        font-weight: bold;
    }

    /* Sidebar style */
    .css-1d391kg {
        background-color: #f0f4f8 !important;
        border-right: 2px solid #e0e0e0;
    }

    /* Buttons style */
    button {
        background-color: #6C63FF !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold;
    }
    button:hover {
        background-color: #4c45b3 !important;
        transition: 0.3s ease-in-out;
    }

    /* Chat messages style */
    .chat-message {
        padding: 12px 20px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 70%;
        font-size: 16px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #c8e6c9;
        margin-left: auto;
        margin-right: 0;
    }
    .aira-message {
        background-color: #e6e6fa;
        margin-left: 0;
        margin-right: auto;
    }

    /* Text input placeholder styling */
    input::placeholder, textarea::placeholder {
        color: #a6a6a6 !important;
        font-style: italic;
    }

    /* Divider lines */
    hr {
        border: 1px solid #ccc;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# API Key Setup (Replace with your GEMINI API Key)
API_KEY = "AIzaSyDrXpYTmQc4BbQBtV5pQQRfFYGATibeGL0"
if not API_KEY:
    st.error("API Key not found. Please set your API key.")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load Data
jobs_df = pd.read_csv("sample_jobs.csv")
with open("sample_sessions.json", "r") as f:
    sessions_data = json.load(f)

# Session State for Conversation Memory
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def query_llm(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def detect_bias(user_input):
    bias_words = ["weak", "emotional", "fragile", "female jobs", "can't"]
    if any(word in user_input.lower() for word in bias_words):
        return True
    return False

def respond(user_input):
    if detect_bias(user_input):
        return "🚫 AIra promotes inclusivity and positivity. Let's focus on empowering conversations!"
    else:
        full_context = "\n".join([f"User: {u}\nAIra: {a}" for u,a in st.session_state.conversation])
        full_prompt = full_context + f"\nUser: {user_input}\nAIra:"
        return query_llm(full_prompt)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.image('assets/asha_logo.png', width=150)
    st.title("Welcome to AIra")
    st.markdown("""
    **Your AI-Powered Career Companion**
    - Profile Page
    - Find Jobs
    - Explore Events
    - Discover Mentorships
    - Chat for Career Guidance
    - Resume Analyzer

    Built ethically for empowering women careers 
    """)
    st.markdown("---")
    page = st.radio("Navigate", ["Home","Profile Page", "Job Listings", "Events & Mentorships", "Chat with AIra","Resume Analyzer","Helpline Numbers", "Support Forum", "Skill Courses", "Career Stories", "Mental Wellness"])

# -----------------------------
# MAIN CONTENT
# -----------------------------



if page == "Home":
    st.markdown("""
    <div style='background-color: #fceff9; padding: 50px; border-radius: 15px; text-align: center; box-shadow: 2px 2px 15px rgba(0,0,0,0.1);'>

    <h1 style='color: #6C63FF; font-size: 50px;'>🌟 Welcome to AIra!</h1>
    <h3 style='color: #555; font-weight: normal;'>Your Personal Career Empowerment Partner </h3>

    <br><br>

    <a href="#start_section">
    <button style='background-color: #6C63FF; color: white; padding: 15px 30px; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer;'> Get Started</button>
    </a>

    <br><br><br>

    <h4 style='color: #777; font-style: italic;'>"Empowered women empower the world."</h4>

    </div>
    """, unsafe_allow_html=True)

    # A hidden anchor link for scrolling
    st.markdown("<div id='start_section'></div>", unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("✨ What Can AIra Help You With?")
    st.markdown("""
    - 💼 Explore women-centric job opportunities
    - 📚 Upskill with free courses and certifications
    - 🫂 Share and discuss challenges anonymously
    - 📞 Access women's safety helplines
    - 💬 Chat with an AI career assistant 24x7
    - 📄 Analyze and upgrade your resume
    """)


elif page == "Job Listings":
    st.title("💼 Explore Job Opportunities")
    for idx, row in jobs_df.iterrows():
        st.markdown(f"### {row['Job Title']}")
        st.write(row['Description'])
        st.markdown(f"[Apply Here]({row['Link']})", unsafe_allow_html=True)
        st.markdown("---")

elif page == "Events & Mentorships":
    st.title("📅 Community Events & Mentorships")
    for event in sessions_data['events']:
        st.markdown(f"### {event['title']}")
        st.write(event['description'])
        if event.get('link'):
            st.markdown(f"[Know More]({event['link']})", unsafe_allow_html=True)
        st.markdown("---")

elif page == "Chat with AIra":
    import speech_recognition as sr
    from gtts import gTTS
    import base64
    import os

    # Title Section (without the box)
    st.markdown(
        """
        <style>
        /* Remove the default box and padding from the header */
        .streamlit-expanderHeader {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("🗪 Chat with AIra - Your Career Assistant")

    # Initialize Chat History
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Functions
    def query_llm_with_context(user_message):
        full_context = "\n".join([f"User: {u}\nAIra: {a}" for u, a in st.session_state.chat_history])
        prompt = f"{full_context}\nUser: {user_message}\nAIra:"
        ai_message = query_llm(prompt)
        return ai_message

    def speech_to_text():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎙️ Listening...")
            audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except Exception:
            return "Sorry, couldn't recognize your voice."

    def text_to_speech(text):
        tts = gTTS(text=text, lang="en")
        tts.save("aira_response.mp3")
        audio_file = open("aira_response.mp3", "rb")
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio autoplay controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        """
        return audio_html

    # Layout
    st.markdown(
        """
        <style>
        .chat-message {
            padding: 12px 20px;
            border-radius: 20px;
            margin-bottom: 10px;
            max-width: 70%;
            font-size: 16px;
            box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
        }
        .user-message {
            background-color: #c8e6c9;
            margin-left: auto;
            margin-right: 0;
        }
        .aira-message {
           background-color: #f0f0f0;
           margin-left: 0;
           margin-right: auto;
        }

        .chat-container {
            display: flex;
            flex-direction: column;
            height: 500px;
            overflow-y: scroll;
            border: 1px solid #ccc;
            padding: 15px;
            border-radius: 10px;
            background-color: #ffffff;
            margin-top: 10px;  /* Added to avoid large gap */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Chat Area

    for idx, (user_text, ai_text) in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(
            f'<div class="chat-message user-message"> 🐼 <strong>You:</strong> {user_text}</div>',
            unsafe_allow_html=True
        )

        # AIra message
        st.markdown(
            f'<div class="chat-message aira-message"> ☯ <strong>AIra:</strong> {ai_text}</div>',
            unsafe_allow_html=True
        )

        # Copy and Edit Options
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button(f"🗐 Copy", key=f"copy_{idx}"):
                st.session_state.to_copy = ai_text
                st.success("Copied to clipboard! (Use Ctrl+V to paste)")

        with col2:
            if st.button(f"🖊 Edit & Resend", key=f"edit_{idx}"):
                st.session_state.edit_text = user_text
                st.session_state.edit_mode = True
    st.markdown('</div>', unsafe_allow_html=True)

    # User Input
    if "edit_mode" in st.session_state and st.session_state.edit_mode:
        user_input = st.text_input("🖊 Edit your message and resend:", value=st.session_state.edit_text, key="edit_input")
        if st.button("Resend"):
            ai_response = query_llm_with_context(user_input)
            st.session_state.chat_history.append((user_input, ai_response))
            st.session_state.edit_mode = False
            st.rerun()
    else:
        col1, col2 = st.columns([7, 1])
        with col1:
            user_input = st.text_input("💭 Your message:", placeholder="Type a message...", key="text_input")
        with col2:
            if st.button("🎙️"):
                voice_text = speech_to_text()
                if voice_text:
                    user_input = voice_text
                    st.success(f"🗣 ️You said: {voice_text}")

        if st.button("╰┈➤Send") and user_input:
            if detect_bias(user_input):
                ai_response = "🚫 AIra promotes inclusivity and positive conversations. Please reframe your message!"
            else:
                ai_response = query_llm_with_context(user_input)
            st.session_state.chat_history.append((user_input, ai_response))
            st.rerun()

    # Scroll to bottom automatically
    st.markdown(
        """
        <script>
        var chatContainer = window.parent.document.querySelector('.chat-container');
        if(chatContainer){
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        </script>
        """,
        unsafe_allow_html=True
    )

elif page == "Resume Analyzer":
    st.title("📄 AI-Powered Resume Analyzer")
    st.markdown("""
    Get detailed feedback on your resume including:
    - Structure analysis
    - Missing skills identification
    - Improvement suggestions
    - Overall quality rating
    """)

    # Upload resume
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from PDF
        def extract_text_from_pdf(uploaded_file):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text


        resume_text = extract_text_from_pdf(uploaded_file)

        # Display extracted text
        with st.expander("View Extracted Resume Text"):
            st.text_area("Resume Content", resume_text, height=300)

        # Analysis options
        analysis_option = st.radio("Choose analysis type:",
                                   ["Quick Scan", "Detailed Analysis", "Career Path Suggestions"])

        if st.button("Analyze Resume"):
            with st.spinner("Analyzing your resume..."):
                if analysis_option == "Quick Scan":
                    prompt = f"""Quickly analyze this resume and provide:
                    1. 3 strengths
                    2. 3 areas for improvement
                    3. Overall rating (1-5 stars)
                    Resume: {resume_text}"""
                elif analysis_option == "Detailed Analysis":
                    prompt = f"""Comprehensively analyze this resume and provide:
                    1. Structure evaluation
                    2. Missing key skills
                    3. Content quality assessment
                    4. Formatting suggestions
                    Resume: {resume_text}"""
                else:
                    prompt = f"""Suggest career paths based on this resume:
                    1. Top 3 suitable roles
                    2. Skills to develop for each
                    3. Salary expectations
                    4. Growth potential
                    Resume: {resume_text}"""

                try:
                    response = model.generate_content(prompt)
                    st.subheader("Analysis Results")
                    st.markdown(response.text)

                    # Add interactive features
                    col1, col2 = st.columns(2)
                    with col1:
                        import gTTS
                        if st.button("🔊 Read Analysis Aloud"):
                            tts = gTTS(text=response.text, lang='en')
                            tts.save("analysis.mp3")
                            audio_file = open("analysis.mp3", "rb")
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/mp3')

                    with col2:
                        st.download_button(
                            label="📥 Download Analysis",
                            data=response.text,
                            file_name="resume_analysis.txt",
                            mime="text/plain"
                        )

                    # Skill matching with job listings
                    st.subheader("🔍 Skills Match with Job Listings")
                    skills_prompt = f"""Extract the top 5 technical skills from this resume: {resume_text}"""
                    skills_response = model.generate_content(skills_prompt)
                    extracted_skills = [skill.strip() for skill in skills_response.text.split('\n') if skill.strip()]

                    if extracted_skills:
                        st.write("Detected Skills:", ", ".join(extracted_skills))
                        matching_jobs = []
                        for idx, row in jobs_df.iterrows():
                            if any(skill.lower() in row['Description'].lower() for skill in extracted_skills):
                                matching_jobs.append(row)

                        if matching_jobs:
                            st.write("Matching Job Opportunities:")
                            for job in matching_jobs[:3]:  # Show top 3 matches
                                st.markdown(f"""
                                **{job['Job Title']}**  
                                {job['Description'][:150]}...  
                                [Apply Here]({job['Link']})
                                """)
                        else:
                            st.info("No exact matches found, but check out similar roles:")
                            for idx, row in jobs_df.sample(3).iterrows():
                                st.markdown(f"""
                                **{row['Job Title']}**  
                                {row['Description'][:150]}...  
                                [Apply Here]({row['Link']})
                                """)
                except Exception as e:
                    st.error(f"Error analyzing resume: {str(e)}")
        st.success("✅ Successfully submitted!")
        time.sleep(1)
        st.balloons()
        # Add learning resources section
        st.markdown("---")
        st.subheader("🎯 Improve Your Resume")
        if st.button("Get Personalized Learning Resources"):
            with st.spinner("Finding resources to enhance your resume..."):
                learning_prompt = f"""Based on this resume: {resume_text[:2000]}...
                Suggest 3 free online resources (courses, articles, videos) to improve it"""
                try:
                    learning_response = model.generate_content(learning_prompt)
                    st.markdown(learning_response.text)
                except Exception as e:
                    st.error(f"Error finding resources: {str(e)}")
    else:
        st.info("Please upload a PDF resume to get started")
        
elif page == "Profile Page":
    st.title("👩‍💼 My Profile")

    if "profile" not in st.session_state:
        st.session_state.profile = {
            "Name": "",
            "Email": "",
            "Phone": "",
            "Skills": [],
            "Career Goals": ""
        }

    st.subheader("📝 Update Your Profile")
    st.session_state.profile["Name"] = st.text_input("Full Name", st.session_state.profile["Name"])
    st.session_state.profile["Email"] = st.text_input("Email", st.session_state.profile["Email"])
    st.session_state.profile["Phone"] = st.text_input("Phone Number", st.session_state.profile["Phone"])
    st.session_state.profile["Skills"] = st.text_input("Skills (comma separated)",
                                                       ", ".join(st.session_state.profile["Skills"])).split(",")
    st.session_state.profile["Career Goals"] = st.text_area("Career Goals", st.session_state.profile["Career Goals"])

    if st.button("Save Profile"):
        st.success("✅ Profile Saved Successfully!")
        time.sleep(1)
        st.balloons()
    st.subheader("👀 Preview")
    st.write(st.session_state.profile)

elif page == "Helpline Numbers":
    st.title("📞 Women Helpline Numbers")

    st.markdown("""
    Here are important national helpline numbers for women safety, emergencies, and mental health support:

    - **📞 181 - Women Helpline (All India)**
    - **📞 112 - Emergency Number (Police, Ambulance, Fire)**
    - **📞 1091 - Women Police Helpline**
    - **📞 1098 - Child Helpline**
    - **📞 1075 - COVID-19 Helpline**
    - **📞 9152987821 - NCW WhatsApp Helpdesk (for complaints)**

    **Mental Health Support:**
    - **📞 9152987820 - iCall Psychosocial Helpline**
    - **📞 1800-599-0019 - Fortis Mental Health Helpline**

    > Your safety and well-being matters. Please don't hesitate to reach out if you need support. 💛
    """, unsafe_allow_html=True)

    st.success("Tap the numbers if you're on mobile to call directly.")

elif page == "Support Forum":
    st.title("🫂 Anonymous Women's Support Forum")

    st.markdown("""
    Share your problems anonymously and get support, advice, and encouragement from other women.  
    Let's lift each other up! 💪💖
    """)

    if "support_posts" not in st.session_state:
        st.session_state.support_posts = []

    st.subheader("💬 Share Your Problem Anonymously")
    problem_text = st.text_area("Describe your situation (don't mention personal details)...")

    if st.button("Post Anonymously"):
        if problem_text.strip() != "":
            st.session_state.support_posts.append({"problem": problem_text, "responses": []})
            st.success("✅ Your problem has been posted anonymously!")

    st.markdown("---")
    st.subheader("🫶 Community Support")

    if st.session_state.support_posts:
        for idx, post in enumerate(st.session_state.support_posts):
            st.markdown(f"**Anonymous User #{idx+1}:** {post['problem']}")
            if post['responses']:
                for response in post['responses']:
                    st.markdown(f"- 🧡 {response}")
            response_input = st.text_input(f"Support Message for Post {idx+1}", key=f"response_input_{idx}")
            if st.button(f"Send Support for Post {idx+1}", key=f"response_button_{idx}"):
                if response_input.strip() != "":
                    post['responses'].append(response_input)
                    st.success("✅ Support message added!")
    else:
        st.info("No problems shared yet. Be the first to support someone! 💬")

elif page == "Skill Courses":
    st.title("📚 Skill Development Opportunities for Women")
    st.markdown("""
    Upgrade your career by learning new skills! Here are free or affordable online courses:
    - [Python for Everybody - Coursera](https://www.coursera.org/specializations/python)
    - [Google Project Management Certificate](https://grow.google/certificates/project-management/)
    - [Data Science Free Course - Kaggle](https://www.kaggle.com/learn/overview)
    - [AI for Everyone - Andrew Ng](https://www.coursera.org/learn/ai-for-everyone)
    - [Communication Skills - edX](https://www.edx.org/course/essential-communication-skills)
    - [Leadership for Women - FutureLearn](https://www.futurelearn.com/courses/leadership-for-women)

    > 📢 We recommend taking at least 1 course every 2-3 months to stay ahead!
    """, unsafe_allow_html=True)

elif page == "Career Stories":
    st.title("🌟 Inspirational Career Stories")

    st.markdown("""
    > **Real Women. Real Journeys. Real Inspiration.**

    **1. Aditi's Journey from Homemaker to Software Engineer**
    - After a career gap of 8 years, Aditi started learning coding through online courses. Today, she works at a top IT company!

    **2. Meera's Leap into Entrepreneurship**
    - Meera left a stable job to follow her passion in eco-friendly startups. She now runs a successful business with 50+ employees.

    **3. Sneha's Story: Breaking Stereotypes in Mechanical Engineering**
    - Being the only woman in her class, Sneha pushed through and now works on futuristic automotive designs!

    _"Your story could be the next one inspiring someone!"_ 💬
    """, unsafe_allow_html=True)


elif page == "Mental Wellness":
    st.title("🧠 Mental Wellness Resources")

    st.markdown("""
    > **Career growth matters. Your mental health matters more.**

    **Helplines:**
    - 📞 *iCall Mental Health Helpline*: 9152987820
    - 📞 *Fortis 24x7 Mental Health Support*: 1800-599-0019

    **Articles:**
    - [Managing Stress at Work - WHO Guide](https://www.who.int/occupational_health/topics/stressatwp/en/)
    - [Overcoming Imposter Syndrome](https://hbr.org/2021/02/stop-telling-women-they-have-imposter-syndrome)

    **Apps for Mindfulness:**
    - [Headspace](https://www.headspace.com/)
    - [Calm](https://www.calm.com/)
    - [Insight Timer](https://insighttimer.com/)

    > 🌟 _Strong minds build strong futures._  
    > It's okay to ask for help. It’s okay to take a break.
    """, unsafe_allow_html=True)

#-------------
st.markdown("""
---
<p style='text-align: center; font-size: 14px;'>
Made with ❤️ by Team AIra | Empowering Careers One Step at a Time
</p>
""", unsafe_allow_html=True)
