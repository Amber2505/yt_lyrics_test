import re
import textwrap

line_spacing = 95
max_chars = 29
fixed_spacing = 5

def wrap_text(text, max_chars_per_line=29):
    wrapped_lines = textwrap.fill(text, width=max_chars_per_line).split("\n")
    max_length = max(len(line) for line in wrapped_lines)  # Find longest line
    centered_text = "\n".join(line.center(max_length) for line in wrapped_lines)  # Center each line
    return centered_text, len(wrapped_lines)  # Return wrapped text & number of lines

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


lyrics_with_timestamps = parse_lrc_file("dirfile/lyrics_with_ts.lrc")

for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
    # print(lyric)
    for j in range(i - 1, max(0, i - 4), -1):
        past_wrapped, past_line_count = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=max_chars)
        print(past_wrapped)
        # past_height = past_line_count * line_spacing
        # print(f'j = {j} (i={i}')
        # print(past_wrapped)
        # print(past_height)

# for i, (timestamp, lyric) in enumerate(lyrics_with_timestamps):
#     # Modified range to ensure it always goes back to include the first line
#     # Start at i-1 (previous line) and go down to max line index of 0
#     # Limit to 3 past lines maximum
#     past_lines_to_process = min(3, i)  # Calculate how many past lines we can show
#
#     for j in range(i - 1, i - 1 - past_lines_to_process, -1):
#         past_wrapped, past_line_count = wrap_text(lyrics_with_timestamps[j][1], max_chars_per_line=max_chars)
#         past_height = past_line_count * line_spacing
#         print(f"Showing past line {j} (i={i}): {past_wrapped}")
#         print(f"Height: {past_height}")