'''upload video on youtube'''

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import requests
import json
import re

# Define the required YouTube API scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def authenticate():
    """Authenticate using OAuth 2.0 and return YouTube API service."""
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=credentials)


def upload_video(youtube, file_path, title, description, tags, privacy_status, made_for_kids, thumbnail_path):
    """Upload a video to YouTube."""
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "10",  # Category ID (22 = People & Blogs)
            },
            "status": {
                "privacyStatus": privacy_status,  # public, private, unlisted
                "madeForKids": made_for_kids
            },
        },
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True),
    )
    response = request.execute()
    video_id = response["id"]
    print("Uploaded video ID:", video_id)
    # Upload Thumbnail
    if thumbnail_path:
        set_thumbnail(youtube, video_id, thumbnail_path)


def set_thumbnail(youtube, video_id, thumbnail_path):
    """Set a custom thumbnail for an uploaded video."""
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    )
    response = request.execute()
    print(response)
    print("Thumbnail uploaded successfully!")

def song_title(directory_passed):
    with open(directory_passed, 'r', encoding='utf-8-sig') as file:
        for line in file:
            # print(line)
            title = line.split(']')[-1].strip()
            return title

def convert_lrc_to_txt(input_file, output_file, hashtag):
    # Step 1: Read LRC file and remove timestamps
    with open(input_file, "r", encoding="utf-8-sig") as infile:  # Use 'utf-8-sig' to remove BOM
        lines = infile.readlines()

    cleaned_lines = []
    for line in lines:
        clean_line = re.sub(r"\[\d{2}:\d{2}\.\d{2}\]", "", line).strip()  # Remove timestamps & trim spaces
        if clean_line:
            cleaned_lines.append(clean_line)

    # Step 2: Write cleaned lyrics to output file
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(cleaned_lines))

    # Step 3: Reopen the file and adjust the first line
    with open(output_file, "r", encoding="utf-8") as outfile:
        updated_lines = outfile.readlines()

    if updated_lines:
        first_line = updated_lines[0].lstrip()  # Remove any leading spaces
        updated_lines[0] = hashtag + "\n\n" + first_line + "\n"  # Add two new lines after first line

    # Step 4: Write back adjusted lyrics
    with open(output_file, "w", encoding="utf-8") as final_outfile:
        final_outfile.writelines(updated_lines)

def getting_artist_and_song_name_for_hashtag(song_name):

    url = "https://shazam.p.rapidapi.com/search"
    artist_list = []

    song_name = song_name.split('(Lyrics)')[0].strip()
    if "(Official Video)" in song_name:
        song_name = song_name.split('(Official Video)')[0].strip()

    querystring = {"term":f"{song_name}","locale":"en-US","offset":"0","limit":"5"}

    headers = {
        "x-rapidapi-key": "1dc406c142msh3655a2a0d7c612ep1f4293jsnc9baa7b3ad3c",
        "x-rapidapi-host": "shazam.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    raw_json = response.json()

    response = json.dumps(raw_json, indent=4)

    # print(response)

    # Convert the JSON string back to a Python object
    loaded_data = json.loads(response)
    # print(loaded_data)
    main_tracks = loaded_data["tracks"]
    main_hits = main_tracks["hits"]
    # print(main_hits)
    main_track = main_hits[0]["track"]
    title =  main_track["title"]
    if "(" in title:
        title = "".join(title).split('(')[0].lstrip()
    else:
        title = "".join(title).lstrip()
    try:
        # Access the "artists" list
        artists = loaded_data["artists"]
        # print(artists)
        # Access the "hits" list
        hits = artists["hits"]
        # Extract the names
        artist_names = [hit["artist"]["name"] for hit in hits]

        # Print the names
        for name in artist_names:
            # print(name)
            artist_list.append(name)
    except KeyError:
        artist = main_track["subtitle"]
        # print(len("".join(artist).split('&')))
        for i in "".join(artist).split('&'):
            artist_individual_name = i.strip()
            artist_list.append(artist_individual_name)

    # print(artist_list)

    title_lower = title.lower() #Make the title lower case for easier comparison

    found_artists = []

    for artist in artist_list:
        if artist.lower() in title_lower:
            found_artists.append(artist)

    #Get the remainder of the title
    remainder = title

    # for artist in found_artists:
    #     remainder = remainder.replace(artist, "") #Remove the artist names.

    # remainder = remainder.replace("feat.","") #clean up feat.
    # remainder = remainder.replace("&","") #clean up &
    # remainder = remainder.replace("-","") #clean up -
    # remainder = remainder.replace("(Lyrics)","") #clean up (Lyrics)
    remainder = remainder.replace(" ", "").lower()
    remainder_clean = remainder.strip() #clean up extra spaces.

    # print(remainder)
    # print(artist_list)
    # print('printing #hashtag')
    output_string = f"#{remainder_clean}"
    rest_hashtag = "#music #lyrics #lyricvideo #lyrical #scrolllyrics"

    for artist_name_print in artist_list:
        artist_clean = artist_name_print.lower().replace(" ", "").replace("-", "") #Clean artist name
        output_string += f" #{artist_clean}"

    return f"{output_string} {rest_hashtag}"


if __name__ == "__main__":
    youtube = authenticate()

    # Set video details
    # file_path = "dirfile/video_without_music.mp4"
    file_path = "video_final_output/Gracie Abrams - That’s So True (Lyrics)/Gracie Abrams - That’s So True (Lyrics).mp4"
    title = song_title('video_final_output/Gracie Abrams - That’s So True (Lyrics)/Gracie Abrams - That’s So True (Lyrics).lrc')
    # create a txt file that could further be used to copy and
    # past the lyrics without the time stamps as well as the tags should be created on top of the lyrics
    hashtag_generate = getting_artist_and_song_name_for_hashtag(title)
    convert_lrc_to_txt("video_final_output/Gracie Abrams - That’s So True (Lyrics)/Gracie Abrams - That’s So True (Lyrics).lrc", "dirfile/plain_lyrics.txt", hashtag_generate)
    # Read description from the text file
    description_file_path = "dirfile/plain_lyrics.txt"  # Replace with your actual file path
    with open(description_file_path, "r", encoding="utf-8") as file:
        description = file.read()
    # pass the tags on top of description as well as below in tags section
    tag_list = []
    if hashtag_generate:  # Check if hashtag_generate is not empty
        hashtag_list = hashtag_generate.split()  # Split the string into a list of words

        for word in hashtag_list:
            if word.startswith("#"):
                tag_list.append(word[1:])  # Add the word without the '#' to the tags list
    tags = tag_list
    # have to change this to public instead
    privacy_status = "public"
    made_for_kids = False  # Change to True if it's made for kids
    thumbnail_path = "video_final_output/Gracie Abrams - That’s So True (Lyrics)/Gracie Abrams - That’s So True (Lyrics)-thumbnail.jpg"

    # Upload the video
    upload_video(youtube, file_path, title, description, tags, privacy_status, made_for_kids, thumbnail_path)


