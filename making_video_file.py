import re
import textwrap
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, ImageClip
import os
from datetime import datetime
import shutil
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import subprocess

song_name = ''
current_song_folder_name_created = ''

"""Add music to video file as in merging both of them together"""

def video_audio_merge(video_clip_path, audio_clip_path):
    video: VideoFileClip = VideoFileClip(video_clip_path)
    audio: AudioFileClip = AudioFileClip(audio_clip_path)

    # Set audio to video
    video = video.with_audio(audio)

    # Save the final video
    video.write_videofile("output_video.mp4")


def folder_creation_with_song_name(song_name):
    # Define the final folder inside 'video_final_output/'
    base_folder = "video_final_output"
    folder_name = os.path.join(base_folder, song_name)

    # Ensure 'video_final_output/' exists
    os.makedirs(base_folder, exist_ok=True)

    # Check if the folder already exists
    if os.path.exists(folder_name):
        # Generate a timestamped backup name
        new_name = f"{folder_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(folder_name, new_name)  # Rename the existing folder
        print(f"Existing folder renamed to '{new_name}'")

    # Create a new fresh folder
    os.makedirs(folder_name)
    print(f"New folder '{folder_name}' created successfully!")

    return folder_name  # Return the new folder path


def parse_lrc_file(lrc_file):
    lyrics_with_timestamps = []
    try:
        with open(lrc_file, 'r', encoding='utf-8-sig') as file:  # Use utf-8-sig
            for line in file:
                line = line.strip()
                # Handle lines with multiple timestamps for the same lyric
                matches = re.findall(r"\[(\d{2}:\d{2}\.\d{2,3})](.*)", line) # Find all matches
                for timestamp, lyric in matches: # Iterate over all matches on the current line
                    lyrics_with_timestamps.append((timestamp, lyric.strip()))

    except FileNotFoundError:
        print(f"Error: File not found at {lrc_file}")
        return None
    return lyrics_with_timestamps


def timestamp_to_seconds(timestamp):
    """
    Converts a timestamp in [mm:ss.xx] format to seconds.
    """
    minutes, seconds = timestamp.split(':')
    return int(minutes) * 60 + float(seconds)

def wrap_text(text, max_chars_per_line=29):
    wrapped_lines = textwrap.fill(text, width=max_chars_per_line).split("\n")
    max_length = max(len(line) for line in wrapped_lines)  # Find longest line
    centered_text = "\n".join(line.center(max_length) for line in wrapped_lines)  # Center each line
    return centered_text, len(wrapped_lines)  # Return wrapped text & number of lines

def get_audio_length(file_path):
    try:
        if file_path.lower().endswith('.mp3'):
            audio = MP3(file_path)
        elif file_path.lower().endswith('.wav'):
            audio = WAVE(file_path)
        else:
            return "Unsupported file format"
        length_music = audio.info.length  # Returns duration in seconds
        total_music_seconds = round(length_music)
        return total_music_seconds
    except Exception as e:
        return f"Error: {str(e)}"

def create_lyrics_video_singular(video_file, lrc_file, output_file):
    # Define the output file path inside the created folder
    output_file = os.path.join(output_file)
    """
    Creates a video with scrolling lyrics from an LRC file.
    """

    lyrics_with_timestamps = parse_lrc_file(lrc_file)
    clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions

    # Screen dimensions
    screen_width, screen_height = 1920, 1080

    # Create a list of text clips for each lyric
    text_clips = []
    for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
        # Calculate start and end times for the current lyric
        start_time = timestamp_to_seconds(timestamp)
        end_time = (
            timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
            if i + 1 < len(lyrics_with_timestamps)
            else start_time + (get_audio_length('dirfile/music_file.mp3') - start_time) #end time this when the lyrics would disappear if no other line is given at the end of the video (lik the last line)
        )

        # Calculate the height for the current line
        wrapped_text, len_line = wrap_text(lyric, max_chars_per_line=29)
        # current_text_height = 180 + (len_line - 1) * 20  # Adjust height based on line count
        line_spacing = 95  # Increase spacing for better readability
        current_text_height = len_line * line_spacing

        # Center position for the current line
        y_position_center = (screen_height / 2) - (current_text_height / 2)

        # Add the current lyric with a highlighted style
        current_clip = TextClip(
            text="\n" + wrapped_text + "\n",
            font="fontttffile/Designer.otf",
            color="white",  # Highlighted color for the current lyric
            method="caption",
            font_size=90,
            horizontal_align='center',
            vertical_align='center',
            size=(screen_width, current_text_height),
        ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)

        text_clips.append(current_clip)

    # Combine the video clip (background) with text clips
    final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))

    # Export the final video
    final_video.write_videofile(output_file, fps=24)


