# from mutagen.mp3 import MP3
# from mutagen.wave import WAVE
# # import re
# #
# def get_audio_length(file_path):
#     try:
#         if file_path.lower().endswith('.mp3'):
#             audio = MP3(file_path)
#         elif file_path.lower().endswith('.wav'):
#             audio = WAVE(file_path)
#         else:
#             return "Unsupported file format"
#         length_music = audio.info.length  # Returns duration in seconds
#         total_music_seconds = round(length_music)
#         return total_music_seconds
#     except Exception as e:
#         return f"Error: {str(e)}"
#
# # Example usage
# # file_path = "dirfile/music_file.mp3"
# # length = get_audio_length(file_path)
#
# # # Format as minutes:seconds
# # if isinstance(length, float):
# #     total_seconds = round(length)  # Round to nearest integer
# #     print(total_seconds)
# #     # minutes = total_seconds // 60
# #     # seconds = total_seconds % 60
# #     # print(f"Duration: {total_seconds} seconds")
# #     # print(f"Duration: {minutes}:{seconds:02d}")  # Ensures seconds is two digits
# # else:
# #     print(length)  # Prints error message if applicable
#
# def parse_lrc_file(lrc_file):
#     lyrics_with_timestamps = []
#     try:
#         with open(lrc_file, 'r', encoding='utf-8-sig') as file:  # Use utf-8-sig
#             for line in file:
#                 line = line.strip()
#                 # Handle lines with multiple timestamps for the same lyric
#                 matches = re.findall(r"\[(\d{2}:\d{2}\.\d{2,3})](.*)", line) # Find all matches
#                 for timestamp, lyric in matches: # Iterate over all matches on the current line
#                     lyrics_with_timestamps.append((timestamp, lyric.strip()))
#     except FileNotFoundError:
#         print(f"Error: File not found at {lrc_file}")
#         return None
#     return lyrics_with_timestamps
#
# def timestamp_to_seconds(timestamp):
#     """
#     Converts a timestamp in [mm:ss.xx] format to seconds.
#     """
#     minutes, seconds = timestamp.split(':')
#     return int(minutes) * 60 + float(seconds)
#
# lrc_file = "dirfile/lyrics_with_ts.lrc"
# lyrics_with_timestamps = parse_lrc_file(lrc_file)
# for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#     # print(timestamp_to_seconds(timestamp))
#     # Calculate start and end times for the current lyric
#     start_time = timestamp_to_seconds(timestamp)
#     end_time = (
#         timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#         if i + 1 < len(lyrics_with_timestamps)
#         else{
#             start_time + (get_audio_length('dirfile/music_file.mp3') - start_time)
#         }
#     # end time this when the lyrics would disappear if no other line is given (lik the last line)
#     )
#


# from moviepy import ImageClip
#
# def create_video_from_image(image_path, output_path, duration=5, resolution=(1920, 1080), fps=30):
#     """
#     Creates a 1920x1080 video from an image.
#
#     :param image_path: Path to the input image (JPEG or other format).
#     :param output_path: Path to save the output video (MP4 format).
#     :param duration: Duration of the video in seconds (default: 5).
#     :param resolution: Tuple for video resolution (default: 1920x1080).
#     :param fps: Frames per second (default: 30).
#     """
#     # Load the image and resize it to fit the resolution
#     clip = ImageClip(image_path).resized(resolution).with_duration(duration)
#
#     # Write the video file
#     clip.write_videofile(output_path, fps=fps, codec="libx264", audio=False)
#
#     print(f"Video saved at {output_path}")
#
# # Example Usage
# create_video_from_image("dirfile/image_background.jpg", "output.mp4", duration=60)


# from moviepy import ImageClip, ColorClip, CompositeVideoClip
#
# def create_video_from_image(image_path, output_path, duration=5, resolution=(1920, 1080), fps=30):
#     # Load the image and resize it to fit the resolution
#     image_clip = ImageClip(image_path).resized(resolution).with_duration(duration)
#
#     # Create a black rectangle with the same resolution and 40% transparency (alpha=0.4)
#     black_overlay = ColorClip(size=resolution, color=(0, 0, 0)).with_duration(duration).with_opacity(0.4)
#
#     # Composite the image and the black overlay
#     final_clip = CompositeVideoClip([image_clip, black_overlay])
#
#     # Write the video file
#     final_clip.write_videofile(output_path, fps=fps, codec="libx264", audio=False)
#
#     print(f"Video saved at {output_path}")

# Example Usage
# create_video_from_image("dirfile/image_background.jpg", "dirfile/video_without_music.mp4", duration=get_audio_length("dirfile/music_file.mp3"))


# import re
# import requests

# def convert_lrc_to_txt(input_file, output_file):
#     with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
#         for line in infile:
#             # Remove timestamps (patterns like [00:00.00])
#             clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()
#             if clean_line:  # Ignore empty lines
#                 outfile.write(clean_line + "\n")

'''removing the extra space in the beginning and adding  2 lines after the title in the oplain_lyrics.txt file'''
import requests
import yt_dlp
from ytmusicapi import YTMusic

# import aeneas

# import re
#
#
# def convert_lrc_to_txt(input_file, output_file, hashtag):
#     # Step 1: Read LRC file and remove timestamps
#     with open(input_file, "r", encoding="utf-8-sig") as infile:  # Use 'utf-8-sig' to remove BOM
#         lines = infile.readlines()
#
#     cleaned_lines = []
#     for line in lines:
#         clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()  # Remove timestamps & trim spaces
#         if clean_line:
#             cleaned_lines.append(clean_line)
#
#     # Step 2: Write cleaned lyrics to output file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         outfile.write("\n".join(cleaned_lines))
#
#     # Step 3: Reopen the file and adjust the first line
#     with open(output_file, "r", encoding="utf-8") as outfile:
#         updated_lines = outfile.readlines()
#
#     if updated_lines:
#         first_line = updated_lines[0].lstrip()  # Remove any leading spaces
#         updated_lines[0] = hashtag + "\n\n" + first_line + "\n"  # Add two new lines after first line
#
#     # Step 4: Write back adjusted lyrics
#     with open(output_file, "w", encoding="utf-8") as final_outfile:
#         final_outfile.writelines(updated_lines)
#
# convert_lrc_to_txt("dirfile/lyrics_with_ts.lrc", "dirfile/plain_lyrics.txt")
# print("Conversion completed! Lyrics saved in 'plain_lyrics.txt'.")

