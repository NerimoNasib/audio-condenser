import os
import subprocess
from pydub import AudioSegment, silence

SUPPORTED_FORMATS = (".mkv", ".mp4", ".mp3", ".mov", ".avi", ".webm")
AUDIO_FORMATS = (".mp3", ".wav", ".flac", ".ogg")

def extract_audio(input_file, audio_file):
    if input_file.endswith(AUDIO_FORMATS):
        command = ["ffmpeg", "-i", input_file, "-vn", "-acodec", "copy", audio_file, "-y"]
    else:
        command = ["ffmpeg", "-i", input_file, "-q:a", "0", "-map", "a", audio_file, "-y"]

    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = process.stderr.strip().split("\n")
    last_lines = "\n".join(output_lines[-2:])
    print(last_lines)


def condense_audio(input_file, output_file, silence_threshold=-40, min_silence_len=500):
    silence_threshold = int(input("Silence threshold (default -40 dB): ") or silence_threshold)
    min_silence_len = int(input("Minimum silence length in ms (default 500): ") or min_silence_len)
    print(f"Condensing: {input_file}")
    audio = AudioSegment.from_file(input_file, format="mp3")
    chunks = silence.split_on_silence(audio, silence_thresh=silence_threshold, min_silence_len=min_silence_len)

    condensed_audio = AudioSegment.silent(duration=0)
    for chunk in chunks:
        condensed_audio += chunk

    condensed_audio.export(output_file, format="mp3")
    print(f"Saved: {output_file}")

def process_files():
    for file in os.listdir():
        if file.lower().endswith(SUPPORTED_FORMATS):
            base_name, _ = os.path.splitext(file)
            audio_file = f"{base_name}_audio.mp3"
            output_file = f"{base_name}_condensed.mp3"
            print(f"Processing: {file}")
            extract_audio(file, audio_file)
            condense_audio(audio_file, output_file)
            os.remove(audio_file)

process_files()
