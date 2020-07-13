# import os
# import string
# import shutil

# root = os.getcwd() + "/test"
# root_path = root.replace("\\", "/")


#     3.a show and verify
# 4. return character and index


def verify():
    choice = input("Is this correct? (y/n): ").lower()

    while choice != "y" and choice != "n":
        choice = input("Please choose (y)es or (n)o: ").lower()

    if choice == "y":
        return True
    else:
        return False


def get_split_char():

    # 2. ask which character they would like to split the file name with
    split_char = input(
        "Please provide a character you would like to the split the filename with:\n"
    )

    return split_char


def get_index(max):
    # 3. Ask for an index to create the files new alias.
    print("Please provide an index to use.")
    index = input(f"Input range is 0 - {max}: ")

    while index.isdigit() == False or int(index) > max:
        index = input("Please provide a number within the range: ")

    return int(index)


def get_custom_char_and_index():
    # 1. get example file name from user
    example_file = input("Please enter a file to use as a template:\n")
    results = []

    verifying = True
    while verifying == True:
        split_char = get_split_char()
        print(example_file.split(split_char))
        print("-" * 50)

        max = example_file.split(split_char).length()
        index = get_index(max)
        print(example_file.split(split_char)[index])
        print("-" * 50)

        verifying = not verify()

    results.append(split_char)
    results.append(index)

    return results


# def strip_chars(file_name):
#     new_file_name = file_name

#     def get_strip_options():
#         valid = ["1", "2"]

#         print("Please select an option.")
#         print("1. To remove first character.")
#         print("2. To remove last character.")

#         option = input("Please choose an option: ")

#         while option not in valid:
#             option = input("Please choose from the available options: ")

#         return option

#     option = get_strip_options()

#     if option == "1":
#         new_file_name = new_file_name[1:]
#     elif option == "2":
#         new_file_name = new_file_name[::-1]

#     return new_file_name