'''Shazam api to find the artist name and songs name however it get confused when feat it merges song name with feat artist name'''
# def convert_lrc_to_txt(input_file, output_file):
#     # Step 1: Read LRC file and remove timestamps
#     with open(input_file, "r", encoding="utf-8-sig") as infile:
#         lines = infile.readlines()
#
#     cleaned_lines = []
#     for line in lines:
#         clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()
#         if clean_line:
#             cleaned_lines.append(clean_line)
#
#     first_line = cleaned_lines[0] if cleaned_lines else ""
#
#     # Step 2: Try to identify artist and song using Shazam API
#     artist = ""
#     song = ""
#
#     try:
#         # Extract potential song title from first line for search
#         search_term = re.sub(r'\s*[\(\[].*?[\)\]]', '', first_line).strip()  # Remove parenthetical info
#
#         # Set up Shazam API request
#         # Note: You'll need to replace with the actual Shazam API endpoint and your API key
#         headers = {
#             'X-RapidAPI-Key': '1dc406c142msh3655a2a0d7c612ep1f4293jsnc9baa7b3ad3c',
#             'X-RapidAPI-Host': 'shazam.p.rapidapi.com'
#         }
#
#         # Use Shazam search API
#         response = requests.get(
#             f'https://shazam.p.rapidapi.com/search?term={search_term}&limit=1',
#             headers=headers
#         )
#
#         if response.status_code == 200:
#             data = response.json()
#             # Extract artist and song info from response
#             if 'tracks' in data and 'hits' in data['tracks'] and data['tracks']['hits']:
#                 track = data['tracks']['hits'][0]['track']
#                 artist = track.get('subtitle', '')  # Artist name is usually in subtitle
#                 song = track.get('title', '')  # Song title
#
#     except Exception as e:
#         # Fallback to regex-based extraction if API fails
#         print(f"API extraction failed: {e}. Falling back to title parsing.")
#
#     # If Shazam API failed or didn't return results, fall back to original parsing logic
#     if not artist or not song:
#         # Fallback parsing logic (using the previously defined regex approach)
#         # [Include your existing parsing logic here]
#
#         # For brevity, I'm including a simplified version:
#         if " - " in first_line:
#             parts = first_line.split(" - ")
#             artist = parts[0].strip()
#             song_parts = parts[1].split("(")
#             song = song_parts[0].strip() if song_parts else ""
#
#     # Create hashtags
#     hashtags = []
#
#     if artist:
#         artist_tag = "#" + re.sub(r'[^\w]', '', artist.lower())
#         hashtags.append(artist_tag)
#
#     if song:
#         song_tag = "#" + re.sub(r'[^\w]', '', song.lower())
#         hashtags.append(song_tag)
#
#     # Add default hashtags
#     default_hashtags = ["#music", "#lyrics", "#lyricvideo", "#lyrical", "#scrolllyrics"]
#     hashtags.extend(default_hashtags)
#
#     # Create hashtag line
#     hashtag_line = " ".join(hashtags)
#
#     # Step 3: Prepare final content with hashtags
#     final_content = [hashtag_line, "", first_line, ""]
#     final_content.extend(cleaned_lines[1:])
#
#     # Step 4: Write to output file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         outfile.write("\n".join(final_content))

# import re
# import json
# import http.client
# from urllib.parse import quote


