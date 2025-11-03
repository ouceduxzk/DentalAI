"""
Configuration file parser
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Union


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML or JSON file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    # Load based on file extension
    if config_path.suffix in ['.yaml', '.yml']:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    elif config_path.suffix == '.json':
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        raise ValueError(f"Unsupported config format: {config_path.suffix}")
    
    return config


def save_config(config: Dict[str, Any], save_path: str, format: str = 'yaml'):
    """
    Save configuration to file
    
    Args:
        config: Configuration dictionary
        save_path: Path to save configuration
        format: File format ('yaml' or 'json')
    """
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'yaml':
        with open(save_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
    elif format == 'json':
        with open(save_path, 'w') as f:
            json.dump(config, f, indent=2)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"Config saved to {save_path}")


def merge_configs(base_config: Dict[str, Any], 
                  override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two configuration dictionaries
    
    Args:
        base_config: Base configuration
        override_config: Configuration to override base
        
    Returns:
        Merged configuration
    """
    merged = base_config.copy()
    
    for key, value in override_config.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged


def validate_config(config: Dict[str, Any], required_keys: list) -> bool:
    """
    Validate that configuration contains required keys
    
    Args:
        config: Configuration dictionary
        required_keys: List of required keys
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    missing_keys = []
    
    for key in required_keys:
        if '.' in key:
            # Nested key
            parts = key.split('.')
            current = config
            for part in parts:
                if part not in current:
                    missing_keys.append(key)
                    break
                current = current[part]
        else:
            if key not in config:
                missing_keys.append(key)
    
    if missing_keys:
        raise ValueError(f"Missing required config keys: {missing_keys}")
    
    return True
