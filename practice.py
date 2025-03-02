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


from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from pydub import AudioSegment
import argparse
import os


def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 file to WAV format using pydub"""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")


def align_lyrics(mp3_path, text_path, output_path, language="en"):
    # Convert MP3 to temporary WAV file
    temp_wav = "temp_audio.wav"
    convert_mp3_to_wav(mp3_path, temp_wav)

    # Create Aeneas task
    config_string = (
        f"task_language={language}|"
        "is_text_type=plain|"
        "os_task_file_format=tsv|"
        "algorithm=dtw|"
        "dtw_margin=100"
    )

    task = Task(config_string=config_string)
    task.audio_file_path_absolute = os.path.abspath(temp_wav)
    task.text_file_path_absolute = os.path.abspath(text_path)
    task.sync_map_file_path_absolute = os.path.abspath(output_path)

    # Execute task
    ExecuteTask(task).execute()

    # Cleanup temporary WAV file
    os.remove(temp_wav)

    print(f"Alignment complete. Results saved to {output_path}")


def print_timestamps(output_path):
    """Print the aligned timestamps from the output file"""
    with open(output_path, 'r') as f:
        print("\nTimestamps:")
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                start = float(parts[0])
                end = float(parts[1])
                lyric = parts[2]
                print(f"{format_time(start)} --> {format_time(end)}: {lyric}")


def format_time(seconds):
    """Convert seconds to hh:mm:ss.sss format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"


def main():
    parser = argparse.ArgumentParser(description='Align lyrics with audio timestamps')
    parser.add_argument('audio', help='Input MP3 file path')
    parser.add_argument('text', help='Plain text file with lyrics')
    parser.add_argument('output', help='Output TSV file path')
    parser.add_argument('--language', default='en', help='Language code (e.g., en, es, fr)')

    args = parser.parse_args()

    # Align lyrics
    align_lyrics(args.audio, args.text, args.output, args.language)

    # Print results
    print_timestamps(args.output)


if __name__ == "__main__":
    main()