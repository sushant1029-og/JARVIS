# JARVIS AI Assistant

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)](CONTRIBUTING.md)

JARVIS is an intelligent AI assistant designed to help with various tasks through natural language processing, voice recognition, and automation capabilities. Inspired by the fictional AI from Marvel's Iron Man, JARVIS provides a seamless and intuitive interface for users to interact with their system.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
  - [Configuration](#configuration)
- [Usage Guide](#usage-guide)
  - [Basic Commands](#basic-commands)
  - [Voice Commands](#voice-commands)
  - [Advanced Features](#advanced-features)
- [API Reference](#api-reference)
- [How to Extend JARVIS](#how-to-extend-jarvis)
  - [Creating Custom Skills](#creating-custom-skills)
  - [Adding New Intents](#adding-new-intents)
  - [Integrating External APIs](#integrating-external-apis)
  - [Building Plugins](#building-plugins)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Capabilities

- **Natural Language Processing**: Understand and process user queries in natural language
- **Voice Recognition**: Recognize and process voice commands (text-to-speech and speech-to-text)
- **Task Automation**: Automate routine tasks and workflows
- **Context Awareness**: Maintain conversation context across multiple interactions
- **Multi-language Support**: Support for multiple languages and dialects
- **Learning Capability**: Learn from user interactions and improve responses over time

### Advanced Features

- **Skill System**: Extensible skill-based architecture for adding new capabilities
- **Intent Recognition**: Advanced intent detection with confidence scoring
- **Entity Extraction**: Extract and process named entities from user input
- **Memory Management**: Persistent memory for user preferences and history
- **Cross-Platform Support**: Run on Windows, macOS, and Linux systems
- **API Integration**: Connect with external services and APIs
- **Scheduled Tasks**: Execute tasks at specific times or intervals
- **Error Handling**: Comprehensive error handling and logging

## Project Structure

```
JARVIS/
├── jarvis/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── jarvis.py              # Main JARVIS class
│   │   ├── nlu_engine.py           # Natural Language Understanding
│   │   ├── intent_matcher.py       # Intent matching logic
│   │   └── entity_extractor.py     # Named entity extraction
│   ├── skills/
│   │   ├── __init__.py
│   │   ├── base_skill.py           # Base skill class
│   │   ├── builtin/
│   │   │   ├── greeting.py
│   │   │   ├── time.py
│   │   │   ├── weather.py
│   │   │   └── web_search.py
│   │   └── custom/
│   │       └── example_skill.py
│   ├── voice/
│   │   ├── __init__.py
│   │   ├── speech_recognition.py   # Speech-to-text
│   │   └── text_to_speech.py       # Text-to-speech
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration management
│   │   ├── logger.py               # Logging utilities
│   │   ├── memory.py               # Memory management
│   │   └── helpers.py              # Helper functions
│   └── api/
│       ├── __init__.py
│       └── rest_api.py             # REST API endpoints
├── tests/
│   ├── __init__.py
│   ├── test_nlu.py
│   ├── test_skills.py
│   └── test_voice.py
├── examples/
│   ├── basic_usage.py
│   ├── voice_interaction.py
│   ├── custom_skill_example.py
│   └── api_server.py
├── config/
│   ├── default_config.yaml
│   └── skills_config.yaml
├── docs/
│   ├── API.md
│   ├── SKILLS.md
│   ├── DEVELOPMENT.md
│   └── TROUBLESHOOTING.md
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Microphone (for voice features)
- Speaker or headphones (for audio output)

### Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/sushant1029-og/JARVIS.git
cd JARVIS
```

#### 2. Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install JARVIS

```bash
pip install -e .
```

Or, if using setup.py directly:

```bash
python setup.py install
```

### Configuration

#### Basic Configuration

Create a `.jarvis_config.yaml` file in your home directory:

```yaml
# JARVIS Configuration File

# Assistant name
assistant_name: "JARVIS"

# Language settings
language: "en-US"
supported_languages:
  - "en-US"
  - "es-ES"
  - "fr-FR"

# Voice settings
voice:
  enabled: true
  engine: "default"  # Options: default, google, azure
  rate: 150
  volume: 0.9

# NLU settings
nlu:
  model: "default"
  confidence_threshold: 0.6
  max_entities: 10

# Memory settings
memory:
  enabled: true
  storage: "local"  # Options: local, redis, mongodb
  retention_days: 30

# API settings
api:
  host: "127.0.0.1"
  port: 5000
  debug: false
```

#### Skills Configuration

Edit `config/skills_config.yaml` to enable/disable skills:

```yaml
skills:
  greeting:
    enabled: true
    priority: 10
  
  time:
    enabled: true
    priority: 5
  
  weather:
    enabled: true
    api_key: "YOUR_WEATHER_API_KEY"
    priority: 8
  
  web_search:
    enabled: true
    search_engine: "google"
    priority: 7
```

## Usage Guide

### Basic Commands

#### 1. Starting JARVIS

```python
from jarvis import JARVIS

# Initialize JARVIS
jarvis = JARVIS()

# Start the assistant
jarvis.start()
```

#### 2. Processing Text Input

```python
# Process a text query
response = jarvis.process("What's the current time?")
print(response)

# Get detailed response with metadata
result = jarvis.process_detailed("What's the weather like?")
print(f"Response: {result['response']}")
print(f"Confidence: {result['confidence']}")
print(f"Intent: {result['intent']}")
```

#### 3. Interactive Mode

```python
# Start interactive conversation
jarvis.interactive_mode()
```

### Voice Commands

#### 1. Basic Voice Interaction

```python
from jarvis.voice import VoiceInterface

voice = VoiceInterface()

# Listen for command and process
response = voice.listen_and_process()
print(f"You said: {response['text']}")
print(f"JARVIS: {response['reply']}")

# Speak the response
voice.speak(response['reply'])
```

#### 2. Continuous Voice Mode

```python
# Listen continuously with wake word detection
voice.start_continuous_listening(wake_word="jarvis")
```

### Advanced Features

#### 1. Working with Memory

```python
# Store information in memory
jarvis.memory.store("user_name", "John")
jarvis.memory.store("favorite_color", "blue")

# Retrieve from memory
name = jarvis.memory.retrieve("user_name")

# Clear memory
jarvis.memory.clear()
```

#### 2. Context Management

```python
# Get current context
context = jarvis.get_context()

# Update context
jarvis.set_context({"user_mood": "happy", "task": "work"})

# Clear context
jarvis.clear_context()
```

#### 3. Scheduling Tasks

```python
# Schedule a task for a specific time
jarvis.schedule_task(
    name="morning_briefing",
    time="08:00",
    skill="briefing",
    action="daily_summary"
)

# Schedule recurring tasks
jarvis.schedule_recurring_task(
    name="hourly_check",
    interval="hourly",
    skill="system_monitor",
    action="check_system"
)
```

## API Reference

### JARVIS Class

```python
class JARVIS:
    def __init__(self, config_path=None):
        """Initialize JARVIS with optional configuration file"""
        
    def process(self, query: str) -> str:
        """Process a text query and return response"""
        
    def process_detailed(self, query: str) -> dict:
        """Process query and return detailed result with metadata"""
        
    def start(self) -> None:
        """Start the JARVIS assistant"""
        
    def stop(self) -> None:
        """Stop the JARVIS assistant"""
        
    def register_skill(self, skill: BaseSkill) -> None:
        """Register a new skill"""
        
    def remove_skill(self, skill_name: str) -> None:
        """Remove a registered skill"""
        
    def get_context(self) -> dict:
        """Get current conversation context"""
        
    def set_context(self, context: dict) -> None:
        """Update conversation context"""
```

### BaseSkill Class

```python
class BaseSkill:
    def __init__(self, name: str, description: str):
        """Initialize a skill"""
        
    def execute(self, intent: str, entities: dict, context: dict) -> str:
        """Execute the skill with given parameters"""
        
    def get_intents(self) -> List[str]:
        """Return list of intents this skill handles"""
```

## How to Extend JARVIS

### Creating Custom Skills

#### Step 1: Create a Skill Class

```python
from jarvis.skills.base_skill import BaseSkill

class CalculatorSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Perform mathematical calculations"
        )
    
    def execute(self, intent: str, entities: dict, context: dict) -> str:
        """
        Execute calculator operations
        
        Args:
            intent: The detected intent (e.g., "calculate")
            entities: Extracted entities (numbers, operators)
            context: Conversation context
            
        Returns:
            Result string with calculation
        """
        operation = entities.get("operation")
        numbers = entities.get("numbers", [])
        
        if operation == "add":
            result = sum(numbers)
        elif operation == "multiply":
            result = 1
            for num in numbers:
                result *= num
        # ... handle other operations
        
        return f"The result is {result}"
    
    def get_intents(self) -> list:
        """Return intents handled by this skill"""
        return ["calculate", "math", "arithmetic"]
```

#### Step 2: Register the Skill

```python
# In your main application
from jarvis import JARVIS
from skills.calculator import CalculatorSkill

jarvis = JARVIS()
calculator_skill = CalculatorSkill()
jarvis.register_skill(calculator_skill)
```

### Adding New Intents

#### 1. Define Intent Patterns

```python
# In config/intents.yaml
intents:
  greeting:
    patterns:
      - "hello"
      - "hi"
      - "hey jarvis"
    entities:
      - "greeting_type"
  
  calculate:
    patterns:
      - "calculate .* and .*"
      - "what is .* plus .*"
    entities:
      - "operation"
      - "numbers"
```

#### 2. Train the NLU Model

```python
from jarvis.core.nlu_engine import NLUEngine

nlu = NLUEngine()
nlu.train_from_file("config/intents.yaml")
nlu.save_model("models/custom_model")
```

### Integrating External APIs

#### Example: Weather API Integration

```python
from jarvis.skills.base_skill import BaseSkill
import requests

class WeatherSkill(BaseSkill):
    def __init__(self, api_key: str):
        super().__init__(
            name="weather",
            description="Get weather information"
        )
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def execute(self, intent: str, entities: dict, context: dict) -> str:
        location = entities.get("location", "current")
        
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The weather in {location} is {description} with a temperature of {temp}°C"
        else:
            return "Unable to fetch weather information"
    
    def get_intents(self) -> list:
        return ["weather", "temperature"]
```

### Building Plugins

#### Create a Plugin Structure

```
my_plugin/
├── __init__.py
├── plugin.py
├── skills/
│   ├── __init__.py
│   └── custom_skill.py
├── config.yaml
└── requirements.txt
```

#### Plugin Implementation

```python
# plugin.py
class JARVISPlugin:
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
        self.name = "MyPlugin"
        self.version = "1.0.0"
    
    def initialize(self):
        """Initialize the plugin"""
        from .skills.custom_skill import CustomSkill
        skill = CustomSkill()
        self.jarvis.register_skill(skill)
    
    def shutdown(self):
        """Clean up when plugin is unloaded"""
        pass
    
    def get_info(self) -> dict:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "My custom JARVIS plugin"
        }
```

#### Register the Plugin

```python
from jarvis import JARVIS
from my_plugin.plugin import JARVISPlugin

jarvis = JARVIS()
plugin = JARVISPlugin(jarvis)
plugin.initialize()
```

## Examples

### Example 1: Basic Text Interaction

```python
from jarvis import JARVIS

# Create instance
jarvis = JARVIS()

# Process queries
print(jarvis.process("Hello JARVIS"))
print(jarvis.process("What time is it?"))
print(jarvis.process("Tell me a joke"))
```

### Example 2: Voice-Based Interaction

```python
from jarvis import JARVIS
from jarvis.voice import VoiceInterface

jarvis = JARVIS()
voice = VoiceInterface(jarvis)

# Start voice interaction
voice.start_continuous_listening(wake_word="jarvis")
```

### Example 3: Creating a Custom Skill

```python
from jarvis.skills.base_skill import BaseSkill

class ToDoSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="todo",
            description="Manage to-do lists"
        )
        self.todos = []
    
    def execute(self, intent: str, entities: dict, context: dict) -> str:
        action = entities.get("action")
        task = entities.get("task")
        
        if action == "add":
            self.todos.append(task)
            return f"Added {task} to your to-do list"
        elif action == "list":
            return "Your to-do list: " + ", ".join(self.todos)
        elif action == "remove":
            if task in self.todos:
                self.todos.remove(task)
                return f"Removed {task} from your to-do list"
        
        return "Task not recognized"
    
    def get_intents(self) -> list:
        return ["add_task", "list_tasks", "remove_task"]
```

### Example 4: REST API Server

```python
from flask import Flask, request, jsonify
from jarvis import JARVIS

app = Flask(__name__)
jarvis = JARVIS()

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get('query')
    
    result = jarvis.process_detailed(query_text)
    
    return jsonify(result)

@app.route('/api/skills', methods=['GET'])
def get_skills():
    return jsonify({
        'skills': jarvis.get_registered_skills()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Voice Recognition Not Working

**Problem**: Microphone input is not being detected.

**Solutions**:
```python
# Check if microphone is properly configured
from jarvis.voice import VoiceInterface

voice = VoiceInterface()
devices = voice.list_audio_devices()
print(devices)

# Set specific device
voice.set_audio_device(device_id=0)
```

#### 2. Intent Not Recognized

**Problem**: JARVIS doesn't understand your commands.

**Solutions**:
```python
# Check NLU confidence threshold
from jarvis.core.nlu_engine import NLUEngine

nlu = NLUEngine()
result = nlu.recognize("your query here")
print(f"Intent: {result['intent']}, Confidence: {result['confidence']}")

# Lower threshold if needed
jarvis.config.nlu.confidence_threshold = 0.5
```

#### 3. Memory Issues

**Problem**: Memory usage is too high.

**Solutions**:
```python
# Clear old memory
jarvis.memory.clear_old_entries(days=7)

# Optimize memory usage
jarvis.memory.compress()

# Switch to external storage
jarvis.memory.switch_storage("redis")
```

#### 4. API Connection Errors

**Problem**: External APIs are not responding.

**Solutions**:
```python
# Check API configuration
print(jarvis.config.get_api_settings())

# Test connectivity
from jarvis.utils.helpers import test_api_connection
test_api_connection("https://api.example.com")

# Enable offline mode
jarvis.config.offline_mode = True
```

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

jarvis = JARVIS(debug=True)
```

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/sushant1029-og/JARVIS.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clear, commented code
   - Follow PEP 8 style guidelines
   - Add unit tests for new features

4. **Test Your Changes**
   ```bash
   pytest tests/
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "Add detailed commit message"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe your changes
   - Reference any related issues
   - Include screenshots/examples if applicable

### Development Guidelines

- **Code Style**: Follow PEP 8
- **Documentation**: Add docstrings to all functions
- **Testing**: Maintain >80% code coverage
- **Commits**: Use clear, descriptive commit messages
- **Branches**: Use feature branches for new features

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:

- **GitHub Issues**: [Report issues](https://github.com/sushant1029-og/JARVIS/issues)
- **Discussions**: [Join discussions](https://github.com/sushant1029-og/JARVIS/discussions)
- **Email**: Contact the maintainers

## Acknowledgments

- The JARVIS project is inspired by the AI assistant from Marvel's Iron Man universe
- Thanks to all contributors and the open-source community
- Special thanks to libraries like `nltk`, `spacy`, and `pyaudio`

---

**Last Updated**: January 2, 2026

For more detailed information, please check out the [Documentation](docs/) folder.
