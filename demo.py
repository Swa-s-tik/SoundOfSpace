import streamlit as st
import os

# Custom CSS for card-like components
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def card(title, content, image_path=None):
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            if image_path:
                st.image(image_path, use_column_width=True)
        with col2:
            st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
            st.write(content)

def main():
    st.set_page_config(page_title="The Sound of Space", page_icon="🌌", layout="wide")
    
    # Apply custom CSS
    local_css("style.css")

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["Home", "Our Project", "Experience Space", "Interactive Demo"])

    if page == "Home":
        st.title("Welcome to The Sound of Space Project")
        st.write("""
        Explore the cosmos through sound! Our project transforms NASA's open-source astronomical data 
        into unique auditory experiences, allowing you to hear the wonders of the universe.
        """)

        col1, col2 = st.columns(2)
        with col1:
            card("Our Goal", """
            Create a unique intersection between science and art, making space data more accessible 
            and engaging through immersive auditory experiences.
            """)
        with col2:
            card("Our Vision", """
            Redefine how we experience space by transforming astronomical data into multisensory 
            experiences, inspiring curiosity and fostering a deeper connection with the cosmos.
            """)

    elif page == "Our Project":
        st.title("About Our Project")
        
        with st.expander("What Our Project Does", expanded=True):
            st.write("""
            The SkyView-to-Audio Converter transforms NASA's SkyView images into unique soundscapes. 
            It processes visual representations of astronomical phenomena and maps them to corresponding audio frequencies.
            """)
            st.markdown("""
            - Input coordinates of celestial objects
            - Fetch NASA SkyView images
            - Convert visual characteristics into sound chimes
            - Listen to audio representations of cosmic data
            """)

        with st.expander("How It Works", expanded=False):
            st.write("Our process involves three main steps:")
            col1, col2, col3 = st.columns(3)
            with col1:
                card("1. Fetching Images", "We use NASA's SkyView tool to obtain astronomical images based on user-input coordinates.")
            with col2:
                card("2. Image-to-Audio Conversion", "We process the image and map colors to audio frequencies, generating unique sound chimes.")
            with col3:
                card("3. Audio Enhancement", "We add effects like reverb to create an immersive cosmic soundscape.")

    elif page == "Experience Space":
        st.title("Experience the Sounds of Space")
        st.write("Explore these examples of space images and their corresponding audio representations:")



        for i in range(6):
            with st.container():
                col1, col2 = st.columns([2, 3])
                with col1:
                    image_path = os.path.join("images", f"space_object_{i}.jpg")
                    if os.path.exists(image_path):
                        st.image(image_path)
                    
                with col2:
                    audio_path = os.path.join("audio", f"space_object_{i}.wav")
                    if os.path.exists(audio_path):
                        st.audio(audio_path, format="audio/wav", start_time=0)

                st.markdown("---")
    elif page == "Interactive Demo":
        st.title("Interactive Space Sound Generator")
        st.write("Input celestial coordinates to generate a unique cosmic soundscape!")

        col1, col2 = st.columns(2)
        with col1:
            ra = st.number_input("Right Ascension (degrees)", min_value=0.0, max_value=360.0, value=180.0)
        with col2:
            dec = st.number_input("Declination (degrees)", min_value=-90.0, max_value=90.0, value=0.0)

        if st.button("Generate Soundscape"):
                st.write("Generating soundscape... Coming SOON, Audio Generation model TOO resource intensive to host on any FREE demo platforms!")

if __name__ == "__main__":
    main()