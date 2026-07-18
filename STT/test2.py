import sounddevice as sd
import soundfile as sf

print(sd.query_devices())

device = int(input("Enter microphone index: "))

print("Speak for 5 seconds...")

audio = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    dtype="int16",
    device=device
)

sd.wait()

sf.write("test.wav", audio, 16000)

print("Saved test.wav")