---
title: "Git configure password in linux"
date: 2024-06-05T12:24:01+05:30
draft: false

---
# clone the desired repo
(git clone repourl)
```
git clone https://github.com/yashbhangale/geeksdirhugo.git
```
# assign access token (password) to the remote repo 
```
sudo git remote set-url origin https://Accesstokenpastehere@github.com/yashbhangale/geeksdirhugo.git
```
then cd into repo 
# assign username and user email 
```
sudo git config --global user.email "yashbhangale9@gmail.com"
```
```
sudo git config --global user.name "yashbhangale"
```


# Impt -- git remote add origin ( if we create repo and code on local machine and we have to push code from local machine to that repo)

```
git remote add origin https://github.com/your-username/repo-name.git
```

# Switch to main branch 
```
git checkout -b main
```

