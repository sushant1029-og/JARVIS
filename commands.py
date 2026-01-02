"""
JARVIS Command Definitions and Handlers
========================================

This module contains command definitions and handlers for JARVIS to execute
various tasks including:
- Opening applications
- Web searches
- Telling time and date
- Providing weather information
- System operations
"""

import os
import sys
import subprocess
import webbrowser
from datetime import datetime
from typing import Dict, Callable, Any, Optional
import json

# Try to import optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import platform
    PLATFORM_INFO = platform.system()
except ImportError:
    PLATFORM_INFO = "Unknown"


class CommandHandler:
    """Base class for command handlers."""
    
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self._register_commands()
    
    def _register_commands(self):
        """Register all available commands."""
        self.commands = {
            # Application commands
            'open': self.open_application,
            'launch': self.open_application,
            
            # Web search commands
            'search': self.web_search,
            'google': self.google_search,
            'wikipedia': self.wikipedia_search,
            
            # Time and date commands
            'time': self.tell_time,
            'date': self.tell_date,
            'now': self.tell_current_datetime,
            
            # Weather commands
            'weather': self.get_weather,
            'forecast': self.get_weather_forecast,
            
            # System commands
            'help': self.show_help,
            'commands': self.list_commands,
        }
    
    def execute(self, command: str, *args, **kwargs) -> Any:
        """
        Execute a command with given arguments.
        
        Args:
            command: The command name to execute
            *args: Positional arguments for the command
            **kwargs: Keyword arguments for the command
            
        Returns:
            Result of the command execution
        """
        command = command.lower().strip()
        
        if command not in self.commands:
            return f"Command '{command}' not found. Type 'help' for available commands."
        
        try:
            handler = self.commands[command]
            return handler(*args, **kwargs)
        except Exception as e:
            return f"Error executing command '{command}': {str(e)}"
    
    # ==================== Application Commands ====================
    
    def open_application(self, app_name: str) -> str:
        """
        Open an application by name.
        
        Args:
            app_name: Name of the application to open
            
        Returns:
            Status message
        """
        app_name = app_name.lower().strip()
        
        # Common application mappings
        app_map = {
            # Web browsers
            'chrome': 'google-chrome' if PLATFORM_INFO == 'Linux' else 'chrome',
            'firefox': 'firefox',
            'edge': 'msedge',
            'safari': 'safari',
            
            # Office applications
            'notepad': 'notepad' if PLATFORM_INFO == 'Windows' else 'gedit',
            'word': 'winword',
            'excel': 'excel',
            'powerpoint': 'powerpnt',
            'vs code': 'code',
            'vscode': 'code',
            
            # Media players
            'vlc': 'vlc',
            'spotify': 'spotify',
            'youtube': None,  # Opens in browser
            
            # System applications
            'calculator': 'calc' if PLATFORM_INFO == 'Windows' else 'gnome-calculator',
            'terminal': 'gnome-terminal' if PLATFORM_INFO == 'Linux' else 'Terminal',
            'file manager': 'nautilus' if PLATFORM_INFO == 'Linux' else 'explorer',
        }
        
        # Special handling for YouTube
        if app_name == 'youtube':
            webbrowser.open('https://www.youtube.com')
            return f"Opening YouTube in default browser..."
        
        # Get the executable name
        executable = app_map.get(app_name, app_name)
        
        if executable is None:
            return f"Application '{app_name}' is not configured."
        
        try:
            if PLATFORM_INFO == 'Windows':
                os.startfile(executable)
            elif PLATFORM_INFO == 'Darwin':  # macOS
                subprocess.Popen(['open', '-a', executable])
            else:  # Linux
                subprocess.Popen([executable])
            
            return f"Opening {app_name}..."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"
    
    # ==================== Web Search Commands ====================
    
    def web_search(self, query: str, engine: str = 'google') -> str:
        """
        Perform a web search using the specified search engine.
        
        Args:
            query: Search query
            engine: Search engine to use (google, bing, duckduckgo)
            
        Returns:
            Status message
        """
        query = query.strip()
        
        if not query:
            return "Please provide a search query."
        
        search_urls = {
            'google': f'https://www.google.com/search?q={query.replace(" ", "+")}',
            'bing': f'https://www.bing.com/search?q={query.replace(" ", "+")}',
            'duckduckgo': f'https://www.duckduckgo.com/?q={query.replace(" ", "+")}',
        }
        
        url = search_urls.get(engine.lower(), search_urls['google'])
        
        try:
            webbrowser.open(url)
            return f"Searching for '{query}' using {engine}..."
        except Exception as e:
            return f"Failed to perform search: {str(e)}"
    
    def google_search(self, query: str) -> str:
        """Perform a Google search."""
        return self.web_search(query, 'google')
    
    def wikipedia_search(self, query: str) -> str:
        """
        Search Wikipedia for a query.
        
        Args:
            query: Search query
            
        Returns:
            Status message
        """
        query = query.strip()
        
        if not query:
            return "Please provide a search query."
        
        url = f'https://www.wikipedia.org/wiki/{query.replace(" ", "_")}'
        
        try:
            webbrowser.open(url)
            return f"Searching Wikipedia for '{query}'..."
        except Exception as e:
            return f"Failed to search Wikipedia: {str(e)}"
    
    # ==================== Time and Date Commands ====================
    
    def tell_time(self) -> str:
        """
        Tell the current time.
        
        Returns:
            Current time as a formatted string
        """
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"
    
    def tell_date(self) -> str:
        """
        Tell the current date.
        
        Returns:
            Current date as a formatted string
        """
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"
    
    def tell_current_datetime(self) -> str:
        """
        Tell the current date and time.
        
        Returns:
            Current date and time as a formatted string
        """
        current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        return f"It is {current_datetime}"
    
    # ==================== Weather Commands ====================
    
    def get_weather(self, location: str = 'auto', unit: str = 'metric') -> str:
        """
        Get current weather information for a location.
        
        Args:
            location: City name or 'auto' for automatic location detection
            unit: Temperature unit ('metric' for Celsius, 'imperial' for Fahrenheit)
            
        Returns:
            Weather information or error message
        """
        if not REQUESTS_AVAILABLE:
            return "Weather functionality requires the 'requests' library. Install it with: pip install requests"
        
        try:
            # Using Open-Meteo API (free, no API key required)
            if location.lower() == 'auto':
                # Get user's location from IP
                try:
                    ip_response = requests.get('https://ipapi.co/json/', timeout=5)
                    location_data = ip_response.json()
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')
                    city = location_data.get('city', 'Your Location')
                except:
                    return "Could not determine your location. Please specify a city name."
            else:
                # Geocode the location
                try:
                    geo_response = requests.get(
                        f'https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json',
                        timeout=5
                    )
                    results = geo_response.json().get('results', [])
                    if not results:
                        return f"Location '{location}' not found."
                    
                    location_data = results[0]
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')
                    city = location_data.get('name', location)
                except:
                    return "Error geocoding location."
            
            # Get weather data
            weather_response = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
                f'&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m'
                f'&temperature_unit={"Fahrenheit" if unit == "imperial" else "Celsius"}',
                timeout=5
            )
            
            weather_data = weather_response.json().get('current', {})
            
            if not weather_data:
                return "Could not retrieve weather data."
            
            temperature = weather_data.get('temperature_2m', 'N/A')
            humidity = weather_data.get('relative_humidity_2m', 'N/A')
            wind_speed = weather_data.get('wind_speed_10m', 'N/A')
            weather_code = weather_data.get('weather_code', 0)
            
            # Convert weather code to description
            weather_description = self._get_weather_description(weather_code)
            
            unit_symbol = '°F' if unit == 'imperial' else '°C'
            
            return (
                f"Weather in {city}:\n"
                f"  Temperature: {temperature}{unit_symbol}\n"
                f"  Conditions: {weather_description}\n"
                f"  Humidity: {humidity}%\n"
                f"  Wind Speed: {wind_speed} km/h"
            )
        
        except requests.exceptions.Timeout:
            return "Weather service request timed out. Please try again."
        except Exception as e:
            return f"Error retrieving weather: {str(e)}"
    
    def get_weather_forecast(self, location: str = 'auto', days: int = 3) -> str:
        """
        Get weather forecast for upcoming days.
        
        Args:
            location: City name or 'auto' for automatic location detection
            days: Number of days to forecast (1-10)
            
        Returns:
            Weather forecast or error message
        """
        if not REQUESTS_AVAILABLE:
            return "Weather functionality requires the 'requests' library. Install it with: pip install requests"
        
        days = min(max(days, 1), 10)  # Clamp between 1 and 10
        
        try:
            # Get location
            if location.lower() == 'auto':
                try:
                    ip_response = requests.get('https://ipapi.co/json/', timeout=5)
                    location_data = ip_response.json()
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')
                    city = location_data.get('city', 'Your Location')
                except:
                    return "Could not determine your location. Please specify a city name."
            else:
                try:
                    geo_response = requests.get(
                        f'https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json',
                        timeout=5
                    )
                    results = geo_response.json().get('results', [])
                    if not results:
                        return f"Location '{location}' not found."
                    
                    location_data = results[0]
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')
                    city = location_data.get('name', location)
                except:
                    return "Error geocoding location."
            
            # Get forecast data
            forecast_response = requests.get(
                f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}'
                f'&daily=weather_code,temperature_2m_max,temperature_2m_min'
                f'&timezone=auto&forecast_days={days}',
                timeout=5
            )
            
            forecast_data = forecast_response.json().get('daily', {})
            
            if not forecast_data:
                return "Could not retrieve forecast data."
            
            forecast_str = f"Weather Forecast for {city} ({days} days):\n"
            
            dates = forecast_data.get('time', [])
            weather_codes = forecast_data.get('weather_code', [])
            temp_max = forecast_data.get('temperature_2m_max', [])
            temp_min = forecast_data.get('temperature_2m_min', [])
            
            for i in range(min(days, len(dates))):
                date = datetime.fromisoformat(dates[i]).strftime("%A, %b %d")
                weather = self._get_weather_description(weather_codes[i])
                high = temp_max[i]
                low = temp_min[i]
                
                forecast_str += f"\n{date}:\n"
                forecast_str += f"  {weather}\n"
                forecast_str += f"  High: {high}°C, Low: {low}°C"
            
            return forecast_str
        
        except requests.exceptions.Timeout:
            return "Forecast service request timed out. Please try again."
        except Exception as e:
            return f"Error retrieving forecast: {str(e)}"
    
    @staticmethod
    def _get_weather_description(code: int) -> str:
        """
        Convert WMO weather code to description.
        
        Args:
            code: WMO weather code
            
        Returns:
            Weather description
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail",
        }
        return weather_codes.get(code, "Unknown")
    
    # ==================== Help and Information Commands ====================
    
    def show_help(self) -> str:
        """
        Show help information and available commands.
        
        Returns:
            Help text
        """
        help_text = """
