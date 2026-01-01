import streamlit as st
import requests
from io import BytesIO
import time

# --- Page Config ---
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# --- Title & Style ---
st.title("🎨 Free AI Image Generator")
st.markdown("Generate images instantly using **Pollinations.ai** (No API Key needed).")

# --- Sidebar ---
st.sidebar.header("Settings")
width = st.sidebar.slider("Width", 256, 1024, 1024, step=64)
height = st.sidebar.slider("Height", 256, 1024, 1024, step=64)
seed = st.sidebar.number_input("Seed (Optional)", value=42, help="Same seed + same prompt = same image")

# --- Main Interface ---
prompt = st.text_input("Enter your imagination:", placeholder="A futuristic city with flying cars, cyberpunk style")

generate_btn = st.button("✨ Generate Image", type="primary")

if generate_btn and prompt:
    with st.spinner("🎨 Painting your dream..."):
        try:
            # Construct URL
            # Pollinations Format: https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&seed={s}
            safe_prompt = prompt.replace(" ", "%20")
            url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width={width}&height={height}&seed={seed}&nologo=true"
            
            # Fetch Image
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Display Image
                image_bytes = BytesIO(response.content)
                st.image(image_bytes, caption=f"Generated: {prompt}", use_container_width=True)
                
                # Download Button
                st.download_button(
                    label="⬇️ Download Image",
                    data=image_bytes,
                    file_name=f"generated_image_{int(time.time())}.jpg",
                    mime="image/jpeg"
                )
                st.success("Refreshed successfully!")
            else:
                st.error(f"Server returned error: {response.status_code}")
                
        except Exception as e:
            st.error(f"Connection Error: {e}")

elif generate_btn and not prompt:
    st.warning("Please enter a prompt first!")

# --- Footer ---
st.markdown("---")
st.caption("Powered by [Pollinations.ai](https://pollinations.ai) • Built with Streamlit")