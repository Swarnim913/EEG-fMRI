import os

def create_directories(base_name="trial", count=40):
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Loop to create the specified number of directories
    for i in range(1, count + 1):
        # Construct the directory name
        directory_name = f"{base_name}_{i}"
        
        # Create the full path for the new directory
        directory_path = os.path.join(current_directory, directory_name)
        
        # Create the directory
        try:
            os.makedirs(directory_path)
            print(f"Created directory: {directory_name}")
        except FileExistsError:
            print(f"Directory {directory_name} already exists.")
        except Exception as e:
            print(f"An error occurred while creating {directory_name}: {e}")

# Run the function to create 40 directories
if __name__ == "__main__":
    create_directories()
