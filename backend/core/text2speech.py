# install requirements

# !pip install TTS
# !sudo apt-get -y install espeak-ng

# !tts - -text "زندگی فقط یک بار است؛ از آن به خوبی استفاده کن" \
#      - -model_path "best_model_30824.pth" \
#      - -config_path "config.json" \
#      - -out_path "speech1.wav"


from TTS.config import load_config
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import IPython
import shutil

config = "core/config.json"
model = "core/best_model_30824.pth"

model_path = model  # Absolute path to the model checkpoint.pth
config_path = config  # Absolute path to the model config.json


synthesizer = Synthesizer(
    model_path, config_path
)


def text2speech(text):
    wavs = synthesizer.tts(text)
    synthesizer.save_wav(wavs, 'tts/voice.wav')
    # shutil.copyfile('voice.wav', '../Frontend/public/voice.wav')