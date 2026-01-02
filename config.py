"""
JARVIS Assistant Configuration Module
Configuration settings for API keys, user preferences, and command mappings
Last Updated: 2026-01-02 16:27:33 UTC
"""

import os
from pathlib import Path

# ============================================================================
# API KEYS AND CREDENTIALS
# ============================================================================
# Note: For security, use environment variables instead of hardcoding keys

API_KEYS = {
    'openai': os.getenv('OPENAI_API_KEY', ''),
    'google': os.getenv('GOOGLE_API_KEY', ''),
    'weather': os.getenv('WEATHER_API_KEY', ''),
    'news': os.getenv('NEWS_API_KEY', ''),
    'spotify': os.getenv('SPOTIFY_API_KEY', ''),
}

# Authentication tokens
AUTH_TOKENS = {
    'github': os.getenv('GITHUB_TOKEN', ''),
    'slack': os.getenv('SLACK_TOKEN', ''),
    'discord': os.getenv('DISCORD_TOKEN', ''),
}

# ============================================================================
# USER PREFERENCES
# ============================================================================

USER_PREFERENCES = {
    'name': 'User',
    'language': 'en',
    'timezone': 'UTC',
    'theme': 'dark',  # 'light' or 'dark'
    'voice_enabled': True,
    'voice_speed': 1.0,  # 0.5 to 2.0
    'notifications_enabled': True,
    'notification_sound': True,
    'email_notifications': False,
    'logging_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
}

# ============================================================================
# COMMAND MAPPINGS
# ============================================================================

COMMAND_MAPPINGS = {
    # General Commands
    'help': {
        'aliases': ['assist', 'support', 'info'],
        'description': 'Display help information',
        'enabled': True,
    },
    'hello': {
        'aliases': ['hi', 'greet', 'hey'],
        'description': 'Greet the user',
        'enabled': True,
    },
    'status': {
        'aliases': ['check', 'system_status'],
        'description': 'Check system status',
        'enabled': True,
    },
    
    # Information Commands
    'weather': {
        'aliases': ['forecast', 'climate'],
        'description': 'Get weather information',
        'enabled': True,
        'requires_api': True,
    },
    'news': {
        'aliases': ['headlines', 'updates'],
        'description': 'Get latest news',
        'enabled': True,
        'requires_api': True,
    },
    'time': {
        'aliases': ['date', 'clock'],
        'description': 'Get current time and date',
        'enabled': True,
    },
    
    # Productivity Commands
    'remind': {
        'aliases': ['reminder', 'alert'],
        'description': 'Set a reminder',
        'enabled': True,
    },
    'timer': {
        'aliases': ['countdown', 'stopwatch'],
        'description': 'Set a timer',
        'enabled': True,
    },
    'todo': {
        'aliases': ['task', 'tasks', 'list'],
        'description': 'Manage to-do list',
        'enabled': True,
    },
    'calendar': {
        'aliases': ['schedule', 'event'],
        'description': 'Manage calendar events',
        'enabled': True,
    },
    
    # System Commands
    'search': {
        'aliases': ['find', 'query'],
        'description': 'Search the web',
        'enabled': True,
        'requires_api': True,
    },
    'email': {
        'aliases': ['mail', 'message'],
        'description': 'Send and manage emails',
        'enabled': True,
    },
    'call': {
        'aliases': ['ring', 'dial', 'phone'],
        'description': 'Make phone calls',
        'enabled': False,
    },
    
    # Media Commands
    'music': {
        'aliases': ['play', 'song', 'audio'],
        'description': 'Control music playback',
        'enabled': True,
        'requires_api': True,
    },
    'video': {
        'aliases': ['watch', 'film', 'movie'],
        'description': 'Watch videos',
        'enabled': True,
    },
    
    # Control Commands
    'volume': {
        'aliases': ['sound', 'mute'],
        'description': 'Control volume',
        'enabled': True,
    },
    'brightness': {
        'aliases': ['screen', 'light'],
        'description': 'Control screen brightness',
        'enabled': True,
    },
    'settings': {
        'aliases': ['config', 'preferences'],
        'description': 'Access settings',
        'enabled': True,
    },
    'exit': {
        'aliases': ['quit', 'close', 'shutdown'],
        'description': 'Exit JARVIS',
        'enabled': True,
    },
}

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_CONFIG = {
    # Paths
    'base_dir': Path(__file__).parent.absolute(),
    'data_dir': Path.home() / '.jarvis' / 'data',
    'logs_dir': Path.home() / '.jarvis' / 'logs',
    'cache_dir': Path.home() / '.jarvis' / 'cache',
    
    # Application Info
    'app_name': 'JARVIS',
    'version': '1.0.0',
    'author': 'Sushant1029',
    'description': 'Just A Rather Very Intelligent System',
    
    # Server Configuration
    'host': 'localhost',
    'port': 5000,
    'debug': False,
    
    # Performance
    'max_workers': 4,
    'request_timeout': 30,  # seconds
    'cache_ttl': 3600,  # seconds
    
    # Features
    'voice_recognition': True,
    'text_to_speech': True,
    'natural_language_processing': True,
}

