# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("automatic-speech-recognition", model="m3hrdadfi/wav2vec2-large-xlsr-persian-v3")

def speech2text(fname):
    return pipe(fname)