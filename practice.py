from mutagen.mp3 import MP3
from mutagen.wave import WAVE
# import re
#
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