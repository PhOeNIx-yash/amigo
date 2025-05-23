# Amigo Voice Assistant

Amigo is a voice-activated personal assistant with AI capabilities, built in Python.

## Features

- **Voice Recognition**: Wake up Amigo with "Hey Amigo" and speak your commands
- **Web Browsing**: Open websites like GitHub, StackOverflow, ChatGPT, and more
- **Media Control**: Play music, control volume, and navigate media playback
- **App Launcher**: Open any installed application by voice command
- **System Operations**: Take screenshots, check time, and access file system
- **Weather Information**: Get current weather information for any location
- **Calculations**: Perform mathematical calculations via voice
- **AI Conversation**: Chat with an advanced NVIDIA AI model (llama-3.1-nemotron-70b-instruct)
- **Memory System**: Amigo remembers your conversations for context-aware responses

## AI Commands

- **"Chat" or "Talk to me" or "Let's talk"**: Start a casual conversation with the AI
- **"Ask AI [your question]"**: Directly ask the AI a specific question
- **"Conversation history" or "Chat history"**: Review your recent conversation history
- **"Clear memory" or "Clear history"**: Delete all saved conversation history
- **Any unrecognized command**: Will be sent to the AI for a response

## Requirements

- Python 3.6+
- OpenAI Python package (for NVIDIA API integration)
- pyttsx3 (for text-to-speech)
- SpeechRecognition (for voice recognition)
- PyAutoGUI (for system control)
- Additional dependencies in specific modules

## Getting Started

1. Ensure all required packages are installed
2. Run `python "amigo main.py"`
3. Say "Hey Amigo" to activate the assistant
4. Start issuing voice commands

## Memory System

Amigo maintains conversation history to provide context-aware responses. The memory system:

- Stores up to 50 conversation exchanges
- Uses the 10 most recent exchanges for context in new responses
- Saves data to `amigo_memory.json` in the same directory
- Can be cleared at any time with voice commands #   a m i g o 
 
 
