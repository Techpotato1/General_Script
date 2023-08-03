import platform
import os
import shutil
import subprocess
import tempfile
import datetime

system = 0
# If the system is Windows continue as normal, if not exit on Mac and display a warning on Linux
if platform.system() != "Windows":
    # Make sure user ran the script with sudo
    if os.geteuid() != 0:
        print("This script requires root (sudo) privileges. Please re-run with sudo.")
        exit(1)
    print(f"Unsupported operating system: {platform.system()}")
    print("This script is designed for Windows. Certain functions will not work. Proceed with caution.")
    system = 1
elif platform.system() == "Mac":
    print("Not compatible with Mac")
    exit()


def create_log_file():
    file_path = "log.txt"
    try:
        with open(file_path, 'w') as log_file:
            log_file.write(
                f"Log file created at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} successfully.\n")
            log_file.write(
                f"System started successfully with OS: {platform.system()}.\n")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

# Write actions to the log file


def write_to_log_file(s):
    file_path = "log.txt"
    try:
        with open(file_path, 'a') as log_file:
            log_file.write(s)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

# Func for searching through a folder and deleting everything inside


def remove_all_files_and_folders(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            # Use proper commands
            if not system == 1:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            else:
                if not os.path.isdir(file_path):
                    os.system(f"sudo rm {file_path}")
                else:
                    os.system(f"sudo rm -rf {file_path}")
        # Write file failures to the log file
        except Exception as e:
            with open('log.txt', 'a') as log_file:
                log_file.write('Failed to delete %s. Reason: %s' %
                               (file_path, e) + "\n")

# Clear the cache depending on the system


def clear_cache():
    print("Clearing System cache...")
    user_temp_folder = tempfile.gettempdir()
    remove_all_files_and_folders(user_temp_folder)

    # Ignore Windows folder if not Windows
    if system == 0:
        windows_temp_folder = os.path.join(
            os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')
        remove_all_files_and_folders(windows_temp_folder)
    else:
        pass

    write_to_log_file("System cache cleared successfully.")
    print("System cache cleared successfully.")

# Install Chocolaty
# Win only


def install_choco():
    try:
        # Check if the user already has choco installed and if not install
        run_with_powershell(os.path.abspath("Powershell\install_choco.ps1"))
        write_to_log_file("Choco installed successfully.")

    except subprocess.CalledProcessError:
        print("Failed to run the script with administrative privileges.")
        write_to_log_file("Failed to install Choco.")
        exit(1)

# Func for running PS commands in a separate window with admin


def run_with_powershell(fp):
    script_path = fp
    # Run the PowerShell script with administrative privileges
    try:
        subprocess.run(["powershell", "-NoExit", "-Command",
                       f"Start-Process powershell -Verb runAs -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\"'"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to run the script with administrative privileges.")
        exit(1)


def display_menu(included_indices):
    menu_options = ["\nGeneral Script Menu:", "1. Clear cache",
                     "2. Install Choco", "3. Install Essential Programs", "Exit"]
    # Exclude the last option (Exit)
    for i, option in enumerate(menu_options[:-1]):
        if i in included_indices:
            print(f"{option}")
    print(f"0. {menu_options[-1]}")  # Display Exit option at the bottom


def main():
    print("******************************")
    print("*   System Cleaning Script   *")
    print("******************************")

    while True:
        if system != 0:
            display_menu([0,1])
        else:
            display_menu([0,1,2,3])
        choice = input("Enter your choice: ")
        if system == 0:
            os.system("cls")
        else:
            os.system("clear")
        if choice == "0":
            exit()
        elif choice == "1":
            clear_cache()
        elif choice == "2":
            install_choco()
        elif choice == "3":
            if (input("This script will install 7-zip and VLC, do you wish to continue? \nEnter \"y\" if you do and Enter to exit.\n") == "y"):
                run_with_powershell(os.path.abspath(
                    "Powershell\install_programs.ps1"))
            else:
                os.system("cls")
                pass
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_log_file()
    main()
