import os
import time
import playsound
from transformers import pipeline
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import sentencepiece as spm
from datasets import load_dataset
from gtts import gTTS
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf
from IPython.display import display, Audio #IPython.display need to run on Jupyter environment
import random
import string
import numpy as np
import soundfile as sf
import torch
import gradio as gr

# load the pipeline
transcriber = pipeline("automatic-speech-recognition",model="openai/whisper-base.en")
# load device
device = "cuda" if torch.cuda.is_available() else "cpu"
# load the processor
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
# load the model
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
# load the vocoder, that is the voice encoder
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)
# we load this dataset to get the speaker embeddings
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
# speaker ids from the embeddings dataset
speakers = {
    'awb': 0,     # Scottish male
    'bdl': 1138,  # US male
    'clb': 2271,  # US female
    'jmk': 3403,  # Canadian male
    'ksp': 4535,  # Indian male
    'rms': 5667,  # US male
    'slt': 6799   # US female
}

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def save_text_to_speech(text, speaker=None, soundPlay=None):
    # preprocess text
    inputs = processor(text=text, return_tensors="pt").to(device)
    if speaker is not None:
        # load xvector containing speaker's voice characteristics from a dataset
        speaker_embeddings = torch.tensor(embeddings_dataset[speaker]["xvector"]).unsqueeze(0).to(device)
    else:
        # random vector, meaning a random voice
        speaker_embeddings = torch.randn((1, 512)).to(device)
    # generate speech with the models
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
    if speaker is not None:
        # if we have a speaker, we use the speaker's ID in the filename
        output_filename = f"{speaker}-{'-'.join(text.split()[:6])}.wav"
    else:
        # if we don't have a speaker, we use a random string in the filename
        random_str = ''.join(random.sample(string.ascii_letters+string.digits, k=5))
        output_filename = f"{random_str}-{'-'.join(text.split()[:6])}.wav"
    # save the generated speech to a file with 16KHz sampling rate
    sf.write(output_filename, speech.cpu().numpy(), samplerate=16000)

    # Load the file on an object
    data = wavfile.read(output_filename)
    print(data) #from wavfile read the output is a tuple with rate and numarray and dtype
    # Separete the object elements
    framerate = data[0]
    sounddata = data[1]
    time_audio      = np.arange(0,len(sounddata))/framerate
    # Show information about the object
    print('Sample rate:',framerate,'Hz')
    print('Total time:',len(sounddata)/framerate,'s')

    if soundPlay:
      #if sound play is active, play sound
      # for playing sound data
      wn= Audio(sounddata,rate=framerate, autoplay=True)
      display(wn)
      print('playing sound using pydub')
    else:
      print("sound play is not active")

    # return the filename for reference
    return output_filename

# def get_audio():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         said = ""

#         try:
#             said = r.recognize_google(audio)
#             print(said)
#         except Exception as e:
#             print("Exception: " + str(e))

#     return said

# text = get_audio()

# if "hi chatbot" in text:
#     speak("turning on the chatbot.")


# handles audio processing and transcription
# takes a streaming audio chunk : new_chunck
# returns the transcribed text

def transcribe(stream, new_chunck):
  sr,y = new_chunck
  y = y.astype(np.float32)
  y /= np.max(np.abs(y))

  if stream is not None:
    stream = np.concatenate([stream,y])
  else:
    stream = y
  transcription = transcriber({"sampling_rate":sr,"raw":stream})["text"]
  return stream, transcription


def store_transcription(new_transcription):
    transcribed_text=[] 
    transcribed_text[:] = new_transcription
    return transcribed_text

def is_chatbot(text):
   if text.count('chatbot') >= 1:
      return True
      
demo = gr.Interface(
    transcribe,
    ["state", gr.Audio(sources=["microphone"], streaming=True)], # sets up the microphone as the audio source for streaming
    ["state","text"],
    live = True,
)

demo.launch()


    