"""
Training configuration management
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingConfig:
    """Configuration for model training"""
    
    # Model parameters
    model_name: str = "resnet50"
    num_classes: int = 32  # Number of teeth
    
    # Training parameters
    batch_size: int = 32
    epochs: int = 100
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    
    # Data parameters
    train_data_path: str = "data/train"
    val_data_path: str = "data/val"
    test_data_path: str = "data/test"
    
    # Optimization
    optimizer: str = "adam"
    scheduler: str = "cosine"
    warmup_epochs: int = 5
    
    # Device
    device: str = "cuda"
    num_workers: int = 4
    
    # Checkpointing
    checkpoint_dir: str = "checkpoints"
    save_frequency: int = 5
    
    # Logging
    log_dir: str = "logs"
    log_frequency: int = 10
    
    # Early stopping
    early_stopping_patience: Optional[int] = 10
    
    def to_dict(self):
        """Convert config to dictionary"""
        return self.__dict__
    
    @classmethod
    def from_dict(cls, config_dict):
        """Create config from dictionary"""
        return cls(**config_dict)
