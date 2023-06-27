import PySimpleGUI as sg
import re
import os
from tqdm import tqdm
from pytube import YouTube
from moviepy.editor import *
sg.theme('Dark')

# Print logo
#region Print ASCII art. I put it in a function to collapse it all.
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
#endregion

# Functions
#region Functions

def FunCom(lame, fun):
    if not values['-FUN_COM-']:
        print(lame)
    else:
        print("\nBapll - "+fun)

def VideoToAudio(mp4, mp3):
    FunCom("Converting tmp mp4 to mp3 using MoviePy","Bapll - Okay, I dunno how to convert videos to audio, so Imma call up one of my good buddies to help me... MOVIEPYYYYY!\n")
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()
    FunCom("Conversion complete","Bapll - Awww, thanks bestie! <3")

def GenerateUniqueFileName(directory, base_filename):
    counter = 1
    filename = base_filename + f"-{counter}"
    if not os.path.exists(directory):
        os.mkdir(directory)
    while any(file.startswith(filename) for file in os.listdir(directory)):
        counter += 1
        filename = f"{base_filename}-{counter}"
    filename = f"{base_filename}-{counter}"
    FunCom(f"Unique filename generated: {filename}",f"Bapll - I generated cool and unique file name: {filename}")
    return filename

def FormatSeconds(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # Add leading zeros if necessary
    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)

    # Return as a formatted string
    return f"{hours_str}:{minutes_str}:{seconds_str}"

def UpdateDownloadProgress(stream, chunk, bytes_remaining):
    # Calculate the progress percentage
    bytes_downloaded = stream.filesize - bytes_remaining
    progress_percentage = (bytes_downloaded / stream.filesize) * 100

    # Update the tqdm progress bar
    progress_bar.update(progress_percentage - progress_bar.n)

def ConvertToSeconds(time, duration):
    time = time.lower()  # Convert the input to lowercase for easier processing
    parts = time.split(',')
    hours = 0
    minutes = 0
    seconds = 0

    for part in parts:
        part = part.strip()  # Remove leading/trailing whitespaces
        if part.endswith('h'):
            hours += int(part.replace('h', ''))
        elif part.endswith('m'):
            minutes += int(part.replace('m', ''))
        elif part.endswith('s'):
            seconds += int(part.replace('s', ''))
        elif part == ('end'):
            seconds = duration

    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def GetAudioOptions():
    # Check if the next line contains audio options
    audio_options = ''
    if current_line + 1 < total_lines:
        next_line = youtube_links[current_line + 1].strip()
        if next_line.startswith('&'):
            audio_options = next_line[1:]
    return audio_options

