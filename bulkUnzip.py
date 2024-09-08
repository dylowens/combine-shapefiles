import os
import zipfile


def bulk_unzip(source_dir):
    # Remove any surrounding quotes from the path
    source_dir = source_dir.strip('"')

    for filename in os.listdir(source_dir):
        if filename.endswith('.zip'):
            file_path = os.path.join(source_dir, filename)
            extract_dir = os.path.splitext(file_path)[0]

            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            print(f"Extracted: {filename}")


if __name__ == "__main__":
    source_directory = input(
        "Enter the directory path containing ZIP files: ").strip('"')
    bulk_unzip(source_directory)