# def convert_lrc_to_txt(input_file, output_file):
#     # Step 1: Read LRC file and remove timestamps
#     with open(input_file, "r", encoding="utf-8-sig") as infile:
#         lines = infile.readlines()
#
#     cleaned_lines = []
#     for line in lines:
#         clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()
#         if clean_line:
#             cleaned_lines.append(clean_line)
#
#     first_line = cleaned_lines[0] if cleaned_lines else ""
#     print(f"Processing title: {first_line}")  # Debug output
#
#     # Step 2: Initialize variables
#     main_artist = ""
#     song = ""
#     featuring_artists = []
#
#     try:
#         # Extract potential song title from first line for search
#         search_term = re.sub(r'\s*[\(\[].*?[\)\]]', '', first_line).strip()  # Remove parenthetical info
#         encoded_search = quote(search_term)
#
#         # Set up Shazam API connection
#         conn = http.client.HTTPSConnection("shazam.p.rapidapi.com")
#         headers = {
#             'x-rapidapi-key': "1dc406c142msh3655a2a0d7c612ep1f4293jsnc9baa7b3ad3c",
#             'x-rapidapi-host': "shazam.p.rapidapi.com"
#         }
#
#         # Step 3: Get search results
#         conn.request("GET", f"/search?term={encoded_search}&limit=1", headers=headers)
#         search_response = conn.getresponse()
#         search_data = json.loads(search_response.read().decode("utf-8"))
#
#         if 'tracks' in search_data and 'hits' in search_data['tracks'] and search_data['tracks']['hits']:
#             track = search_data['tracks']['hits'][0]['track']
#             song = track.get('title', '')
#
#             # Get primary artist
#             primary_artist = track.get('subtitle', '')
#             main_artist = primary_artist.split('&')[0].split('feat')[0].strip()
#
#             # Extract featuring artists from subtitle if present
#             if '&' in primary_artist or 'feat' in primary_artist.lower() or 'ft' in primary_artist.lower():
#                 # Will process in fallback logic to be consistent
#                 pass
#
#     except Exception as e:
#         print(f"API extraction failed: {e}. Falling back to title parsing.")
#
#     # Fallback to parsing if API fails or returns incomplete data
#     if not main_artist or not song:
#         # Parse the title line
#         if " - " in first_line:
#             parts = first_line.split(" - ", 1)
#             main_artist = parts[0].strip()
#             remainder = parts[1].strip()
#
#             # Check for featuring artists in various formats
#             # Pattern to match feat./ft./featuring with optional period and spaces
#             feat_pattern = re.compile(r'(.*?)\s+(?:feat\.?|ft\.?|featuring)\s+(.*?)(?:\s+[\(\[]|$)', re.IGNORECASE)
#             feat_match = feat_pattern.search(remainder)
#
#             if feat_match:
#                 # Get the song name (before featuring)
#                 song = feat_match.group(1).strip()
#                 # Get featuring artists part
#                 featuring_part = feat_match.group(2).strip()
#
#                 # Remove parenthetical parts like "(Lyrics)" or "(Extended Mix)"
#                 featuring_part = re.sub(r'\s*[\(\[].*?[\)\]]', '', featuring_part).strip()
#
#                 # Split featuring artists by "&" or ","
#                 if "&" in featuring_part:
#                     featuring_artists = [a.strip() for a in featuring_part.split("&")]
#                 elif "," in featuring_part:
#                     featuring_artists = [a.strip() for a in featuring_part.split(",")]
#                 else:
#                     featuring_artists = [featuring_part]
#             else:
#                 # Check for parentheses that might contain additional info
#                 paren_match = re.search(r'(.*?)\s*[\(\[]', remainder)
#                 if paren_match:
#                     song = paren_match.group(1).strip()
#                 else:
#                     song = remainder
#
#     # Check for any remix/extended version indicators
#     remix_pattern = re.compile(r'(.*?)\s*(?:\(|\[)?((?:remix|extended|mix|edit|version).*?)(?:\)|\])?$', re.IGNORECASE)
#     remix_match = remix_pattern.search(song)
#     remix_info = ""
#
#     if remix_match:
#         song = remix_match.group(1).strip()
#         remix_info = remix_match.group(2).strip()
#
#     print(f"Extracted: Main artist: {main_artist}, Song: {song}, Featured: {featuring_artists}")  # Debug output
#
#     # Create hashtags
#     hashtags = []
#
#     # Add main artist hashtag
#     if main_artist:
#         main_artist_tag = "#" + re.sub(r'[^\w]', '', main_artist.lower())
#         hashtags.append(main_artist_tag)
#
#     # Add song hashtag
#     if song:
#         # Remove any remaining "feat" parts
#         song = re.sub(r'\s+(?:feat\.?|ft\.?|featuring).*', '', song, flags=re.IGNORECASE).strip()
#         song_tag = "#" + re.sub(r'[^\w]', '', song.lower())
#         hashtags.append(song_tag)
#
#     # Add remix info as a separate hashtag if present
#     if remix_info:
#         remix_tag = "#" + re.sub(r'[^\w]', '', remix_info.lower())
#         hashtags.append(remix_tag)
#
#     # Add hashtags for featuring artists
#     for feat_artist in featuring_artists:
#         if not feat_artist.strip():
#             continue
#         feat_artist_tag = "#" + re.sub(r'[^\w]', '', feat_artist.lower())
#         hashtags.append(feat_artist_tag)
#
#     # Add default hashtags
#     default_hashtags = ["#music", "#lyrics", "#lyricvideo", "#lyrical", "#scrolllyrics"]
#     hashtags.extend(default_hashtags)
#
#     # Create hashtag line
#     hashtag_line = " ".join(hashtags)
#     print(f"Generated hashtags: {hashtag_line}")  # Debug output
#
#     # Step 5: Prepare final content with hashtags
#     final_content = [hashtag_line, "", first_line, ""]
#     final_content.extend(cleaned_lines[1:])
#
#     # Step 6: Write to output file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         outfile.write("\n".join(final_content))
#
# # Usage
# convert_lrc_to_txt("dirfile/lyrics_with_ts.lrc", "dirfile/plain_lyrics.txt")
# print("Conversion completed! Lyrics saved in 'plain_lyrics.txt'.")
#
# '''upload video on youtube'''
#
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google_auth_oauthlib.flow import InstalledAppFlow
# import requests
# import json
# import re
#
# # Define the required YouTube API scope
# SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
#
#
# def authenticate():
#     """Authenticate using OAuth 2.0 and return YouTube API service."""
#     flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
#     credentials = flow.run_local_server(port=0)
#     return build("youtube", "v3", credentials=credentials)
#
#
# def upload_video(youtube, file_path, title, description, tags, privacy_status, made_for_kids):
#     """Upload a video to YouTube."""
#     request = youtube.videos().insert(
#         part="snippet,status",
#         body={
#             "snippet": {
#                 "title": title,
#                 "description": description,
#                 "tags": tags,
#                 "categoryId": "10",  # Category ID (22 = People & Blogs)
#             },
#             "status": {
#                 "privacyStatus": privacy_status,  # public, private, unlisted
#                 "madeForKids": made_for_kids
#             },
#         },
#         media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True),
#     )
#     response = request.execute()
#     print("Uploaded video ID:", response["id"])
#
# def song_title(directory_passed):
#     with open(directory_passed, 'r', encoding='utf-8-sig') as file:
#         for line in file:
#             # print(line)
#             title = line.split(']')[-1].strip()
#             return title
#
# def convert_lrc_to_txt(input_file, output_file, hashtag):
#     # Step 1: Read LRC file and remove timestamps
#     with open(input_file, "r", encoding="utf-8-sig") as infile:  # Use 'utf-8-sig' to remove BOM
#         lines = infile.readlines()
#
#     cleaned_lines = []
#     for line in lines:
#         clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()  # Remove timestamps & trim spaces
#         if clean_line:
#             cleaned_lines.append(clean_line)
#
#     # Step 2: Write cleaned lyrics to output file
#     with open(output_file, "w", encoding="utf-8") as outfile:
#         outfile.write("\n".join(cleaned_lines))
#
#     # Step 3: Reopen the file and adjust the first line
#     with open(output_file, "r", encoding="utf-8") as outfile:
#         updated_lines = outfile.readlines()
#
#     if updated_lines:
#         first_line = updated_lines[0].lstrip()  # Remove any leading spaces
#         updated_lines[0] = hashtag + "\n\n" + first_line + "\n"  # Add two new lines after first line
#
#     # Step 4: Write back adjusted lyrics
#     with open(output_file, "w", encoding="utf-8") as final_outfile:
#         final_outfile.writelines(updated_lines)
#
# def getting_artist_and_song_name_for_hashtag(song_name):
#
#     url = "https://shazam.p.rapidapi.com/search"
#     artist_list = []
#
#     song_name = song_name.split('(Lyrics)')[0].strip()
#     if "(Official Video)" in song_name:
#         song_name = song_name.split('(Official Video)')[0].strip()
#
#     querystring = {"term":f"{song_name}","locale":"en-US","offset":"0","limit":"5"}
#
#     headers = {
#         "x-rapidapi-key": "1dc406c142msh3655a2a0d7c612ep1f4293jsnc9baa7b3ad3c",
#         "x-rapidapi-host": "shazam.p.rapidapi.com"
#     }
#
#     response = requests.get(url, headers=headers, params=querystring)
#
#     raw_json = response.json()
#
#     response = json.dumps(raw_json, indent=4)
#
#     # print(response)
#
#     # Convert the JSON string back to a Python object
#     loaded_data = json.loads(response)
#     # print(loaded_data)
#     main_tracks = loaded_data["tracks"]
#     main_hits = main_tracks["hits"]
#     # print(main_hits)
#     main_track = main_hits[0]["track"]
#     title =  main_track["title"]
#     if "(" in title:
#         title = "".join(title).split('(')[0].lstrip()
#     else:
#         title = "".join(title).lstrip()
#     try:
#         # Access the "artists" list
#         artists = loaded_data["artists"]
#         # print(artists)
#         # Access the "hits" list
#         hits = artists["hits"]
#         # Extract the names
#         artist_names = [hit["artist"]["name"] for hit in hits]
#
#         # Print the names
#         for name in artist_names:
#             # print(name)
#             artist_list.append(name)
#     except KeyError:
#         artist = main_track["subtitle"]
#         # print(len("".join(artist).split('&')))
#         for i in "".join(artist).split('&'):
#             artist_individual_name = i.strip()
#             artist_list.append(artist_individual_name)
#
#     # print(artist_list)
#
#     title_lower = title.lower() #Make the title lower case for easier comparison
#
#     found_artists = []
#
#     for artist in artist_list:
#         if artist.lower() in title_lower:
#             found_artists.append(artist)
#
#     #Get the remainder of the title
#     remainder = title
#
#     # for artist in found_artists:
#     #     remainder = remainder.replace(artist, "") #Remove the artist names.
#
#     # remainder = remainder.replace("feat.","") #clean up feat.
#     # remainder = remainder.replace("&","") #clean up &
#     # remainder = remainder.replace("-","") #clean up -
#     # remainder = remainder.replace("(Lyrics)","") #clean up (Lyrics)
#     remainder = remainder.replace(" ", "").lower()
#     remainder_clean = remainder.strip() #clean up extra spaces.
#
#     # print(remainder)
#     # print(artist_list)
#     # print('printing #hashtag')
#     output_string = f"#{remainder_clean}"
#     rest_hashtag = "#music #lyrics #lyricvideo #lyrical #scrolllyrics"
#
#     for artist_name_print in artist_list:
#         artist_clean = artist_name_print.lower().replace(" ", "").replace("-", "") #Clean artist name
#         output_string += f" #{artist_clean}"
#
#     return f"{output_string} {rest_hashtag}"
#
#
# if __name__ == "__main__":
#     youtube = authenticate()
#
#     # Set video details
#     # file_path = "dirfile/video_without_music.mp4"
#     file_path = "video_final_output/The Weeknd - Hurry Up Tomorrow (Lyrics)/The Weeknd - Hurry Up Tomorrow (Lyrics).mp4"
#     title = song_title('video_final_output/The Weeknd - Hurry Up Tomorrow (Lyrics)/The Weeknd - Hurry Up Tomorrow (Lyrics).lrc')
#     # create a txt file that could further be used to copy and
#     # past the lyrics without the time stamps as well as the tags should be created on top of the lyrics
#     hashtag_generate = getting_artist_and_song_name_for_hashtag(title)
#     convert_lrc_to_txt("video_final_output/The Weeknd - Hurry Up Tomorrow (Lyrics)/The Weeknd - Hurry Up Tomorrow (Lyrics).lrc", "dirfile/plain_lyrics.txt", hashtag_generate)
#     # Read description from the text file
#     description_file_path = "dirfile/plain_lyrics.txt"  # Replace with your actual file path
#     with open(description_file_path, "r", encoding="utf-8") as file:
#         description = file.read()
#     # pass the tags on top of description as well as below in tags section
#     tag_list = []
#     if hashtag_generate:  # Check if hashtag_generate is not empty
#         hashtag_list = hashtag_generate.split()  # Split the string into a list of words
#
#         for word in hashtag_list:
#             if word.startswith("#"):
#                 tag_list.append(word[1:])  # Add the word without the '#' to the tags list
#     tags = tag_list
#     # have to change this to public instead
#     privacy_status = "public"
#     made_for_kids = False  # Change to True if it's made for kids
#
#     # Upload the video
#     upload_video(youtube, file_path, title, description, tags, privacy_status, made_for_kids)

