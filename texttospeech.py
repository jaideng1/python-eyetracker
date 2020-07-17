import speech_recognition as sr

r = sr.Recognizer()
commands = []

while True:
    with sr.Microphone() as source: # use the default microphone as the audio source
        audio = r.listen(source) # listen for the first phrase and extract it into audio data
    try:
        said = r.recognize_google(audio);
        print("You said " + said) # recognize speech using Google Speech Recognition
        #command.push(said);
    except LookupError: # speech is unintelligible
        print("Could not understand audio")
    
