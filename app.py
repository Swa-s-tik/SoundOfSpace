import streamlit as st
import os
import tempfile
from PIL import Image
import numpy as np
from scipy.io.wavfile import write
import scipy.signal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# SkyView image fetching functions
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def fetch_skyview_image(coords):
    driver = setup_driver()
    driver.get("https://skyview.gsfc.nasa.gov/current/cgi/query.pl")
    
    # Input the coordinates
    input_element = driver.find_element(By.ID, "object")
    input_element.send_keys(coords)
    
    # Select "RXTE Allsky 3-20keV Flux" from the dropdown with the class 'selectbox' and ID 'HardX-ray'
    select_element = driver.find_element(By.ID, "HardX-ray")  # ID of the select element
    select = Select(select_element)
    
    # Select the option with visible text "RXTE Allsky 3-20keV Flux"
    select.select_by_visible_text("RXTE Allsky 3-8keV Flux")
    
    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//input[@value='Submit Request']")
    submit_button.click()
    
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    
    # Wait for the image to be present
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "img1")))
    
    # Get the image URL and download the image
    img_element = driver.find_element(By.ID, "img1")
    img_url = img_element.get_attribute("src")
    
    # Download the image
    temp_dir = tempfile.mkdtemp()
    img_path = os.path.join(temp_dir, "skyview_image.jpg")
    urllib.request.urlretrieve(img_url, img_path)
    
    driver.quit()
    return img_path

# Audio generation functions
def generate_smooth_chime(frequency, duration, sample_rate, volume=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    envelope = np.sin(np.pi * t / duration)
    wave = volume * envelope * np.sin(2 * np.pi * frequency * t)
    wave += 0.2 * envelope * np.sin(4 * np.pi * frequency * t)
    wave += 0.1 * envelope * np.sin(6 * np.pi * frequency * t)
    return wave

def add_reverb(wave, sample_rate, reverb_time=0.5):
    delay = int(reverb_time * sample_rate)
    reverb_filter = np.zeros(delay + 1)
    reverb_filter[0] = 1
    reverb_filter[1] = 0.5
    reverb_wave = scipy.signal.convolve(wave, reverb_filter, mode='full')
    return reverb_wave[:len(wave)]

def get_color_frequencies(image_array, num_colors=50):
    colors = image_array.reshape(-1, image_array.shape[2])
    unique_colors = np.unique(colors, axis=0)
    if len(unique_colors) > num_colors:
        unique_colors = unique_colors[:num_colors]
    frequencies = np.linspace(110, 440, len(unique_colors))
    color_to_freq = {tuple(color): freq for color, freq in zip(unique_colors, frequencies)}
    return color_to_freq

def image_to_unique_chimes(image_path, duration=15, sample_rate=44100):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((100, 100))
    image_array = np.array(image)

    color_to_freq = get_color_frequencies(image_array)
    
    num_samples = sample_rate * duration
    audio_signal = np.zeros(num_samples)

    height, width, _ = image_array.shape
    for y in range(height):
        for x in range(width):
            color = tuple(image_array[y, x])
            if color in color_to_freq:
                frequency = color_to_freq[color]
                chime_duration = np.random.uniform(1, 2)
                start_time = np.random.uniform(0, duration - chime_duration)
                start_sample = int(start_time * sample_rate)
                wave = generate_smooth_chime(frequency, chime_duration, sample_rate, volume=0.3)
                wave = add_reverb(wave, sample_rate, reverb_time=0.5)
                end_sample = start_sample + len(wave)
                if end_sample > len(audio_signal):
                    wave = wave[:len(audio_signal) - start_sample]
                audio_signal[start_sample:start_sample + len(wave)] += wave

    audio_signal = np.int16(audio_signal / np.max(np.abs(audio_signal)) * 32767)
    return audio_signal, sample_rate

# Streamlit app
def main():
    st.title("SkyView to Audio Converter")
    
    coords = st.text_input("Enter coordinates (format: 161.265, -59.685)", "161.265, -59.685")
    
    if st.button("Generate Image and Audio"):
        with st.spinner("Fetching SkyView image..."):
            img_path = fetch_skyview_image(coords)
        
        st.image(img_path, caption="SkyView Image", use_column_width=True)
        
        with st.spinner("Generating audio..."):
            audio_signal, sample_rate = image_to_unique_chimes(img_path)
            
            temp_dir = tempfile.mkdtemp()
            audio_path = os.path.join(temp_dir, "skyview_audio.wav")
            write(audio_path, sample_rate, audio_signal)
        
        st.audio(audio_path, format="audio/wav")
        
        st.success("Image and audio generated successfully!")

if __name__ == "__main__":
    main()