'''getting new songs with youtube link and poster'''
# import requests
# import datetime
#
# API_KEY = "AIzaSyBTK7JvwtqxPbLjDBHdd9Ud28DofGXu0-Q"  # Replace with your actual API key
# SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
# CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"
#
# # Get recent videos (last 7 days)
# time_threshold = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat("T") + "Z"
#
# # Search for popular pop music videos
# params = {
#     "part": "snippet",
#     "q": "pop music",
#     "order": "viewCount",
#     "publishedAfter": time_threshold,
#     "type": "video",
#     "videoCategoryId": "10",
#     "maxResults": 10,
#     "key": API_KEY
# }
#
# response = requests.get(SEARCH_URL, params=params)
# if response.status_code != 200:
#     print("Error:", response.json())
#     exit()
#
# results = response.json()
# filtered_videos = []
#
# for item in results.get("items", []):
#     title = item["snippet"]["title"]
#     video_id = item["id"]["videoId"]
#     channel_id = item["snippet"]["channelId"]
#     channel_title = item["snippet"]["channelTitle"]
#
#     # Get the highest available thumbnail
#     thumbnails = item["snippet"]["thumbnails"]
#     poster_url = thumbnails.get("maxres", thumbnails.get("standard", thumbnails.get("high", thumbnails["medium"])))[
#         "url"]
#
#     # Get channel details (subscribers)
#     channel_params = {"part": "statistics", "id": channel_id, "key": API_KEY}
#     channel_response = requests.get(CHANNELS_URL, params=channel_params)
#
#     if channel_response.status_code != 200:
#         continue
#
#     channel_data = channel_response.json()
#     subscribers = int(channel_data["items"][0]["statistics"].get("subscriberCount", 0))
#
#     # Only include artists with at least 3M subscribers
#     if subscribers >= 5_000_000:
#         video_url = f"https://www.youtube.com/watch?v={video_id}"
#         filtered_videos.append((channel_title, title, video_url, poster_url))
#
# # Display results
# for artist, title, url, poster in filtered_videos:
#     print(f"{artist} - {title}\n{url}\nPoster: {poster}\n")


