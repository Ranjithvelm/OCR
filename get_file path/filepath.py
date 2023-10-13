import os

def get_file_paths(folder_name):
    file_paths = []
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

# Example usage
folder_name = "Aptitude"  # Replace with the actual folder name
file_paths = get_file_paths(folder_name)

# Print the file paths
with open('my_list.txt', 'w') as file:
    for path in file_paths:
        print(path)
        file.write("%s\n" %path)
