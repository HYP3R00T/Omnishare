import json
import os
from functools import wraps
from typing import Any, Dict

from omnishare.constants import CONFIG_DEFAULT_DATA, CONFIG_FILE


def ensure_file_exists(func):
    """Decorator to ensure the config file exists before operations"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "w") as f:
                json.dump(CONFIG_DEFAULT_DATA, f)
        return func(*args, **kwargs)

    return wrapper


@ensure_file_exists
def read_config() -> Dict:
    """
    Read the entire configuration file

    Args:
        CONFIG_FILE: Path to the config file

    Returns:
        Dict containing all configuration data
    """
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


@ensure_file_exists
def write_config(data: Dict) -> bool:
    """
    Write data to configuration file (overwrites existing data)

    Args:
        CONFIG_FILE: Path to the config file
        data: Dictionary containing configuration data

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error writing to config file: {e}")
        return False


@ensure_file_exists
def update_config(key_path: str, value: Any) -> bool:
    """
    Update a specific key in the configuration file

    Args:
        CONFIG_FILE: Path to the config file
        key_path: Dot-separated path to the key (e.g., "database.host")
        value: Value to set

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = read_config(CONFIG_FILE)
        keys = key_path.split(".")
        current = config

        # Navigate to the nested location
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set the value
        current[keys[-1]] = value

        return write_config(CONFIG_FILE, config)
    except Exception as e:
        print(f"Error updating config: {e}")
        return False


@ensure_file_exists
def get_value(key_path: str, default: Any = None) -> Any:
    """
    Get a specific value from the configuration file

    Args:
        CONFIG_FILE: Path to the config file
        key_path: Dot-separated path to the key (e.g., "database.host")
        default: Default value if key doesn't exist

    Returns:
        Value if found, default if not found
    """
    try:
        config = read_config(CONFIG_FILE)
        keys = key_path.split(".")
        current = config

        # Navigate through the nested structure
        for key in keys:
            if key not in current:
                return default
            current = current[key]

        return current
    except Exception:
        return default


@ensure_file_exists
def delete_key(key_path: str) -> bool:
    """
    Delete a key from the configuration file

    Args:
        CONFIG_FILE: Path to the config file
        key_path: Dot-separated path to the key to delete

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = read_config(CONFIG_FILE)
        keys = key_path.split(".")
        current = config

        # Navigate to the parent of the key to delete
        for key in keys[:-1]:
            if key not in current:
                return False
            current = current[key]

        # Delete the key if it exists
        if keys[-1] in current:
            del current[keys[-1]]
            return write_config(CONFIG_FILE, config)
        return False
    except Exception as e:
        print(f"Error deleting key: {e}")
        return False


@ensure_file_exists
def merge_config(new_data: Dict) -> bool:
    """
    Merge new data with existing configuration

    Args:
        CONFIG_FILE: Path to the config file
        new_data: Dictionary containing new configuration data

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        current_config = read_config(CONFIG_FILE)

        def deep_merge(source: Dict, destination: Dict) -> Dict:
            for key, value in source.items():
                if key in destination and isinstance(destination[key], dict) and isinstance(value, dict):
                    deep_merge(value, destination[key])
                else:
                    destination[key] = value
            return destination

        merged_config = deep_merge(new_data, current_config)
        return write_config(CONFIG_FILE, merged_config)
    except Exception as e:
        print(f"Error merging config: {e}")
        return False
