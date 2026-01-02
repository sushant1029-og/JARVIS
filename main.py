"""
JARVIS AI Assistant Engine
Main entry point for the JARVIS voice-activated AI assistant
Includes voice recognition, text-to-speech, command processing, and conversational abilities

Author: JARVIS Development Team
Date: 2026-01-02
"""

import os
import sys
import json
import threading
import time
from datetime import datetime
from typing import Optional, Dict, List, Callable, Any
from abc import ABC, abstractmethod

try:
    import speech_recognition as sr
    from pyttsx3 import init as tts_init
    import pyttsx3
except ImportError:
    print("Warning: Some dependencies are not installed. Install them using:")
    print("pip install SpeechRecognition pyttsx3")


class VoiceRecognitionEngine:
    """Handles speech-to-text conversion using speech_recognition library"""
    
    def __init__(self, language: str = 'en-US'):
        """
        Initialize voice recognition engine
        
        Args:
            language: Language code for speech recognition (default: 'en-US')
        """
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.language = language
        self.is_listening = False
        
    def listen(self, timeout: int = 10, phrase_time_limit: int = None) -> Optional[str]:
        """
        Listen for audio input and convert to text
        
        Args:
            timeout: Maximum time to wait for input (seconds)
            phrase_time_limit: Maximum time to listen for a phrase (seconds)
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            self.is_listening = True
            print("🎤 Listening...")
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            self.is_listening = False
            print("🔄 Processing audio...")
            
            # Try Google Speech Recognition API
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"✓ Recognized: {text}")
            return text
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error in voice recognition: {e}")
            return None


class TextToSpeechEngine:
    """Handles text-to-speech conversion"""
    
    def __init__(self, rate: int = 150, volume: float = 1.0):
        """
        Initialize text-to-speech engine
        
        Args:
            rate: Speech rate (words per minute)
            volume: Speech volume (0.0 to 1.0)
        """
        try:
            self.engine = tts_init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
        except Exception as e:
            print(f"Warning: Could not initialize TTS engine: {e}")
            self.engine = None
    
    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Convert text to speech and play audio
        
        Args:
            text: Text to speak
            async_mode: If True, run speech in background thread
        """
        if not self.engine:
            print(f"[JARVIS] {text}")
            return
            
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str) -> None:
        """Synchronous text-to-speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")


class CommandProcessor:
    """Process and execute voice commands"""
    
    def __init__(self):
        """Initialize command processor"""
        self.commands: Dict[str, Callable] = {}
        self.aliases: Dict[str, str] = {}
        self._register_default_commands()
    
    def register_command(self, 
                        command: str, 
                        handler: Callable,
                        aliases: List[str] = None) -> None:
        """
        Register a new command
        
        Args:
            command: Command name
            handler: Function to execute
            aliases: List of command aliases
        """
        self.commands[command.lower()] = handler
        if aliases:
            for alias in aliases:
                self.aliases[alias.lower()] = command.lower()
    
    def _register_default_commands(self) -> None:
        """Register default built-in commands"""
        self.register_command('time', self._handle_time, ['what time', 'current time'])
        self.register_command('date', self._handle_date, ['what date', 'current date'])
        self.register_command('help', self._handle_help, ['commands', 'what can you do'])
        self.register_command('exit', self._handle_exit, ['quit', 'stop', 'goodbye'])
    
    def process_command(self, user_input: str) -> Optional[str]:
        """
        Process user command and return response
        
        Args:
            user_input: User's voice command
            
        Returns:
            Response string or None
        """
        user_input = user_input.lower().strip()
        
        # Check for direct command match
        if user_input in self.commands:
            return self.commands[user_input]()
        
        # Check for alias match
        for alias, command in self.aliases.items():
            if alias in user_input:
                return self.commands[command]()
        
        # Check for partial command match
        for command, handler in self.commands.items():
            if command in user_input:
                return handler()
        
        return None
    
    @staticmethod
    def _handle_time() -> str:
        """Handle time command"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    @staticmethod
    def _handle_date() -> str:
        """Handle date command"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    @staticmethod
    def _handle_help() -> str:
        """Handle help command"""
        return "Available commands: time, date, help, exit. You can also ask me questions!"
    
    @staticmethod
    def _handle_exit() -> str:
        """Handle exit command"""
        return "Goodbye! Shutting down..."


class ConversationEngine:
    """Handle conversational AI capabilities"""
    
    def __init__(self, system_prompt: str = None):
        """
        Initialize conversation engine
        
        Args:
            system_prompt: System prompt for context
        """
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.max_history = 10
    
    @staticmethod
    def _get_default_system_prompt() -> str:
        """Get default system prompt"""
        return """You are JARVIS, an intelligent voice-activated AI assistant created by the JARVIS Development Team.
        You are helpful, friendly, and knowledgeable. You speak naturally and conversationally.
        Keep responses concise and relevant to the user's question."""
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        Add message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.conversation_history.append({
            'role': role,
            'content': content
        })
        
        # Keep history size manageable
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate conversational response to user input
        
        Args:
            user_input: User's text input
            
        Returns:
            AI response
        """
        self.add_to_history('user', user_input)
        
        # This is a placeholder for AI response generation
        # In production, integrate with OpenAI GPT, Hugging Face, or similar
        response = self._generate_simple_response(user_input)
        
        self.add_to_history('assistant', response)
        return response
    
    @staticmethod
    def _generate_simple_response(user_input: str) -> str:
        """
        Generate simple response using basic NLP patterns
        Can be replaced with actual AI API calls
        
        Args:
            user_input: User input text
            
        Returns:
            Generated response
        """
        user_input_lower = user_input.lower()
        
        # Basic response patterns
        responses = {
            'hello': "Hello! How can I assist you today?",
            'hi': "Hi there! What can I do for you?",
            'how are you': "I'm functioning perfectly, thank you for asking!",
            'what is your name': "I'm JARVIS, your AI assistant.",
            'who created you': "I was created by the JARVIS Development Team.",
            'thank you': "You're welcome! Happy to help.",
            'thanks': "Always happy to help!",
        }
        
        # Check for pattern matches
        for pattern, response in responses.items():
            if pattern in user_input_lower:
                return response
        
        # Default response for unknown inputs
        return f"That's interesting. I'm still learning about {user_input.split()[0] if user_input.split() else 'that'}."
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []


class JARVISAssistant:
    """Main JARVIS AI Assistant class"""
    
    def __init__(self, 
                 enable_voice: bool = True,
                 enable_text: bool = True,
                 voice_lang: str = 'en-US'):
        """
        Initialize JARVIS Assistant
        
        Args:
            enable_voice: Enable voice input/output
            enable_text: Enable text input/output
            voice_lang: Language for voice recognition
        """
        print("🚀 Initializing JARVIS AI Assistant...")
        print(f"⏰ Startup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        self.enable_voice = enable_voice
        self.enable_text = enable_text
        self.is_running = False
        self.exit_flag = False
        
        # Initialize engines
        if enable_voice:
            try:
                self.voice_recognition = VoiceRecognitionEngine(language=voice_lang)
                self.text_to_speech = TextToSpeechEngine()
            except Exception as e:
                print(f"⚠️  Voice modules unavailable: {e}")
                self.enable_voice = False
        
        self.command_processor = CommandProcessor()
        self.conversation_engine = ConversationEngine()
        
        print("✅ JARVIS initialized successfully")
        print("-" * 50)
    
    def process_input(self, user_input: str) -> str:
        """
        Process user input and generate response
        
        Args:
            user_input: User's input text
            
        Returns:
            Response text
        """
        print(f"\n👤 User: {user_input}")
        
        # Try command processing first
        command_response = self.command_processor.process_command(user_input)
        if command_response:
            print(f"🤖 JARVIS: {command_response}")
            if self.enable_voice:
                self.text_to_speech.speak(command_response, async_mode=True)
            return command_response
        
        # Fall back to conversational AI
        ai_response = self.conversation_engine.generate_response(user_input)
        print(f"🤖 JARVIS: {ai_response}")
        if self.enable_voice:
            self.text_to_speech.speak(ai_response, async_mode=True)
        return ai_response
    
    def voice_interaction_loop(self) -> None:
        """Run voice interaction loop"""
        print("\n🎤 JARVIS Voice Mode Active")
        print("📣 Say 'exit' or 'quit' to stop\n")
        
        self.is_running = True
        while self.is_running and not self.exit_flag:
            try:
                # Listen for voice input
                user_input = self.voice_recognition.listen(timeout=5)
                
                if user_input is None:
                    continue
                
                # Process the input
                response = self.process_input(user_input)
                
                # Check for exit command
                if user_input.lower() in ['exit', 'quit', 'stop', 'goodbye']:
                    self.is_running = False
                    self.exit_flag = True
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\n⏹️  Interrupted by user")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Error in voice loop: {e}")
    
    def text_interaction_loop(self) -> None:
        """Run text interaction loop"""
        print("\n⌨️  JARVIS Text Mode Active")
        print("Type your commands or questions (type 'exit' to quit)\n")
        
        self.is_running = True
        while self.is_running and not self.exit_flag:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Process the input
                response = self.process_input(user_input)
                
                # Check for exit command
                if user_input.lower() in ['exit', 'quit', 'stop', 'goodbye']:
                    self.is_running = False
                    self.exit_flag = True
                    if self.enable_voice:
                        self.text_to_speech.speak("Goodbye!", async_mode=False)
                    print("Shutting down...")
                
            except KeyboardInterrupt:
                print("\n⏹️  Interrupted by user")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Error in text loop: {e}")
    
    def run(self, mode: str = 'text') -> None:
        """
        Start JARVIS assistant
        
        Args:
            mode: 'voice' or 'text' interaction mode
        """
        try:
            if mode.lower() == 'voice' and self.enable_voice:
                self.voice_interaction_loop()
            else:
                self.text_interaction_loop()
        except Exception as e:
            print(f"❌ Fatal error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self) -> None:
        """Shutdown JARVIS gracefully"""
        print("\n" + "=" * 50)
        print("🛑 JARVIS Shutdown")
        print(f"⏰ Shutdown Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("📊 Session Statistics:")
        print(f"   - Conversation turns: {len(self.conversation_engine.get_history())}")
        print("=" * 50)
        self.is_running = False
    
    def save_conversation(self, filename: str = 'conversation_log.json') -> None:
        """
        Save conversation history to file
        
        Args:
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'conversation': self.conversation_engine.get_history()
                }, f, indent=2)
            print(f"✅ Conversation saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")


def main():
    """Main entry point for JARVIS"""
    print("""
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║              🤖 JARVIS AI ASSISTANT 🤖            ║
    ║                                                   ║
    ║           Voice-Activated Intelligent AI          ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    """)
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='JARVIS - Voice-Activated AI Assistant'
    )
    parser.add_argument(
        '--mode',
        choices=['voice', 'text'],
        default='text',
        help='Interaction mode (default: text)'
    )
    parser.add_argument(
        '--language',
        default='en-US',
        help='Voice recognition language (default: en-US)'
    )
    parser.add_argument(
        '--no-voice',
        action='store_true',
        help='Disable voice output'
    )
    
    args = parser.parse_args()
    
    # Initialize JARVIS
    jarvis = JARVISAssistant(
        enable_voice=not args.no_voice,
        enable_text=True,
        voice_lang=args.language
    )
    
    # Run JARVIS
    jarvis.run(mode=args.mode)


if __name__ == '__main__':
    main()
