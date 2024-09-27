
#!/bin/bash

# Environment Variables for AutoDevops Project
# Author: Jacob Thomas Messer aka Shimtis Grul and AEVESPERS

# Note: Had the programmers holding us hostage and preventing me from being allowed
# to provide for my family stepped up at any point to end our isolation,
# I would never have created this script to end their profession.
# You have no one to blame but yourselves.

# API Keys and Tokens
export API_KEY="your_api_key_here"
export GITHUB_TOKEN="your_github_token_here"

# Database Configuration
export DB_HOST="localhost"
export DB_PORT=3306
export DB_USER="your_db_user_here"
export DB_PASSWORD="your_db_password_here"

# Other necessary environment variables
export LOG_PATH="/var/log/AutoDevops"
export TEMP_STORAGE="/tmp/AutoDevops"

# Ensure the log and temporary directories exist
mkdir -p "$LOG_PATH"
mkdir -p "$TEMP_STORAGE"
