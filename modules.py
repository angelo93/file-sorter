""" This file stores main feature modules. """

# Import required libraries
import os
import shutil
import string
import helpers


def del_empty_dirs(root_path):
    """ Delete all empty directories and subdirectories
        root_path = path of root folder passed in from menu instance. """

    msg = "Find and delete all empty directories? (y/n): "

    choice = helpers.verify(msg)

    if choice == False:
        return print("Empty directories will not be deleted.")

    deleted_dirs = []  # List to record deleted directories
    deleted_txt = "deleted_dirs.txt"  # Text file to view deleted directories

    if choice == True:
        for dirpath, dirnames, _ in os.walk(root_path, topdown=False):
            # Skip hidden directories
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            try:
                os.rmdir(dirpath)
                deleted_dirs.append(dirpath)
            except:
                print("{} is not empty".format(dirpath))

        if len(deleted_dirs) > 0:
            print("All empty directories have been deleted")
            print(
                "If you would like to review the directories deleted, please review the deleted_dirs.txt file"
            )
            write_logs(deleted_dirs, deleted_txt)
        else:
            print("There were no empty directories to delete")


def create_file_dictionary(root_path, split_char=".", index=-1, organize=False, by_ext=True):
    """ Create a dictionary of all files in a directory tree.
        The filename serves as the first level key and it's value is composed of a nested dictionary.
        The nested dictionary holds the information to be used to move and organize the file according to user selected options"""

    dirs_to_skip = []
    file_dictionary = {}
    parent_dir = ""

    dirs_to_skip = helpers.get_dirs_to_skip()

    for dirpath, _, filenames in os.walk(root_path):
        # Skip hidden directories & aformentioned dirs to skip.
        if dirpath.split("\\")[-1].startswith(".") or dirpath.split("\\")[-1] in dirs_to_skip:
            continue

        for file_name in filenames:
            # If split_char == '.', file's extension otherwise file's name w/out extension
            current_file_alias = file_name.split(split_char)[index].strip()

            # Skip hidden files.
            if file_name.startswith("."):
                continue

            # If organizing by file name, set parent directory to...
            if organize and not by_ext:
                parent_dir = helpers.get_parent_dir_ONBE(
                    file_name) + "\\" + current_file_alias
                destination = os.path.join(
                    root_path, parent_dir, file_name).replace("\\", "/")

            # If organizing by file extension, set parent directory to...
            elif organize and by_ext:
                parent_dir = (
                    helpers.get_parent_dir_OBE(file_name, split_char, index)
                    + "\\"
                    + current_file_alias
                )
                destination = os.path.join(
                    root_path, parent_dir, file_name).replace("\\", "/")

            else:
                parent_dir = current_file_alias
                destination = os.path.join(root_path, current_file_alias, file_name).replace(
                    "\\", "/"
                )

            # Source path of current file.
            source = os.path.join(dirpath, file_name).replace("\\", "/")

            file_dictionary[file_name] = {
                "parent_dir": parent_dir,
                "source": source,
                "destination": destination,
            }

    return file_dictionary


def move_files(root_path, file_dictionary):
    """ Move files from one directory to another using a given dictionary of files. """

    for _, file_info in file_dictionary.items():
        # Check to see if the file needs to be moved, if not continue to next file.
        if file_info["source"] == file_info["destination"]:
            continue

        try:
            os.makedirs(os.path.join(
                root_path, file_info["parent_dir"]), exist_ok=True)
            shutil.move(file_info["source"], file_info["destination"])
        except FileExistsError:
            print('The file "{}" already exists.'.format(
                file_info["destination"]))
        except FileNotFoundError:
            print('Source "{}" does not exist'.format(file_info["source"]))


def write_logs(list_name, file_name):
    """ Record elements in a given list to a text file for reference. """

    save_path = os.getcwd() + "\\logs"

    # Create the complete path name for the text file.
    complete_file_path = os.path.join(save_path, file_name)

    # Call make_dir to make the text folder in case it's not present.
    if os.path.isdir(save_path) == False:
        helpers.make_logs_dir(save_path)

    print(f"Proceeding to write {file_name}.")

    with open(complete_file_path, "w", encoding="utf-8") as log_file:
        for item in list_name:
            log_file.write(item + "\n")

    log_file.close()

    return print("Write was succesful")


def rename_extension(root_path, old_ext, new_ext):
    """ Batch rename one file extension at a time in a given directory """

    if os.path.isdir(root_path) == False:
        return print(f"Unable to find:\n{root_path}")

    file_list = helpers.get_file_list(root_path)

    for filename in file_list:
        if filename.split(".")[-1] == old_ext:
            new_filename = filename
            temp_ext = new_filename.split(".")
            temp_ext[-1] = new_ext
            new_filename = ".".join(temp_ext)
            try:
                os.rename(os.path.join(root_path, filename),
                          os.path.join(root_path, new_filename))
            except:
                print(f"Unable to rename the extension of {filename}.")