def create_lyrics_video(video_file, lrc_file, output_file):
    """
    Creates a video with scrolling lyrics from an LRC file.
    """
    output_file = os.path.join(output_file)
    lyrics_with_timestamps = parse_lrc_file(lrc_file)
    clip = VideoFileClip(video_file).resized((1920, 1080))

    # Screen dimensions
    screen_width, screen_height = 1920, 1080

    # Constants for text display
    line_spacing = 95
    font_size = 90
    max_chars = 29
    fixed_spacing = 5  # Increased fixed spacing between lines

    # Create a list of text clips for each lyric
    text_clips = []
    for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
        # Calculate start and end times for the current lyric
        start_time = timestamp_to_seconds(timestamp)
        end_time = (
            timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
            if i + 1 < len(lyrics_with_timestamps)
            else start_time + (get_audio_length('dirfile/music_file.mp3') - start_time) #end time this when the lyrics would disappear if no other line is given at the end of the video (lik the last line)
        )

        # Process current line first
        current_wrapped, current_line_count = wrap_text(lyric, max_chars_per_line=max_chars)
        current_height = current_line_count * line_spacing

        # Center the current line vertically
        current_y = (screen_height - current_height) / 2

        # Create the current line clip (highlighted)
        current_clip = TextClip(
            text="\n" + current_wrapped + "\n",
            font="fontttffile/Designer.otf",
            color="white",
            method="caption",
            font_size=font_size,
            horizontal_align='center',
            vertical_align='center',
            size=(screen_width, current_height),
        ).with_position(("center", current_y)).with_start(start_time).with_end(end_time)

        text_clips.append(current_clip)

        # Add past lines (above the current line)
        past_y = current_y
        for j in range(i - 1, max(-1, i - 4 - 1), -1):  # Adjusted range
            if j < 0:  # Skip if index is invalid
                continue
            past_wrapped, past_line_count = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=max_chars)
            past_height = past_line_count * line_spacing

            # Position above previous line with fixed spacing
            # Modified positioning logic to ensure more visibility
            past_y = past_y - (past_height + fixed_spacing)

            # More lenient boundary check - allow partial visibility
            if past_y + (past_height / 2) < 0:
                continue

            # Adjust position if partially off-screen
            if past_y < 0:
                visible_portion = past_height + past_y  # Calculate visible portion
                if visible_portion > past_height / 3:  # If at least 1/3 is visible
                    # Keep it partially visible
                    past_clip = TextClip(
                        text="\n" + past_wrapped + "\n",
                        font="fontttffile/Designer.otf",
                        color="gray",
                        method="caption",
                        font_size=font_size,
                        horizontal_align='center',
                        vertical_align='center',
                        size=(screen_width, past_height),
                    ).with_position(("center", past_y)).with_start(start_time).with_end(end_time)

                    text_clips.append(past_clip)
            else:
                # Fully visible
                past_clip = TextClip(
                    text="\n" + past_wrapped + "\n",
                    font="fontttffile/Designer.otf",
                    color="gray",
                    method="caption",
                    font_size=font_size,
                    horizontal_align='center',
                    vertical_align='center',
                    size=(screen_width, past_height),
                ).with_position(("center", past_y)).with_start(start_time).with_end(end_time)

                text_clips.append(past_clip)

        # Add future lines (below the current line)
        future_y = current_y + current_height
        for j in range(i + 1, min(len(lyrics_with_timestamps), i + 4)):
            future_wrapped, future_line_count = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=max_chars)
            future_height = future_line_count * line_spacing

            # Add fixed spacing between lines
            future_y = future_y + fixed_spacing

            # Skip if it would go off screen
            if future_y + future_height > screen_height:
                continue

            future_clip = TextClip(
                text="\n" + future_wrapped + "\n",
                font="fontttffile/Designer.otf",
                color="gray",
                method="caption",
                font_size=font_size,
                horizontal_align='center',
                vertical_align='center',
                size=(screen_width, future_height),
            ).with_position(("center", future_y)).with_start(start_time).with_end(end_time)

            text_clips.append(future_clip)

            # Update y position for next future line
            future_y = future_y + future_height

    # Combine the video clip (background) with text clips
    final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))

    # Export the final video
    final_video.write_videofile(output_file, fps=24)

