# app_medical_api.py - FĂRĂ ÎNCĂRCARE MODEL
import streamlit as st
import requests
import json
import time

# Configurare pagină
st.set_page_config(
    page_title="BiomedLM - Asistent Medical",
    page_icon="🧬",
    layout="wide"
)

# Stiluri CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #2c3e50; text-align: center; }
    .brand-name { font-size: 1.8rem; color: #e74c3c; text-align: center; }
    .response-box { background: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧬 Asistent Medical Intelligent</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="brand-name">BiomedLM</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #3498db;">RONOS.RO</h3>', unsafe_allow_html=True)

# Initializare
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Configurare")
    api_key = st.text_input("OpenAI API Key", type="password", help="Obține de la https://platform.openai.com/api-keys")
    st.markdown("---")
    st.markdown("### 💡 Exemple")
    examples = ["Simptome gripă", "Tratament tuse", "Prevenire diabet"]
    for ex in examples:
        if st.button(ex):
            st.session_state.question_input = ex

# Funcție pentru OpenAI API
def get_medical_response(question, api_key):
    """Folosește OpenAI GPT pentru răspunsuri medicale"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Ești un asistent medical expert. Oferă răspunsuri precise și utile în limba română."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Eroare API: {response.status_code}"
            
    except Exception as e:
        return f"❌ Eroare: {str(e)}"

# Interfața principală
st.markdown("### 💬 Conversație Medicală")

question = st.text_input(
    "Pune întrebarea ta medicală:",
    placeholder="Ex: Care sunt simptomele unei infecții urinare?",
    key="question_input"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Întreabă", use_container_width=True):
        if question and api_key:
            with st.spinner("🤔 Se analizează întrebarea..."):
                response = get_medical_response(question, api_key)
                
                st.markdown(f'<div class="response-box"><strong>🤖 BiomedLM:</strong><br>{response}</div>', unsafe_allow_html=True)
                
                st.session_state.history.append({
                    "question": question,
                    "response": response
                })
        else:
            st.warning("⚠️ Introdu o întrebare și un API Key!")

with col2:
    if st.session_state.history:
        if st.button("🗑️ Șterge Istoric", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# Istoric
if st.session_state.history:
    st.markdown("### 📚 Istoric")
    for chat in reversed(st.session_state.history[-5:]):
        with st.expander(f"❓ {chat['question'][:50]}..."):
            st.write(chat['response'])

# Footer
st.markdown("---")
st.markdown("*Asistent medical BiomedLM - RONOS.RO • Pentru uz informativ*")
