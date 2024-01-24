#!/bin/bash

# Asking for the location and name of the environment to delete
read -p "Enter the location of the environment you wish to delete: " env_location
read -p "Enter the name of the environment you wish to delete: " env_name

# Confirming the deletion with the user
while true; do
    read -p "Are you sure you want to delete the virtual environment '$env_name' at '$env_location'? (yes/no): " confirmation

    if [[ $confirmation == "yes" ]]; then
        break
    elif [[ $confirmation == "no" ]]; then
        echo "Exiting. No changes made."
        exit
    else
        echo "Invalid response. Please answer 'yes' or 'no'."
    fi
done

# Deleting the virtual environment
rm -rf "$env_location/$env_name"
echo "Virtual environment '$env_name' deleted from '$env_location'."

