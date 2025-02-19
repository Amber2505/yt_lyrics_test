# import librosa
# import numpy as np
#
#
# def get_lyrics_timing(audio_file, lyrics_file):
#     # Load the audio file
#     print("Loading audio file...")
#     y, sr = librosa.load(audio_file)
#     duration = librosa.get_duration(y=y, sr=sr)
#     print(f"Audio loaded. Duration: {duration:.2f} seconds")
#
#     # Get tempo and beat frames
#     tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
#     print(f"Detected tempo: {float(tempo):.2f} BPM")
#
#     # Convert beat frames to time
#     beat_times = librosa.frames_to_time(beat_frames, sr=sr)
#
#     # Read lyrics
#     with open(lyrics_file, 'r', encoding='utf-8') as f:
#         lyrics = [line.strip() for line in f.readlines() if line.strip()]
#
#     # Calculate number of lyrics and spacing
#     num_lyrics = len(lyrics)
#     print(f"Number of lyrics lines: {num_lyrics}")
#
#     # Create evenly spaced timestamps across the duration
#     time_per_line = duration / (num_lyrics - 1)
#
#     # Match lyrics with timestamps
#     timestamped_lyrics = []
#     for i, lyric in enumerate(lyrics):
#         if lyric.strip():  # Skip empty lines
#             time = i * time_per_line
#             minutes = int(time // 60)
#             seconds = time % 60
#             timestamp = f"[{minutes:02d}:{seconds:05.2f}]"
#             timestamped_lyrics.append(f"{timestamp}{lyric}")
#
#     return timestamped_lyrics
#
#
# # Example usage
# if __name__ == "__main__":
#     audio_path = "dirfile/music_file.mp3"
#     lyrics_path = "dirfile/plain_lyrics.text"
#
#     try:
#         timestamped_lyrics = get_lyrics_timing(audio_path, lyrics_path)
#
#         print("\nFinal Results:")
#         print(f"Total timestamped lyrics: {len(timestamped_lyrics)}")
#         for line in timestamped_lyrics:
#             print(line)
#
#     except Exception as e:
#         print(f"Error processing files: {str(e)}")
#         import traceback
#
#         print(traceback.format_exc())


import librosa
import numpy as np


def get_lyrics_timing(audio_file, lyrics_file):
    # Load the audio file
    print("Loading audio file...")
    y, sr = librosa.load(audio_file)
    duration = librosa.get_duration(y=y, sr=sr)
    print(f"Audio loaded. Duration: {duration:.2f} seconds")

    # Get tempo and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print(f"Detected tempo: {float(tempo):.2f} BPM")

    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    print(f"Detected {len(beat_times)} beats")

    # Read lyrics
    with open(lyrics_file, 'r', encoding='utf-8') as f:
        lyrics = [line.strip() for line in f.readlines() if line.strip()]

    # Calculate number of lyrics and beats per lyric line
    num_lyrics = len(lyrics)
    print(f"Number of lyrics lines: {num_lyrics}")

    # Calculate approximately how many beats should be between each lyric line
    beats_per_lyric = len(beat_times) / num_lyrics
    print(f"Approximately {beats_per_lyric:.2f} beats per lyric line")

    # Match lyrics with beat-aligned timestamps
    timestamped_lyrics = []
    for i, lyric in enumerate(lyrics):
        if lyric.strip():  # Skip empty lines
            # Find the nearest beat to where we expect this lyric to be
            expected_beat_index = int(i * beats_per_lyric)

            # Make sure we don't exceed the available beats
            if expected_beat_index >= len(beat_times):
                expected_beat_index = len(beat_times) - 1

            # Get the time from the beat detection
            time = beat_times[expected_beat_index]

            # Format the timestamp
            minutes = int(time // 60)
            seconds = time % 60
            timestamp = f"[{minutes:02d}:{seconds:05.2f}]"
            timestamped_lyrics.append(f"{timestamp}{lyric}")

    return timestamped_lyrics


# Example usage
if __name__ == "__main__":
    audio_path = "dirfile/music_file.mp3"
    lyrics_path = "dirfile/plain_lyrics.text"

    try:
        timestamped_lyrics = get_lyrics_timing(audio_path, lyrics_path)

        print("\nFinal Results:")
        print(f"Total timestamped lyrics: {len(timestamped_lyrics)}")
        for line in timestamped_lyrics:
            print(line)

    except Exception as e:
        print(f"Error processing files: {str(e)}")
        import traceback

        print(traceback.format_exc())