def copying_raw_file(song_name):
    source_files = [
        "lyrics_with_ts.lrc",
        "music_file.mp3",
        "video_without_music.mp4"
    ]

    destination_files = [
        f"{song_name}.lrc",
        f"{song_name}.mp3",
        f"{song_name}_without_audio.mp4"
    ]

    # Define source and destination directories
    source_folder = "dirfile/"
    destination_folder = f"video_final_output/{song_name}"

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Loop through both lists simultaneously
    for src_file, dest_file in zip(source_files, destination_files):
        source_path = os.path.join(source_folder, src_file)
        destination_path = os.path.join(destination_folder, dest_file)

        if os.path.exists(source_path):  # Check if source file exists
            # If destination file already exists, rename it with a timestamp
            if os.path.exists(destination_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
                name, ext = os.path.splitext(dest_file)  # Split name and extension
                destination_path = os.path.join(destination_folder, f"{name}_{timestamp}{ext}")

            # Copy the file to the destination
            shutil.copy(source_path, destination_path)
            print(f"Copied '{source_path}' to '{destination_path}'")
        else:
            print(f"Warning: Source file '{source_path}' does not exist!")

    print("All files processed successfully!")


def song_title(directory_passed):
    with open(directory_passed, 'r', encoding='utf-8-sig') as file:
        for line in file:
            # print(line)
            title = line.split(']')[-1].strip()
            return title

def create_blank_mp4(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create the empty file
    with open(output_path, "wb") as f:
        pass

def create_video_from_image(image_path, output_path, duration, resolution=(1920, 1080), fps=30):
    # Load the image and resize it to fit the resolution
    image_clip = ImageClip(image_path).resized(resolution).with_duration(duration)

    # Create a black rectangle with the same resolution and 40% transparency (alpha=0.4)
    black_overlay = ColorClip(size=resolution, color=(0, 0, 0)).with_duration(duration).with_opacity(0.4)

    # Composite the image and the black overlay
    final_clip = CompositeVideoClip([image_clip, black_overlay])

    # Write the video file
    final_clip.write_videofile(output_path, fps=fps, codec="libx264", audio=False)

    print(f"Video saved at {output_path}")

def extract_thumbnail(video_path, output_image, time="00:00.01"):
    """Extracts a frame from the video as a thumbnail."""
    command = [
        "ffmpeg",
        "-i", video_path,  # Input video
        "-ss", time,  # Timestamp (e.g., 5 seconds)
        "-vframes", "1",  # Extract 1 frame
        "-s", "1920x1080",  # Set output resolution
        output_image  # Output file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Thumbnail saved as {output_image}")
    except subprocess.CalledProcessError:
        print("Failed to extract thumbnail. Ensure FFmpeg is installed.")

# Example usage
song_title_created = song_title('dirfile/lyrics_with_ts.lrc')
create_video_from_image("dirfile/image_background.jpg", "dirfile/video_without_music.mp4", duration=get_audio_length("dirfile/music_file.mp3"))
video_audio_merge("dirfile/video_without_music.mp4", "dirfile/music_file.mp3")
folder_creation_with_song_name(str(song_title_created))
create_blank_mp4(f"video_final_output/{song_title_created}/{song_title_created}.mp4")
# create_lyrics_video_singular("output_video.mp4", "dirfile/lyrics_with_ts.lrc", f"video_final_output/{song_title_created}/{song_title_created}singular.mp4")
create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", f"video_final_output/{song_title_created}/{song_title_created}.mp4")
extract_thumbnail(f"video_final_output/{song_title_created}/{song_title_created}.mp4", f"video_final_output/{song_title_created}/{song_title_created}thumbnail.jpg")
copying_raw_file(song_title_created)