'''getting the tumbnail size to 1920 * 1080 to fit the full screen in youtube'''
# from PIL import Image
# import requests
# from io import BytesIO
#
# def save_image_from_youtube(code):
#     # YouTube Thumbnail URL (replace VIDEO_ID)
#     thumbnail_url = f"https://i.ytimg.com/vi/{code}/maxresdefault.jpg"
#
#     # Fetch and upscale image
#     response = requests.get(thumbnail_url)
#     if response.status_code == 200:
#         img = Image.open(BytesIO(response.content))
#         img = img.resize((1920, 1080), Image.LANCZOS)
#         img.save("thumbnail_1920x1080.jpg")  # Save the new image
#         print("Saved: thumbnail_1920x1080.jpg")
#     else:
#         print("Failed to fetch thumbnail.")
#
# save_image_from_youtube('4QIZE708gJ4')

'''search for the official audio file using the official video id'''
# import yt_dlp
# from ytmusicapi import YTMusic
#
# def search_official_audio(video_id):
#     """Search YouTube Music for the official audio of a given video."""
#     ytmusic = YTMusic()  # Initialize API without authentication
#     video_url = f"https://www.youtube.com/watch?v={video_id}"
#
#     # Get search results for the video title
#     with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
#         info = ydl.extract_info(video_url, download=False)
#         search_query = info.get('title', '')
#
#     print(f"🔍 Searching for: {search_query}")
#
#     # Search for the official song on YouTube Music
#     search_results = ytmusic.search(search_query, filter="songs")
#     if search_results:
#         return search_results[0]['videoId']  # Return the first result (most relevant)
#
#     print("⚠️ No official audio found.")
#     return None

# print(search_official_audio("KhnVcAC5bIM"))

'''downloading music from video'''
# import yt_dlp
#
# def download_youtube_music(video_url_id, output_path="."):
#     """Download YouTube audio as an MP3 file."""
#     video_music_id_found = search_official_audio(video_url_id)
#     if video_music_id_found is not None:
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#             'outtmpl': f"{output_path}/%(title)s.%(ext)s",
#         }
#
#         video_url = f'https://www.youtube.com/watch?v={video_music_id_found}'
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([video_url])
#     else:
#         print('No audio file (mp3) found')
# # Example Usage
# # video_url = "https://www.youtube.com/watch?v=4QIZE708gJ4"
# download_youtube_music('4QIZE708gJ4')

'''getting video thumbnail from local directory'''

# import subprocess
#
#
# def extract_thumbnail(video_path, output_image, time="00:00.01"):
#     """Extracts a frame from the video as a thumbnail."""
#     command = [
#         "ffmpeg",
#         "-i", video_path,  # Input video
#         "-ss", time,  # Timestamp (e.g., 5 seconds)
#         "-vframes", "1",  # Extract 1 frame
#         "-s", "1920x1080",  # Set output resolution
#         output_image  # Output file
#     ]
#
#     try:
#         subprocess.run(command, check=True)
#         print(f"Thumbnail saved as {output_image}")
#     except subprocess.CalledProcessError:
#         print("Failed to extract thumbnail. Ensure FFmpeg is installed.")
#
#
# # Example Usage
# video_file = "video_final_output/The Weeknd - Hurry Up Tomorrow (Lyrics)/The Weeknd - Hurry Up Tomorrow (Lyrics).mp4"  # Replace with your actual video file path
# output_image = "thumbnail_1920x1080.jpg"
# extract_thumbnail(video_file, output_image)

'''getting plain_lyrics using lyricsgenuis'''
# import yt_dlp
# import lyricsgenius
#
# GENIUS_API_KEY = "KT6XN3FHd0Hy1N8TmombJtgILOSEpW4-o-lXjpQBY4jNLngrnL0pvDzG7QVlBO8p"  # 🔹 Replace with your Genius API key
# genius = lyricsgenius.Genius(GENIUS_API_KEY)
#
# def get_song_title(video_id):
#     """Fetch the song title from YouTube using yt_dlp."""
#     video_url = f"https://www.youtube.com/watch?v={video_id}"
#     ydl_opts = {'quiet': True}
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(video_url, download=False)
#         return info.get('title', '')
#
# def fetch_lyrics(song_title):
#     """Fetch lyrics from Genius using the song title."""
#     song = genius.search_song(song_title)
#     if song:
#         return song.lyrics
#     return "Lyrics not found."
#
# def get_youtube_lyrics(video_id):
#     """Main function to get lyrics from a YouTube video ID."""
#     song_title = get_song_title(video_id)
#     print(f"🔍 Searching lyrics for: {song_title}")
#
#     lyrics = fetch_lyrics(song_title)
#     return lyrics
#
# # Example Usage
# video_id = "B8VEqSBTjZQ"  # Replace with a YouTube video ID
# lyrics = get_youtube_lyrics(video_id)
# print(lyrics)

'''tried using aeneas however getting error while using pip'''

