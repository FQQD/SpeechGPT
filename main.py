import speech_recognition as sr
import time
import sounddevice
from gtts import gTTS
from pathlib import Path
import openai
from vlc import MediaPlayer as AudioPlayer

apikeyfile = Path(__file__).with_name('apikey.txt')
with open(apikeyfile, 'r') as token:
    apikey = token.read()


r = sr.Recognizer()
mic = sr.Microphone()

rufwort = "muffins "
rufwort2 = "muffin "

while True:

    with mic as source:
        
        r.adjust_for_ambient_noise(source, duration=0.2)
        
        audio = r.listen(source)
        
        
        try:
            input = r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            output = ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        
        print(input)
        
        if input.lower().startswith(rufwort) or input.lower().startswith(rufwort2):
            print("ich wurde gerufen!")
            gpt_input = input[len(rufwort2):]
            
            init = AudioPlayer("init.mp3")
            init.play()
            time.sleep(1)

            
            wartemusik = AudioPlayer("elev.mp3")
            wartemusik.volume = 10
            wartemusik.play()
            
            openai.api_key = apikey

            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=gpt_input,
            temperature=0.5,
            max_tokens=60,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=[" Human:", " AI:", " You:"]
            )
            
            output=response.choices[0].text.strip()
            
            

            myobj = gTTS(text=output, lang="en", slow=False)
            myobj.save("tts.mp3")
            
            wartemusik.stop()
            
            print(output)
            
            AudioPlayer("tts.mp3").play()
            
        input = ""
        gpt_input = ""
        output = ""
            
        time.sleep(1)