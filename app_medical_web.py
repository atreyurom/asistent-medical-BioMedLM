# app_medical_free.py - CU API GRATUIT
import streamlit as st
import requests
import json

st.set_page_config(page_title="BiomedLM - Asistent Medical", layout="wide")

# Stiluri
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #2c3e50; text-align: center; }
    .brand-name { font-size: 1.8rem; color: #e74c3c; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🧬 Asistent Medical Intelligent</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="brand-name">BiomedLM</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #3498db;">RONOS.RO</h3>', unsafe_allow_html=True)

# Funcție cu API gratuit
def get_medical_answer(question):
    """Folosește Hugging Face Inference API gratuit"""
    try:
        API_URL = "https://api-inference.huggingface.co/models/medalpaca/medalpaca-7b"
        headers = {"Authorization": "Bearer hf_xxxxxxxxxxxxxxxx"}  # Token gratuit
        
        payload = {
            "inputs": f"Întrebare medicală: {question}\nRăspuns:",
            "parameters": {"max_new_tokens": 200, "temperature": 0.7}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]['generated_text'].split("Răspuns:")[-1].strip()
        else:
            return "⚠️ Serviciul este temporar indisponibil"
            
    except:
        return "❌ Eroare de conexiune"

# Interfață simplă
question = st.text_area("💬 Întrebarea ta medicală:", height=100)

if st.button("🚀 Obține Răspuns"):
    if question:
        with st.spinner("🔍 Căutăm răspunsul..."):
            answer = get_medical_answer(question)
            st.success("🤖 Răspuns BiomedLM:")
            st.info(answer)
    else:
        st.warning("📝 Introdu o întrebare mai întâi!")

st.markdown("---")
st.markdown("**BiomedLM - RONOS.RO** • Asistență medicală 24/7")