# import yt_dlp
# import lyricsgenius
# import re
# import os
# from aeneas.executetask import ExecuteTask
# from aeneas.task import Task
# from aeneas.tools.execute_task import ExecuteTaskCLI
#
#
# def generate_lrc(audio_file, lyrics_file, output_lrc):
#     """Use Aeneas to generate an LRC file with real timestamps."""
#     print('audio_file')
#     print(lyrics_file)
#     config_string = "task_language=eng|is_text_type=plain|os_task_file_format=lrc"
#     task = Task(config_string=config_string)
#
#     task.audio_file_path = audio_file
#     task.text_file_path = lyrics_file
#     task.sync_map_file_path = output_lrc
#
#     ExecuteTask(task).execute()
#     task.output_sync_map_file()
#
#     print(f"✅ LRC file saved as {output_lrc}")
#     return output_lrc
#
#
# generate_lrc("dirfile/music_file.mp3", "dirfile/plain_lyrics.txt", "dirfile/lyrics_with_ts.lrc")
#


'''test lrc'''
# import whisper
#
# model = whisper.load_model("small")
# result = model.transcribe("dirfile/music_file.mp3")
#
# # Print out timestamps with lyrics
# for segment in result["segments"]:
#     start_time = segment["start"]
#     lyric_line = segment["text"]
#     print(f"[{start_time:.2f}] {lyric_line}")

'''start and end time , perfect synced'''
# import whisper
#
# # Load Whisper model
# model = whisper.load_model("small")
#
# # Transcribe the audio
# result = model.transcribe("dirfile/music_file.mp3", verbose=True)
#
# # Read and clean the plain lyrics file
# with open("dirfile/plain_lyrics.txt", "r", encoding="utf-8") as file:
#     lyrics = [line.strip() for line in file.readlines() if line.strip()]
# if len(lyrics) > 2:
#     lyrics = lyrics[1:-1]
#
# # Whisper outputs (sorted by timestamp) - for reference
# segments = sorted(result["segments"], key=lambda x: x["start"])
# whisper_texts = [segment["text"] for segment in segments]
# whisper_timestamps = [segment["start"] for segment in segments]
#
# # Print Whisper transcription for reference
# print("Whisper Transcription (for reference):")
# for time, text in enumerate(zip(whisper_timestamps, whisper_texts)):
#     minutes, seconds = divmod(time[0], 60)
#     formatted_time = f"{int(minutes):02d}:{seconds:05.2f}"
#     print(f"[{formatted_time}] {text[1]}")
#
# # Function to format time as [MM:SS.MS]
# def format_timestamp(seconds):
#     minutes, secs = divmod(seconds, 60)
#     return f"[{int(minutes):02d}:{secs:05.2f}]"
#
# # Simple sequential timing: assume each line takes ~2-3 seconds
# aligned_lyrics = []
# current_time = 0.0  # Start at 0 seconds
# avg_line_duration = 2.5  # Average seconds per line (adjust based on song pace)
#
# for i, lyric_line in enumerate(lyrics):
#     # Use Whisper timestamp if available and reasonable, else increment
#     if i < len(whisper_timestamps):
#         whisper_time = whisper_timestamps[i]
#         # Only use Whisper time if it’s after the last time and not too far ahead
#         if whisper_time > current_time and whisper_time < current_time + 5.0:
#             current_time = whisper_time
#         else:
#             current_time += avg_line_duration
#     else:
#         current_time += avg_line_duration
#
#     formatted_time = format_timestamp(current_time)
#     aligned_lyrics.append(f"{formatted_time} {lyric_line}")
#     print(f"Assigned: '{lyric_line}' -> {formatted_time}")
#
# # Save and print results
# with open("timestamped_lyrics.txt", "w", encoding="utf-8") as out_file:
#     out_file.write("\n".join(aligned_lyrics))
#
# print("\nFinal Output:")
# for line in aligned_lyrics:
#     print(line)

'''trying to just print the starttime in [02:45.000] format so could pass it and make an lrc file'''
# import whisper
#
# # Load Whisper model
# model = whisper.load_model("small")
#
# # Transcribe the audio
# result = model.transcribe("dirfile/music_file.mp3", verbose=True)
#
# # Read and clean the plain lyrics file
# with open("dirfile/plain_lyrics.txt", "r", encoding="utf-8") as file:
#     lyrics = [line.strip() for line in file.readlines() if line.strip()]
# if len(lyrics) > 2:
#     lyrics = lyrics[1:-1]
#
# # Whisper outputs (sorted by timestamp)
# segments = sorted(result["segments"], key=lambda x: x["start"])
# whisper_timestamps = [segment["start"] for segment in segments]
#
# # Function to format time as [MM:SS.MS]
# def format_timestamp(seconds):
#     minutes, secs = divmod(seconds, 60)
#     return f"[{int(minutes):02d}:{secs:06.3f}]"
#
# # Print only the start times
# print("Whisper Start Times:")
# for timestamp in whisper_timestamps:
#     formatted_time = format_timestamp(timestamp)
#     print(formatted_time)

# Print Whisper transcription for reference
# print("Whisper Transcription (for reference):")
# for time, text in zip(whisper_timestamps, whisper_texts):
#     minutes, seconds = divmod(time, 60)
#     formatted_time = f"[{int(minutes):02d}:{seconds:05.2f}]"
#     print(f"{formatted_time} {text}")
#
# # Function to format time as [MM:SS.MS] for LRC
# def format_timestamp(seconds):
#     minutes, secs = divmod(seconds, 60)
#     return f"[{int(minutes):02d}:{secs:05.2f}]"
#
# # Align lyrics with Whisper timestamps
# aligned_lyrics = []
# current_time = 0.0  # Start at 0 seconds
# segment_idx = 0
# increment = 2.5  # Fallback increment if needed
#
# for lyric_line in lyrics:
#     # Use Whisper timestamp if available
#     if segment_idx < len(whisper_timestamps):
#         timestamp = whisper_timestamps[segment_idx]
#         # Ensure timestamp progresses forward
#         if timestamp <= current_time:
#             timestamp = current_time + 0.1  # Small bump to avoid overlap
#         current_time = timestamp
#         segment_idx += 1
#     else:
#         # If out of Whisper timestamps, increment from last time
#         current_time += increment
#         timestamp = current_time
#
#     formatted_time = format_timestamp(timestamp)
#     aligned_lyrics.append(f"{formatted_time} {lyric_line}")
#     print(f"Assigned: '{lyric_line}' -> {formatted_time}")
#
# # Save as .lrc file with correct song length
# lrc_filename = "dirfile/lyrics_with_ts.lrc"
# with open(lrc_filename, "w", encoding="utf-8") as out_file:
#     out_file.write("[ar: Artist]\n")
#     out_file.write("[ti: Song Title]\n")
#     out_file.write("[al: Album]\n")
#     out_file.write("[length: 02:51]\n")  # Updated to match song duration
#     out_file.write("\n")
#     out_file.write("\n".join(aligned_lyrics))
#
# print("\nFinal Output (saved to timestamped_lyrics.lrc):")
# for line in aligned_lyrics:
#     print(line)
#
# print(f"\nLRC file saved as: {lrc_filename}")

