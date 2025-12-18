"""Test configuration and fixtures."""

import os
import sys

# Set up test environment BEFORE any imports
os.environ["PROJECT_ID"] = "test-project"
os.environ["LOCATION"] = "us-central1"
os.environ["GEMINI_MODEL"] = "gemini-1.5-pro"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/test-credentials.json"
os.environ["API_HOST"] = "0.0.0.0"
os.environ["API_PORT"] = "8000"
os.environ["FRONTEND_URL"] = "http://localhost:5173"

import pytest
