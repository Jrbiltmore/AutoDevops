#!/bin/bash

# API Keys Configuration

# This script loads API keys from environment variables.
# Ensure that these keys are stored securely and never hardcoded into the application code.
# You can store these keys in a separate environment file (.env) and load them here using source.

# Usage:
# source config/api_keys.sh

# Ensure that the API keys are set in the environment.
# Add a warning if any key is not set, but do not expose the actual key in logs.

# Example:
# export SERVICE_API_KEY="your_api_key_here"

# Function to check if an API key is set
check_api_key() {
    local key_name="$1"
    local key_value="${!key_name}"

    if [ -z "$key_value" ]; then
        echo "Warning: API key '$key_name' is not set. Please configure it in your environment."
    else
        echo "API key '$key_name' is loaded successfully."
    fi
}

# API key variables
# Replace these variable names with actual service names, e.g., AWS, Google, etc.
export SERVICE_1_API_KEY=${SERVICE_1_API_KEY:-""}
export SERVICE_2_API_KEY=${SERVICE_2_API_KEY:-""}
export SERVICE_3_API_KEY=${SERVICE_3_API_KEY:-""}

# Check if the API keys are set
check_api_key "SERVICE_1_API_KEY"
check_api_key "SERVICE_2_API_KEY"
check_api_key "SERVICE_3_API_KEY"

# For production, avoid logging sensitive information
# Consider integrating a secret management system such as AWS Secrets Manager, HashiCorp Vault, or environment variable management in Docker/Kubernetes.
