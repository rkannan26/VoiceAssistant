import speech_recognition as sr
import pyttsx3
import requests
import openai

r = sr.Recognizer()
engine = pyttsx3.init()


voices = engine.getProperty('voices')
selected_voice = voices[1]
engine.setProperty('voice', selected_voice.id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.8)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        return None

while True:
    command = listen()
    if command is None:
        continue

    elif "remind me" in command:
        speak("What should I remind you about?")
        reminder = listen()
        speak(f"Sure! I'll remind you to do that {reminder} later.")
    elif "create a to-do list" in command:
        speak("What tasks do you want to add to the to-do list?")
        tasks = []
        while True:
            task = listen()
            if "stop" in task:
                break
            tasks.append(task)
        speak("Here's your to-do list:")
        for i, task in enumerate(tasks):
            speak(f"{i+1}: {task}")
    elif "search for" in command:
        query = command.replace("search for", "")
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url)
        data = response.json()
        if 'Abstract' in data and data['Abstract']:
            abstract = data['Abstract']
            speak(abstract)
        elif 'RelatedTopics' in data and data['RelatedTopics']:
            related_topics = data['RelatedTopics']
            first_topic = related_topics[0]
            speak(first_topic['Text'])
        else:
            speak(f"Sorry, I couldn't find any information about {query}.")

    elif "hello" in command:
       speak("Hi! What would you like me to do today? I can remind you to do something, create a to-do list, or search for something on the web. Say quit or exit to stop talking.")

    elif "quit" in command or "exit" in command:
        speak("Goodbye!")
        break
    else:
        speak("I'm sorry, I didn't understand that. Can you please repeat?")

"""

    openai.api_key = "OPENAI API KEY GOES HERE"

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": command}])
    speak(response.choices[0].message.content)
    if any(exit_word in command for exit_word in ["quit", "exit"]):
        break

    """
