# Batch-YouTube-Downloader

This program is designed for downloading a large number of YouTube videos to train RVC models. It provides a convenient way to download and process multiple videos at once.

## Project Links

- Trello Board: [Batch YouTube Downloader](https://trello.com/b/drUldcw7/youtube-mc-ai)
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

Example:

```plaintext
## Rick Astley
# This will be printed in the console
https://www.youtube.com/watch?v=dQw4w9WgXcQ
# https://youtu.be/dQw4w9WgXcQ
# This won't be read

## Bapll
# This will be printed in the console
https://www.youtube.com/watch?v=X3HrBg--wk4
https://www.youtube.com/watch?v=3NnIfuvEiec