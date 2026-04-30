"""
SubD3 - Fast Subdomain Discovery Tool
Enterprise-grade subdomain enumeration with AI & automation
"""

__version__ = "2.0.0"
__author__ = "DarkVector-bot"
__license__ = "MIT"

from .core.engine import SubD3Engine
from .stages.passive import PassiveStage
from .stages.active import ActiveStage
from .stages.generate import GenerateStage
from .stages.validate import ValidateStage

__all__ = [
    "SubD3Engine",
    "PassiveStage", 
    "ActiveStage",
    "GenerateStage",
    "ValidateStage"
]
