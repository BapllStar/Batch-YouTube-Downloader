import PySimpleGUI as sg
import re
import os
import math
from tqdm import tqdm
from pytube import YouTube
from moviepy.editor import *

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

def ApplyAudioOptions(audio_clip, audio_options):
    FunCom(f"Applying Audio Options: \"{audio_options}\" using MoviePy",f"\"{audio_options}\"\n^ Ahem! What is this? Well, I'm not doing that... MOVIEPYYY!")

    # Split the audio options based on '&' separator
    options_list = audio_options.split('& ')
    
    # Set the duration of the audio clip
    clip_duration = audio_clip.duration
    
    #nameIndex = 0

    subclip_list = []

    # Add the audio before the first start_time
    post = ConvertToSeconds(options_list[0].split(' - ')[0], clip_duration)
    if post < 0 or post > clip_duration:
        FunCom(f"Cutting post ({post}) is out of bounds ({clip_duration})", f"Houston, we have a problem. It seems that the cutting post ({post}) is trying to escape the duration of the video ({clip_duration})!")
    if post > 0 and post < clip_duration:
        subclip = audio_clip.subclip(0, post)
        subclip_list.append(subclip)
        #nameIndex += 1
        #subclip.write_audiofile(f"{filePath}-{nameIndex}.mp3")
    
    # Iterate over the options and apply the cutting
    for i in range(len(options_list) - 1):
        start_time = ConvertToSeconds(options_list[i].split(' - ')[1], clip_duration)
        end_time = ConvertToSeconds(options_list[i+1].split(' - ')[0], clip_duration)
        
        # Ensure the start and end times are within the duration
        start_time = min(start_time, clip_duration)
        end_time = min(end_time, clip_duration)
        
        if start_time >= end_time:
            FunCom(f"Cutting post ({end_time}) overlaps with other cutting post ({start_time})",f"I don't understand this. A cutting post ({start_time}) can't overlap with another ({end_time}), can it?")
        if start_time < 0 or start_time > clip_duration:
            FunCom(f"Cutting post ({start_time}) is out of bounds ({clip_duration})", f"Houston, we have a problem. It seems that the cutting post ({start_time}) is trying to escape the duration of the video ({clip_duration})!")
        if end_time < 0 or end_time > clip_duration:
            FunCom(f"Cutting post ({end_time}) is out of bounds ({clip_duration})", f"Houston, we have a problem. It seems that the cutting post ({stop_time}) is trying to escape the duration of the video ({clip_duration})!")
        if start_time > 0 and start_time < clip_duration and end_time > 0 and end_time < clip_duration:
            subclip = audio_clip.subclip(start_time, end_time)
            subclip_list.append(subclip)
            #nameIndex += 1
            #subclip.write_audiofile(f"{filePath}-{nameIndex}.mp3")

    
    # Add the audio after the last end_time        
    post = ConvertToSeconds(options_list[-1].split(' - ')[1], clip_duration)
    if post < 0 or post > clip_duration:
        FunCom(f"Cutting post ({post}) is out of bounds ({clip_duration})", f"Houston, we have a problem. It seems that the cutting post ({post}) is trying to escape the duration of the video ({clip_duration})!")
    if post > 0 and post < clip_duration:
        subclip = audio_clip.subclip(post, clip_duration)
        subclip_list.append(subclip)
    
    FunCom("Audio options successfully aplied","Oh, he's done. Good job, MoviePy!")

    return subclip_list

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

def CutAudio(audio_clip, size):

    # Set the duration of the audio clip
    clip_duration = audio_clip.duration

    # Calculate the number of pieces based on the specified size
    num_pieces = math.ceil(clip_duration / size)

    FunCom(f"Number of pieces: {num_pieces}",f"I'll be cutting this into {num_pieces} pieces.")

    subclip_list = []

    # Cut the audio into pieces
    pieces = []
    for i in range(num_pieces):
        start_time = i * size
        end_time = (i + 1) * size
        if end_time > clip_duration:
            end_time = clip_duration
        subclip = audio_clip.subclip(start_time, end_time)
        subclip_list.append(subclip)
    
    return subclip_list

def MergeLists(l1,l2):
    for thing in l2:
        l1.append(thing)

def CloseClips(list):
    for i in range(len(list)):
        list[0].close()

#endregion

# Create the Window
#region Create the Window
sg.theme('DarkTanBlue')
sg.set_options(font=("Arial Bold",10))

download_tab_layout = [
    [sg.Text('Ayo, bro! What are we downloading?')],
    [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True ,key='-PATH-'), sg.FolderBrowse()],
    [sg.Text('Select .txt file with YouTube links (line separated)'), sg.InputText(size=(15,1), key='-FILE-'), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
    [sg.Checkbox('Download highest res video (No audio)', key='-DOWNLOAD_VIDEO-', enable_events=True), sg.Checkbox('Also download audio', key='-DOWNLOAD_AUDIO-', visible=False, enable_events=True)],
    [sg.Checkbox('Cut up large files', key='-CUT_UP_FILES-', enable_events=True), sg.Input(size=(15, 1), key='-CUT_SIZE-', visible=False)],
    [sg.Checkbox('You want my funny commentary?', key='-FUN_COM-')],
    [sg.Button('Download'), sg.Button('Check Duration')]
]
remove_silence_tab_layout = [
    [sg.Text('I see you are not a big fan of the Sound of Silence?')]
]

download_tab = sg.Tab("Download Audio", download_tab_layout)
remove_silence_tab = sg.Tab("Remove Silence", remove_silence_tab_layout)

tab_group = sg.TabGroup([[download_tab,remove_silence_tab]])

layout = [
    [tab_group]
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

    # Cut up large files checkbox
    if event == '-CUT_UP_FILES-':
        # Toggle visibility of the input field based on the checkbox state
        window['-CUT_SIZE-'].update(visible=values['-CUT_UP_FILES-'])


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

                    audio_options = GetAudioOptions()


                    # Cutting the video
                    clip_changes = audio_options or values['-CUT_UP_FILES-']

                    if clip_changes:

                        # Options
                        audio_clip = AudioFileClip(f"{filePath}.mp3")
                        clip_list = [audio_clip]
                        if audio_options:
                            clip_list = ApplyAudioOptions(audio_clip, audio_options)
                                

                        # Cutting into pieces
                        if values['-CUT_UP_FILES-']:
                            cut_size = ConvertToSeconds(values['-CUT_SIZE-'],video.length)
                            FunCom(f"Cutting files into maximum {cut_size}s long pieces.", f"How big you want them audio files? {cut_size}s? Okay then...")
                            old_clip_list = clip_list
                            clip_list = []
                            for clip in old_clip_list:
                                MergeLists(clip_list,CutAudio(clip, cut_size))

                        
                        # Exporting audio files
                        FunCom("Writing new audiofiles", "Oh look! The original audioclip had babies! Wait, is that you, MoviePy?")
                        
                        for i in range(len(clip_list)):
                            file_name = f"{filePath}-{i+1}.mp3"
                            clip_list[i].write_audiofile(file_name)

                        FunCom("All new audiofiles done", "Yup, he's done now.")
                        
                        FunCom("Removing original mp3", "Oh, the mom mp3 died. I guess you're gonna have to take care of those new mp3 files...")
                        # Remove original clip
                        CloseClips(clip_list)
                        os.remove(f"{filePath}.mp3")
                        FunCom("Removal done", "Mom is dead a burried now.")


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