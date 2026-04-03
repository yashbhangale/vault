---
title: nanite config todo
tags: [projects, nanite]
---


create image: GRUB_BACKGROUND="/usr/share/backgrounds/nanite-grub.png"



background=/usr/share/backgrounds/nanite-login.jpg


plymouth theme 

calamares images


wallpaper :
value="/usr/share/backgrounds/nanite-default.jpg"/>


```bash
# Boot splash (1024x768 or 1920x1080)
config/includes.chroot/usr/share/backgrounds/nanite-grub.png

# Login background (1920x1080 recommended)
config/includes.chroot/usr/share/backgrounds/nanite-login.jpg

# Desktop wallpaper (1920x1080 or higher)
config/includes.chroot/usr/share/backgrounds/nanite-default.jpg

# Logo files
config/includes.chroot/usr/share/pixmaps/nanite-logo.png (48x48)
config/includes.chroot/usr/share/pixmaps/nanite-icon.png (32x32)

# Calamares branding images
config/includes.chroot/etc/calamares/branding/nanite/nanite-logo.png
config/includes.chroot/etc/calamares/branding/nanite/nanite-icon.png
config/includes.chroot/etc/calamares/branding/nanite/nanite-welcome.png
```

