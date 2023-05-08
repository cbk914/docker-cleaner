#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)
import docker
import argparse
import subprocess
import re

def list_dangling_images(client):
    images = client.images.list(filters={"dangling": True})

    if not images:
        print("No dangling images found.")
    else:
        print("Dangling images:")
        for image in images:
            print(f"ID: {image.id}, Created: {image.attrs['Created']}, Size: {image.attrs['Size']} bytes")

def delete_dangling_images(client):
    images = client.images.list(filters={"dangling": True})

    if not images:
        print("No dangling images found.")
    else:
        print("Deleting dangling images:")
        for image in images:
            print(f"Deleting: ID: {image.id}, Created: {image.attrs['Created']}, Size: {image.attrs['Size']} bytes")
            client.images.remove(image.id)

def parse_cache_size(size_str):
    if size_str.strip() == '0' or size_str.strip() == '0B':
        return 0

    units = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    size, unit = re.search(r'(\d+(?:\.\d+)?)\s*([A-Za-z]+)?', size_str).groups()
    size = float(size) * units[unit]
    return int(size)

def list_build_cache(client):
    try:
        docker_system_df = subprocess.run(["docker", "system", "df"],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"docker system df stdout: {docker_system_df.stdout}")
        regex_result = re.search(r'(?i)Build Cache\s+(\d+(?:\.\d+)?\s*[A-Za-z]*).*', docker_system_df.stdout)
        print(f"regex result: {regex_result}")
        build_cache_size = parse_cache_size(regex_result.group(1))

        if build_cache_size == 0:
            print("No build cache found.")
        else:
            print(f"Build cache size: {build_cache_size} bytes")

    except Exception as e:
        print(f"Error listing build cache: {e}")

def remove_build_cache():
    try:
        # Get build cache size before pruning
        before_prune = subprocess.run(["docker", "system", "df"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"Before prune stdout: {before_prune.stdout}")
        regex_result = re.search(r'(?i)Build Cache\s+(\d+(?:\.\d+)?\s*[A-Za-z]*).*', before_prune.stdout)
        print(f"regex result: {regex_result}")
        before_prune_size = parse_cache_size(regex_result.group(1))

        # Prune build cache
        subprocess.run(["docker", "builder", "prune", "-f"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Get build cache size after pruning
        after_prune = subprocess.run(["docker", "system", "df"],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        regex_result = re.search(r'(?i)Build Cache\s+(\d+(?:\.\d+)?\s*[A-Za-z]*).*', after_prune.stdout)
        print(f"regex result: {regex_result}")
        after_prune_size = parse_cache_size(regex_result.group(1))

        # Calculate reclaimed space
        reclaimed_space = before_prune_size - after_prune_size
        print(f"Reclaimed {reclaimed_space} bytes from build cache")

    except Exception as e:
        print(f"Error removing build cache: {e}")

def main():
    parser = argparse.ArgumentParser(description="Manage dangling Docker images and build cache.")
    parser.add_argument("action", choices=["list-images", "delete-images", "list-cache", "remove-cache"],
                        help="Choose an action to perform on dangling images or build cache.")
    args = parser.parse_args()

    client = docker.from_env()

    if args.action == "list-images":
        list_dangling_images(client)
    elif args.action == "delete-images":
        delete_dangling_images(client)
    elif args.action == "list-cache":
        list_build_cache(client)
    elif args.action == "remove-cache":
        remove_build_cache()

if __name__ == "__main__":
    main()
