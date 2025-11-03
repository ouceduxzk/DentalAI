"""
Model evaluation and testing
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List
import numpy as np
from tqdm import tqdm


class Evaluator:
    """
    Model evaluator for testing and inference
    
    Example:
        >>> model = load_model("checkpoints/best_model.pth")
        >>> evaluator = Evaluator(model, test_loader)
        >>> metrics = evaluator.evaluate()
    """
    
    def __init__(
        self,
        model: nn.Module,
        test_loader: DataLoader,
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.model = model.to(device)
        self.test_loader = test_loader
        self.device = device
        
    def evaluate(self) -> Dict[str, float]:
        """Evaluate model on test set"""
        self.model.eval()
        
        all_predictions = []
        all_targets = []
        all_probs = []
        
        with torch.no_grad():
            for data, target in tqdm(self.test_loader, desc="Evaluating"):
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                
                probs = torch.softmax(output, dim=1)
                _, predicted = output.max(1)
                
                all_predictions.extend(predicted.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
                all_probs.extend(probs.cpu().numpy())
        
        all_predictions = np.array(all_predictions)
        all_targets = np.array(all_targets)
        all_probs = np.array(all_probs)
        
        # Calculate metrics
        accuracy = (all_predictions == all_targets).mean() * 100
        
        return {
            'accuracy': accuracy,
            'predictions': all_predictions,
            'targets': all_targets,
            'probabilities': all_probs
        }
    
    def predict(self, data: torch.Tensor) -> torch.Tensor:
        """Make predictions on new data"""
        self.model.eval()
        with torch.no_grad():
            data = data.to(self.device)
            output = self.model(data)
            predictions = output.argmax(dim=1)
        return predictions
    
    def predict_with_confidence(self, data: torch.Tensor) -> tuple:
        """Make predictions with confidence scores"""
        self.model.eval()
        with torch.no_grad():
            data = data.to(self.device)
            output = self.model(data)
            probs = torch.softmax(output, dim=1)
            confidence, predictions = probs.max(dim=1)
        return predictions, confidence
