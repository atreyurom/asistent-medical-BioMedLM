# app_medical_web.py - ASISTENT MEDICAL BIOMEDLM - RONOS.RO
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import time
import requests
import urllib.parse

# Configurare pentru server cloud
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Funcție de traducere stabilă
def translate_text(text, src='en', dest='ro'):
    """
    Traduce text folosind MyMemory Translation API (gratuit și stabil)
    """
    try:
        # URL encode text
        encoded_text = urllib.parse.quote(text)
        
        # Folosim MyMemory Translation API
        url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={src}|{dest}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'responseData' in data and 'translatedText' in data['responseData']:
                translated = data['responseData']['translatedText']
                # Curăță textul dacă este necesar
                if translated.strip():
                    return translated
        
        # Dacă traducerea eșuează, returnăm textul original
        return text
        
    except Exception as e:
        # În caz de eroare, returnăm textul original
        return text

# Configurare pagină
st.set_page_config(
    page_title="BiomedLM - Asistent Medical",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stiluri CSS personalizate
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        color: #2c3e50 !important;
        text-align: center;
        margin-bottom: 0 !important;
    }
    .brand-name {
        font-size: 1.8rem !important;
        color: #e74c3c !important;
        text-align: center;
        margin-bottom: 1rem !important;
        font-weight: bold;
    }
    .website-url {
        font-size: 1.2rem !important;
        color: #3498db !important;
        text-align: center;
        margin-bottom: 2rem !important;
        font-style: italic;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .response-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #27ae60;
        margin: 10px 0;
    }
    .question-box {
        background-color: #e8f4fd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #3498db;
    }
    .info-box {
        background-color: #fffbf0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        border-left: 5px solid #f39c12;
    }
    .success-box {
        background-color: #d4edda;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #28a745;
    }
    .brand-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        text-align: center;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">🧬 Asistent Medical Intelligent</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="brand-name">BiomedLM</h2>', unsafe_allow_html=True)
st.markdown('<h3 class="website-url">RONOS.RO</h3>', unsafe_allow_html=True)

# Initializare sesiune
if 'history' not in st.session_state:
    st.session_state.history = []
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'tokenizer' not in st.session_state:
    st.session_state.tokenizer = None
if 'model' not in st.session_state:
    st.session_state.model = None
if 'loading_time' not in st.session_state:
    st.session_state.loading_time = None

