#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)
import docker
import argparse

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

def list_build_cache(client):
    build_cache = client.df()["LayersSize"]
    if build_cache == 0:
        print("No build cache found.")
    else:
        print(f"Build cache size: {build_cache} bytes")

def remove_build_cache(client):
    response = client.images.prune(filters={"dangling": False})
    build_cache_reclaimed = response["SpaceReclaimed"]
    print(f"Reclaimed {build_cache_reclaimed} bytes from build cache")

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
        remove_build_cache(client)
        
if __name__ == "__main__":
    main()        