'''printing lyrics and timestamp from whisper'''
# import whisper
#
# # Load Whisper model
# model = whisper.load_model("small")
#
# # Transcribe the audio
# result = model.transcribe("dirfile/music_file.mp3", verbose=True)
#
# # Read and clean the plain lyrics file
# with open("dirfile/plain_lyrics.txt", "r", encoding="utf-8") as file:
#     lyrics = [line.strip() for line in file.readlines() if line.strip()]
# if len(lyrics) > 2:
#     lyrics = lyrics[1:-1]
#
# # Whisper outputs (sorted by timestamp)
# segments = sorted(result["segments"], key=lambda x: x["start"])
#
# # Format timestamps and pair with Whisper-transcribed lyrics
# for segment in segments:
#     start_time = segment["start"]
#     # Convert seconds to [MM:SS.MS] format
#     minutes = int(start_time // 60)
#     seconds = int(start_time % 60)
#     milliseconds = int((start_time % 1) * 100)  # Get 2 decimal places
#     formatted_time = f"[{minutes:02d}:{seconds:02d}.{milliseconds:02d}]"
#
#     # Get the transcribed text from Whisper
#     whisper_lyrics = segment["text"].strip()
#
#     # Print formatted timestamp and Whisper lyrics
#     print(f"{formatted_time} {whisper_lyrics}")

# import re
# import whisper
# import re
# from difflib import SequenceMatcher
#
# # Function to find the best matching segment in plain lyrics
# def find_matching_segment(whisper_text, plain_words, start_idx):
#     whisper_words = whisper_text.lower().split()
#     best_match = None
#     best_ratio = 0
#     best_end_idx = start_idx
#
#     # Search within a reasonable window of words
#     # window_size = len(whisper_words) * 2
#     for i in range(start_idx, min(start_idx + 50, len(plain_words) - len(whisper_words) + 1)):
#         candidate = " ".join(plain_words[i:i + len(whisper_words)])
#         ratio = SequenceMatcher(None, whisper_text.lower(), candidate.lower()).ratio()
#         if ratio > best_ratio and ratio > 0.5:  # Threshold for a decent match
#             best_ratio = ratio
#             best_match = candidate
#             best_end_idx = i + len(whisper_words)
#
#     return best_match, best_end_idx
#
# def getting_lrc_file():
#     # Load Whisper model
#     model = whisper.load_model("small")
#
#     # Transcribe the audio
#     result = model.transcribe("dirfile/music_file.mp3", verbose=False)
#
#     # Read and clean the plain lyrics file
#     with open("dirfile/plain_lyrics.txt", "r", encoding="utf-8") as file:
#         lyrics_lines = [line.strip() for line in file.readlines() if line.strip()]
#
#     if len(lyrics_lines) > 2:
#         lyrics_lines = lyrics_lines[1:-1]
#
#     plain_lyrics_string = " ".join(lyrics_lines)
#     plain_lyrics_words = plain_lyrics_string.split()
#
#     # Whisper outputs (sorted by timestamp)
#     segments = sorted(result["segments"], key=lambda x: x["start"])
#
#     # Split plain lyrics to match Whisper segments
#     split_lyrics = []
#     current_idx = 0
#     aligned_lyrics = []
#
#     for segment in segments:
#         start_time = segment["start"]
#         minutes = int(start_time // 60)
#         seconds = int(start_time % 60)
#         milliseconds = int((start_time % 1) * 100)
#         formatted_time = f"[{minutes:02d}:{seconds:02d}.{milliseconds:02d}]"
#
#         whisper_lyrics = segment["text"].strip()
#
#         # Find the matching segment in plain lyrics
#         matched_segment, new_idx = find_matching_segment(whisper_lyrics, plain_lyrics_words, current_idx)
#
#         if matched_segment:
#             split_lyrics.append((formatted_time, matched_segment))
#             current_idx = new_idx
#         else:
#             # If no match found, use the Whisper text as fallback and advance minimally
#             split_lyrics.append((formatted_time, whisper_lyrics))
#             current_idx += len(whisper_lyrics.split())
#
#     # Output the results
#     for timestamp, lyrics in split_lyrics:
#         print("time stamp")
#         print(f"{timestamp} {lyrics}")
#         aligned_lyrics.append(f"{timestamp} {lyrics}")
#
#     with open('dirfile/plain_lyrics.txt', 'r', encoding='utf-8') as file:
#         first_line = file.readline().strip()
#         print(first_line)
#
#
#     lrc_filename = "dirfile/lyrics_with_ts.lrc"
#     with open(lrc_filename, "w", encoding="utf-8") as out_file:
#         out_file.write(f"[00:00.00] {first_line}\n")
#         out_file.write("\n".join(aligned_lyrics))
#
#     with open(lrc_filename, "r", encoding="utf-8") as file:
#         lines = file.readlines()
#
#     count = 0
#     for i in range(len(lines)):
#         if "[00:00.00]" in lines[i]:
#             count += 1
#             if count == 2:  # Modify the second occurrence
#                 lines[i] = lines[i].replace("[00:00.00]", "[00:00.01]", 1)
#                 break  # Stop after modifying the second occurrence
#     if lines:
#         match = re.match(r"(\[.*?\]) (.*)", lines[-1].strip())  # Extract timestamp if present
#         timestamp, _ = match.groups()
#         lines[-1] = f"{timestamp} By Video Junkie\n"  # Preserve timestamp
#
#     with open(lrc_filename, "w", encoding="utf-8") as file:
#         file.writelines(lines)
#
# getting_lrc_file()


