

"""
give lrc file with lyrics time stamp, and it would give us time stamp and lyrics to show on the video
"""

# def parse_lrc_file(lrc_file):
#     """
#     Parses an LRC file and returns a list of (timestamp, lyric) tuples.
#     """
#     lyrics_with_timestamps = []
#     with open(lrc_file, 'r', encoding='utf-8') as file:
#         for line in file:
#             line = line.strip()
#             # print(f"Processing line: {line}")  # Debugging: Print the line being processed
#             if line and line.startswith('['):  # Ensure the line starts with a timestamp
#                 # Split the line into timestamp and lyric
#                 timestamp_end = line.find(']')
#                 if timestamp_end != -1:
#                     timestamp = line[1:timestamp_end]  # Extract the timestamp without brackets
#                     lyric = line[timestamp_end + 1:].strip()  # Extract the lyric
#                     print(f"Parsed: timestamp={timestamp}, lyric={lyric}")  # Debugging: Print parsed values
#                     lyrics_with_timestamps.append((timestamp, lyric))
#     return lyrics_with_timestamps
#
# # Call the function and store the return value
# lyrics_with_timestamps = parse_lrc_file('dirfile/lyrics_with_ts.lrc')
#
# # Print the lyrics_with_timestamps list outside the function
# print("Lyrics with Timestamps:")
# for timestamp, lyric in lyrics_with_timestamps:
#     print(f"[{timestamp}] {lyric}")

# import re
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
# # Call the function and store the return value
# lyrics_with_timestamps = parse_lrc_file('dirfile/lyrics_with_ts.lrc')

# Print the lyrics_with_timestamps list outside the function
# print("Lyrics with Timestamps:")
# for timestamp, lyric in lyrics_with_timestamps:
#     print(f"[{timestamp}] {lyric}")



"""Showing text on Video file"""
# from moviepy import VideoFileClip, TextClip, CompositeVideoClip
#
# # Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
# # adjust the audio volume to 100% of its original volume
#
# clip = (
#     VideoFileClip("dirfile/video_without_music.mp4")
#     .subclipped(10, 20)
#     .with_volume_scaled(1.0)
# )
#
#
# # Generate a text clip. You can customize the font, color, etc.
# txt_clip = TextClip(
#     font="C:/Windows/Fonts/Arial.ttf",
#     text="Hello there!",
#     font_size=70,
#     color='white'
# ).with_duration(10).with_position('center')
#
# # Overlay the text clip on the first video clip
# final_video = CompositeVideoClip([clip, txt_clip])
# final_video.write_videofile("result.mp4")



"""final merging video with lyrics"""

# from moviepy import VideoFileClip, TextClip, CompositeVideoClip
# import re
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
#
# def timestamp_to_seconds(timestamp):
#     """
#     Converts a timestamp in [mm:ss.xx] format to seconds.
#     """
#     minutes, seconds = timestamp.split(':')
#     return int(minutes) * 60 + float(seconds)

"""Final version of merging video and lyrics together"""


# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 120  # Actual height of text
#     padding_vertical = 10  # Vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         # Center y-position for the current lyric
#         y_position_center = screen_height // 2
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text=lyric,
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="caption",
#             size=(screen_width, text_height),
#             transparent=True  # Enable transparency for text
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text=lyrics_with_timestamps[j][1],
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="caption",
#                     size=(screen_width, text_height),
#                     transparent=True  # Enable transparency for text
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)
#
#
# # Example usage
# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")

"""Shrink  text"""

#
# def wrap_text(text, max_chars_per_line=50):
#     """Wrap text into multiple lines based on the maximum characters per line."""
#     return textwrap.fill(text, width=max_chars_per_line)
#
# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 120  # Approximate height of text
#     padding_vertical = 10  # Increased vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         # Center y-position for the current lyric
#         y_position_center = (screen_height // 2) - (text_height // 2)   # Adjusted for top buffer
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text="\n" + wrap_text(lyric) + "\n",
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="label",
#             font_size=90,
#             # size=(screen_width, text_height),
#             bg_color="red",  # Temporary background to visualize text bounds
#             transparent=False  # Disable transparency for debugging
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Ensure the y_position is within the visible area
#                 if y_position < 0 or y_position + text_height > screen_height:
#                     continue  # Skip if the text would be cut off
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text="\n" + wrap_text(lyrics_with_timestamps[j][1]) + "\n",
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="label",
#                     font_size=90,
#                     # size=(screen_width, text_height),
#                     bg_color="red",  # Temporary background to visualize text bounds
#                     transparent=False  # Disable transparency for debugging
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)
#
# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")
#
#
# """Final 02/13/2025"""
# import re

