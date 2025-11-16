# AI-Powered Voice Assistant

A desktop voice assistant built with Python that can understand and respond to voice commands using speech recognition and OpenAI's API.

## Features

- Voice recognition using Google's speech recognition
- Text-to-speech response
- Integration with OpenAI for intelligent responses
- Wikipedia search
- Web browsing (YouTube, Google)
- Play music on YouTube
- Tell time and date
- Customizable wake word and settings

## Prerequisites

- Python 3.7 or higher
- Microphone
- Internet connection
- OpenAI API key (free tier available at [OpenAI](https://platform.openai.com/))

## Installation

1. Clone the repository or download the files
2. Navigate to the project directory:
   ```
   cd ai_voice_assistant
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Get an API key from [OpenAI](https://platform.openai.com/)
5. Create a `.env` file in the project directory and add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the assistant:
   ```
   python assistant.py
   ```
2. The assistant will greet you and start listening for commands
3. Speak your command after hearing the "Listening..." prompt

## Example Commands

- "What's the time?"
- "Search Wikipedia for artificial intelligence"
- "Open YouTube"
- "Play Despacito"
- "Tell me a joke"
- "Goodbye" (to exit)

## Customization

You can customize the assistant by modifying the `VoiceAssistant` class in `assistant.py`:
- Change the assistant's name
- Adjust speech rate
- Add new commands and responses
- Modify the voice (male/female)

## Troubleshooting

- If you get a `pyaudio` error, try installing it separately:
  ```
  pip install pyaudio
  ```
  On Windows, you might need to download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

- Make sure your microphone is properly connected and working.
- Ensure you have a stable internet connection for speech recognition and API calls.

## License

This project is open source and available under the [MIT License](LICENSE).
