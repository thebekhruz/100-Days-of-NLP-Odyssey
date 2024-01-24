#!/bin/bash

# Asking for the environment name
read -p "Please provide the environment name: " env_name

# Asking for the location where the environment should be created
read -p "Please enter the desired location for '$env_name': " env_location

# Confirming the details with the user
while true; do
    read -p "Create virtual environment '$env_name' at '$env_location'? (yes/no): " confirmation

    if [[ $confirmation == "yes" ]]; then
        break
    elif [[ $confirmation == "no" ]]; then
        echo "Exiting. No changes made."
        exit
    else
        echo "Invalid response. Please answer 'yes' or 'no'."
    fi
done

# Creating the virtual environment
mkdir -p "$env_location"
python3.9 -m venv "$env_location/$env_name"
echo "Virtual environment '$env_name' created at '$env_location'."