"""Add music to video file as in merging both of them together"""
# import textwrap
#
# from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip

# # Add type hints
# video: VideoFileClip = VideoFileClip("dirfile/video_without_music.mp4")
# audio: AudioFileClip = AudioFileClip("dirfile/music_file.mp3")
#
# # Set audio to video
# video = video.with_audio(audio)
#
# # Save the final video
# video.write_videofile("output_video.mp4")

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
#
# def timestamp_to_seconds(timestamp):
#     """
#     Converts a timestamp in [mm:ss.xx] format to seconds.
#     """
#     minutes, seconds = timestamp.split(':')
#     return int(minutes) * 60 + float(seconds)
#
# def wrap_text(text, max_chars_per_line=40):
#     # wrapped_lines = textwrap.fill(text, width=max_chars_per_line)
#     wrapped_lines = textwrap.fill(text, width=max_chars_per_line).split("\n")
#     max_length = max(len(line) for line in wrapped_lines)  # Find longest line
#     centered_text = "\n".join(line.center(max_length) for line in wrapped_lines)  # Center each line
#     return centered_text
#
#
# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 180  # Approximate height of text
#     padding_vertical = 10  # Increased vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         # Center y-position for the current lyric
#         y_position_center = (screen_height // 2) - (text_height // 2)   # Adjusted for top buffer
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text="\n" + wrap_text(lyric, max_chars_per_line=40) + "\n",
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="caption",
#             font_size=90,
#             horizontal_align='center',
#             vertical_align='center',
#             size=(screen_width, text_height),
#             # bg_color="red",  # Temporary background to visualize text bounds
#             # transparent=False  # Disable transparency for debugging
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Ensure the y_position is within the visible area
#                 if y_position < 0 or y_position + text_height > screen_height:
#                     continue  # Skip if the text would be cut off
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text="\n" + wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=40) + "\n",
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="caption",
#                     font_size=90, # Limit the width to 80% of the screen width
#                     horizontal_align='center',
#                     vertical_align='center',
#                     size=(screen_width, text_height),
#                     # bg_color="red",  # Temporary background to visualize text bounds
#                     # transparent=False  # Disable transparency for debugging
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)
#
# # Example usage
# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")

"""test"""


# def wrap_text(text, max_chars_per_line=50):
#     """Wrap text manually and center-align it."""
#     wrapped_lines = textwrap.wrap(text, width=max_chars_per_line)
#     max_width = max(len(line) for line in wrapped_lines)  # Find longest line
#     return "\n".join(line.center(max_width) for line in wrapped_lines)  # Center-align each line

# def wrap_text(text, max_chars_per_line=50):
#     """
#     Wrap text into multiple lines with perfect center alignment for all lines.
#
#     Args:
#         text (str): The text to wrap and center.
#         max_chars_per_line (int): Maximum characters per line.
#
#     Returns:
#         str: The wrapped and perfectly center-aligned text.
#     """
#     words = text.split()
#     lines = []
#     current_line = []
#     current_length = 0
#
#     # Build lines word by word
#     for word in words:
#         # Check if adding this word would exceed max length
#         if current_length + len(word) + (1 if current_line else 0) <= max_chars_per_line:
#             current_line.append(word)
#             current_length += len(word) + (1 if current_line else 0)
#         else:
#             # Add completed line
#             if current_line:
#                 lines.append(' '.join(current_line))
#             # Start new line with current word
#             current_line = [word]
#             current_length = len(word)
#
#     # Add the last line
#     if current_line:
#         lines.append(' '.join(current_line))
#
#     # Find maximum line length
#     max_line_length = max(len(line) for line in lines)
#
#     # Center each line
#     centered_lines = []
#     for line in lines:
#         padding = ' ' * ((max_line_length - len(line)) // 2)
#         centered_line = padding + line
#         centered_lines.append(centered_line)
#
#     # Join with newlines to maintain spacing
#     return '\n'.join(centered_lines)

# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 120  # Approximate height of text
#     padding_vertical = 10  # Increased vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         # Center y-position for the current lyric
#         y_position_center = (screen_height // 2) - (text_height // 2)   # Adjusted for top buffer
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text=lyric,
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="caption",
#             # font_size=60,
#             horizontal_align='center',
#             vertical_align='center',
#             size=(screen_width, text_height),
#             bg_color="red",  # Temporary background to visualize text bounds
#             transparent=False  # Disable transparency for debugging
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Ensure the y_position is within the visible area
#                 if y_position < 0 or y_position + text_height > screen_height:
#                     continue  # Skip if the text would be cut off
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text=lyrics_with_timestamps[j][1],
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="caption",
#                     font_size=60, # Limit the width to 80% of the screen width
#                     horizontal_align='center',
#                     vertical_align='center',
#                     size=(screen_width, text_height),
#                     bg_color="red",  # Temporary background to visualize text bounds
#                     transparent=False  # Disable transparency for debugging
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)

# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")


#
#
# """reworking on not resize long text """
# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 120  # Approximate height of text
#     padding_vertical = 5  # Increased vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         # Center y-position for the current lyric
#         y_position_center = (screen_height // 2) - (text_height // 2)   # Adjusted for top buffer
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text="\n" + lyric + "\n",
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="caption",
#             size=(screen_width, text_height),
#             bg_color="red",  # Temporary background to visualize text bounds
#             transparent=False  # Disable transparency for debugging
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Ensure the y_position is within the visible area
#                 if y_position < 0 or y_position + text_height > screen_height:
#                     continue  # Skip if the text would be cut off
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text="\n" + lyrics_with_timestamps[j][1] + "\n",
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="caption",
#                     size=(screen_width, text_height),
#                     bg_color="red",  # Temporary background to visualize text bounds
#                     transparent=False  # Disable transparency for debugging
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)
#
#
# # Example usage
# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")



"""Main code"""
# import re
# import textwrap
# from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
#
# """Add music to video file as in merging both of them together"""
#
# # Add type hints
# video: VideoFileClip = VideoFileClip("dirfile/video_without_music.mp4")
# audio: AudioFileClip = AudioFileClip("dirfile/music_file.mp3")
#
# # Set audio to video
# video = video.with_audio(audio)
#
# # Save the final video
# video.write_videofile("output_video.mp4")

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
#
# def timestamp_to_seconds(timestamp):
#     """
#     Converts a timestamp in [mm:ss.xx] format to seconds.
#     """
#     minutes, seconds = timestamp.split(':')
#     return int(minutes) * 60 + float(seconds)
#
# def wrap_text(text, max_chars_per_line=29):
#     wrapped_lines = textwrap.fill(text, width=max_chars_per_line).split("\n")
#     max_length = max(len(line) for line in wrapped_lines)  # Find longest line
#     centered_text = "\n".join(line.center(max_length) for line in wrapped_lines)  # Center each line
#     return centered_text, len(wrapped_lines)  # Return wrapped text & number of lines
#
# def create_lyrics_video(video_file, lrc_file, output_file):
#     """
#     Creates a video with scrolling lyrics from an LRC file.
#     """
#     lyrics_with_timestamps = parse_lrc_file(lrc_file)
#     clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions
#
#     # Screen dimensions
#     screen_width, screen_height = 1920, 1080
#     text_height = 180  # Approximate height of text
#     padding_vertical = 10  # Increased vertical padding between lines
#     line_height = text_height + padding_vertical  # Total height including padding
#
#     # Create a list of text clips for each lyric
#     text_clips = []
#     for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#         # Calculate start and end times for the current lyric
#         start_time = timestamp_to_seconds(timestamp)
#         end_time = (
#             timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
#             if i + 1 < len(lyrics_with_timestamps)
#             else start_time + 5
#         )
#
#         wrapped_text, len_line = wrap_text(lyric, max_chars_per_line=29)
#
#         # Center y-position for the current lyric
#         y_position_center = (screen_height / 2) - (text_height * len_line / 2)   # Adjusted for top buffer
#
#
#         # Add the current lyric with a highlighted style
#         current_clip = TextClip(
#             text="\n" + wrapped_text + "\n",
#             font="fontttffile/Designer.otf",
#             color="white",  # Highlighted color for the current lyric
#             method="caption",
#             font_size=90,
#             horizontal_align='center',
#             vertical_align='center',
#             size=(screen_width, text_height),
#             # bg_color="red",  # Temporary background to visualize text bounds
#             # transparent=False  # Disable transparency for debugging
#         ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)
#
#         # Add the current lyric to the text clips list
#         text_clips.append(current_clip)
#
#         # Add previous and future lines with dimmed styles
#         for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
#             if j != i:  # Skip the current lyric since it's already added
#                 lines_away = j - i  # How many lines away from current
#                 offset = lines_away * line_height  # Use line_height for spacing
#                 y_position = y_position_center + offset
#
#                 # Ensure the y_position is within the visible area
#                 if y_position < 0 or y_position + text_height > screen_height:
#                     continue  # Skip if the text would be cut off
#
#                 # Determine the color for past (light gray) and future (gray) lines
#                 color = "gray" if j > i else "gray"
#
#                 prev_wrapped_text, prev_len_line = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=29)
#
#                 # Create the clip for the previous or future line
#                 previous_clip = TextClip(
#                     text="\n" + prev_wrapped_text + "\n",
#                     font="fontttffile/Designer.otf",
#                     color=color,
#                     method="caption",
#                     font_size=90, # Limit the width to 80% of the screen width
#                     horizontal_align='center',
#                     vertical_align='center',
#                     size=(screen_width, text_height),
#                     # bg_color="red",  # Temporary background to visualize text bounds
#                     # transparent=False  # Disable transparency for debugging
#                 ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)
#
#                 # Add the clip to the text clips list
#                 text_clips.append(previous_clip)
#
#     # Combine the video clip (background) with text clips
#     final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))
#
#     # Export the final video
#     final_video.write_videofile(output_file, fps=24)
#
# # Example usage
# create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")