def ApplyAudioOptions(mp3_file):
    audio_options = GetAudioOptions()

    if audio_options:

        FunCom(f"Applying Audio Options: \"{audio_options}\" using MoviePy",f"\"{audio_options}\"\n^ Ahem! What is this? Well, I'm not doing that... MOVIEPYYY!")

        # Split the audio options based on '&' separator
        options_list = audio_options.split('& ')

        # Load the MP3 file as an AudioFileClip
        audio_clip = AudioFileClip(mp3_file)
        
        # Set the duration of the audio clip
        duration = audio_clip.duration
        
        nameIndex = 0

        # Add the audio before the first start_time
        post = ConvertToSeconds(options_list[0].split(' - ')[0], duration)
        if post < 0 or post > duration:
            FunCom(f"Cutting post ({post}) is out of bounds ({duration})", f"Houston, we have a problem. It seems that the cutting post ({post}) is trying to escape the duration of the video ({duration})!")
        if post > 0 and post < duration:
            subclip = audio_clip.subclip(0, post)
            nameIndex += 1
            subclip.write_audiofile(f"{filePath}-{nameIndex}.mp3")
        
        # Iterate over the options and apply the cutting
        for i in range(len(options_list) - 1):
            start_time = ConvertToSeconds(options_list[i].split(' - ')[1], duration)
            end_time = ConvertToSeconds(options_list[i+1].split(' - ')[0], duration)
            
            # Ensure the start and end times are within the duration
            start_time = min(start_time, duration)
            end_time = min(end_time, duration)
            
            if start_time >= end_time:
                FunCom(f"Cutting post ({end_time}) overlaps with other cutting post ({start_time})",f"I don't understand this. A cutting post ({start_time}) can't overlap with another ({end_time}), can it?")
            if start_time < 0 or start_time > duration:
                FunCom(f"Cutting post ({start_time}) is out of bounds ({duration})", f"Houston, we have a problem. It seems that the cutting post ({start_time}) is trying to escape the duration of the video ({duration})!")
            if end_time < 0 or end_time > duration:
                FunCom(f"Cutting post ({end_time}) is out of bounds ({duration})", f"Houston, we have a problem. It seems that the cutting post ({stop_time}) is trying to escape the duration of the video ({duration})!")
            if start_time > 0 and start_time < duration and end_time > 0 and end_time < duration:
                subclip = audio_clip.subclip(start_time, end_time)
                nameIndex += 1
                subclip.write_audiofile(f"{filePath}-{nameIndex}.mp3")

        
        # Add the audio after the last end_time        
        post = ConvertToSeconds(options_list[-1].split(' - ')[1], duration)
        if post < 0 or post > duration:
            FunCom(f"Cutting post ({post}) is out of bounds ({duration})", f"Houston, we have a problem. It seems that the cutting post ({post}) is trying to escape the duration of the video ({duration})!")
        if post > 0 and post < duration:
            subclip = audio_clip.subclip(post, duration)
            nameIndex += 1
            subclip.write_audiofile(f"{filePath}-{nameIndex}.mp3")

        # Close the audio clips
        audio_clip.close()
        subclip.close()

        FunCom("Audio options successfully aplied","Oh, he's done. Good job, MoviePy!")
        FunCom("Removing original mp3","Hey, MoviePy... You forgot to de- oh, forget it. I'll just delete the original mp3... Hold oooon.")
        os.remove(filePath + ".mp3")
        FunCom("mp3 removed","There we go.")

def GetCutDuration(duration):
    audio_options = GetAudioOptions()

    cut_time = 0

    if audio_options:

        FunCom(f"Accounting for: \"{audio_options}\"",f"I see you have some Audio Options here... \"{audio_options}\". You're not using all of the audio?")

        # Split the audio options based on '&' separator
        options_list = audio_options.split('& ')
        
        # Iterate over the options and apply the cutting
        for i in range(len(options_list)):
            times_list = options_list[i].split(' - ')
            start_time = ConvertToSeconds(times_list[0], duration)
            end_time = ConvertToSeconds(times_list[1], duration)
            cut_time += end_time - start_time

        FunCom(f"Cut off {FormatSeconds(cut_time)}",f"There we go, I removed {FormatSeconds(cut_time)} from the clip!")
        return cut_time
    else:
        return 0


def DownloadVideo(video, fileName):
    try:
        # Download the video
        video.download(filename=fileName + ".mp4", output_path=f"{path}/{authorName}")

        # Replace the progress bar with a completion message
        progress_bar.bar_format = f"Downloaded {fileName}.mp4 successfully"

        # Close the progress bar
        progress_bar.close()
    except pytube.exceptions.AgeRestricted:
        FunCom("Age-restricted video detected", "Hold on, bro! This video is age-restricted.")

#endregion

# Create the Window
#region Create the Window
layout = [
            [sg.Text('Ayo, bro! What are we downloading?')],
            [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True ,key='-PATH-'), sg.FolderBrowse()],
            [sg.Text('Select .txt file with YouTube links (line separated)'), sg.InputText(size=(15,1), key='-FILE-'), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
            [sg.Checkbox('Download highest res video (No audio)', key='-DOWNLOAD_VIDEO-', enable_events=True), sg.Checkbox('Also download audio', key='-DOWNLOAD_AUDIO-', visible=False, enable_events=True)],
            [sg.Checkbox('You want my funny commentary?', key='-FUN_COM-')],
            [sg.Button('Download'), sg.Button('Check Duration')]
]

window = sg.Window('Bapll\'s Batch Youtube Downloader', layout)
#endregion

