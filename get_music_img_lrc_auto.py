from PIL import Image
import requests
from io import BytesIO
import yt_dlp
from ytmusicapi import YTMusic
import lyricsgenius
import whisper
import re
from difflib import SequenceMatcher
from making_video_file import create_video_from_image, video_audio_merge, folder_creation_with_song_name, \
    create_blank_mp4, create_lyrics_video, extract_thumbnail, copying_raw_file, song_title, get_audio_length

GENIUS_API_KEY = "KT6XN3FHd0Hy1N8TmombJtgILOSEpW4-o-lXjpQBY4jNLngrnL0pvDzG7QVlBO8p"  # 🔹 Replace with your Genius API key
genius = lyricsgenius.Genius(GENIUS_API_KEY)

'''getting image from the main video file for background'''
def save_image_from_youtube(code):
    # YouTube Thumbnail URL (replace VIDEO_ID)
    thumbnail_url = f"https://i.ytimg.com/vi/{code}/maxresdefault.jpg"

    # Fetch and upscale image
    response = requests.get(thumbnail_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.resize((1920, 1080), Image.LANCZOS)
        img.save("dirfile/image_background.jpg")  # Save the new image
        print("Saved: image_background.jpg")
    else:
        print("Failed to fetch image_background")

# save_image_from_youtube('4QIZE708gJ4')

'''searching the official audio file so it doesnt have the video disturbances'''

def search_official_audio(video_id):
    """Search YouTube Music for the official audio of a given video."""
    ytmusic = YTMusic()  # Initialize API without authentication
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    # Get search results for the video title
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        search_query = info.get('title', '')

    print(f"🔍 Searching for: {search_query}")

    # Search for the official song on YouTube Music
    search_results = ytmusic.search(search_query, filter="songs")
    if search_results:
        return search_results[0]['videoId']  # Return the first result (most relevant)

    print("⚠️ No official audio found.")
    return None

'''Once the official audio is found then trying to download the music'''

def download_youtube_music(video_url_id, output_path="dirfile/music_file"):
    """Download YouTube audio as an MP3 file."""
    video_music_id_found = search_official_audio(video_url_id)
    if video_music_id_found is not None:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            # 'outtmpl': f"{output_path}/%(title)s.%(ext)s",
            'outtmpl': f"{output_path}.%(ext)s",
            'overwrites': True,  # ✅ Overwrites existing files
            'nopostoverwrites': False,  # ✅ Ensures processing isn't skipped
        }

        video_url = f'https://www.youtube.com/watch?v={video_music_id_found}'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    else:
        print('No audio file (mp3) found')