╔════════════════════════════════════════════════════════════╗
║                    JARVIS Command Help                     ║
╚════════════════════════════════════════════════════════════╝

APPLICATION COMMANDS:
  open <app_name>     - Open an application
  launch <app_name>   - Launch an application

  Examples: open chrome, launch notepad, open vs code

WEB SEARCH COMMANDS:
  search <query>      - Search using Google
  google <query>      - Search using Google
  wikipedia <query>   - Search Wikipedia
  
  Examples: search machine learning, google Python tutorials

TIME & DATE COMMANDS:
  time                - Tell current time
  date                - Tell current date
  now                 - Tell current date and time
  
  Examples: what time is it, what's the date

WEATHER COMMANDS:
  weather [location]  - Get current weather
  forecast [location] [days] - Get weather forecast
  
  Examples: weather london, forecast new york 5

SYSTEM COMMANDS:
  help                - Show this help message
  commands            - List all available commands

Use: jarvis.execute('command', args...)
        """
        return help_text
    
    def list_commands(self) -> str:
        """
        List all available commands.
        
        Returns:
            List of commands
        """
        commands_list = "Available Commands:\n" + "=" * 40 + "\n"
        
        for cmd in sorted(self.commands.keys()):
            commands_list += f"  • {cmd}\n"
        
        commands_list += "\nType 'help' for detailed information."
        return commands_list


# Initialize global command handler
def initialize() -> CommandHandler:
    """
    Initialize the JARVIS command handler.
    
    Returns:
        CommandHandler instance
    """
    return CommandHandler()


# Create a default instance
jarvis = initialize()


# Convenience functions for easy access
def execute(command: str, *args, **kwargs) -> Any:
    """Execute a JARVIS command."""
    return jarvis.execute(command, *args, **kwargs)


def open_app(app_name: str) -> str:
    """Open an application."""
    return jarvis.open_application(app_name)


def search_web(query: str, engine: str = 'google') -> str:
    """Search the web."""
    return jarvis.web_search(query, engine)


def get_time() -> str:
    """Get current time."""
    return jarvis.tell_time()


def get_date() -> str:
    """Get current date."""
    return jarvis.tell_date()


def get_weather(location: str = 'auto') -> str:
    """Get weather information."""
    return jarvis.get_weather(location)


# Example usage and testing
if __name__ == '__main__':
    print("JARVIS Command Handler Initialized")
    print("=" * 50)
    
    # Test commands
    test_commands = [
        ('commands', []),
        ('time', []),
        ('date', []),
        ('help', []),
    ]
    
    for cmd, args in test_commands:
        print(f"\n>>> {cmd} {' '.join(map(str, args))}")
        result = execute(cmd, *args)
        print(result)