import re
import textwrap
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip


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

def create_lyrics_video(video_file, lrc_file, output_file):
    """
    Creates a video with scrolling lyrics from an LRC file.
    """
    lyrics_with_timestamps = parse_lrc_file(lrc_file)
    clip = VideoFileClip(video_file).resized((1920, 1080))  # Ensure the background fits the screen dimensions

    # Screen dimensions
    screen_width, screen_height = 1920, 1080
    text_height = 180  # Approximate height of text
    padding_vertical = 10  # Increased vertical padding between lines
    line_height = text_height + padding_vertical  # Total height including padding

    # Create a list of text clips for each lyric
    text_clips = []
    for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
        # Calculate start and end times for the current lyric
        start_time = timestamp_to_seconds(timestamp)
        end_time = (
            timestamp_to_seconds(lyrics_with_timestamps[i + 1][0])
            if i + 1 < len(lyrics_with_timestamps)
            else start_time + 5
        )

        wrapped_text, len_line = wrap_text(lyric, max_chars_per_line=29)

        # Center y-position for the current lyric
        y_position_center = (screen_height / 2) - (text_height * len_line / 2)   # Adjusted for top buffer


        # Add the current lyric with a highlighted style
        current_clip = TextClip(
            text="\n" + wrapped_text + "\n",
            font="fontttffile/Designer.otf",
            color="white",  # Highlighted color for the current lyric
            method="caption",
            font_size=90,
            horizontal_align='center',
            vertical_align='center',
            size=(screen_width, line_height * len_line),
            # bg_color="red",  # Temporary background to visualize text bounds
            # transparent=False  # Disable transparency for debugging
        ).with_position(("center", y_position_center)).with_start(start_time).with_end(end_time)

        # Add the current lyric to the text clips list
        text_clips.append(current_clip)

        # Add previous and future lines with dimmed styles
        for j in range(max(0, i - 3), min(len(lyrics_with_timestamps), i + 4)):
            if j != i:  # Skip the current lyric since it's already added
                lines_away = j - i  # How many lines away from current
                offset = lines_away * line_height  # Use line_height for spacing
                y_position = y_position_center + offset

                # Ensure the y_position is within the visible area
                if y_position < 0 or y_position + text_height > screen_height:
                    continue  # Skip if the text would be cut off

                # Determine the color for past (light gray) and future (gray) lines
                color = "gray" if j > i else "gray"

                prev_wrapped_text, prev_len_line = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=29)

                # Create the clip for the previous or future line
                previous_clip = TextClip(
                    text="\n" + prev_wrapped_text + "\n",
                    font="fontttffile/Designer.otf",
                    color=color,
                    method="caption",
                    font_size=90, # Limit the width to 80% of the screen width
                    horizontal_align='center',
                    vertical_align='center',
                    size=(screen_width, line_height * prev_len_line),
                    # bg_color="red",  # Temporary background to visualize text bounds
                    # transparent=False  # Disable transparency for debugging
                ).with_position(("center", y_position)).with_start(start_time).with_end(end_time)

                # Add the clip to the text clips list
                text_clips.append(previous_clip)

    # Combine the video clip (background) with text clips
    final_video = CompositeVideoClip([clip] + text_clips, size=(screen_width, screen_height))

    # Export the final video
    final_video.write_videofile(output_file, fps=24)

# Example usage
create_lyrics_video("output_video.mp4", "dirfile/lyrics_with_ts.lrc", "result.mp4")
