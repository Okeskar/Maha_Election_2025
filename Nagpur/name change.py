import os

# Folder containing the files
folder_path = r"C:\Onkar\Swapnil\Election maps\Nagpur\New folder"

# Phrase to remove (case-insensitive)
phrase_to_remove = "ward-wise structure and ward structure map"

for filename in os.listdir(folder_path):
    # Check if the phrase is in filename (case insensitive)
    if phrase_to_remove.lower() in filename.lower():
        # Create new filename by removing the phrase (case insensitive)
        # To keep original case except the phrase removed:
        # We'll do a case-insensitive replace:
        
        # Find the start and end index of phrase (lowercased)
        lower_filename = filename.lower()
        start_idx = lower_filename.find(phrase_to_remove.lower())
        end_idx = start_idx + len(phrase_to_remove)
        
        # Remove the phrase
        new_filename = filename[:start_idx] + filename[end_idx:]
        
        # Also clean up extra spaces that might appear at start/end or double spaces
        new_filename = new_filename.strip()
        new_filename = " ".join(new_filename.split())
        
        # Rename file on disk
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        
        print(f'Renaming:\n  "{filename}" → "{new_filename}"')
        os.rename(old_path, new_path)

print("Done renaming files.")