# Sidebar pentru setări
with st.sidebar:
    # Brand box în sidebar
    st.markdown('<div class="brand-box"><strong>🧬 BiomedLM</strong><br>Asistență Medicală Avansată<br><em>RONOS.RO</em></div>', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Setări Aplicație")
    
    # Informații server cloud
    st.markdown('<div class="success-box">🌐 <strong>Server Cloud Activ</strong><br>⚡ Performanță optimizată</div>', unsafe_allow_html=True)
    
    # Opțiuni traducere
    auto_translate = st.checkbox("🌍 Traduce automat în română", value=True, help="Răspunsurile vor fi traduse automat din engleză în română")
    font_size = st.slider("📏 Mărime font răspuns:", min_value=12, max_value=20, value=14)
    
    st.markdown("---")
    
    # Buton încărcare model
    if not st.session_state.model_loaded:
        st.markdown("### 🔄 Încărcare Model")
        st.info("Prima încărcare poate dura 1-2 minute datorită descărcării modelului.")
        
        if st.button("🚀 Încarcă Model Medical", use_container_width=True, type="primary"):
            with st.spinner("🔄 Se încarcă modelul BiomedLM... Vă rugăm așteptați"):
                start_time = time.time()
                try:
                    # TOKEN-UL TĂU HF
                    HF_TOKEN = "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"
                    
                    # Încarcă tokenizer-ul
                    st.session_state.tokenizer = AutoTokenizer.from_pretrained(
                        "stanford-crfm/BiomedLM", 
                        token=HF_TOKEN, 
                        trust_remote_code=True
                    )
                    
                    # Încarcă modelul cu setări optimizate pentru cloud
                    st.session_state.model = AutoModelForCausalLM.from_pretrained(
                        "stanford-crfm/BiomedLM",
                        token=HF_TOKEN,
                        trust_remote_code=True,
                        torch_dtype=torch.float16,  # Economiseste memorie
                        low_cpu_mem_usage=True      # Optimizare memorie
                    )
                    
                    # Folosește CPU pe server cloud
                    st.session_state.model = st.session_state.model.to("cpu")
                    st.session_state.model_loaded = True
                    
                    # Calculează timpul de încărcare
                    loading_time = time.time() - start_time
                    st.session_state.loading_time = loading_time
                    
                    st.success(f"✅ Model BiomedLM încărcat cu succes în {loading_time:.1f} secunde!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Eroare la încărcare: {str(e)}")
                    st.info("💡 Asigură-te că token-ul HF este valid și ai acces la model.")
    else:
        st.markdown("### ✅ Status Model")
        if st.session_state.loading_time:
            st.success(f"BiomedLM încărcat în {st.session_state.loading_time:.1f}s")
        else:
            st.success("BiomedLM încărcat și gata!")
            
        if st.button("🔄 Reîncarcă Model", use_container_width=True):
            st.session_state.model_loaded = False
            st.session_state.model = None
            st.session_state.tokenizer = None
            st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Exemple de întrebări:")
    
    example_questions = [
        "Care sunt simptomele bolii Lyme?",
        "Cum funcționează antibioticelor?",
        "Explică mecanismul acțiunii insuliniei",
        "Ce sunt bolile autoimune?",
        "Cum se diagnostichează diabetul?",
        "Care sunt factorii de risc pentru boli cardiace?"
    ]
    
    for example in example_questions:
        if st.button(example, key=example, use_container_width=True):
            st.session_state.question_input = example
            st.rerun()

# Coloana principală
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Conversație Medicală")
    
    if not st.session_state.model_loaded:
        st.markdown('<div class="info-box">📋 <strong>Instrucțiuni:</strong><br>1. Apasă butonul "Încarcă Model Medical" în sidebar<br>2. Așteaptă încărcarea modelului BiomedLM (1-2 minute)<br>3. Pune întrebări medicale în caseta de mai jos</div>', unsafe_allow_html=True)
    
    # Input întrebare
    question = st.text_input(
        "Scrie întrebarea ta medicală aici:",
        placeholder="Exemplu: Care sunt simptomele unei infecții urinare?",
        key="question_input",
        label_visibility="collapsed"
    )
    
    # Butoane acțiune
    col1_1, col1_2, col1_3 = st.columns(3)
    
    with col1_1:
        ask_disabled = not st.session_state.model_loaded
        if st.button("📝 Întreabă", disabled=ask_disabled, use_container_width=True, type="primary"):
            if question and question.strip():
                with st.spinner("🤔 BiomedLM analizează întrebarea..."):
                    try:
                        # Afișează întrebarea
                        st.markdown(f'<div class="question-box"><strong>👤 Utilizator:</strong> {question}</div>', unsafe_allow_html=True)
                        
                        # Informații procesare
                        st.markdown('<div class="info-box"><strong>🔧 BiomedLM Cloud:</strong> Se procesează cererea...</div>', unsafe_allow_html=True)
                        
                        # Generează răspuns
                        prompt = f"Medical question: {question}"
                        inputs = st.session_state.tokenizer(prompt, return_tensors="pt")
                        
                        outputs = st.session_state.model.generate(
                            **inputs,
                            max_new_tokens=350,
                            temperature=0.7,
                            do_sample=True,
                            pad_token_id=st.session_state.tokenizer.eos_token_id,
                            repetition_penalty=1.1,
                            no_repeat_ngram_size=2
                        )
                        
                        response = st.session_state.tokenizer.decode(outputs[0], skip_special_tokens=True)
                        english_response = response[len(prompt):].strip()
                        
                        # Traducere dacă este selectată
                        if auto_translate and english_response:
                            st.markdown('<div class="info-box"><strong>🔄 Se traduce în română...</strong></div>', unsafe_allow_html=True)
                            try:
                                final_response = translate_text(english_response, src='en', dest='ro')
                                # Verifică dacă traducerea a funcționat
                                if final_response == english_response:
                                    final_response = english_response + "\n\n💡 *Traducerea nu a putut fi efectuată - răspuns în engleză*"
                            except Exception as e:
                                final_response = english_response + f"\n\n⚠️ Eroare traducere - răspuns în engleză"
                        else:
                            final_response = english_response
                        
                        # Afișează răspunsul
                        st.markdown(
                            f'<div class="response-box" style="font-size: {font_size}px;">'
                            f'<strong>🤖 BiomedLM:</strong><br><br>{final_response}'
                            f'</div>', 
                            unsafe_allow_html=True
                        )
                        
                        # Salvează în istoric
                        st.session_state.history.append({
                            "question": question,
                            "response": final_response,
                            "timestamp": time.time()
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Eroare la generarea răspunsului: {str(e)}")
            else:
                st.warning("⚠️ Te rog introdu o întrebare înainte de a apăsa butonul!")
    
    with col1_2:
        if st.button("🗑️ Șterge Istoric", use_container_width=True):
            st.session_state.history = []
            st.success("Istoricul conversației a fost șters!")
            st.rerun()
    
    with col1_3:
        if st.session_state.history:
            last_response = st.session_state.history[-1]["response"]
            if st.button("📋 Copiază Răspuns", use_container_width=True):
                st.code(last_response)
                st.success("✅ Răspuns copiat în clipboard! Poți să-l lipesti cu Ctrl+V")

with col2:
    st.markdown("### 📚 Istoric Conversație")
    
    if st.session_state.history:
        # Afișează ultimele 6 conversații (cele mai recente primele)
        for i, chat in enumerate(reversed(st.session_state.history[-6:])):
            with st.expander(f"💬 Conversația {len(st.session_state.history)-i}", expanded=False):
                st.write(f"**❓ Întrebare:** {chat['question']}")
                st.write(f"**🤖 BiomedLM:** {chat['response']}")
                
                # Buton copiere rapidă pentru fiecare răspuns
                if st.button(f"📋 Copiază", key=f"copy_{i}", use_container_width=True):
                    st.code(chat['response'])
                    st.success("Răspuns copiat!")
    else:
        st.markdown('<div class="info-box">💡 Încă nu există conversații.<br>Pune prima întrebare medicală!</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎯 Ghid Utilizare")
    
    tips = [
        "✅ **Folosește întrebări clare și specifice**",
        "✅ **Menționează simptome sau condiții medicale**",
        "✅ **Cere explicații pentru mecanisme fiziologice**",
        "✅ **Întreabă despre diagnostic și tratament**",
        "⚠️ **Consultă întotdeauna medic pentru diagnostic**",
        "💡 **Primele întrebări pot fi mai lente**"
    ]
    
    for tip in tips:
        st.markdown(tip)

    st.markdown("---")
    st.markdown("### 🌐 Despre Noi")
    st.info("""
    **BiomedLM - RONOS.RO**
    
    Platformă avansată de asistență medicală 
    bazată pe inteligență artificială.
    
    • Asistență medicală 24/7
    • Răspunsuri personalizate
    • Tehnologie de ultimă oră
    """)

# Footer profesional
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #7f8c8d; font-style: italic; padding: 20px;'>"
    "🧬 <strong>BiomedLM - Asistent Medical Intelligent</strong><br>"
    "O soluție <strong>RONOS.RO</strong> pentru sănătatea dumneavoastră<br>"
    "Pentru uz educațional și informativ • "
    "<em>Consultați întotdeauna personalul medical calificat pentru diagnostic și tratament</em><br>"
    "<strong>www.ronos.ro</strong>"
    "</div>", 
    unsafe_allow_html=True
)
