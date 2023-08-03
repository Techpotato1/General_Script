import platform
import os
import shutil
import subprocess
import tempfile
import datetime

if platform.system() != "Windows":
    print(f"Unsupported operating system: {platform.system()}")
    print("This script is designed for Windows. Certain functions will not work. Proceed with caution.")


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


def write_to_log_file(s):
    file_path = "log.txt"
    try:
        with open(file_path, 'a') as log_file:
            log_file.write(s)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


def remove_all_files_and_folders(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            with open('log.txt', 'a') as log_file:
                log_file.write('Failed to delete %s. Reason: %s' %
                               (file_path, e) + "\n")


def clear_cache():
    print("Clearing System cache...")
    user_temp_folder = tempfile.gettempdir()
    remove_all_files_and_folders(user_temp_folder)

    if platform.system() == "Windows":
        windows_temp_folder = os.path.join(
            os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')
        remove_all_files_and_folders(windows_temp_folder)
    else:
        pass

    write_to_log_file("System cache cleared successfully.")
    print("System cache cleared successfully.")


def install_choco():
    try:
        run_with_powershell(os.path.abspath("Powershell\install_choco.ps1"))
        write_to_log_file("Choco installed successfully.")
        
    except subprocess.CalledProcessError:
        print("Failed to run the script with administrative privileges.")
        write_to_log_file("Failed to install Choco.")
        exit(1)


def run_with_powershell(fp):
    script_path = fp
    # Run the PowerShell script with administrative privileges
    try:
        subprocess.run(["powershell", "-NoExit", "-Command", f"Start-Process powershell -Verb runAs -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\"'"], check=True)
    except subprocess.CalledProcessError:
        print("Failed to run the script with administrative privileges.")
        exit(1)


def display_menu():
    print("\nGeneral Script Menu:")
    print("1. Clear cache")
    print("2. Install Choco")
    print("3. Install Essential Programs")
    print("0. Exit")


def display_menu_unsupported():
    print("\nYour OS is unsupported, some features are locked.")
    print("General Script Menu:")
    print("1. Clear cache")
    print("0. Exit")


def main():
    print("******************************")
    print("*   System Cleaning Script   *")
    print("******************************")
    if platform.system() == "Windows":
        while True:
            display_menu()
            choice = input("Enter your choice: ")
            os.system("cls")
            if choice == "0":
                exit()
            elif choice == "1":
                clear_cache()
            elif choice == "2":
                install_choco()
            elif choice == "3":
                if(input("This script will install 7-zip and VLC, do you wish to continue? \nEnter \"y\" if you do and Enter to exit.\n") == "y"):
                    run_with_powershell(os.path.abspath("Powershell\install_programs.ps1"))
                else:
                    os.system("cls")
                    pass
            else:
                print("Invalid choice. Please try again.")
    else:
        while True:
            display_menu_unsupported()
            choice = input("Enter your choice: ")
            os.system("clear")
            if choice == "0":
                exit()
            elif choice == "1":
                clear_cache()
            elif choice == "2":

                pass
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    create_log_file()
    main()
