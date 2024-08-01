import subprocess


def play_mp3(file_path):
    """
    Play an MP3 file in Raspberry zero 2w

    :parameter(s):
        file_path: Path to the MP3 file
    
    :return: None
    """
    try:
        subprocess.run(['mpg123', file_path])
    except FileNotFoundError:
        print("mpg123 command not found. Make sure you're on macOS and afplay is installed.")


def text_to_speech(text, file_path, client):
    """
    Play an MP3 file in Meta Quest 3

    :parameters:
        text: String, text 
        file_path: String, path to the MP3 file
    
    :return: none
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(file_path)