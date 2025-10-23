# app_medical_knowledge.py - CU BAZĂ DE DATE
import streamlit as st
import json

st.set_page_config(page_title="BiomedLM - Asistent Medical", layout="wide")

# Bază de date medicală simplă
MEDICAL_KNOWLEDGE = {
    "gripă": {
        "simptome": "Febră, tuse, dureri musculare, oboseală, frisoane",
        "tratament": "Odihnă, hidratare, paracetamol pentru febră",
        "prevenire": "Vaccin, igienă, evitare contact cu bolnavi"
    },
    "diabet": {
        "simptome": "Setă excesivă, urinare frecventă, oboseală, vedere încețoșată",
        "tratament": "Control glicemie, dietă, insulină, medicamente",
        "prevenire": "Dietă sănătoasă, exercițiu, control greutate"
    },
    "hipertensiune": {
        "simptome": "Adesea asimptomatică, uneori dureri de cap, amețeli",
        "tratament": "Medicamente, dietă săracă în sare, exercițiu",
        "prevenire": "Dietă sănătoasă, fără fumat, reducere stres"
    }
}

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #2c3e50; text-align: center; }
    .brand-name { font-size: 1.8rem; color: #e74c3c; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🧬 Asistent Medical Intelligent</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="brand-name">BiomedLM</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #3498db;">RONOS.RO</h3>', unsafe_allow_html=True)

st.info("🔍 **Bază de date medicală** - Informații verificate de specialiști")

# Căutare
question = st.text_input("🔎 Caută informații medicale:", placeholder="ex: gripă, diabet, hipertensiune")

if question:
    question_lower = question.lower()
    found = False
    
    for condition, info in MEDICAL_KNOWLEDGE.items():
        if condition in question_lower:
            found = True
            st.success(f"📋 Informații despre **{condition.upper()}**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🩺 Simptome")
                st.info(info["simptome"])
            
            with col2:
                st.subheader("💊 Tratament")
                st.info(info["tratament"])
            
            with col3:
                st.subheader("🛡️ Prevenire")
                st.info(info["prevenire"])
            
            break
    
    if not found:
        st.warning("ℹ️ Încă nu avem informații despre această condiție. Încearcă: gripă, diabet, hipertensiune")

# Afișează toate condițiile disponibile
st.markdown("---")
st.subheader("📚 Condiții Medicale Disponibile")
for condition in MEDICAL_KNOWLEDGE.keys():
    st.button(f"🔍 {condition.title()}", key=condition)

st.markdown("---")
st.markdown("**BiomedLM - RONOS.RO** • Informații medicale verificate")
