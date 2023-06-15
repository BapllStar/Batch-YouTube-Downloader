import PySimpleGUI as sg
import re
import os
from tqdm import tqdm
from pytube import YouTube
from moviepy.editor import *
sg.theme('Dark')

# Print ASCII art
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

layout = [
            [sg.Text('Ayo, bro! What are we downloading?')],
            [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Text('Select .txt file with YouTube links (line separated)'), sg.InputText(size=(15,1), key='-FILE-'), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
            [sg.Checkbox('Download highest res video (No audio)', key='-FULL_RES-', enable_events=True), sg.Checkbox('Also download audio', key='-DOWNLOAD_AUDIO-', visible=False, enable_events=True)],
            [sg.Checkbox('You want my funny commentary?', key='-FUN_COM-')],
            [sg.Button('Download'), sg.Button('Cancel')]
]

def funcom(lame, fun):
    if not values['-FUN_COM-']:
        print(lame)
    else:
        print("\n"+fun)

def MP4ToMP3(mp4, mp3):
    funcom("Converting tmp mp4 to mp3 using MoviePy","Bapll - Okay, I dunno how to convert videos to audio, so Imma call up one of my good buddies to help me... MOVIEPYYYYY!\n")
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
    funcom("Conversion complete","Bapll - Awww, thanks bestie! <3")

def generate_unique_filename(directory, base_filename):
    counter = 1
    filename = base_filename + f"-{counter}"
    while os.path.exists(os.path.join(directory, filename + ".mp3")) or os.path.exists(os.path.join(directory, filename + ".mp4")):
        counter += 1
        filename = f"{base_filename}-{counter}"
    filename = f"{base_filename}-{counter}"
    funcom(f"Unique filename generated: {filename}",f"Bapll - I generated cool and unique file name: {filename}")
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



def progress_callback(stream, chunk, bytes_remaining):
    # Calculate the progress percentage
    bytes_downloaded = stream.filesize - bytes_remaining
    progress_percentage = (bytes_downloaded / stream.filesize) * 100

    # Update the tqdm progress bar
    progress_bar.update(progress_percentage - progress_bar.n)



# Create the Window
window = sg.Window('Bapll\'s Batch Youtube Downloader', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    if event == '-FOLDER-':
        path = values['-FOLDER-']
    if event == '-FULL_RES-':
        # Toggle visibility of the 'Also download audio' checkbox
        window['-DOWNLOAD_AUDIO-'].update(visible=values['-FULL_RES-'])
    if event == 'Download':
        file_path = values['-FILE-']  # Get the file path entered by the user
        with open(file_path, 'r') as file:
            youtube_links = file.readlines()  # Read all the YouTube links from the file
        total_links = len(youtube_links)  # Total number of YouTube links
        current_link = 0  # Initialize current link counter
        for link in youtube_links:
            link = link.strip()  # Remove leading/trailing whitespace and newline characters
            if re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link):
                video = YouTube(link, on_progress_callback = progress_callback)
                # Rest of your code for downloading and converting the video
                funcom(f"Video from \"{video.author}\" called \"{video.title}\" was found",f"Bapll - I found a video from \"{video.author}\" called \"{video.title}\"!")
                funcom(f"   Duration: {convert_seconds(video.length)}",f"Bapll - It's like {convert_seconds(video.length)} long.")

                authorName = re.sub('[\W_]+', '', video.author)

                fileName = generate_unique_filename(f"{path}/{authorName}", authorName)

                filePath = f"{path}/{authorName}/{fileName}"
                
                if not values['-FULL_RES-'] or values['-FULL_RES-'] and values['-DOWNLOAD_AUDIO-']:
                    
                    funcom("Downloading low res tmp mp4","Bapll - Imma download a temporary low res video for the audio. Hold on a minute, okay?\n")
                    # Set up the tqdm progress bar
                    progress_bar = tqdm(total=100, unit='%', ncols=80, bar_format='Downloading:  {l_bar}{bar}{r_bar}', initial=0)

                    # Donwloading the video  
                    video.streams.filter(only_audio = True).first().download(filename = fileName + ".mp4", output_path = f"{path}/{authorName}")
                    
                    # Replace the progress bar with a completion message
                    progress_bar.bar_format = f"Downloaded {fileName}.mp4 successfully"
                    
                    # Close the progress bar
                    progress_bar.close()


                    funcom("\nDownload complete","\nBapll - I'm dooooone!")

                    funcom(f"   path: \"{filePath}.mp4\"",f"Bapll - I put it here: \"{filePath}.mp4\"")
                    
                    # Convert to mp3
                    MP4ToMP3(f"{filePath}.mp4", filePath + ".mp3")

                    # Remove mp4
                    os.remove(filePath + ".mp4")
                    funcom("Deleting tmp mp4","Bapll - I'm deleting that low res video, so you don't have to deal with that...")


                if  values['-FULL_RES-']:
                    funcom("Downloading highest res mp4","Bapll - I'm downloading the highest res video I can find now!")

                    progress_bar = tqdm(total=100, unit='%', ncols=80, bar_format='Downloading:  {l_bar}{bar}{r_bar}', initial=0)

                    video.streams.order_by('resolution').desc().first().download(filename = fileName + ".mp4", output_path = f"{path}/{authorName}")
                    
                    # Replace the progress bar with a completion message
                    progress_bar.bar_format = f"Downloaded {fileName}.mp4 successfully"

                    # Close the progress bar
                    progress_bar.close()
                    funcom("\nDownload complete","\nBapll - I'm fiiiiiiniiiished!")
                    funcom(f"   path: \"{filePath}.mp4\"",f"Bapll - I put it here: \"{filePath}.mp4\"")
                
                current_link += 1
                links_left = total_links - current_link
                funcom(f"\nThe job \"{fileName}\" has been completed!\n\n   [{current_link}/{total_links} tasks completed]",f"Ayo, this one's done! Only like {links_left} to go...")
                print("\n=======================================================================================================================")
            else:
                funcom(f"\n\"{link}\" isn't a YouTube link!",f"Heeeeeyy, wait a minute... \"{link}\" isn't a YouTube link you sillybilly!")
                print("\n=======================================================================================================================")
        funcom(f"\n\n   All {total_links} jobs done",f"\nBapll - Heeeeyyy, 0 to go means I'm finished with all {total_links} now! :D")
        print("\n\n=======================================================================================================================")
window.close()