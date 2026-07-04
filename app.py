import streamlit as st
from google import genai

# 1. Muuqaalka Bogga Website-ka
st.set_page_config(page_title="Umal Personal AI", page_icon="🤖")

# 2. API Key-gaaga
API_KEY = "AQ.Ab8RN6L3loz555RnYqO3UkWK-kEYu4EsGsuYDYtVZFmS5SaLyQ" 
client = genai.Client(api_key=API_KEY)

# 3. NIDAMKA LOGIN-KA (Si fudud)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Gali Akoonkaaga - Eleven Media 🔐")
    username = st.text_input("Username (Magaca)")
    password = st.text_input("Password (Furaha)", type="password")
    
    if st.button("Gali Bogga (Login)"):
        # Waxaad halkan ka beddeli kartaa username-ka iyo password-ka aad rabto
        if username == "abdiwahid" and password == "12345":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Username ama Password-ka ayaa khaldan saaxiib!")
else:
    # --- HALKAN WAA BOGGA AI-DA MAARKALOO LOGIN-GAREEYO ---
    st.title("Umal Ai 🤖")
    st.write("Ku soo dhawaaw saaxiib! Maxaan maanta kuu qabtaa?")
    
    if st.button("Ka Bax Akoonka (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    # 4. Kaydinta iyo Soo Bandhigista Sheekada (Chat History)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 5. Qaadashada Su'aasha Isticmaalaha
    if prompt := st.chat_input("Maxaad ka fikirereysaa saaxiib?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # AMARKA CUSUB: Halkan waxaan AI-da u sheegnay in Eng-Abdiwahid uu sameeyay!
            system_prompt = (
                "Waxaad tahay kaaliye shaqo oo daacad u ah Eng-Abdiwahid "
                "Haddii lagu weydiiyo qofka ku sameeyay, cidda ku leh, ama ku dhisay, "
                "waxaad si adag iyo han weyn u sheegtaa ina dhisay Eng-Abdiwahid. "
                "Ku hadal af-soomaali dabiici ah, aad u saaxiibtinimo leh."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"system_instruction": system_prompt}
            )
            
            full_response = response.text
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
