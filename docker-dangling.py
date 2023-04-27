# By David Espejo (Fortytwo Security)
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

def main():
    parser = argparse.ArgumentParser(description="List or delete dangling Docker images.")
    parser.add_argument("action", choices=["list", "delete"], help="Choose whether to list or delete dangling images.")
    args = parser.parse_args()

    client = docker.from_env()

    if args.action == "list":
        list_dangling_images(client)
    elif args.action == "delete":
        delete_dangling_images(client)

if __name__ == "__main__":
    main()
