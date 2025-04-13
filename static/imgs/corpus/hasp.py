
from PIL import Image
import imagehash
import os

# Folders to process
folders = ['0', '1', '2', '3', '4']

# Function to process images and store hashes
def generate_hashes():
    for folder in folders:
        hash_file = f"{folder}_hashes.txt"

        with open(hash_file, "w") as f:
            folder_path = os.path.join(os.getcwd(), folder)

            for filename in os.listdir(folder_path):
                if filename.endswith(".png"):
                    letter = filename.split(".")[0]  # Extract letter from filename
                    img_path = os.path.join(folder_path, filename)

                    # Generate perceptual hash
                    img = Image.open(img_path)
                    img_hash = str(imagehash.phash(img))

                    # Write to file
                    f.write(f"{letter}:{img_hash}\n")

        print(f"Hashes stored in: {hash_file}")

if __name__ == "__main__":
    generate_hashes()