import pytest
import sys
import os

# Agregar directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from validator import PasswordValidator