'''using lrc api to get lrc files'''

import googleapiclient.discovery
import googleapiclient.errors
import re
import isodate

# Replace with your actual API key
API_KEY = "AIzaSyBTK7JvwtqxPbLjDBHdd9Ud28DofGXu0-Q"


def get_youtube_video_info(video_id):
    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

    try:
        # Request video details including contentDetails
        request = youtube.videos().list(
            part="snippet,contentDetails",
            id=video_id
        )
        response = request.execute()

        if response["items"]:
            video = response["items"][0]
            snippet = video["snippet"]
            content_details = video["contentDetails"]

            track_name = snippet["title"]
            channel_name = snippet["channelTitle"]
            description = snippet["description"]

            # Try to extract artist from "Associated Performer" in description
            artist_match = re.search(r"Associated Performer: (.+?)(?:\n|$)", description)
            artist_name = artist_match.group(1).strip() if artist_match else None

            # Fallback: Parse title for "Artist - Song" format
            if not artist_name and " - " in track_name:
                potential_artist, potential_track = track_name.split(" - ", 1)
                artist_name = potential_artist.strip()
                track_name = potential_track.strip()

            # Final fallback: Use channel name
            if not artist_name:
                artist_name = channel_name

            # Parse duration from ISO 8601 format to seconds
            duration_iso = content_details["duration"]
            duration_seconds = int(isodate.parse_duration(duration_iso).total_seconds())

            return {
                "track_name": track_name,
                "artist_name": artist_name,
                "duration_seconds": duration_seconds,
                "description": description
            }
        else:
            return "No video found with that ID"

    except googleapiclient.errors.HttpError as e:
        return f"Error: {str(e)}"

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
        print(search_results[0]['videoId'])
        return search_results[0]['videoId']  # Return the first result (most relevant)

    print("⚠️ No official audio found.")

def clean_synced_lyrics(synced_lyrics):
    # Split lyrics into lines and filter out blank lines with timestamps
    lines = synced_lyrics.split('\n')
    cleaned_lines = []
    for line in lines:
        # Match lines with timestamp (e.g., [mm:ss.xx]) and check if content is empty or whitespace
        match = re.match(r'^\[(\d{2}:\d{2}\.\d{2})\]\s*$', line.strip())
        if not match:  # Keep lines that aren't just a timestamp with no content
            cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)

def writing_in_lrc_file(first_line, remaining_lyrics):
    lrc_filename = "dirfile/lyrics_with_ts.lrc"
    with open(lrc_filename, "w", encoding="utf-8") as out_file:
        out_file.write(f"[00:00.00] {first_line}\n")
        out_file.write(remaining_lyrics)

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
        match = re.match(r"(\[.*?\])\s?(.*)", lines[-1].strip())  # Extract timestamp dynamically
        if match:
            timestamp, _ = match.groups()
            lines[-1] = f"{timestamp} By Video Junkie\n"  # Preserve the dynamic timestamp
        else:
            print("No valid timestamp found in the last line.")

    # Clean blank lines AFTER adding "By Video Junkie"
    cleaned_content = clean_synced_lyrics(''.join(lines))

    with open(lrc_filename, "w", encoding="utf-8") as file:
        file.writelines(cleaned_content)

    print("LRC file successfully written!")


def getting_lrc_json_from_api(track_name, artist_name, duration):
    url = "https://lrclib.net/api/search"
    params = {
        "track_name": track_name,
        "artist_name": artist_name,
        "duration": duration
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        matching_results = [item for item in data if item.get("duration") == duration]

        if matching_results:
            print(matching_results[0])  # Print first matching result
            print(matching_results[0]['syncedLyrics'])
            lrc_api_synced_lyrics = matching_results[0]['syncedLyrics']
            if lrc_api_synced_lyrics is not None:
                first_line = f"{artist_name} - {track_name} (Lyrics)"
                writing_in_lrc_file(first_line, lrc_api_synced_lyrics)
            else:
                # Filter out exact matches and find closest non-exact duration
                non_exact_data = [item for item in data if item.get("duration") != duration]
                if not non_exact_data:
                    print("\nNo non-exact duration results available.")
                    return

                closest_result = min(non_exact_data, key=lambda x: abs(x.get("duration", float('inf')) - duration))
                duration_diff = abs(closest_result["duration"] - duration)
                print(f"\nClosest non-exact match found (diff: {duration_diff:.3f}s):")
                print(closest_result)
                # print("\nSynced Lyrics:")
                # print(closest_result['syncedLyrics'])
                if closest_result['syncedLyrics']:
                    first_line = f"{artist_name} - {track_name} (Lyrics)"
                    writing_in_lrc_file(first_line, closest_result['syncedLyrics'])
                else:
                    print("No results available to compare.")
                    return
        else:
            # No exact match, find closest duration
            if not data:
                print("No results available to compare.")
                return

            closest_result = min(data, key=lambda x: abs(x.get("duration", float('inf')) - duration))
            duration_diff = abs(closest_result["duration"] - duration)
            print(f"\nNo exact match found for duration {duration}. Closest match (diff: {duration_diff:.3f}s):")
            print(closest_result)
            print("\nSynced Lyrics:")
            print(closest_result['syncedLyrics'])
            first_line = f"{artist_name} - {track_name} (Lyrics)"
            writing_in_lrc_file(first_line, closest_result['syncedLyrics'])
    else:
        print(f"Error: {response.status_code}")


def getting_artist_track_info_and_save(video_id):
    result = get_youtube_video_info(video_id)
    track_name = result['track_name']
    artist_name = result['artist_name']
    duration = result['duration_seconds']
    print(track_name)
    print(artist_name)
    if '- Topic' in artist_name:
        artist_name = "".join(artist_name).split('-')[0].strip()
        print(artist_name)
    print(duration)
    getting_lrc_json_from_api(track_name, artist_name, duration)


# video_id = "UyAKpowkUDA"
# video_id = search_official_audio(video_id)
# getting_artist_track_info_and_save(video_id)


# search_official_audio('b1aBzAE-IFY')