# ============================================================================
# VOICE SETTINGS
# ============================================================================

VOICE_CONFIG = {
    'engine': 'pyttsx3',  # pyttsx3, google_tts, azure
    'voice_id': 0,  # Voice selection (0 = default)
    'rate': 150,  # Speech rate (words per minute)
    'volume': 1.0,  # 0.0 to 1.0
    'language': 'en-US',
    'listen_on_startup': False,
    'wake_word': 'JARVIS',  # Wake word for voice activation
}

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_CONFIG = {
    'engine': 'sqlite',  # sqlite, mysql, postgresql
    'sqlite': {
        'path': Path.home() / '.jarvis' / 'jarvis.db',
    },
    'mysql': {
        'host': 'localhost',
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': 'jarvis_db',
        'port': 3306,
    },
    'postgresql': {
        'host': 'localhost',
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': 'jarvis_db',
        'port': 5432,
    },
}

# ============================================================================
# PLUGIN CONFIGURATION
# ============================================================================

PLUGINS = {
    'enabled': True,
    'plugin_dir': Path(__file__).parent / 'plugins',
    'auto_load': True,
    'plugins_list': [
        'weather',
        'news',
        'music',
        'calendar',
        'email',
        'web_search',
    ],
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'detailed',
            'filename': str(APP_CONFIG['logs_dir'] / 'jarvis.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
    },
}

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

SECURITY_CONFIG = {
    'enable_ssl': False,
    'ssl_cert_path': '',
    'ssl_key_path': '',
    'enable_authentication': False,
    'auth_timeout': 3600,  # seconds
    'max_login_attempts': 5,
    'lockout_duration': 900,  # seconds (15 minutes)
}

# ============================================================================
# RESPONSE TEMPLATES
# ============================================================================

RESPONSE_TEMPLATES = {
    'greeting': "Hello! I'm JARVIS, your personal assistant. How can I help you today?",
    'error': "Sorry, I encountered an error: {}",
    'success': "Task completed successfully!",
    'unknown_command': "I'm sorry, I didn't understand that command. Type 'help' for assistance.",
    'api_error': "There was an issue connecting to the external service. Please try again later.",
    'goodbye': "Thank you for using JARVIS. Goodbye!",
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_config(key, default=None):
    """Get configuration value by key"""
    return globals().get(key, default)


def load_config_from_env():
    """Load configuration from environment variables"""
    for key, value in os.environ.items():
        if key.startswith('JARVIS_'):
            config_key = key.replace('JARVIS_', '').lower()
            # You can set nested config values here


def validate_config():
    """Validate configuration settings"""
    required_dirs = [
        APP_CONFIG['data_dir'],
        APP_CONFIG['logs_dir'],
        APP_CONFIG['cache_dir'],
    ]
    
    for dir_path in required_dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


# Initialize configuration
if __name__ == '__main__':
    validate_config()
    print("Configuration loaded successfully!")
