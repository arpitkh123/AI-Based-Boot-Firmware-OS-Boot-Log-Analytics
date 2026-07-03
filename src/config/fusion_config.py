import os
import json
from pathlib import Path

# Default weights for the Confidence Fusion algorithm
DEFAULT_FUSION_WEIGHTS = {
    "rule_match": 2.0,      # High priority if a deterministic rule matches
    "kb_match": 1.5,        # High priority if knowledge base matches
    "iforest_score": 1.0,   # Standard priority for ML anomaly detection
    "template_sim": 0.5,    # Minor contributor: how many unseen templates
    "boot_health": 1.0,     # Standard priority for boot progress
    "severity": 1.0         # Standard priority for severity level
}

class FusionConfig:
    def __init__(self):
        self.weights = DEFAULT_FUSION_WEIGHTS.copy()
        self._load_from_env_or_file()
        
    def _load_from_env_or_file(self):
        # We can add logic here to load from a config.json if needed
        # For now, it uses defaults which can be overridden via DI or env vars
        pass
        
    def get_weights(self):
        return self.weights
