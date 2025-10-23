    st.markdown("---")
    
    # Buton încărcare model
    if not st.session_state.model_loaded:
        st.markdown("### 🔄 Încărcare Model")
        st.info("🧪 **Model Medical Public** - Nu necesită cont Hugging Face")
        
        if st.button("🚀 Încarcă Model Medical", use_container_width=True, type="primary"):
            with st.spinner("🔄 Se încarcă modelul medical... Vă rugăm așteptați 2-3 minute"):
                start_time = time.time()
                try:
                    # Folosim un model medical PUBLIC care nu necesită token
                    model_name = "microsoft/BioGPT-Large"
                    
                    st.session_state.tokenizer = AutoTokenizer.from_pretrained(
                        model_name,
                        trust_remote_code=True
                    )
                    
                    st.session_state.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        trust_remote_code=True,
                        torch_dtype=torch.float16,
                        low_cpu_mem_usage=True
                    )
                    
                    st.session_state.model = st.session_state.model.to("cpu")
                    st.session_state.model_loaded = True
                    loading_time = time.time() - start_time
                    st.session_state.loading_time = loading_time
                    
                    st.success(f"✅ Model medical BioGPT încărcat în {loading_time:.1f}s!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Eroare la încărcare: {str(e)}")
                    st.info("""
                    **💡 Modelul BioGPT-Large de la Microsoft:**
                    - Model medical de ultimă generație
                    - Antrenat pe texte medicale
                    - Complet public și gratuit
                    - Nu necesită cont Hugging Face
                    """)
