
# this guide is followed while building distribution

# Nanite Distribution Branding Guide

  

This guide covers all the necessary changes to rebrand your live-build distribution from Debian to Nanite.

  

## Table of Contents

1. [Directory Structure Setup](#directory-structure-setup)

2. [System Information Files](#system-information-files)

3. [Boot Loader Branding](#boot-loader-branding)

4. [Desktop Environment Branding](#desktop-environment-branding)

5. [Login Screen Customization](#login-screen-customization)

6. [Plymouth Boot Splash](#plymouth-boot-splash)

7. [Calamares Installer Branding](#calamares-installer-branding)

8. [Application Menu Branding](#application-menu-branding)

9. [Wallpapers and Themes](#wallpapers-and-themes)

10. [Final Steps](#final-steps)

  

## Directory Structure Setup

  

First, create the necessary directory structure:

  

```bash

mkdir -p config/includes.chroot/etc

mkdir -p config/includes.chroot/usr/share/pixmaps

mkdir -p config/includes.chroot/usr/share/backgrounds

mkdir -p config/includes.chroot/usr/share/applications

mkdir -p config/includes.chroot/etc/lightdm

mkdir -p config/includes.chroot/etc/calamares

mkdir -p config/includes.binary/isolinux

mkdir -p config/bootloaders/isolinux

mkdir -p config/hooks/live

```

  

## System Information Files

  

### 1. OS Release Information

Create `config/includes.chroot/etc/os-release`:

```bash

PRETTY_NAME="Nanite Linux"

NAME="Nanite"

VERSION_ID="1.0"

VERSION="1.0 (Stable)"

ID=nanite

ID_LIKE=debian

HOME_URL="https://nanite-linux.org/"

SUPPORT_URL="https://nanite-linux.org/support"

BUG_REPORT_URL="https://nanite-linux.org/bugs"

```

  

### 2. LSB Release Information

Create `config/includes.chroot/etc/lsb-release`:

```bash

DISTRIB_ID=Nanite

DISTRIB_RELEASE=1.0

DISTRIB_CODENAME=stable

DISTRIB_DESCRIPTION="Nanite Linux 1.0"

```

  

### 3. Issue Files

Create `config/includes.chroot/etc/issue`:

```

Nanite Linux 1.0 \n \l

```

  

Create `config/includes.chroot/etc/issue.net`:

```

Nanite Linux 1.0

```

  

### 4. MOTD (Message of the Day)

Create `config/includes.chroot/etc/motd`:

```

Welcome to Nanite Linux!

  

For support and documentation, visit: https://nanite-linux.org

```

  

## Boot Loader Branding

  

### 1. ISOLINUX Configuration

Create `config/bootloaders/isolinux/isolinux.cfg`:

```

UI vesamenu.c32

MENU TITLE Nanite Linux Boot Menu

MENU BACKGROUND splash.png

MENU COLOR border 30;44 #40ffffff #a0000000 std

MENU COLOR title 1;36;44 #9033ccff #a0000000 std

MENU COLOR sel 7;37;40 #e0ffffff #20ffffff all

MENU COLOR unsel 37;44 #50ffffff #a0000000 std

MENU COLOR help 37;40 #c0ffffff #a0000000 std

MENU COLOR timeout_msg 37;40 #80ffffff #00000000 std

MENU COLOR timeout 1;37;40 #c0ffffff #00000000 std

MENU COLOR msg07 37;40 #90ffffff #a0000000 std

MENU COLOR tabmsg 31;40 #30ffffff #00000000 std

  

LABEL live

MENU LABEL Nanite Linux (Live)

MENU DEFAULT

KERNEL /live/vmlinuz

APPEND initrd=/live/initrd.img boot=live components quiet splash

  

LABEL live-safe

MENU LABEL Nanite Linux (Safe Mode)

KERNEL /live/vmlinuz

APPEND initrd=/live/initrd.img boot=live components quiet splash nomodeset

  

TIMEOUT 30

```

  

### 2. GRUB Configuration

Create `config/includes.chroot/etc/default/grub.d/nanite.cfg`:

```bash

GRUB_DISTRIBUTOR="Nanite"

GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"

GRUB_BACKGROUND="/usr/share/backgrounds/nanite-grub.png"

```

  

## Desktop Environment Branding

  

### 1. Desktop Files

Create `config/includes.chroot/usr/share/applications/nanite-about.desktop`:

```ini

[Desktop Entry]

Version=1.0

Type=Application

Name=About Nanite

Comment=Information about Nanite Linux

Exec=zenity --info --title="About Nanite Linux" --text="Nanite Linux 1.0\nA modern, lightweight Linux distribution\n\nWebsite: https://nanite-linux.org"

Icon=nanite-logo

Terminal=false

Categories=System;

```

  

### 2. System Information Script

Create `config/includes.chroot/usr/bin/nanite-info`:

```bash

#!/bin/bash

echo "Nanite Linux System Information"

echo "================================"

echo "Distribution: Nanite Linux"

echo "Version: 1.0"

echo "Kernel: $(uname -r)"

echo "Architecture: $(uname -m)"

echo "Desktop: XFCE"

echo ""

echo "Website: https://nanite-linux.org"

```

  

Make it executable:

```bash

chmod +x config/includes.chroot/usr/bin/nanite-info

```

  

## Login Screen Customization

  

### 1. LightDM GTK Greeter Configuration

Create `config/includes.chroot/etc/lightdm/lightdm-gtk-greeter.conf`:

```ini

[greeter]

background=/usr/share/backgrounds/nanite-login.jpg

theme-name=Adwaita

icon-theme-name=Adwaita

font-name=Sans 11

xft-antialias=true

xft-dpi=96

xft-hintstyle=slight

xft-rgba=rgb

show-indicators=~host;~spacer;~clock;~spacer;~language;~session;~a11y;~power

show-clock=true

clock-format=%A, %B %d, %Y %H:%M

```

  

### 2. Custom Login Message

Create `config/includes.chroot/etc/lightdm/lightdm.conf.d/50-nanite.conf`:

```ini

[Seat:*]

greeter-show-manual-login=true

greeter-hide-users=false

allow-guest=false

```

  

## Plymouth Boot Splash

  

### 1. Plymouth Theme Configuration

Create `config/includes.chroot/etc/plymouth/plymouthd.conf`:

```ini

[Daemon]

Theme=nanite

ShowDelay=0

DeviceTimeout=5

```

  

### 2. Custom Plymouth Theme (Advanced)

Create directory structure:

```bash

mkdir -p config/includes.chroot/usr/share/plymouth/themes/nanite

```

  

Create `config/includes.chroot/usr/share/plymouth/themes/nanite/nanite.plymouth`:

```ini

[Plymouth Theme]

Name=Nanite

Description=Nanite Linux boot splash

ModuleName=script

  

[script]

ImageDir=/usr/share/plymouth/themes/nanite

ScriptFile=/usr/share/plymouth/themes/nanite/nanite.script

```

  

## Calamares Installer Branding

  

### 1. Calamares Branding Configuration

Create `config/includes.chroot/etc/calamares/branding/nanite/branding.desc`:

```yaml

componentName: nanite

  

strings:

productName: "Nanite Linux"

shortProductName: "Nanite"

version: "1.0"

shortVersion: "1.0"

versionedName: "Nanite Linux 1.0"

shortVersionedName: "Nanite 1.0"

bootloaderEntryName: "Nanite"

productUrl: "https://nanite-linux.org/"

supportUrl: "https://nanite-linux.org/support"

knownIssuesUrl: "https://nanite-linux.org/issues"

releaseNotesUrl: "https://nanite-linux.org/releases"

  

images:

productLogo: "nanite-logo.png"

productIcon: "nanite-icon.png"

productWelcome: "nanite-welcome.png"

  

style:

sidebarBackground: "#2c3e50"

sidebarText: "#ffffff"

sidebarTextSelect: "#4d7cf4"

```

  

### 2. Calamares Settings

Create `config/includes.chroot/etc/calamares/settings.conf`:

```yaml

modules-search: [ local, /usr/lib/x86_64-linux-gnu/calamares/modules ]

  

instances:

- id: nanite

module: packages

config: packages.conf

  

sequence:

- show:

- welcome

- locale

- keyboard

- partition

- users

- summary

- exec:

- partition

- mount

- unpackfs

- packages@nanite

- machineid

- fstab

- locale

- keyboard

- localecfg

- users

- displaymanager

- networkcfg

- hwclock

- services-systemd

- bootloader

- umount

- show:

- finished

  

branding: nanite

```

  

## Application Menu Branding

  

### 1. XFCE Panel Configuration

Create `config/hooks/live/0030-xfce-branding.hook.chroot`:

```bash

#!/bin/bash

  

# Create XFCE configuration for branding

mkdir -p /etc/skel/.config/xfce4/panel

mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml

  

# Set custom application menu

cat > /etc/skel/.config/xfce4/panel/whiskermenu-1.rc << 'EOF'

favorites=firefox-esr.desktop,thunar.desktop,xfce4-terminal.desktop,mousepad.desktop

button-title=Nanite Menu

button-icon=nanite-logo

show-button-title=true

EOF

```

  

Make it executable:

```bash

chmod +x config/hooks/live/0030-xfce-branding.hook.chroot

```

  

## Wallpapers and Themes

  

### 1. Default Wallpaper Setup

Create `config/hooks/live/0040-wallpaper.hook.chroot`:

```bash

#!/bin/bash

  

# Set default wallpaper for XFCE

mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml

  

cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml << 'EOF'

<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-desktop" version="1.0">

<property name="backdrop" type="empty">

<property name="screen0" type="empty">

<property name="monitor0" type="empty">

<property name="workspace0" type="empty">

<property name="last-image" type="string" value="/usr/share/backgrounds/nanite-default.jpg"/>

<property name="image-style" type="int" value="5"/>

</property>

</property>

</property>

</property>

</channel>

EOF

```

  

Make it executable:

```bash

chmod +x config/hooks/live/0040-wallpaper.hook.chroot

```

  

### 2. Required Image Files

You'll need to create/place these image files:

  

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

  

## Final Steps

  

### 1. Update Build Configuration

Add this to your `config/build` file:

```bash

LB_DISTRIBUTION="bookworm"

LB_DEBIAN_INSTALLER="live"

LB_BOOTAPPEND_LIVE="boot=live components quiet splash username=nanite hostname=nanite-live"

```

  

### 2. Create Post-Install Hook

Create `config/hooks/live/0050-final-branding.hook.chroot`:

```bash

#!/bin/bash

  

# Update hostname

echo "nanite-live" > /etc/hostname

  

# Update hosts file

sed -i 's/127.0.1.1.*/127.0.1.1\tnanite-live/' /etc/hosts

  

# Set live user

useradd -m -s /bin/bash -G sudo,audio,video,plugdev,netdev nanite 2>/dev/null || true

echo "nanite:nanite" | chpasswd

  

# Set default session

echo "exec startxfce4" > /home/nanite/.xsession

chown nanite:nanite /home/nanite/.xsession

```

  

Make it executable:

```bash

chmod +x config/hooks/live/0050-final-branding.hook.chroot

```

  

### 3. Build Commands

After implementing all changes, rebuild your distribution:

  

```bash

sudo lb clean

sudo lb config

sudo lb build

```

  

## Testing Your Branding

  

1. **Boot Test**: Check boot loader shows "Nanite Linux"

2. **Login Screen**: Verify custom background and branding

3. **Desktop**: Check wallpaper, menu, and applications

4. **System Info**: Run `nanite-info` to verify system information

5. **Installer**: Test Calamares shows Nanite branding

  

## Troubleshooting

  

- If images don't appear, check file permissions: `chmod 644 image-files`

- For hook script issues, check execution permissions: `chmod +x hook-files`

- Monitor build logs for any configuration errors

- Test in QEMU first before burning to physical media

  

---

  

**Note**: Replace placeholder URLs (nanite-linux.org) with your actual project URLs, and ensure all image files are created with appropriate dimensions and quality.