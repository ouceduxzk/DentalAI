"""
Base Trainer class for model training
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from typing import Optional, Dict, Any
import logging


class Trainer:
    """
    Base trainer class for training neural networks
    
    Example:
        >>> model = MyModel()
        >>> trainer = Trainer(model, train_loader, val_loader)
        >>> trainer.train(epochs=100)
    """
    
    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: Optional[DataLoader] = None,
        device: str = "cuda" if torch.cuda.is_available() else "cpu",
        learning_rate: float = 1e-3,
        checkpoint_dir: str = "checkpoints"
    ):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.checkpoint_dir = checkpoint_dir
        
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss()
        
        self.logger = logging.getLogger(__name__)
        
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        pbar = tqdm(self.train_loader, desc="Training")
        for batch_idx, (data, target) in enumerate(pbar):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
            
            pbar.set_postfix({
                'loss': total_loss / (batch_idx + 1),
                'acc': 100. * correct / total
            })
            
        return {
            'loss': total_loss / len(self.train_loader),
            'accuracy': 100. * correct / total
        }
    
    def validate(self) -> Dict[str, float]:
        """Validate the model"""
        if self.val_loader is None:
            return {}
            
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in tqdm(self.val_loader, desc="Validating"):
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                loss = self.criterion(output, target)
                
                total_loss += loss.item()
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        return {
            'val_loss': total_loss / len(self.val_loader),
            'val_accuracy': 100. * correct / total
        }
    
    def train(self, epochs: int) -> None:
        """Train the model for multiple epochs"""
        best_val_acc = 0.0
        
        for epoch in range(epochs):
            self.logger.info(f"Epoch {epoch + 1}/{epochs}")
            
            train_metrics = self.train_epoch()
            self.logger.info(f"Train - Loss: {train_metrics['loss']:.4f}, "
                           f"Acc: {train_metrics['accuracy']:.2f}%")
            
            if self.val_loader is not None:
                val_metrics = self.validate()
                self.logger.info(f"Val - Loss: {val_metrics['val_loss']:.4f}, "
                               f"Acc: {val_metrics['val_accuracy']:.2f}%")
                
                # Save best model
                if val_metrics['val_accuracy'] > best_val_acc:
                    best_val_acc = val_metrics['val_accuracy']
                    self.save_checkpoint(f"best_model_epoch_{epoch + 1}.pth")
    
    def save_checkpoint(self, filename: str) -> None:
        """Save model checkpoint"""
        import os
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        path = os.path.join(self.checkpoint_dir, filename)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, path)
        self.logger.info(f"Checkpoint saved to {path}")
