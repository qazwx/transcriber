#!/usr/bin/env python3

import speech_recognition as sr
import os
import sys

from pydub import AudioSegment
from multiprocessing import Pool, cpu_count

# Profiling, just add @profile over a function.
# from profilehooks import profile

# Global constants, I don't want to create n different instances of sr.Recognizer()
RECOGNIZER = sr.Recognizer()
OUT_FOLDER  = os.path.join(os.path.dirname(os.path.realpath(__file__)), "out/")

def chunkify_audio(full_audio_path, chunks_time_size=60000, audio_format="mp3"):
    """
        Defines chunk of a given audio file (encoded specified 
        by audio_format), which location is specified by 
        full_audio_path, by length in time (chunks_time_size 
        is in milliseconds).
        
        It encodes each chunk in `.wav' format saved in OUT_FOLDER,
        for easier use (for SpeechRecognition lib).
    """

    # Load sound from mp3 to a easier format (.wav)
    sound           = AudioSegment.from_file(full_audio_path, format=audio_format)
    # Chunkify audio in chuncks of chunks_time length.
    audio_chunks    = list(sound[::chunks_time_size])
    length          = len(audio_chunks)

    # Defines all names (just number + audio_format)
    directory       = OUT_FOLDER
    names           = [os.path.join(directory, str(x)+".wav") for x in range(length)]
    for chunk,name in zip(audio_chunks, names):   
        chunk.export(name, format="wav")
    
    # Returns all names of the exported audio chuncks.
    return names 

def load_recognize_audio(audio_file_path):
    loaded_audio = None
    with sr.AudioFile(audio_file_path) as source:
        loaded_audio = RECOGNIZER.record(source)

    try:
        return RECOGNIZER.recognize_sphinx(loaded_audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return "<NOT UNDERSTANDEABLE SPEECH>"
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return "<ERROR REQUEST>"

def parallel_process_audio(audio_chuncks):
    
    leng        = len(audio_chuncks)
    agents      = cpu_count()
    
    # Defines a pool with number of CPUs as number of agents. 
    with Pool(processes=agents) as pool:
        return pool.map(load_recognize_audio, audio_chuncks)


def main():
    print(
    """ 
        Transcribing: %a,
        Using Sphinx and chunking (60s) and parallelized %a-times.

        Note: it's not fast nor accurate.
    """ % (sys.argv[1], cpu_count()))

    # Load file path, if the file exist, transcribes
    filepath = sys.argv[1]
    if (not os.path.isfile(filepath)):
        print("Not known file.")
        return 1
    
    song_ext = os.path.splitext(filepath)[1][1:]
    
    names       = chunkify_audio(sys.argv[1], audio_format=song_ext)
    transcribed = parallel_process_audio(names)

    for t in transcribed:
        try:
            print(t)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))


if __name__ == "__main__":
    main()