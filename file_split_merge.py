import os

# Split a file into multiple files
def split_file(file_path, num_parts):
    # Open the file
    with open(file_path, 'rb') as f:
        # Read the contents of the file
        data = f.read()
        # Calculate the size of each part
        part_size = len(data) // num_parts
        # Split the data into parts, don't forget the last part
        parts = [data[i * part_size:(i + 1) * part_size] for i in range(num_parts)]
        parts[-1] += data[num_parts * part_size:]
        # Create a directory to store the parts
        parts_dir = file_path + '_parts'
        os.makedirs(parts_dir, exist_ok=True)
        # Write each part to a separate file
        for i, part in enumerate(parts):
            part_path = os.path.join(parts_dir, f'{i}.part')
            with open(part_path, 'wb') as f:
                f.write(part)


# Merge multiple files into a single file
def merge_files(parts_dir, output_file):
    # Get the list of part files
    part_files = [os.path.join(parts_dir, f) for f in os.listdir(parts_dir) if f.endswith('.part')]
    # Sort the part files according to their tailing part number
    part_files.sort(key=lambda x: int(x.split('\\')[-1].replace('.part', '')))
    # Open the output file
    with open(output_file, 'wb') as f:
        # Write the contents of each part file to the output file
        for part_file in part_files:
            with open(part_file, 'rb') as part_f:
                f.write(part_f.read())


# Compute SHA1 hash of a file
def compute_sha1(file_path):
    import hashlib
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest(), os.path.getsize(file_path)


if __name__ == '__main__':
    import sys

    which = sys.argv[1]

    if which == 'split':
        file_path = sys.argv[2]
        num_parts = int(sys.argv[3])
        split_file(file_path, num_parts)
    
    elif which == 'merge':
        parts_dir = sys.argv[2]
        output_file = sys.argv[3]
        merge_files(parts_dir, output_file)

    elif which == 'sha1':
        file_path = sys.argv[2]
        print(compute_sha1(file_path))