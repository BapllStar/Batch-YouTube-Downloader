# General
import PySimpleGUI as sg
import re
import os
from tqdm import tqdm
import math
import sys
from os import listdir
import tqdm
import traceback

# Download audio
from pytube import YouTube
from moviepy.editor import *

# Remove silence
from scipy.io import wavfile
from scipy.io.wavfile import read, write
import subprocess
import numpy as np
import wave

try:
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
    
    # General
    #region General
    def handle_exception(exc_type, exc_value, exc_traceback):
        # Write the exception details to a file
        with open('error.txt', 'w') as f:
            f.write('Unhandled exception occurred:\n')
            traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    
    def MergeLists(l1,l2):
        for thing in l2:
            l1.append(thing)
    
    def FunCom(lame, fun):
        if not values['fun_com']:
            print(lame)
        else:
            print("\nBapll - "+fun)
    
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
    
    def NewLine():
        print("")
    
    def PrintSeparator():
        print("\n=======================================================================================================================")
    
    #endregion
    
    
    # Download Audio
    #region Downlaod Audio
    
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
    
    def UpdateDownloadProgress(stream, chunk, bytes_remaining):
        # Calculate the progress percentage
        bytes_downloaded = stream.filesize - bytes_remaining
        progress_percentage = (bytes_downloaded / stream.filesize) * 100
    
        # Update the tqdm progress bar
        progress_bar.update(progress_percentage - progress_bar.n)
    
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
            video.download(filename=fileName + ".mp4", output_path=f"{download_path}/{authorName}")
    
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
         
    def CloseClips(list):
        for i in range(len(list)):
            list[0].close()
        
        #endregion
    
    
    # Remove Silence
    #region Remove Silence
    
    def detect_silence(path, time):
        FunCom("Detecting Silence", "Silence, I don't know who you are, or where you are, but I will find you... And I will kill you.")
        command = f"ffmpeg/bin/ffmpeg.exe -i {path} -af silencedetect=n=-{remove_defined}dB:d={str(time)} -f null -"
        out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        s = stdout.decode("utf-8")
        k = s.split('[silencedetect @')
        if len(k) == 1:
            # print(stderr)
            return None
            
        start, end = [], []
        for i in range(1, len(k)):
            x = k[i].split(']')[1]
            if i % 2 == 0:
                x = x.split('|')[0]
                x = x.split(':')[1].strip()
                try:
                    end.append(float(x))
                except ValueError:
                    print(f"ERROR: x = {x}")
                    try:
                        decimal_part = x.split("[")[0].strip()
                        end.append(float(decimal_part))
                        print("Error fixed")
                    except:
                        print(f"ERROR: decimal_part = {decimal_part}")
                        continue
            else:
                x = x.split(':')[1]
                x = x.split('size')[0]
                x = x.replace('\r', '')
                x = x.replace('\n', '').strip()
                try:
                    start.append(float(x))
                except ValueError:
                    print(f"ERROR: x = {x}")
                    try:
                        decimal_part = x.split("[")[0].strip()
                        start.append(float(decimal_part))
                        print("Error fixed")
                    except:
                        print(f"ERROR: decimal_part = {decimal_part}")
                        continue
        FunCom("Detection Complete", "I found all of the silence.")
        return list(zip(start, end))
        
    def remove_silence(file, sil, keep_sil, out_path):
        FunCom("Gathering non-silent parts","I'm finding all that non-silence now. Without it, the silence will die.")
        rate, aud = read(file)
        a = float(keep_sil) / 2
        sil_updated = [(i[0] + a, i[1] - a) for i in sil]
        
        # Convert the silence patch to non-sil patches
        non_sil = []
        tmp = 0
        ed = len(aud) / rate
        for i in range(len(sil_updated)):
            non_sil.append((tmp, sil_updated[i][0]))
            tmp = sil_updated[i][1]
        if sil_updated[-1][1] + a / 2 < ed:
            non_sil.append((sil_updated[-1][1], ed))
        if non_sil[0][0] == non_sil[0][1]:
            del non_sil[0]
        
        # Cut the audio
        ans = []
        ad = list(aud)
        for i in tqdm.tqdm(non_sil):
            ans = ans + ad[int(i[0] * rate):int(i[1] * rate)]
        
        print("\n")
        FunCom("Writing new wav-file","Packing up all of the non-silent part into a neat little wav-file.")
       # Create a WAV file
        with wave.open(out_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
            wav_file.setframerate(rate*2)  # Set the sample rate to match the original audio
            wav_file.writeframes(np.array(ans).astype(np.int16).tobytes())  # Write audio dataFunCom("R")
        FunCom("Wav-file complete","It's been done...")
        return non_sil
    #endregion
    
    #endregion
    
    # Create the Window
    #region Create the Window
    sg.theme('DarkTanBlue')
    sg.set_options(font=("Arial Bold",10))
    
    download_tab_layout = [
        [sg.Text('Ayo, bro! What are we downloading?')],
        [sg.Text('This exports mp3- and mp4-files')],
        [sg.Text('Select .txt file with YouTube links (line separated)'), sg.InputText(size=(15,1), key='download_list'), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
        [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True ,key='download_path'), sg.FolderBrowse()],
        [sg.Checkbox('Download highest res video (No audio)', key='download_video', enable_events=True), sg.Checkbox('Also download audio', key='download_video_audio', visible=False, enable_events=True)],
        [sg.Checkbox('Cut up large files', key='download_cut_files', enable_events=True), sg.Input(size=(6, 1), key='download_cut_size', default_text='20m', visible=False)],
        [sg.Button('Download'), sg.Button('Check Duration')]
    ]
    remove_silence_tab_layout = [
        [sg.Text('I see you are not a big fan of the Sound of Silence?')],
        [sg.Text('This works only with wav-files.')],
        [sg.Text('Select input location'), sg.In(size=(38,1), enable_events=True, default_text = 'C:/Users/chris/Documents/RVC/samples_unfinished/need-empty-removed', key='remove_in'), sg.FolderBrowse()],
        [sg.Text('Select output location'), sg.In(size=(38,1), enable_events=True, default_text = 'C:/Users/chris/Documents/RVC/samples/Dream', key='remove_out'), sg.FolderBrowse()],
        [sg.Text('Define Silence (intdB)'),sg.Input(size=(8, 1), key='remove_defined', default_text='23')],
        [sg.Text('Silence Threshhold (int)'),sg.Input(size=(8, 1), key='remove_threshhold', default_text='1')],
        [sg.Text('Silence Duration (int)'),sg.Input(size=(8, 1), key='remove_duration', default_text='1')],
        [sg.Button('Remove Silence')]
    ]
    settings_tab_layout = [
        [sg.Text('You don\'t like MY settings? Oh, okay. Yeah, that\'s fine. I have no problem with that.')],
        [sg.Checkbox('You want my funny commentary?', key='fun_com')]
    ]
    
    download_tab = sg.Tab("Download Audio", download_tab_layout)
    remove_silence_tab = sg.Tab("Remove Silence", remove_silence_tab_layout)
    settings_tab = sg.Tab("Settings",settings_tab_layout)
    
    tab_group = sg.TabGroup([[download_tab,remove_silence_tab,settings_tab]])
    
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
    
        # Download Audio Tab
        #region Download Audio Tab
    
        if event == 'download_path':
            download_path = values['download_path']
    
        if event == 'download_video':
            # Toggle visibility of the 'Also download audio' checkbox
            window['download_video_audio'].update(visible=values['download_video'])
    
        if event == 'download_cut_files':
            # Toggle visibility of the input field based on the checkbox state
            window['download_cut_size'].update(visible=values['download_cut_files'])
    
        if event == "Check Duration":
            # Guard Clauses
            #region Guard Clauses
            if not values['download_list']:
                FunCom("Please Select a txt file","WHAT excactly are we downloading? Come on, gimme something to work with!")
                continue
            #endregion
    
    
            # Processing the Inputted Data
            #region Processing the Inputted Data
            # Get the file path entered by the user
            file_path = values['download_list']  
    
    
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
            PrintSeparator()
    
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
                        PrintSeparator()
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
                    PrintSeparator()
                    #endregion
                else:
                    # If this is not a video, a comment or audio setting.
                    FunCom(f"\n\"{link}\" isn't a YouTube link!",f"Heeeeeyy, wait a minute... \"{link}\" isn't a YouTube link you sillybilly!")
                    PrintSeparator()
    
            FunCom(f"\n   All {total_links} links scanned",f"Heeeeyyy, 0 to go means I'm finished with all {total_links} now! :D")
             # Print the total duration for each author
            for author, duration in author_durations.items():
                print(f"{author}: {FormatSeconds(duration)}")
    
            PrintSeparator()
    
        if event == 'Download':
    
            # Guard Clauses
            #region Guard Clauses
            if not values['download_list']:
                FunCom("Please Select a txt file","WHAT excactly are we downloading? Come on, gimme something to work with!")
                continue
    
            if not values['download_path']:
                FunCom("Please Select an output location","And where excactly am I supposed to put the stuff I'm SO KINDLY downloading FOR you?")
                continue
            #endregion
    
    
            # Processing the Inputted Data
            #region Processing the Inputted Data
            # Get the file path entered by the user
            file_path = values['download_list']  
    
    
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
            PrintSeparator()
    
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
                        PrintSeparator()
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
    
                    fileName = GenerateUniqueFileName(f"{download_path}/{authorName}", authorName)
    
                    filePath = f"{download_path}/{authorName}/{fileName}"
                    #endregion
                    
                    if not values['download_video'] or values['download_video'] and values['download_video_audio']:
                        
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
                        clip_changes = audio_options or values['download_cut_files']
    
                        if clip_changes:
    
                            # Options
                            audio_clip = AudioFileClip(f"{filePath}.mp3")
                            clip_list = [audio_clip]
                            if audio_options:
                                clip_list = ApplyAudioOptions(audio_clip, audio_options)
                                    
    
                            # Cutting into pieces
                            if values['download_cut_files']:
                                cut_size = ConvertToSeconds(values['download_cut_size'],video.length)
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
    
    
                    if  values['download_video']:
                        
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
                    PrintSeparator()
                    #endregion
                else:
                    # If this is not a video, a comment or audio setting.
                    FunCom(f"\n\"{link}\" isn't a YouTube link!",f"Heeeeeyy, wait a minute... \"{link}\" isn't a YouTube link you sillybilly!")
                    PrintSeparator()
    
            FunCom(f"\n   All {total_links} jobs done",f"Heeeeyyy, 0 to go means I'm finished with all {total_links} now! :D")
            PrintSeparator()
        #endregion
    
        # Remove Silence Tab
        #region Remove Silence Tab
        if event == 'remove_in':
            remove_in = values['remove_in']
    
        if event == 'remove_out':
            remove_out = values['remove_out']
    
        remove_defined = int(values['remove_defined'])
        remove_threshhold = int(values['remove_threshhold'])
        remove_duration = int(values['remove_duration'])
    
        if event == 'Remove Silence':
            remove_in = values['remove_in']
            remove_out = values['remove_out']
             # Guard Clauses
            #region Guard Clauses
            if not values['remove_in']:
                FunCom("Please select an input directory","I need something to remove the silence from. Gimme a folder with some files in it.")
                continue
    
            if not values['remove_out']:
                FunCom("Please select an output directory","And where excactly am I supposed to put the stuff after I've removed the audio from it?")
                continue
            
            print("")
            FunCom("Removing Silence", "There will be no silence left alive, when I am done here!")
            FunCom(f"Found {len(os.listdir(remove_in))} files",f"I found {len(os.listdir(remove_in))} files to convert for you.")
            PrintSeparator()
            
            # Iterate through files in the input directory
            for filename in os.listdir(remove_in):
                if filename.endswith(".wav"):
                    print("")
                    FunCom(f"Starting removal proces on \"{filename}\"","There shall be no silence, {filename}!")
                    input_file = f"{remove_in}/{filename}"
                    output_file = f"{remove_out}/{filename}"
                    detected_silence = detect_silence(input_file,remove_threshhold)
                    remove_silence(input_file, detected_silence, remove_duration, output_file)
                    PrintSeparator()
                else:
                    FunCom(f"{filename} is not a wav-file",f"{filename} isn't a wav-file you dumdum. Luckily for you, I can just ignore stuff like that.")
                    PrintSeparator()
            #endregion
    
            FunCom("\nRemoval Complete", "They. Are. ALL. DEAD!")
            PrintSeparator()
            
except Exception as e:
    traceback_str = traceback.format_exc()

    # Open error.txt file in write mode
    with open("error.txt", "w") as file:
        # Write the traceback string to the file
        file.write(traceback_str)

    print("An error occurred. The traceback has been exported to error.txt.")
        #endregion
window.close()