def get_song_title(video_id):
    """Fetch the song title from YouTube using yt_dlp."""
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {'quiet': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        return info.get('title', '')

def fetch_lyrics(song_title):
    """Fetch lyrics from Genius using the song title."""
    song = genius.search_song(song_title)
    if song:
        return song.lyrics
    return "Lyrics not found."

def clean_lyrics(lyrics):
    """Remove all text inside square brackets from the lyrics."""
    cleaned_lyrics = re.sub(r"\[.*?\]", "", lyrics)  # Remove bracketed text
    cleaned_lyrics = "\n".join([line.strip() for line in cleaned_lyrics.split("\n") if line.strip()])  # Remove empty lines
    return cleaned_lyrics

def get_plain_lyrics(video_id):
    """Main function to get lyrics from a YouTube video ID."""
    song_title = get_song_title(video_id)
    song_title = "".join(song_title).split('(')[0].strip()

    print(f"🔍 Searching lyrics for: {song_title}")

    lyrics = fetch_lyrics(song_title)
    cleaned_lyrics = clean_lyrics(lyrics)

    # Save to plain_lyrics.txt
    with open("dirfile/plain_lyrics.txt", "w", encoding="utf-8") as file:
        file.write(f"{song_title} (Lyrics)\n\n")
        file.write(cleaned_lyrics)
        file.write(f"\nBy Video Junkie")
    return cleaned_lyrics

# Function to find the best matching segment in plain lyrics
def find_matching_segment(whisper_text, plain_words, start_idx):
    whisper_words = whisper_text.lower().split()
    best_match = None
    best_ratio = 0
    best_end_idx = start_idx

    # Search within a reasonable window of words
    # window_size = len(whisper_words) * 2
    for i in range(start_idx, min(start_idx + 50, len(plain_words) - len(whisper_words) + 1)):
        candidate = " ".join(plain_words[i:i + len(whisper_words)])
        ratio = SequenceMatcher(None, whisper_text.lower(), candidate.lower()).ratio()
        if ratio > best_ratio and ratio > 0.5:  # Threshold for a decent match
            best_ratio = ratio
            best_match = candidate
            best_end_idx = i + len(whisper_words)

    return best_match, best_end_idx

def getting_lrc_file():
    # Load Whisper model
    model = whisper.load_model("small")

    # Transcribe the audio
    result = model.transcribe("dirfile/music_file.mp3", verbose=False)

    # Read and clean the plain lyrics file
    with open("dirfile/plain_lyrics.txt", "r", encoding="utf-8") as file:
        lyrics_lines = [line.strip() for line in file.readlines() if line.strip()]

    if len(lyrics_lines) > 2:
        lyrics_lines = lyrics_lines[1:-1]

    plain_lyrics_string = " ".join(lyrics_lines)
    plain_lyrics_words = plain_lyrics_string.split()

    # Whisper outputs (sorted by timestamp)
    segments = sorted(result["segments"], key=lambda x: x["start"])

    # Split plain lyrics to match Whisper segments
    split_lyrics = []
    current_idx = 0
    aligned_lyrics = []

    for segment in segments:
        start_time = segment["start"]
        minutes = int(start_time // 60)
        seconds = int(start_time % 60)
        milliseconds = int((start_time % 1) * 100)
        formatted_time = f"[{minutes:02d}:{seconds:02d}.{milliseconds:02d}]"

        whisper_lyrics = segment["text"].strip()

        # Find the matching segment in plain lyrics
        matched_segment, new_idx = find_matching_segment(whisper_lyrics, plain_lyrics_words, current_idx)

        if matched_segment:
            split_lyrics.append((formatted_time, matched_segment))
            current_idx = new_idx
        else:
            # If no match found, use the Whisper text as fallback and advance minimally
            split_lyrics.append((formatted_time, whisper_lyrics))
            current_idx += len(whisper_lyrics.split())

    # Output the results
    for timestamp, lyrics in split_lyrics:
        # print("time stamp")
        # print(f"{timestamp} {lyrics}")
        aligned_lyrics.append(f"{timestamp} {lyrics}")

    with open('dirfile/plain_lyrics.txt', 'r', encoding='utf-8') as file:
        first_line = file.readline().strip()
        # print(first_line)


    lrc_filename = "dirfile/lyrics_with_ts.lrc"
    with open(lrc_filename, "w", encoding="utf-8") as out_file:
        out_file.write(f"[00:00.00] {first_line}\n")
        out_file.write("\n".join(aligned_lyrics))

    with open(lrc_filename, "r", encoding="utf-8") as file:
        lines = file.readlines()

    count = 0
    for i in range(len(lines)):
        if "[00:00.00]" in lines[i]:
            count += 1
            if count == 2:  # Modify the second occurrence
                lines[i] = lines[i].replace("[00:00.00]", "[00:00.01]", 1)
                break  # Stop after modifying the second occurrence
    if lines:
        match = re.match(r"(\[.*?\]) (.*)", lines[-1].strip())  # Extract timestamp if present
        timestamp, _ = match.groups()
        lines[-1] = f"{timestamp} By Video Junkie\n"  # Preserve timestamp

    with open(lrc_filename, "w", encoding="utf-8") as file:
        file.writelines(lines)

# video_id_passed = input("Enter the youtube Video_id: ")
# video_id_passed = "VcRc2DHHhoM"
video_id_list = [
    "JNFO40e10CA",
    "fuV4yQWdn_4",
    "eVli-tstM5E",
    "tQg5-6DHxQY",
    "bbw4-yOszDc",
    "JVDUsaqgSq0",
    "GR3Liudev18",
    "JSFG-IE8n_c",
    "JQbjS0_ZfJ0",
]

for video_id_passed in video_id_list:
    print(f"Processing video ID: {video_id_passed}")
    save_image_from_youtube(video_id_passed)
    download_youtube_music(video_id_passed)
    get_plain_lyrics(video_id_passed)
    getting_lrc_file()
    song_title_created = song_title('dirfile/lyrics_with_ts.lrc')
    create_video_from_image("dirfile/image_background.jpg", "dirfile/video_without_music.mp4", duration=get_audio_length("dirfile/music_file.mp3"))
    video_audio_merge("dirfile/video_without_music.mp4", "dirfile/music_file.mp3")
    folder_creation_with_song_name(str(song_title_created))
    create_blank_mp4(f"video_final_output/{song_title_created}/{song_title_created}.mp4")
    # create_lyrics_video_singular("output_video.mp4", "dirfile/lyrics_with_ts.lrc", f"video_final_output/{song_title_created}/{song_title_created}singular.mp4")
    create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", f"video_final_output/{song_title_created}/{song_title_created}.mp4")
    extract_thumbnail(f"video_final_output/{song_title_created}/{song_title_created}.mp4",f"video_final_output/{song_title_created}/{song_title_created}-thumbnail.jpg")
    copying_raw_file(song_title_created)
    print(f"Finished processing video ID: {video_id_passed}")

print("All videos processed successfully!")


