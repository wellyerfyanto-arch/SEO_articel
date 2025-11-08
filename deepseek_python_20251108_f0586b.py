import streamlit as st
import pandas as pd
import requests
import json
import io
import base64
from PIL import Image
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="SEO Article Builder Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS kustom
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1f77b4, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .step-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .keyword-badge {
        background-color: #1f77b4;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.8rem;
    }
    .generated-content {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

class SEOArticleBuilderPro:
    def __init__(self):
        self.steps = [
            "Riset Kata Kunci",
            "Analisis Kompetitor", 
            "Generate Artikel AI",
            "Generate Gambar AI",
            "Optimasi Teknis",
            "Review & Ekspor"
        ]
    
    def render_sidebar(self):
        st.sidebar.title("🚀 SEO Article Builder Pro")
        st.sidebar.markdown("---")
        
        # Progress tracker
        current_step = st.sidebar.radio("Langkah Saat Ini:", self.steps)
        st.sidebar.markdown("---")
        
        # Quick actions
        st.sidebar.subheader("⚡ Quick Actions")
        if st.sidebar.button("🔄 Reset All"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # API Configuration
        st.sidebar.subheader("🔑 Konfigurasi AI")
        st.sidebar.info("Untuk generate konten otomatis, masukkan API key:")
        
        huggingface_token = st.sidebar.text_input("HuggingFace Token", type="password")
        openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
        
        if huggingface_token:
            st.session_state.hf_token = huggingface_token
        if openai_key:
            st.session_state.openai_key = openai_key
        
        return current_step
    
    def generate_with_huggingface(self, prompt, max_length=500):
        """Generate konten menggunakan Hugging Face API"""
        try:
            if 'hf_token' not in st.session_state:
                return "❌ Masukkan HuggingFace Token di sidebar terlebih dahulu"
            
            API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
            headers = {"Authorization": f"Bearer {st.session_state.hf_token}"}
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', 'Tidak ada respons')
            return str(result)
            
        except Exception as e:
            return f"❌ Error generating content: {str(e)}"
    
    def generate_with_openai(self, prompt, max_tokens=500):
        """Generate konten menggunakan OpenAI API"""
        try:
            if 'openai_key' not in st.session_state:
                return "❌ Masukkan OpenAI API Key di sidebar terlebih dahulu"
            
            import openai
            openai.api_key = st.session_state.openai_key
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Anda adalah penulis artikel SEO profesional yang ahli dalam membuat konten berkualitas tinggi."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating content: {str(e)}"
    
    def generate_image(self, prompt):
        """Generate gambar menggunakan Hugging Face API"""
        try:
            if 'hf_token' not in st.session_state:
                return None, "❌ Masukkan HuggingFace Token di sidebar terlebih dahulu"
            
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
            headers = {"Authorization": f"Bearer {st.session_state.hf_token}"}
            
            payload = {"inputs": prompt}
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            image = Image.open(io.BytesIO(response.content))
            return image, "✅ Gambar berhasil digenerate!"
            
        except Exception as e:
            return None, f"❌ Error generating image: {str(e)}"
    
    def step_keyword_research(self):
        st.header("🔍 Langkah 1: Riset Kata Kunci")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Kata Kunci Utama")
            main_keyword = st.text_input("Kata kunci utama/topik artikel:", key="main_keyword")
            
            st.subheader("Kata Kunci Ekor Panjang (Long-tail)")
            st.write("Tambahkan kata kunci turunan yang lebih spesifik:")
            
            long_tail_keywords = st.text_area(
                "Masukkan kata kunci ekor panjang (pisahkan dengan koma):",
                placeholder="contoh: cara membuat artikel SEO untuk pemula, langkah-langkah SEO 2024, template artikel SEO",
                key="long_tail_keywords"
            )
            
            if long_tail_keywords:
                keywords_list = [k.strip() for k in long_tail_keywords.split(",") if k.strip()]
                st.session_state.keywords_list = keywords_list
                st.write("**Kata kunci yang telah ditambahkan:**")
                for keyword in keywords_list:
                    st.markdown(f'<span class="keyword-badge">{keyword}</span>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("Analisis Search Intent")
            intent_type = st.selectbox(
                "Jenis Intent Pencarian:",
                ["Informasional", "Komersial", "Transaksional", "Navigasional"],
                key="intent_type"
            )
            
            # AI-powered keyword suggestions
            st.subheader("💡 Saran Kata Kunci AI")
            if st.button("Dapatkan Saran Kata Kunci", key="suggest_keywords"):
                if st.session_state.get('main_keyword'):
                    with st.spinner("Menganalisis kata kunci..."):
                        prompt = f"Berikan 5 kata kunci long-tail yang relevan untuk: {st.session_state.main_keyword}. Format: daftar dengan koma"
                        suggestions = self.generate_with_huggingface(prompt, 200)
                        st.session_state.keyword_suggestions = suggestions
                
            if st.session_state.get('keyword_suggestions'):
                st.write("**Saran AI:**")
                st.info(st.session_state.keyword_suggestions)
    
    def step_competitor_analysis(self):
        st.header("📊 Langkah 2: Analisis Kompetitor")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Analisis Artikel Pesaing")
            
            competitors = st.number_input("Jumlah kompetitor yang dianalisis:", min_value=1, max_value=5, value=3, key="num_competitors")
            
            competitor_data = []
            
            for i in range(competitors):
                with st.expander(f"Kompetitor {i+1}", expanded=i==0):
                    col1a, col2a = st.columns(2)
                    
                    with col1a:
                        comp_url = st.text_input(f"URL Kompetitor {i+1}", placeholder="https://...", key=f"url_{i}")
                        comp_title = st.text_input(f"Judul Artikel {i+1}", key=f"title_{i}")
                        comp_strength = st.text_area(f"Kelebihan {i+1}", placeholder="Struktur bagus, konten lengkap, dll...", key=f"strength_{i}")
                    
                    with col2a:
                        comp_word_count = st.number_input(f"Perkiraan Jumlah Kata {i+1}", min_value=0, key=f"words_{i}")
                        comp_gap = st.text_area(f"Celah/Kekurangan {i+1}", placeholder="Informasi yang kurang, tidak update, dll...", key=f"gap_{i}")
                    
                    if comp_title:
                        competitor_data.append({
                            'title': comp_title,
                            'strength': comp_strength,
                            'gap': comp_gap,
                            'word_count': comp_word_count
                        })
            
            if competitor_data:
                st.session_state.competitor_data = competitor_data
                st.subheader("Rangkuman Analisis")
                df = pd.DataFrame(competitor_data)
                st.dataframe(df, use_container_width=True)
        
        with col2:
            st.subheader("🤖 Analisis AI Kompetitor")
            if st.button("Analisis Otomatis dengan AI", key="analyze_ai"):
                if st.session_state.get('main_keyword'):
                    with st.spinner("Menganalisis kompetitor dengan AI..."):
                        prompt = f"""
                        Analisis kompetitor untuk kata kunci: {st.session_state.main_keyword}
                        Berikan insight tentang:
                        1. Topik yang sering dibahas kompetitor
                        2. Celah konten yang bisa dimanfaatkan
                        3. Struktur konten yang efektif
                        4. Rekomendasi angle unik
                        """
                        analysis = self.generate_with_huggingface(prompt, 300)
                        st.session_state.competitor_ai_analysis = analysis
            
            if st.session_state.get('competitor_ai_analysis'):
                st.write("**Analisis AI:**")
                st.info(st.session_state.competitor_ai_analysis)
    
    def step_article_generation(self):
        st.header("🤖 Langkah 3: Generate Artikel AI")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Konfigurasi Generate Artikel")
            
            # Template selection
            template = st.selectbox(
                "Pilih Template Artikel:",
                ["How-to Guide", "Listicle", "Review", "News", "Tutorial", "Case Study"],
                key="article_template"
            )
            
            # Article parameters
            tone = st.selectbox(
                "Gaya Bahasa:",
                ["Formal", "Semi-formal", "Casual", "Profesional", "Friendly"],
                key="article_tone"
            )
            
            word_target = st.slider("Target Jumlah Kata:", 500, 2000, 1200, key="word_target")
            
            # Enhanced prompt builder
            st.subheader("Prompt Generator")
            col1a, col2a = st.columns(2)
            
            with col1a:
                focus_points = st.text_area(
                    "Poin Penting yang Harus Dicakup:",
                    placeholder="Masukkan poin-poin utama yang harus ada di artikel...",
                    height=100,
                    key="focus_points"
                )
                
            with col2a:
                exclude_points = st.text_area(
                    "Poin yang Harus Dihindari:",
                    placeholder="Topik yang tidak relevan atau sudah basi...",
                    height=100,
                    key="exclude_points"
                )
            
            # Generate buttons
            col1b, col2b, col3b = st.columns(3)
            
            with col1b:
                if st.button("🚀 Generate Full Article", type="primary", key="generate_full"):
                    self.generate_full_article()
            
            with col2b:
                if st.button("📝 Generate Outline", key="generate_outline"):
                    self.generate_article_outline()
            
            with col3b:
                if st.button("🎯 Generate Introduction", key="generate_intro"):
                    self.generate_introduction()
            
            # Display generated content
            st.subheader("Konten Hasil Generate")
            
            if st.session_state.get('generated_outline'):
                with st.expander("📋 Outline Artikel", expanded=True):
                    st.markdown(f'<div class="generated-content">{st.session_state.generated_outline}</div>', unsafe_allow_html=True)
            
            if st.session_state.get('generated_article'):
                with st.expander("📄 Artikel Lengkap", expanded=True):
                    st.markdown(f'<div class="generated-content">{st.session_state.generated_article}</div>', unsafe_allow_html=True)
            
            # Article editor
            st.subheader("Editor Artikel")
            final_article = st.text_area(
                "Edit dan sesuaikan artikel Anda:",
                value=st.session_state.get('generated_article', ''),
                height=400,
                key="final_article_editor"
            )
        
        with col2:
            st.subheader("⚡ Quick Actions")
            
            if st.button("🔍 Check SEO Score", key="check_seo"):
                self.calculate_seo_score()
            
            if st.button("📊 Analyze Readability", key="analyze_readability"):
                self.analyze_readability()
            
            if st.button("💡 Improve with AI", key="improve_ai"):
                self.improve_with_ai()
            
            # SEO Metrics
            if st.session_state.get('final_article_editor'):
                content = st.session_state.final_article_editor
                word_count = len(content.split())
                paragraph_count = content.count('\n\n') + 1
                
                st.metric("Jumlah Kata", word_count)
                st.metric("Jumlah Paragraf", paragraph_count)
                
                # Readability score (simplified)
                if word_count > 0:
                    avg_sentence_length = word_count / max(content.count('.'), 1)
                    readability_score = max(0, min(100, 100 - (avg_sentence_length * 2)))
                    st.metric("Skor Keterbacaan", f"{readability_score:.0f}/100")
    
    def generate_full_article(self):
        """Generate artikel lengkap"""
        if not st.session_state.get('main_keyword'):
            st.error("Masukkan kata kunci utama terlebih dahulu di Langkah 1")
            return
        
        with st.spinner("🤖 Sedang generate artikel lengkap..."):
            prompt = f"""
            Buat artikel SEO yang komprehensif tentang: {st.session_state.main_keyword}
            
            Template: {st.session_state.article_template}
            Gaya Bahasa: {st.session_state.article_tone}
            Target Kata: {st.session_state.word_target}
            
            Poin penting: {st.session_state.get('focus_points', '')}
            Hindari: {st.session_state.get('exclude_points', '')}
            
            Struktur:
            1. Judul menarik
            2. Pendahuluan yang engaging
            3. Konten utama dengan subheading jelas
            4. Kesimpulan dan call-to-action
            5. FAQ section (jika relevan)
            
            Optimasi untuk SEO dan mudah dibaca.
            """
            
            if st.session_state.get('openai_key'):
                article = self.generate_with_openai(prompt, st.session_state.word_target)
            else:
                article = self.generate_with_huggingface(prompt, st.session_state.word_target)
            
            st.session_state.generated_article = article
            st.success("✅ Artikel berhasil digenerate!")
    
    def generate_article_outline(self):
        """Generate outline artikel"""
        if not st.session_state.get('main_keyword'):
            st.error("Masukkan kata kunci utama terlebih dahulu di Langkah 1")
            return
        
        with st.spinner("📋 Sedang generate outline..."):
            prompt = f"""
            Buat outline terstruktur untuk artikel tentang: {st.session_state.main_keyword}
            
            Format:
            H1: Judul Utama
            H2: Sub Judul 1
            - Poin penting
            - Poin penting
            H2: Sub Judul 2
            - Poin penting
            - Poin penting
            ...dan seterusnya
            
            Buat outline yang komprehensif dan SEO-friendly.
            """
            
            outline = self.generate_with_huggingface(prompt, 300)
            st.session_state.generated_outline = outline
            st.success("✅ Outline berhasil digenerate!")
    
    def generate_introduction(self):
        """Generate introduction"""
        if not st.session_state.get('main_keyword'):
            st.error("Masukkan kata kunci utama terlebih dahulu di Langkah 1")
            return
        
        with st.spinner("🎯 Sedang generate introduction..."):
            prompt = f"""
            Tulis paragraf pembuka (introduction) yang menarik untuk artikel tentang: {st.session_state.main_keyword}
            
            Requirements:
            - Tangkap perhatian pembaca
            - Jelaskan masalah yang dihadapi
            - Berikan janji solusi
            - Sertakan kata kunci secara natural
            - Maksimal 150 kata
            - Gaya bahasa: {st.session_state.get('article_tone', 'Profesional')}
            """
            
            introduction = self.generate_with_huggingface(prompt, 200)
            st.session_state.generated_introduction = introduction
            st.success("✅ Introduction berhasil digenerate!")
    
    def step_image_generation(self):
        st.header("🎨 Langkah 4: Generate Gambar AI")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Generate Gambar untuk Artikel")
            
            # Image prompt builder
            st.write("**Buat Prompt Gambar:**")
            image_style = st.selectbox(
                "Gaya Gambar:",
                ["Realistic", "Digital Art", "Minimalist", "3D Render", "Watercolor", "Line Art"],
                key="image_style"
            )
            
            image_context = st.text_area(
                "Deskripsi Gambar:",
                placeholder="Contoh: orang sedang menulis di laptop dengan grafik SEO di latar belakang...",
                key="image_context"
            )
            
            # Auto-generate image prompt
            if st.button("🪄 Buat Prompt Otomatis", key="auto_prompt"):
                if st.session_state.get('main_keyword'):
                    with st.spinner("Membuat prompt gambar..."):
                        prompt = f"Buat prompt untuk generate gambar ilustrasi artikel tentang: {st.session_state.main_keyword}. Gaya: {st.session_state.image_style}. Deskripsi singkat dan jelas."
                        auto_prompt = self.generate_with_huggingface(prompt, 100)
                        st.session_state.image_context = auto_prompt
            
            final_prompt = f"{st.session_state.image_style} style, {st.session_state.image_context}, high quality, professional, SEO article illustration"
            
            st.write("**Prompt Final:**")
            st.code(final_prompt)
            
            # Generate image
            if st.button("🎨 Generate Gambar", type="primary", key="generate_image"):
                if st.session_state.get('hf_token'):
                    with st.spinner("Sedang generate gambar... Ini mungkin butuh 10-30 detik"):
                        image, message = self.generate_image(final_prompt)
                        
                        if image:
                            st.session_state.generated_image = image
                            st.success(message)
                        else:
                            st.error(message)
                else:
                    st.error("Masukkan HuggingFace Token di sidebar terlebih dahulu")
            
            # Display generated image
            if st.session_state.get('generated_image'):
                st.subheader("Gambar Hasil Generate")
                st.image(st.session_state.generated_image, use_column_width=True)
                
                # Download button
                buf = io.BytesIO()
                st.session_state.generated_image.save(buf, format="PNG")
                buf.seek(0)
                
                st.download_button(
                    label="📥 Download Gambar",
                    data=buf,
                    file_name=f"seo-article-image-{int(time.time())}.png",
                    mime="image/png"
                )
        
        with col2:
            st.subheader("Gambar yang Diupload")
            
            uploaded_file = st.file_uploader(
                "Atau upload gambar sendiri:",
                type=['png', 'jpg', 'jpeg', 'gif'],
                key="image_uploader"
            )
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, use_column_width=True)
                st.session_state.uploaded_image = image
            
            st.subheader("Tips Gambar SEO")
            st.info("""
            **Optimasi Gambar untuk SEO:**
            - Format: WebP atau JPEG
            - Ukuran: <100KB jika mungkin
            - Nama file: deskriptif dengan kata kunci
            - Alt text: jelaskan gambar dengan detail
            - Relevan dengan konten artikel
            """)
    
    def step_technical_optimization(self):
        st.header("⚙️ Langkah 5: Optimasi Teknis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Meta Information")
            
            # Auto-generate meta tags
            if st.button("🤖 Generate Meta Tags Otomatis", key="generate_meta"):
                if st.session_state.get('main_keyword'):
                    with st.spinner("Generate meta tags..."):
                        prompt = f"Buat meta title dan meta description yang optimal untuk artikel tentang: {st.session_state.main_keyword}. Max 60 karakter untuk title, 160 untuk description."
                        meta_suggestion = self.generate_with_huggingface(prompt, 150)
                        st.session_state.meta_suggestion = meta_suggestion
            
            if st.session_state.get('meta_suggestion'):
                st.write("**Saran AI:**")
                st.info(st.session_state.meta_suggestion)
            
            meta_title = st.text_input(
                "Meta Title:",
                placeholder="Judul untuk SEO (max 60 karakter)",
                max_chars=60,
                key="meta_title"
            )
            if meta_title:
                st.write(f"Panjang: {len(meta_title)}/60 karakter")
            
            meta_description = st.text_area(
                "Meta Description:",
                placeholder="Deskripsi untuk hasil pencarian (max 160 karakter)",
                max_chars=160,
                height=100,
                key="meta_description"
            )
            if meta_description:
                st.write(f"Panjang: {len(meta_description)}/160 karakter")
            
            url_slug = st.text_input(
                "URL Slug:",
                placeholder="url-slug-yang-optimasi",
                help="Gunakan huruf kecil dan tanda strip",
                key="url_slug"
            )
        
        with col2:
            st.subheader("Optimasi Lanjutan")
            
            st.write("**Internal Links:**")
            internal_links = st.text_area(
                "Tautan internal yang relevan:",
                placeholder="https://websiteanda.com/artikel-terkait-1\nhttps://websiteanda.com/artikel-terkait-2",
                height=100,
                key="internal_links"
            )
            
            st.write("**Alt Text untuk Gambar:**")
            image_alt = st.text_input(
                "Alt Text untuk gambar utama:",
                placeholder="Deskripsi gambar yang mengandung kata kunci",
                key="image_alt"
            )
            
            # SEO Score
            st.subheader("Skor SEO")
            score = self.calculate_seo_score(silent=True)
            st.progress(score/100)
            st.write(f"Skor: {score}/100")
            
            if score >= 80:
                st.success("✅ Excellent! Artikel sudah optimal")
            elif score >= 60:
                st.warning("⚠️ Good, tapi masih bisa ditingkatkan")
            else:
                st.error("❌ Perlu improvement signifikan")
    
    def calculate_seo_score(self, silent=False):
        """Hitung skor SEO berdasarkan berbagai faktor"""
        score = 0
        factors = []
        
        # Check factors
        if st.session_state.get('main_keyword'):
            score += 15
            factors.append("✅ Kata kunci utama tersedia")
        else:
            factors.append("❌ Kata kunci utama belum diisi")
        
        if st.session_state.get('meta_title') and len(st.session_state.meta_title) <= 60:
            score += 15
            factors.append("✅ Meta title optimal")
        else:
            factors.append("❌ Meta title perlu dioptimasi")
        
        if st.session_state.get('meta_description') and len(st.session_state.meta_description) <= 160:
            score += 15
            factors.append("✅ Meta description optimal")
        else:
            factors.append("❌ Meta description perlu dioptimasi")
        
        if st.session_state.get('generated_article'):
            content = st.session_state.generated_article
            word_count = len(content.split())
            if word_count >= 800:
                score += 20
                factors.append(f"✅ Panjang konten optimal ({word_count} kata)")
            else:
                factors.append(f"⚠️ Konten terlalu pendek ({word_count} kata)")
        
        if st.session_state.get('image_alt'):
            score += 10
            factors.append("✅ Alt text tersedia")
        else:
            factors.append("❌ Alt text belum diisi")
        
        if st.session_state.get('url_slug'):
            score += 10
            factors.append("✅ URL slug tersedia")
        else:
            factors.append("❌ URL slug belum diisi")
        
        # Additional points
        score += 15  # Base score
        
        if not silent:
            st.subheader("Detail Skor SEO")
            for factor in factors:
                st.write(factor)
            st.metric("Skor SEO Total", f"{score}/100")
        
        return score
    
    def step_review_export(self):
        st.header("✅ Langkah 6: Review & Ekspor")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Final Check & Ekspor")
            
            # Comprehensive checklist
            checklist_items = {
                "Kata kunci utama digunakan dalam judul": st.session_state.get('main_keyword') and 
                    st.session_state.main_keyword.lower() in st.session_state.get('meta_title', '').lower(),
                "Meta title dan description sudah optimal": len(st.session_state.get('meta_title', '')) <= 60 and 
                    len(st.session_state.get('meta_description', '')) <= 160,
                "Konten memiliki struktur heading yang jelas": '#' in st.session_state.get('generated_article', ''),
                "Panjang konten memadai (>800 kata)": len(st.session_state.get('generated_article', '').split()) >= 800,
                "Gambar dengan alt text tersedia": st.session_state.get('image_alt') or st.session_state.get('generated_image'),
                "Internal linking sudah direncanakan": st.session_state.get('internal_links'),
                "URL slug sudah dioptimasi": st.session_state.get('url_slug')
            }
            
            st.subheader("Checklist Final")
            completed_items = 0
            for item, checked in checklist_items.items():
                if st.checkbox(item, value=checked, key=f"check_{item}"):
                    completed_items += 1
            
            total_items = len(checklist_items)
            progress = completed_items / total_items
            
            st.metric("Progress Review", f"{completed_items}/{total_items}")
            st.progress(progress)
            
            if progress == 1:
                st.success("🎉 Excellent! Artikel Anda sudah optimal untuk SEO!")
            elif progress >= 0.7:
                st.warning("💡 Good! Beberapa item masih perlu diperbaiki.")
            else:
                st.error("⚠️ Perlu improvement signifikan.")
            
            # Export options
            st.subheader("Ekspor Artikel")
            
            export_col1, export_col2, export_col3 = st.columns(3)
            
            with export_col1:
                if st.button("📄 Export HTML", type="primary"):
                    self.export_html()
            
            with export_col2:
                if st.button("📝 Export Markdown"):
                    self.export_markdown()
            
            with export_col3:
                if st.button("💾 Save to JSON"):
                    self.export_json()
        
        with col2:
            st.subheader("Preview Cepat")
            
            if st.session_state.get('meta_title'):
                st.write("**Meta Title Preview:**")
                st.info(st.session_state.meta_title)
            
            if st.session_state.get('meta_description'):
                st.write("**Meta Description Preview:**")
                st.info(st.session_state.meta_description)
            
            if st.session_state.get('generated_article'):
                st.write("**Konten Preview:**")
                preview_text = st.session_state.generated_article[:200] + "..." if len(st.session_state.generated_article) > 200 else st.session_state.generated_article
                st.text_area("", value=preview_text, height=100, key="preview_area")
    
    def export_html(self):
        """Ekspor artikel dalam format HTML"""
        if not st.session_state.get('generated_article'):
            st.error("Tidak ada artikel untuk diexport")
            return
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{st.session_state.get('meta_title', 'Artikel SEO')}</title>
            <meta name="description" content="{st.session_state.get('meta_description', '')}">
        </head>
        <body>
            <article>
                <h1>{st.session_state.get('meta_title', 'Judul Artikel')}</h1>
                <div class="content">
                    {st.session_state.generated_article.replace(chr(10), '<br>')}
                </div>
            </article>
        </body>
        </html>
        """
        
        st.download_button(
            label="📥 Download HTML",
            data=html_content,
            file_name=f"{st.session_state.get('url_slug', 'article')}.html",
            mime="text/html"
        )
    
    def export_markdown(self):
        """Ekspor artikel dalam format Markdown"""
        if not st.session_state.get('generated_article'):
            st.error("Tidak ada artikel untuk diexport")
            return
        
        markdown_content = f"# {st.session_state.get('meta_title', 'Judul Artikel')}\n\n{st.session_state.generated_article}"
        
        st.download_button(
            label="📥 Download Markdown",
            data=markdown_content,
            file_name=f"{st.session_state.get('url_slug', 'article')}.md",
            mime="text/markdown"
        )
    
    def export_json(self):
        """Ekspor semua data dalam format JSON"""
        article_data = {
            "meta_title": st.session_state.get('meta_title'),
            "meta_description": st.session_state.get('meta_description'),
            "url_slug": st.session_state.get('url_slug'),
            "main_keyword": st.session_state.get('main_keyword'),
            "content": st.session_state.get('generated_article'),
            "created_at": str(pd.Timestamp.now()),
            "seo_score": self.calculate_seo_score(silent=True)
        }
        
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(article_data, indent=2, ensure_ascii=False),
            file_name=f"{st.session_state.get('url_slug', 'article')}.json",
            mime="application/json"
        )
    
    def run(self):
        st.markdown('<h1 class="main-header">🚀 SEO Article Builder Pro</h1>', unsafe_allow_html=True)
        st.markdown("**Panduan Lengkap Membuat Artikel SEO dengan AI - Generate Artikel & Gambar Otomatis**")
        
        current_step = self.render_sidebar()
        
        # Tampilkan step yang sesuai
        if current_step == "Riset Kata Kunci":
            self.step_keyword_research()
        elif current_step == "Analisis Kompetitor":
            self.step_competitor_analysis()
        elif current_step == "Generate Artikel AI":
            self.step_article_generation()
        elif current_step == "Generate Gambar AI":
            self.step_image_generation()
        elif current_step == "Optimasi Teknis":
            self.step_technical_optimization()
        elif current_step == "Review & Ekspor":
            self.step_review_export()
        
        # Footer dengan status
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.get('main_keyword'):
                st.success(f"Keyword: {st.session_state.main_keyword}")
        
        with col2:
            if st.session_state.get('generated_article'):
                word_count = len(st.session_state.generated_article.split())
                st.info(f"Konten: {word_count} kata")
        
        with col3:
            seo_score = self.calculate_seo_score(silent=True)
            st.metric("SEO Score", f"{seo_score}/100")

# Jalankan aplikasi
if __name__ == "__main__":
    # Initialize session state
    if 'generated_article' not in st.session_state:
        st.session_state.generated_article = ""
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
    
    builder = SEOArticleBuilderPro()
    builder.run()