import streamlit as st
from openai import OpenAI
import random
from datetime import datetime

st.set_page_config(page_title="🏠 Grok Architecture Studio", layout="wide", initial_sidebar_state="expanded")

# Dark modern theme
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .generated-image { border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
</style>
""", unsafe_allow_html=True)

st.title("🏠 Grok Architecture Studio")
st.markdown("**xAI Grok Imagine • Professional Architectural Visualizer**")

# Sidebar
with st.sidebar:
    st.header("🔑 API Settings")
    api_key = st.text_input("xAI API Key", type="password", help="Get it from console.x.ai")
    
    st.header("⚙️ Generation Settings")
    num_images = st.slider("Number of images", 1, 4, 4)

# Main tabs
tab1, tab2, tab3 = st.tabs(["🎨 Create", "🖼️ Gallery", "❤️ Favorites"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Design Parameters")
        view_type = st.selectbox("View Type", 
            ["exterior outlook", "interior", "floor plan", "cut view", "isometric", "perspective", "drone view"])
        
        house_type = st.text_input("House Type", "modern minimalist villa")
        roof = st.text_input("Roof Type", "flat roof with generous overhangs")
        materials = st.text_input("Materials & Finishes", "white concrete, warm wood accents, large glass panels, natural stone")
        landscape = st.text_input("Landscape & Surroundings", "Mediterranean garden, olive trees, infinity pool overlooking hills")
        
        lighting = st.selectbox("Lighting", 
            ["golden hour sunset", "soft morning light", "dramatic blue hour", "bright midday", "moody overcast"])
        mood = st.text_input("Mood & Atmosphere", "warm, serene and luxurious")
        details = st.text_area("Additional Details", "architectural masterpiece, lush vegetation, high-end details", height=80)

    with col2:
        st.subheader("Quick Actions")
        if st.button("🎲 Surprise Me!", use_container_width=True, type="primary"):
            presets = [
                ("modern minimalist villa", "flat roof with overhangs", "white concrete and wood", "infinity pool with ocean view", "golden hour sunset", "serene luxury"),
                ("Lisbon-inspired townhouse", "traditional terracotta roof", "colorful azulejo tiles and white walls", "narrow street with cobblestones", "golden hour sunset", "charming and vibrant"),
            ]
            choice = random.choice(presets)
            st.session_state.house_type = choice[0]
            st.session_state.roof = choice[1]
            st.session_state.materials = choice[2]
            st.session_state.landscape = choice[3]
            st.session_state.lighting = choice[4]
            st.session_state.mood = choice[5]
            st.rerun()

        if st.button("🚀 Generate Images", type="primary", use_container_width=True):
            if not api_key:
                st.error("Please enter your xAI API key")
            else:
                base = f"A highly detailed {view_type} of a {house_type} with {roof}, {materials}"
                if landscape:
                    base += f", set in {landscape}"
                prompt = f"{base}. {lighting}, {mood} atmosphere. Professional architectural visualization, sharp details, accurate proportions, intricate textures, high resolution, photorealistic."
                
                with st.spinner(f"Generating {num_images} images..."):
                    try:
                        client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                        response = client.images.generate(
                            model="grok-imagine-image-quality",
                            prompt=prompt,
                            n=num_images,
                            response_format="url"
                        )
                        images = [img.url for img in response.data]
                        
                        if "history" not in st.session_state:
                            st.session_state.history = []
                        
                        st.session_state.history.insert(0, {
                            "prompt": prompt[:150] + "...",
                            "images": images,
                            "time": datetime.now().strftime("%H:%M")
                        })
                        st.success(f"✅ {num_images} images generated!")
                    except Exception as e:
                        st.error(f"Error: {e}")

    # Show latest images
    if "history" in st.session_state and len(st.session_state.history) > 0:
        st.subheader("Latest Generation")
        cols = st.columns(4)
        for i, url in enumerate(st.session_state.history[0]["images"]):
            with cols[i]:
                st.image(url, use_column_width=True, caption=f"Image {i+1}")

with tab2:
    st.subheader("🖼️ Generation History")
    if "history" not in st.session_state or len(st.session_state.history) == 0:
        st.info("No generations yet.")
    else:
        for item in st.session_state.history:
            st.markdown(f"**{item['time']}** — {item['prompt']}")
            cols = st.columns(4)
            for i, url in enumerate(item["images"]):
                with cols[i]:
                    st.image(url, use_column_width=True)

with tab3:
    st.subheader("❤️ Favorites")
    st.info("Coming soon...")

st.caption("Built with ❤️ using Streamlit + xAI Grok Imagine • Lisbon Edition 🏙️")