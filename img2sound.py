from PIL import Image
import numpy as np
from scipy.io.wavfile import write
import scipy.signal

def generate_smooth_chime(frequency, duration, sample_rate, volume=0.5):
    """Generates a smooth sine wave with a gentle envelope and harmonic overtones."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    envelope = np.sin(np.pi * t / duration)  # Smooth fade in and out
    wave = volume * envelope * np.sin(2 * np.pi * frequency * t)
    
    # Add gentle harmonic overtones
    wave += 0.2 * envelope * np.sin(4 * np.pi * frequency * t)  # First overtone
    wave += 0.1 * envelope * np.sin(6 * np.pi * frequency * t)  # Second overtone
    
    return wave

def add_reverb(wave, sample_rate, reverb_time=0.5):
    """Adds a simple reverb effect to the audio signal."""
    # Create a reverb impulse response (simple exponential decay)
    delay = int(reverb_time * sample_rate)
    reverb_filter = np.zeros(delay + 1)
    reverb_filter[0] = 1
    reverb_filter[1] = 0.5  # Decay factor
    
    # Apply the filter using convolution
    reverb_wave = scipy.signal.convolve(wave, reverb_filter, mode='full')
    
    return reverb_wave[:len(wave)]  # Trim to the original length

def get_color_frequencies(image_array, num_colors=50):
    """Maps a limited number of colors to specific frequencies."""
    # Convert image to a 2D array of colors
    colors = image_array.reshape(-1, image_array.shape[2])
    
    # Find unique colors and limit to `num_colors`
    unique_colors = np.unique(colors, axis=0)
    if len(unique_colors) > num_colors:
        unique_colors = unique_colors[:num_colors]
    
    # Map colors to frequencies
    frequencies = np.linspace(110, 440, len(unique_colors))  # Map to a frequency range
    color_to_freq = {tuple(color): freq for color, freq in zip(unique_colors, frequencies)}
    return color_to_freq

def image_to_unique_chimes(image_path, output_wav_path, duration=15, sample_rate=44100):
    """Converts an image into unique chime sounds based on its color palette."""
    # Load and resize the image to reduce complexity
    image = Image.open(image_path).convert('RGB')
    image = image.resize((100, 100))  # Resize to reduce the number of colors
    image_array = np.array(image)

    # Get color to frequency mapping
    color_to_freq = get_color_frequencies(image_array)
    
    # Prepare audio signal array
    num_samples = sample_rate * duration
    audio_signal = np.zeros(num_samples)

    # Generate chimes based on image colors
    height, width, _ = image_array.shape
    for y in range(height):
        for x in range(width):
            color = tuple(image_array[y, x])
            if color in color_to_freq:
                frequency = color_to_freq[color]
                chime_duration = np.random.uniform(1, 2)  # Shorter duration for each chime
                start_time = np.random.uniform(0, duration - chime_duration)
                start_sample = int(start_time * sample_rate)
                wave = generate_smooth_chime(frequency, chime_duration, sample_rate, volume=0.3)
                
                # Add reverb
                wave = add_reverb(wave, sample_rate, reverb_time=0.5)
                
                # Add the wave to the audio signal
                end_sample = start_sample + len(wave)
                if end_sample > len(audio_signal):
                    wave = wave[:len(audio_signal) - start_sample]
                audio_signal[start_sample:start_sample + len(wave)] += wave

    # Normalize and save the audio signal
    audio_signal = np.int16(audio_signal / np.max(np.abs(audio_signal)) * 32767)
    write(output_wav_path, sample_rate, audio_signal)
    print(f"WAV file created: {output_wav_path}")

# Example usage
image_path = 'img2.jpg'  # Replace with your image path
output_wav_path = 'unique_chimes_optimized.wav'  # Output WAV file path
image_to_unique_chimes(image_path, output_wav_path, duration=15, sample_rate=44100)
