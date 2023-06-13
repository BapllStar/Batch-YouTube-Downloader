import PySimpleGUI as sg
import re
import os
from pytube import YouTube
from moviepy.editor import *
sg.theme('Dark')

print(" /$$$$$$$                     /$$ /$$ /$$             /$$$$$$$             /$$               /$$      ")
print("| $$__  $$                   | $$| $$| $/            | $$__  $$           | $$              | $$      ")
print("| $$  \ $$ /$$$$$$   /$$$$$$ | $$| $$|_/$$$$$$$      | $$  \ $$ /$$$$$$  /$$$$$$    /$$$$$$$| $$$$$$$ ")
print("| $$$$$$$ |____  $$ /$$__  $$| $$| $$ /$$_____/      | $$$$$$$ |____  $$|_  $$_/   /$$_____/| $$__  $$")
print("| $$__  $$ /$$$$$$$| $$  \ $$| $$| $$|  $$$$$$       | $$__  $$ /$$$$$$$  | $$    | $$      | $$  \ $$")
print("| $$  \ $$/$$__  $$| $$  | $$| $$| $$ \____  $$      | $$  \ $$/$$__  $$  | $$ /$$| $$      | $$  | $$")
print("| $$$$$$$/  $$$$$$$| $$$$$$$/| $$| $$ /$$$$$$$/      | $$$$$$$/  $$$$$$$  |  $$$$/|  $$$$$$$| $$  | $$")
print("|_______/ \_______/| $$____/ |__/|__/|_______/       |_______/ \_______/   \___/   \_______/|__/  |__/")
print("                   | $$                                                                               ")
print(" /$$     /$$       | $$   /$$$$$$$$        /$$                                                        ")
print("|  $$   /$$/       |__/  |__  $$__/       | $$                                                        ")
print(" \  $$ /$$/$$$$$$  /$$   /$$| $$ /$$   /$$| $$$$$$$   /$$$$$$                                          ")
print("  \  $$$$/$$__  $$| $$  | $$| $$| $$  | $$| $$__  $$ /$$__  $$                                         ")
print("   \  $$/ $$  \ $$| $$  | $$| $$| $$  | $$| $$  \ $$| $$$$$$$$                                         ")
print("    | $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$| $$_____/                                         ")
print("    | $$|  $$$$$$/|  $$$$$$/| $$|  $$$$$$/| $$$$$$$/|  $$$$$$$                                         ")
print("    |__/ \______/  \______/ |__/ \______/ |_______/  \_______/                                         ")
print(" /$$$$$$$                                    /$$                          /$$                          ")
print("| $$__  $$                                  | $$                         | $$                          ")
print("| $$  \ $$  /$$$$$$  /$$  /$$  /$$ /$$$$$$$ | $$  /$$$$$$  /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$      ")
print("| $$  | $$ /$$__  $$| $$ | $$ | $$| $$__  $$| $$ /$$__  $$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$     ")
print("| $$  | $$| $$  \ $$| $$ | $$ | $$| $$  \ $$| $$| $$  \ $$ /$$$$$$$| $$  | $$| $$$$$$$$| $$  \__/     ")
print("| $$  | $$| $$  | $$| $$ | $$ | $$| $$  | $$| $$| $$  | $$/$$__  $$| $$  | $$| $$_____/| $$           ")
print("| $$$$$$$/|  $$$$$$/|  $$$$$/$$$$/| $$  | $$| $$|  $$$$$$/  $$$$$$$|  $$$$$$$|  $$$$$$$| $$           ")
print("|_______/  \______/  \_____/\___/ |__/  |__/|__/ \______/ \_______/ \_______/ \_______/|__/           ")
print("\n\n=======================================================================================================================")


def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

layout = [
            [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Text('Select .txt file with YouTube links (line separated)'), sg.InputText(size=(15,1), key='-FILE-'), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
            [sg.Button('Download'), sg.Button('Cancel')
        ]
]

def generate_unique_filename(directory, base_filename):
    counter = 1
    filename = base_filename + f"-{counter}"
    while os.path.exists(os.path.join(directory, filename + ".mp3")):
        counter += 1
        filename = f"{base_filename}-{counter}"
    filename = f"{base_filename}-{counter}"
    print("\nBapll - Generated file name: " + filename)
    return filename

def convert_seconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # Add leading zeros if necessary
    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)

    # Return as a formatted string
    return f"{hours_str}:{minutes_str}:{seconds_str}"

# Create the Window
window = sg.Window('Bapll\'s Batch Youtube Downloader', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    if event == '-FOLDER-':
        path = values['-FOLDER-']
    if event == 'Download':
        file_path = values['-FILE-']  # Get the file path entered by the user
        with open(file_path, 'r') as file:
            youtube_links = file.readlines()  # Read all the YouTube links from the file
        total_links = len(youtube_links)  # Total number of YouTube links
        current_link = 0  # Initialize current link counter
        for link in youtube_links:
            link = link.strip()  # Remove leading/trailing whitespace and newline characters
            if re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link):
                video = YouTube(link)
                # Rest of your code for downloading and converting the video
                print("\nBapll - Video from \"" + video.author + "\" called \"" + video.title + "\" was found!")
                print("   Duration: " + convert_seconds(video.length))
                # Remember to add duration of the video to this ^

                authorName = re.sub('[\W_]+', '', video.author)

                fileName = generate_unique_filename(path + "/" + authorName, authorName)

                print("\n" + fileName + " - Downloading. Please be patient...")

                # Donwloading the video  
                video.streams.filter(only_audio = True).first().download(filename = fileName + ".mp4", output_path = path + "/" + authorName)
                print("\n" + fileName + " - Download complete!")
    
                
                filePath = path + "/" + authorName + "/" + fileName
                print("   path: \"" + filePath + ".mp4\"")
                # Convert to mp3
                print("\n" + fileName + " - Converting to mp3 file. Initiating MoviePy...")
                MP4ToMP3(filePath + ".mp4", filePath + ".mp3")
                print("\n" + fileName + " - Conversion complete!")

                # Remove mp4
                os.remove(filePath + ".mp4")
                print("\n" + fileName + " - Deleted temporary mp4-file")
                current_link += 1

                print("\n - The job \"" + fileName + "\" has been completed!" + f"\n\n   [{current_link}/{total_links} tasks completed]\n\n=======================================================================================================================")
            else:
                print("\n \"" + link + "\" isn't a YouTube link!\n\n=======================================================================================================================")
        print("\nBapll - Your program has finished :D\n\n=======================================================================================================================")
window.close()