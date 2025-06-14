---
title: "Shellscripting"
date: 2024-06-05T11:52:01+05:30
draft: false
---
## basics of shell scripting : 
### what is shell?
>> A shell is a command-line interpreter that provides a user interface for the Unix/Linux operating system. Users can typecommands to perform specific tasks such as navigating the file system, running programs, and managing system processes. Thereare different types of shells, with Bash (Bourne Again Shell) being one of the most popular.

### what is shell scripting?
>> Shell scripting is a text file with a list of commands that instruct an operating system to perform certain tasks. A shell is an interface that interprets, processes, and executes these commands from the shell script. It can be particularly helpful to automate repetitive tasks, helping to save time and reduce human error. 

### Types of Shells:

    Bash (Bourne Again Shell)
    Zsh (Z Shell)
    Ksh (Korn Shell)
    Tcsh (Tenex C Shell)

>> A shell script is a text file containing a series of commands that the shell can execute. It typically has a .sh extension.

### Creating and Running a Simple Shell Script:
1. Create a new file: Use a text editor like nano, vi, or gedit to create a new file. Name it example.sh.
2. Add the shebang line: The first line of the script should be #!/bin/bash to specify that the script should be run with Bash.
3. Add commands: Write some simple commands. For example:
```
#!/bin/bash
echo "Hello, World!"
```
4. Save the file and exit the editor.
5. Make the script executable: Change the file's permissions to make it executable.
```
chmod +x example.sh
```
6. Run the script: Execute the script by typing:
```
./example.sh
```
## Basic shell scripting commands

### Navigating the Filesystem
1. pwd (Print Working Directory)
2. ls (List)
```
    ls: Basic listing
    ls -l: Long listing format (shows file permissions, ownership, size, and modification date)
    ls -a: Lists all files, including hidden files (those starting with a dot)
    ls -lh: Long listing with human-readable file sizes
```
3. cd (Change Directory)
```
    cd /path/to/directory: Change to a specific directory
    cd ..: Move up one directory level
    cd ~: Move to the home directory
    cd -: Switch to the previous directory
```
4. mkdir (Make Directory)
```
mkdir new_directory
```
5. rmdir (Remove Directory):
remove an empty directory
```
rmdir dirname
```

6. touch: create an empty file with touch command
```
touch filename.extension
```
7. cp (copyfile/dir)
8. mv (move file/dir)
9. rm (remove):
```
rm file: Remove a file
rm -r directory: Remove a directory and its contents recursively
rm -i file: Prompt before each removal (interactive mode)
rm -f file: Force removal without prompt (use with caution)
```
10. viewing file content
```
cat: Concatenate and display file contents
less: View file contents one page at a time, with navigation options
head: View the first few lines of a file
tail: View the last few lines of a file
```
## shell scripting structure 
1. shebang(#!/bin/bash)
The shebang (#!) is used at the beginning of a script to specify the interpreter that should be used to execute the script. The most common shebang for Bash scripts is #!/bin/bash.
```
#!/bin/bash
echo "hii"
```
2. comments: used to add explanation and notes in the script 
```
#!/bin/bash
echo hii
# this is comment
```
3. stores the data that can be referenced and manipulated within the script 

```
#!/bin/bash
# Assign a value to a variable
greeting="Hello, World!"
# Use the variable
echo $greeting
```
- important points
    No spaces around the = sign when assigning a value.
    Use $ before the variable name to reference its value.

- Variable Operations:

    Environment Variables: Access environment variables using $VARIABLE_NAME.
    Local Variables: Defined within the script and accessible only in that script.
    Command Substitution: Assign the output of a command to a variable using backticks `command` or $(command).
```
#!/bin/bash
# Command substitution
current_date=$(date)
echo "Today's date is: $current_date"
```

4. Quoting
Quoting is used to handle strings and special characters. There are three types of quoting: single quotes, double quotes, and backticks.

```
#!/bin/bash
name='John Doe'
echo 'Hello, $name' # Outputs: Hello, $name
```

