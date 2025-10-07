#!/usr/bin/env python3
"""
Quick Start Script for TrustLensAI
Complete setup and launch of AI Governance system
"""

import os
import sys
import subprocess
import logging
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _load_env_file(env_path: Path = Path(".env")) -> None:
    """Lightweight .env loader to populate os.environ without extra deps."""
    if not env_path.exists():
        return
    try:
        for raw in env_path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            # Do not overwrite an already-set environment variable
            if k and (k not in os.environ):
                os.environ[k] = v
    except Exception as e:
        logger.warning(f"⚠️  Could not parse .env file: {e}")


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python version: {sys.version}")
    return True


def check_environment_variables():
    """Check required environment variables"""
    logger.info("Checking environment variables...")

    # Load from existing .env if present, without overwriting OS env
    _load_env_file(Path(".env"))

    google_api_key = os.getenv('GOOGLE_API_KEY')
    if not google_api_key:
        logger.warning("⚠️  GOOGLE_API_KEY not found in environment")
        logger.info("Please set GOOGLE_API_KEY for AI agent functionality")
        logger.info("Get your API key from: https://makersuite.google.com/app/apikey")

        # Create .env file template only if it does not exist
        env_path = Path(".env")
        if not env_path.exists():
            env_template = """# TrustLensAI  Environment Variables
GOOGLE_API_KEY=your_gemini_api_key_here
SECRET_KEY=change-this-in-production
HOST=0.0.0.0
PORT=5001
DEBUG=True
"""
            with env_path.open('w', encoding='utf-8') as f:
                f.write(env_template)
            logger.info("📝 Created .env template file - please update with your API key")
        else:
            logger.info("📝 .env already exists; leaving it unchanged. Update GOOGLE_API_KEY in that file.")

        return False

    logger.info("✅ Environment variables configured")
    return True


def install_dependencies():
    """Install Python dependencies"""
    logger.info("Installing Python dependencies...")

    try:
        # Install dependencies
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'],
            check=True, capture_output=True, text=True
        )

        logger.info("✅ Python dependencies installed successfully")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("❌ requirements.txt not found")
        return False


def setup_directories():
    """Create necessary directories"""
    logger.info("Setting up directories...")

    directories = [
        './data',
        './data/chromadb',
        './data/security',
        './logs',
        './frontend/public',
        './frontend/src'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger.info("✅ Directories created")


def setup_databases():
    """Initialize databases"""
    logger.info("Initializing databases...")

    try:
        # Setup SQLite database
        logger.info("Setting up SQLite governance database...")
        result = subprocess.run(
            [sys.executable, 'setup_database.py'],
            check=True, capture_output=True, text=True
        )
        logger.info("✅ SQLite database initialized")

        # Setup ChromaDB knowledge store
        logger.info("Setting up ChromaDB knowledge store...")
        result = subprocess.run(
            [sys.executable, 'setup_chromadb.py'],
            check=True, capture_output=True, text=True
        )
        logger.info("✅ ChromaDB knowledge store initialized")

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Database setup failed: {e.stderr}")
        return False