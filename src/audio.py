import pyaudio
import wave

CHUNK = 1024  # Number of frames in a buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

audio = pyaudio.PyAudio()

# Open an audio stream
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
)

print("Recording...")

frames = []
num_frames_to_record = int(RATE / CHUNK * 5)

for i in range(num_frames_to_record):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# Stop and close the audio stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio object
audio.terminate()

# Save the recorded audio to a WAV file (optional)
with wave.open("output.wav", "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