# While the PySimpleGUI is active
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    # Choose folder
    if event == '-PATH-':
        path = values['-PATH-']

    # The Video checkbox
    if event == '-DOWNLOAD_VIDEO-':
        # Toggle visibility of the 'Also download audio' checkbox
        window['-DOWNLOAD_AUDIO-'].update(visible=values['-DOWNLOAD_VIDEO-'])

    if event == "Check Duration":
        # Guard Clauses
        #region Guard Clauses
        if not values['-FILE-']:
            FunCom("Please Select a txt file","WHAT excactly are we downloading? Come on, gimme something to work with!")
            continue
        #endregion


        # Processing the Inputted Data
        #region Processing the Inputted Data
        # Get the file path entered by the user
        file_path = values['-FILE-']  


        # Read all the YouTube links from the file
        with open(file_path, 'r') as file:
            youtube_links = file.readlines()  

        total_lines = len(youtube_links)  # Total number of YouTube links
        current_line = 0  # Initialize current link counter
        current_links = 0
        

        # Count links
        total_links = 0
        for link in youtube_links:
            if not link.strip().startswith("#") and not link.strip().startswith("&") and re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link): 
                total_links += 1
        FunCom(f"\nFound {total_links} links",f"Imma check those durations for ya on all {total_links} videos!")
        print("\n=======================================================================================================================")

        #endregion

        author_durations = {}

        # For every link in the file
        for link in youtube_links:
            link = link.strip()

            # Commenting
            #region Handle Commenting
            if link.startswith("#"):
                current_line += 1
                if link.startswith("##"):
                    print("\n" + link.split('##')[1])
                    print("\n=======================================================================================================================")
                continue
            
            if not link or link.startswith('&'):
                current_line += 1
                continue
            #endregion

            # Validate the link
            if re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link):
                
                # Finding the video
                #region Finding the video
                video = YouTube(link)

                # Rest of your code for downloading and converting the video
                FunCom(f"Video from \"{video.author}\" called \"{video.title}\" was found",f"I found a video from \"{video.author}\" called \"{video.title}\"!")
                FunCom(f"   Duration: {FormatSeconds(video.length)}",f"It's like {FormatSeconds(video.length)} long.")
                
                #endregion

                authorName = re.sub('[\W_]+', '', video.author)
                duration = video.length - GetCutDuration(video.length)

                if authorName not in author_durations:
                    author_durations[authorName] = duration
                else:
                    author_durations[authorName] += duration

                # Set Stats for the program
                #region Set Stats for the program
                current_line += 1
                current_links += 1
                links_left = total_links - current_links
                FunCom(f"\nThe video has been scanned\n\n   [{current_links}/{total_links} videos completed]",f"Ayo, this one's done! Only like {links_left} to go...")
                print("\n=======================================================================================================================")
                #endregion
            else:
                # If this is not a video, a comment or audio setting.
                FunCom(f"\n\"{link}\" isn't a YouTube link!",f"Heeeeeyy, wait a minute... \"{link}\" isn't a YouTube link you sillybilly!")
                print("\n=======================================================================================================================")

        FunCom(f"\n   All {total_links} links scanned",f"Heeeeyyy, 0 to go means I'm finished with all {total_links} now! :D")
         # Print the total duration for each author
        for author, duration in author_durations.items():
            print(f"{author}: {FormatSeconds(duration)}")

        print("\n=======================================================================================================================")


    # Event click download button
    if event == 'Download':

        # Guard Clauses
        #region Guard Clauses
        if not values['-PATH-']:
            FunCom("Please Select an output location","And where excactly am I supposed to put the stuff I'm SO KINDLY downloading FOR you?")
            continue

        if not values['-FILE-']:
            FunCom("Please Select a txt file","WHAT excactly are we downloading? Come on, gimme something to work with!")
            continue
        
        #endregion


        # Processing the Inputted Data
        #region Processing the Inputted Data
        # Get the file path entered by the user
        file_path = values['-FILE-']  


        # Read all the YouTube links from the file
        with open(file_path, 'r') as file:
            youtube_links = file.readlines()  

        total_lines = len(youtube_links)  # Total number of YouTube links
        current_line = 0  # Initialize current link counter
        current_links = 0
        

        # Count links
        total_links = 0
        for link in youtube_links:
            if not link.strip().startswith("#") and not link.strip().startswith("&") and re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link): 
                total_links += 1
        FunCom(f"\nFound {total_links} links",f"Readying up for downloading {total_links} thingies!")
        print("\n=======================================================================================================================")

        #endregion

        # For every link in the file
        for link in youtube_links:
            link = link.strip()

            # Commenting
            #region Handle Commenting
            if link.startswith("#"):
                current_line += 1
                if link.startswith("##"):
                    print("\n" + link.split('##')[1])
                    print("\n=======================================================================================================================")
                continue
            
            if not link or link.startswith('&'):
                current_line += 1
                continue
            #endregion

            # Validate the link
            if re.search(r'\byoutube.com\b', link) or re.search(r'\byoutu.be\b', link):
                
                # Finding the video
                #region Finding the video
                video = YouTube(link, on_progress_callback = UpdateDownloadProgress)

                # Rest of your code for downloading and converting the video
                FunCom(f"Video from \"{video.author}\" called \"{video.title}\" was found",f"I found a video from \"{video.author}\" called \"{video.title}\"!")
                FunCom(f"   Duration: {FormatSeconds(video.length)}",f"It's like {FormatSeconds(video.length)} long.")
                
                #endregion

                # Define Path Variables
                #region Path Variables
                authorName = re.sub('[\W_]+', '', video.author)

                fileName = GenerateUniqueFileName(f"{path}/{authorName}", authorName)

                filePath = f"{path}/{authorName}/{fileName}"
                #endregion
                
                if not values['-DOWNLOAD_VIDEO-'] or values['-DOWNLOAD_VIDEO-'] and values['-DOWNLOAD_AUDIO-']:
                    
                    #Download the low res video
                    #region Download the low res video
                    FunCom("Downloading low res tmp mp4","Imma download a temporary low res video for the audio. Hold on a minute, okay?\n")
                    
                    # Set up the tqdm progress bar
                    progress_bar = tqdm(total=100, unit='%', ncols=80, bar_format='Downloading:  {l_bar}{bar}{r_bar}', initial=0)

                    DownloadVideo(video.streams.filter(only_audio=True).first(),fileName)

                    FunCom("\nDownload complete","\nI'm dooooone!")

                    FunCom(f"   path: \"{filePath}.mp4\"",f"I put it here: \"{filePath}.mp4\"")
                    #endregion
                    
                    # Convert to mp3
                    VideoToAudio(f"{filePath}.mp4", f"{filePath}.mp3")

                    # Remove mp4
                    os.remove(filePath + ".mp4")
                    FunCom("Deleting tmp mp4","I'm deleting that low res video, so you don't have to deal with that...")

                    ApplyAudioOptions(f"{filePath}.mp3")

                if  values['-DOWNLOAD_VIDEO-']:
                    
                    # Download High res video
                    #region Download High res video
                    FunCom("Downloading highest res mp4","I'm downloading the highest res video I can find now!")

                    # Set up the tqdm progress bar
                    progress_bar = tqdm(total=100, unit='%', ncols=80, bar_format='Downloading:  {l_bar}{bar}{r_bar}', initial=0)
                    DownloadVideo(video.streams.order_by('resolution').desc().first())

                    FunCom("\nDownload complete","\nI'm fiiiiiiniiiished!")
                    FunCom(f"   path: \"{filePath}.mp4\"",f"I put it here: \"{filePath}.mp4\"")
                    #endregion
                
                # Set Stats for the program
                #region Set Stats for the program
                current_line += 1
                current_links += 1
                links_left = total_links - current_links
                FunCom(f"\nThe job \"{fileName}\" has been completed!\n\n   [{current_links}/{total_links} jobs completed]",f"Ayo, this one's done! Only like {links_left} to go...")
                print("\n=======================================================================================================================")
                #endregion
            else:
                # If this is not a video, a comment or audio setting.
                FunCom(f"\n\"{link}\" isn't a YouTube link!",f"Heeeeeyy, wait a minute... \"{link}\" isn't a YouTube link you sillybilly!")
                print("\n=======================================================================================================================")

        FunCom(f"\n   All {total_links} jobs done",f"Heeeeyyy, 0 to go means I'm finished with all {total_links} now! :D")
        print("\n=======================================================================================================================")
window.close()