---
title: git git branch commands
date: 2024-12-20
---


Here are some common `git` branch commands, along with explanations of how to use them:

### Basic Git Branch Commands

1. **List Branches**  
    To list all branches (both local and remote):
    
    ```bash
    git branch
    ```
    
    To list all branches, including remote ones:
    
    ```bash
    git branch -a
    ```
    
2. **Create a New Branch**  
    To create a new branch:
    
    ```bash
    git branch <branch-name>
    ```
    
    Example:
    
    ```bash
    git branch feature/login
    ```
    
3. **Switch to a Different Branch**  
    To switch to an existing branch:
    
    ```bash
    git checkout <branch-name>
    ```
    
    Example:
    
    ```bash
    git checkout feature/login
    ```
    
    **Note**: In newer versions of Git, you can use the `git switch` command:
    
    ```bash
    git switch <branch-name>
    ```
    
4. **Create and Switch to a New Branch**  
    To create a new branch and immediately switch to it:
    
    ```bash
    git checkout -b <branch-name>
    ```
    
    Or, using the newer command:
    
    ```bash
    git switch -c <branch-name>
    ```
    
5. **Rename a Branch**  
    To rename the current branch:
    
    ```bash
    git branch -m <new-branch-name>
    ```
    
    To rename a branch that you're not currently on:
    
    ```bash
    git branch -m <old-branch-name> <new-branch-name>
    ```
    
6. **Delete a Branch**  
    To delete a local branch:
    
    ```bash
    git branch -d <branch-name>
    ```
    
    If the branch hasn't been merged, you may need to use `-D` (force delete):
    
    ```bash
    git branch -D <branch-name>
    ```
    
7. **Show Branch Details**  
    To show details of the current branch:
    
    ```bash
    git status
    ```
    
8. **Merge a Branch into the Current Branch**  
    To merge another branch into your current branch:
    
    ```bash
    git merge <branch-name>
    ```
    
    Example:
    
    ```bash
    git merge feature/login
    ```
    
9. **List Remote Branches**  
    To list all remote branches:
    
    ```bash
    git branch -r
    ```
    
10. **Delete a Remote Branch**  
    To delete a remote branch:
    
    ```bash
    git push origin --delete <branch-name>
    ```
    
11. **Push a Branch to Remote**  
    To push a local branch to a remote repository:
    
    ```bash
    git push origin <branch-name>
    ```
    
12. **Fetch and Update Remote Branches**  
    To fetch all remote branches:
    
    ```bash
    git fetch --all
    ```
    
13. **Track a Remote Branch**  
    To track a remote branch when you check out a new branch:
    
    ```bash
    git checkout --track origin/<branch-name>
    ```
    
    Or using the newer `switch`:
    
    ```bash
    git switch --track origin/<branch-name>
    ```
    

### Useful Tips

- **Check Which Branch You Are On:** To check the current branch you're on:
    
    ```bash
    git branch
    ```
    
    The current branch will have an asterisk (*) next to its name.
    
- **Create a Branch from Another Branch**  
    To create a new branch from a specific branch:
    
    ```bash
    git checkout -b <new-branch-name> <existing-branch-name>
    ```
    
- **Switch Back to Previous Branch**  
    To switch back to the branch you were on previously:
    
    ```bash
    git checkout -
    ```
    

These commands will help you navigate, manage, and organize your branches within Git.