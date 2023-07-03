# Batch-YouTube-Downloader

This program is designed for downloading a large number of YouTube videos to train RVC models. It provides a convenient way to download and process multiple videos at once.

## Project Links

- Discord: [Join Team Bapll](https://discord.gg/rbk3RCJPda)
- Bapll YouTube Channel: [Bapll](https://www.youtube.com/channel/UC6c-iFvwQJ_qO9x7lQwNFng)

## Usage

To use this program, follow the instructions below:

1. Create a text file and copy/paste the YouTube video links you want to download. Each link should be on a new line.
2. Format the links using one of the following formats:
   - `https://www.youtube.com/watch?v=<id>`
   - `https://youtu.be/<id>`
3. Optional: Add comments using the `#` symbol. Comments will be ignored by the program.
4. Optional: Add headings using the `##` prefix. Headings will be displayed in the console when processed.
5. Optional: Trim the audio of specific videos using the trimming syntax. The syntax is `& xh,xm,xs - xh,xm,xs`, where `x` represents hours, minutes, or seconds.
   - You can use multiple commands on a single line by separating them with `&`.
   - If you want to cut from a specific point until the end, use `end` instead of the second timestamp.
6. Save the file with a `.txt` extension.

### Commenting

```plaintext
##Headlines will show up in the console, when the program is running
#Comments and epty lines will be completely ignored
```

### Basic Download
Literally just insert the links line separated. That's it...
Tutorial on how to get free V-Bucks below:
```plaintext
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Trimming Audio
You can cut out specific parts of a video by using the syntax demonstrated below:
```plaintext
https://youtu.be/dQw4w9WgXcQ
& 0s - 5s & 10s - 1m,5s & 2m - end
```
This will cut out:
The first 5 seconds (&  - 5s)
From 00:10 to 01:05 (& 10s - 1m,5s)
from 02:00 until the end (& 2m - end)

### Alternative trimming syntax
The trimming post (the time mark) is by default 0s.
This makes you able to write nothing in place of "0s", "0m" or "0h". See example below.
```plaintext
https://www.youtube.com/watch?v=X3HrBg--wk4
& - 7s
```
### Commenting options
There are 6 symbols which you can write freely in the audio options: 
`" ", "/", "|", "\", "[" and "]"`
These are here simply to make it easier for you to read your own audio options.
They provide no actual functionality.
KEEP IN MIND: the first symbol still needs to be "&".
```plaintext
https://www.youtube.com/watch?v=3NnIfuvEiec
& [-7s] & [13s /-/ 17s]
```
or
```plaintext
https://www.youtube.com/watch?v=3NnIfuvEiec
&||||| /[-]]]]]]]7s]\   //////\\\\[][][][|&|   /[13s - 17s]\ |||||
```
^ Idk why anyone would want it this complicated, but they can now XD.

