# docker-cleaner

# Description

This Python script allows you to manage dangling Docker images and build cache. Dangling images are images that are not tagged and not being used by any container, while the build cache consists of intermediate layers created during the build process. The script provides options to list or delete dangling images, and to list or remove build cache.

# Instructions

Install Docker SDK for Python:

	pip install docker

Run the script with the desired action using the following command-line arguments:

list-images: List all dangling Docker images

delete-images: Delete all dangling Docker images

list-cache: List the build cache size

remove-cache: Remove build cache


The script will connect to your local Docker daemon, perform the specified action, and print the relevant information. If no dangling images or build cache are found, it will print a message indicating that.
