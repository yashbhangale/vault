# Nanite Branding Assets Integration Guide

This guide provides detailed commands and code for integrating the created branding assets into both the Nanite Linux distribution (via Live-build) and the Calamares installer. It references the specific assets created in the `nanite_project/branding_assets/` directory.

## Table of Contents

1. [Overview of Available Assets](#overview-of-available-assets)
2. [OS Branding Integration](#os-branding-integration)
   - [Logo Integration](#logo-integration)
   - [Wallpaper Integration](#wallpaper-integration)
   - [Plymouth Boot Splash Integration](#plymouth-boot-splash-integration)
   - [LightDM Login Screen Integration](#lightdm-login-screen-integration)
   - [GRUB Bootloader Integration](#grub-bootloader-integration)
3. [Calamares Installer Integration](#calamares-installer-integration)
   - [Branding Directory Setup](#branding-directory-setup)
   - [Branding Configuration](#branding-configuration)
   - [Slideshow Integration](#slideshow-integration)
   - [Stylesheet Integration](#stylesheet-integration)
4. [Testing and Verification](#testing-and-verification)

## Overview of Available Assets

The following branding assets have been created and are available in the `nanite_project/branding_assets/` directory:

- **Logos**:
  - `logos/nanite-logo.png` - Main logo with circuit-like patterns in teal blue

- **Wallpapers**:
  - `wallpapers/default.png` - Desktop wallpaper with neural network patterns
  - `wallpapers/login-background.png` - Login screen background with blurred patterns

- **Plymouth Boot Splash**:
  - `plymouth/background.png` - Black background with subtle circuit patterns
  - `plymouth/logo.png` - Simplified Nanite logo for boot splash

- **Calamares Installer**:
  - `calamares/slide1.png` - First slideshow image showing desktop environment

## OS Branding Integration

### Logo Integration

To integrate the Nanite logo into the system:

1. Create the necessary directories:

```bash
# Create directories for the logo
mkdir -p config/includes.chroot/usr/share/nanite/branding
mkdir -p config/includes.chroot/usr/share/pixmaps
mkdir -p config/includes.chroot/usr/share/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128,256x256}/apps
```

2. Copy and resize the logo for different purposes:

```bash
# Create a hook script to process the logo
cat > config/hooks/live/0020-process-logo.hook.chroot << 'EOF'
#!/bin/bash
set -e

# Source logo
SRC_LOGO="/usr/share/nanite/branding/nanite-logo.png"

# Create resized versions
if [ -f "$SRC_LOGO" ] && command -v convert >/dev/null 2>&1; then
    echo "Creating resized logo versions..."
    
    # Create pixmap version
    convert "$SRC_LOGO" -resize 128x128 /usr/share/pixmaps/nanite-logo.png
    
    # Create icon versions
    convert "$SRC_LOGO" -resize 16x16 /usr/share/icons/hicolor/16x16/apps/nanite.png
    convert "$SRC_LOGO" -resize 22x22 /usr/share/icons/hicolor/22x22/apps/nanite.png
    convert "$SRC_LOGO" -resize 24x24 /usr/share/icons/hicolor/24x24/apps/nanite.png
    convert "$SRC_LOGO" -resize 32x32 /usr/share/icons/hicolor/32x32/apps/nanite.png
    convert "$SRC_LOGO" -resize 48x48 /usr/share/icons/hicolor/48x48/apps/nanite.png
    convert "$SRC_LOGO" -resize 64x64 /usr/share/icons/hicolor/64x64/apps/nanite.png
    convert "$SRC_LOGO" -resize 128x128 /usr/share/icons/hicolor/128x128/apps/nanite.png
    convert "$SRC_LOGO" -resize 256x256 /usr/share/icons/hicolor/256x256/apps/nanite.png
    
    # Update icon cache
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor
fi

exit 0
EOF

# Make the hook executable
chmod +x config/hooks/live/0020-process-logo.hook.chroot
```

3. Copy the logo to the chroot environment:

```bash
# Copy the logo to the chroot environment
cp nanite_project/branding_assets/logos/nanite-logo.png config/includes.chroot/usr/share/nanite/branding/
```

4. Create a desktop entry for the About dialog:

```bash
# Create About dialog desktop entry
mkdir -p config/includes.chroot/usr/share/applications
cat > config/includes.chroot/usr/share/applications/nanite-about.desktop << EOF
[Desktop Entry]
Name=About Nanite
Comment=Information about Nanite AI Linux
Exec=nanite-about
Icon=nanite
Terminal=false
Type=Application
Categories=System;
EOF

# Create the about script
mkdir -p config/includes.chroot/usr/local/bin
cat > config/includes.chroot/usr/local/bin/nanite-about << 'EOF'
#!/bin/bash

# Use zenity to display about dialog
zenity --info \
  --title="About Nanite AI Linux" \
  --width=400 \
  --height=300 \
  --text="<span size='large'><b>Nanite AI Linux</b></span>\n\nVersion 1.0\n\nNanite is a specialized Linux distribution for AI engineers and Vibe Coders. It integrates various AI models, agents, and applications directly into the operating system.\n\n<b>Website:</b> https://nanite.ai\n<b>Support:</b> https://nanite.ai/support\n\n© 2025 Nanite Project" \
  --icon-name="nanite"
EOF

# Make the script executable
chmod +x config/includes.chroot/usr/local/bin/nanite-about
```

### Wallpaper Integration

To integrate the Nanite wallpapers:

1. Create the necessary directories:

```bash
# Create directories for wallpapers
mkdir -p config/includes.chroot/usr/share/nanite/backgrounds
```

2. Copy the wallpapers:

```bash
# Copy the wallpapers
cp nanite_project/branding_assets/wallpapers/default.png config/includes.chroot/usr/share/nanite/backgrounds/
cp nanite_project/branding_assets/wallpapers/login-background.png config/includes.chroot/usr/share/nanite/backgrounds/
```

3. Set the default wallpaper for XFCE:

```bash
# Create a hook to set the default wallpaper
cat > config/hooks/live/0030-set-wallpaper.hook.chroot << 'EOF'
#!/bin/sh
set -e

# Set default wallpaper for all users
echo "Setting default wallpaper..."
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml << INNEREOF
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <property name="workspace0" type="empty">
          <property name="color-style" type="int" value="0"/>
          <property name="image-style" type="int" value="5"/>
          <property name="last-image" type="string" value="/usr/share/nanite/backgrounds/default.png"/>
        </property>
      </property>
    </property>
  </property>
</channel>
INNEREOF

# Exit successfully
exit 0
EOF

# Make the hook executable
chmod +x config/hooks/live/0030-set-wallpaper.hook.chroot
```

### Plymouth Boot Splash Integration

To integrate the Plymouth boot splash:

1. Create the necessary directories:

```bash
# Create directories for Plymouth theme
mkdir -p config/includes.chroot/usr/share/plymouth/themes/nanite
```

2. Copy the Plymouth assets:

```bash
# Copy the Plymouth assets
cp nanite_project/branding_assets/plymouth/background.png config/includes.chroot/usr/share/plymouth/themes/nanite/
cp nanite_project/branding_assets/plymouth/logo.png config/includes.chroot/usr/share/plymouth/themes/nanite/
```

3. Create the Plymouth theme files:

```bash
# Create the Plymouth theme configuration
cat > config/includes.chroot/usr/share/plymouth/themes/nanite/nanite.plymouth << EOF
[Plymouth Theme]
Name=Nanite
Description=Nanite AI Linux boot splash
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/nanite
ScriptFile=/usr/share/plymouth/themes/nanite/nanite.script
EOF

# Create the Plymouth script
cat > config/includes.chroot/usr/share/plymouth/themes/nanite/nanite.script << 'EOF'
# Nanite Plymouth Script

# Screen size
screen_width = Window.GetWidth();
screen_height = Window.GetHeight();

# Background image
bg_image = Image("background.png");
bg_sprite = Sprite(bg_image);
bg_sprite.SetZ(-100);

# Scale background to fit screen
bg_image_width = bg_image.GetWidth();
bg_image_height = bg_image.GetHeight();
bg_scale_x = screen_width / bg_image_width;
bg_scale_y = screen_height / bg_image_height;
bg_sprite.SetScale(bg_scale_x, bg_scale_y);

# Logo image
logo_image = Image("logo.png");
logo_sprite = Sprite(logo_image);
logo_sprite.SetX(screen_width / 2 - logo_image.GetWidth() / 2);
logo_sprite.SetY(screen_height / 2 - logo_image.GetHeight() / 2);

# Progress bar
progress_bar_height = 3;
progress_bar_width = screen_width * 0.3;
progress_bar_x = screen_width / 2 - progress_bar_width / 2;
progress_bar_y = screen_height * 0.6;

progress_bar_bg = Rectangle(progress_bar_width, progress_bar_height);
progress_bar_bg.SetX(progress_bar_x);
progress_bar_bg.SetY(progress_bar_y);
progress_bar_bg.SetColor(0.2, 0.2, 0.2, 0.8);

progress_bar = Rectangle(0, progress_bar_height);
progress_bar.SetX(progress_bar_x);
progress_bar.SetY(progress_bar_y);
progress_bar.SetColor(0.4, 0.8, 1.0, 1.0);

# Message
message_sprite = Sprite();
message_sprite.SetX(screen_width / 2);
message_sprite.SetY(screen_height * 0.7);

fun refresh_callback() {
    progress = Plymouth.GetBootProgress();
    progress_bar.SetWidth(progress_bar_width * progress);
}

Plymouth.SetRefreshFunction(refresh_callback);

# Message callback
fun message_callback(text) {
    message_image = Image.Text(text, 1, 1, 1);
    message_sprite.SetImage(message_image);
    message_sprite.SetX(screen_width / 2 - message_image.GetWidth() / 2);
}

Plymouth.SetMessageFunction(message_callback);
EOF
```

4. Create a hook to set the Plymouth theme:

```bash
# Create a hook to set the Plymouth theme
cat > config/hooks/live/0040-set-plymouth-theme.hook.chroot << 'EOF'
#!/bin/sh
set -e

# Set Plymouth theme
echo "Setting Plymouth theme..."
plymouth-set-default-theme nanite
update-initramfs -u

# Exit successfully
exit 0
EOF

# Make the hook executable
chmod +x config/hooks/live/0040-set-plymouth-theme.hook.chroot
```

### LightDM Login Screen Integration

To integrate the login screen customization:

1. Create the necessary directories:

```bash
# Create directories for LightDM configuration
mkdir -p config/includes.chroot/etc/lightdm
```

2. Configure LightDM:

```bash
# Create LightDM configuration
cat > config/includes.chroot/etc/lightdm/lightdm.conf << EOF
[Seat:*]
greeter-session=lightdm-gtk-greeter
user-session=xfce
EOF

# Create LightDM GTK Greeter configuration
cat > config/includes.chroot/etc/lightdm/lightdm-gtk-greeter.conf << EOF
[greeter]
background=/usr/share/nanite/backgrounds/login-background.png
theme-name=Arc-Dark
icon-theme-name=Papirus-Dark
font-name=Noto Sans 10
xft-antialias=true
xft-dpi=96
xft-hintstyle=hintslight
xft-rgba=rgb
indicators=~host;~spacer;~clock;~spacer;~session;~power
clock-format=%a %d %b, %H:%M
logo=/usr/share/nanite/branding/nanite-logo.png
EOF
```

### GRUB Bootloader Integration

To integrate GRUB bootloader customization:

1. Create the necessary directories:

```bash
# Create directories for GRUB theme
mkdir -p config/includes.chroot/boot/grub/themes/nanite
```

2. Copy the GRUB background (using the Plymouth background):

```bash
# Copy the GRUB background
cp nanite_project/branding_assets/plymouth/background.png config/includes.chroot/boot/grub/themes/nanite/background.png
```

3. Create the GRUB theme:

```bash
# Create the GRUB theme
cat > config/includes.chroot/boot/grub/themes/nanite/theme.txt << EOF
# Nanite GRUB theme

# Global properties
title-text: "Nanite AI Linux"
title-color: "#4DB6AC"
title-font: "DejaVu Sans Regular 18"
desktop-image: "background.png"
desktop-color: "#000000"
terminal-box: "terminal_*.png"
terminal-font: "DejaVu Sans Mono Regular 12"

# Boot menu
+ boot_menu {
    left = 15%
    width = 70%
    top = 30%
    height = 40%
    item_font = "DejaVu Sans Regular 12"
    item_color = "#cccccc"
    selected_item_color = "#4DB6AC"
    selected_item_font = "DejaVu Sans Bold 12"
    icon_width = 32
    icon_height = 32
    item_height = 36
    item_padding = 5
    item_spacing = 10
}

# Progress bar
+ progress_bar {
    id = "__timeout__"
    left = 15%
    width = 70%
    top = 75%
    height = 16
    show_text = true
    text_color = "#ffffff"
    font = "DejaVu Sans Regular 12"
}
EOF

# Create a simple terminal box image for GRUB
mkdir -p config/includes.chroot/boot/grub/themes/nanite/terminal_box
```

4. Configure GRUB to use the theme:

```bash
# Create GRUB configuration
cat > config/includes.chroot/etc/default/grub.d/nanite-theme.cfg << EOF
# Nanite GRUB theme configuration
GRUB_THEME="/boot/grub/themes/nanite/theme.txt"
GRUB_BACKGROUND="/boot/grub/themes/nanite/background.png"
GRUB_DISTRIBUTOR="Nanite"
GRUB_TIMEOUT=5
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
EOF

# Create a hook to update GRUB
cat > config/hooks/live/0050-update-grub.hook.chroot << 'EOF'
#!/bin/sh
set -e

# Update GRUB
echo "Updating GRUB configuration..."
update-grub

# Exit successfully
exit 0
EOF

# Make the hook executable
chmod +x config/hooks/live/0050-update-grub.hook.chroot
```

## Calamares Installer Integration

### Branding Directory Setup

1. Create the necessary directories:

```bash
# Create directories for Calamares branding
mkdir -p config/includes.chroot/etc/calamares/branding/nanite
```

2. Copy the branding assets:

```bash
# Copy the logo
cp nanite_project/branding_assets/logos/nanite-logo.png config/includes.chroot/etc/calamares/branding/nanite/logo.png

# Copy the slideshow images
cp nanite_project/branding_assets/calamares/slide1.png config/includes.chroot/etc/calamares/branding/nanite/slide1.png
```

### Branding Configuration

Create the Calamares branding configuration:

```bash
# Create the branding.desc file
cat > config/includes.chroot/etc/calamares/branding/nanite/branding.desc << EOF
# Nanite branding information
---
componentName: nanite

# Welcome screen configuration
welcomeStyleCalamares: false
welcomeExpandingLogo: true

# Window behavior and size
windowExpanding: normal
windowSize: 800px,520px
windowPlacement: center

# Navigation and sidebar
sidebar: widget
navigation: widget

# Product information strings
strings:
    productName:         "Nanite AI Linux"
    shortProductName:    "Nanite"
    version:             "1.0"
    shortVersion:        "1.0"
    versionedName:       "Nanite AI Linux 1.0"
    shortVersionedName:  "Nanite 1.0"
    bootloaderEntryName: "Nanite"
    productUrl:          "https://nanite.ai/"
    supportUrl:          "https://nanite.ai/support/"
    knownIssuesUrl:      "https://nanite.ai/issues/"
    releaseNotesUrl:     "https://nanite.ai/releases/"

# Branding images
images:
    productIcon:         "logo.png"
    productLogo:         "logo.png"
    productWelcome:      "logo.png"

# Slideshow configuration
slideshow:               "show.qml"
slideshowAPI:            2

# Colors for text and background components
style:
    # Sidebar colors
    sidebarBackground:    "#1a1a1a"
    sidebarText:          "#FFFFFF"
    sidebarTextHighlight: "#4DB6AC"
    sidebarSelect:        "#4DB6AC"
    
    # Button colors
    buttonBackground:     "#4DB6AC"
    buttonText:           "#FFFFFF"
    buttonHighlightedBackground: "#80CBC4"
    buttonHighlightedText: "#FFFFFF"
    
    # Text field colors
    textFieldBackground:  "#2A2A2A"
    textFieldText:        "#FFFFFF"
EOF
```

### Slideshow Integration

Create the QML slideshow for Calamares:

```bash
# Create the QML slideshow
cat > config/includes.chroot/etc/calamares/branding/nanite/show.qml << 'EOF'
/* Nanite Installer Slideshow */
import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation

    // Property to track if the slideshow is active
    property bool activatedInCalamares: false

    // Timer to advance slides automatically
    Timer {
        id: advanceTimer
        interval: 20000  // 20 seconds per slide
        running: false
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    // First slide
    Slide {
        Image {
            id: background1
            source: "slide1.png"
            width: 810
            height: 485
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }
        
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 50
            font.pixelSize: 22
            color: "#ffffff"
            text: "Welcome to Nanite AI Linux"
            wrapMode: Text.WordWrap
            width: parent.width
            horizontalAlignment: Text.Center
        }
    }

    // Functions called by Calamares
    function onActivate() {
        presentation.activatedInCalamares = true;
        advanceTimer.running = true;
    }
    
    function onLeave() {
        presentation.activatedInCalamares = false;
        advanceTimer.running = false;
    }

    // Start the slideshow if not started by Calamares
    Component.onCompleted: {
        if (!presentation.activatedInCalamares) {
            advanceTimer.running = true;
        }
    }
}
EOF
```

### Stylesheet Integration

Create a CSS stylesheet for Calamares:

```bash
# Create the stylesheet
cat > config/includes.chroot/etc/calamares/branding/nanite/stylesheet.qss << 'EOF'
/* Nanite Calamares Stylesheet */

/* Main application styling */
QWidget {
    font-family: "Noto Sans";
    font-size: 11pt;
}

#mainApp {
    background: #1a1a1a;
    color: #ffffff;
}

/* Button styling */
QPushButton {
    background-color: #4DB6AC;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #80CBC4;
}

QPushButton:pressed {
    background-color: #26A69A;
}

/* Progress bar styling */
QProgressBar {
    border: none;
    background-color: #2a2a2a;
    height: 8px;
    border-radius: 4px;
}

QProgressBar::chunk {
    background-color: #4DB6AC;
    border-radius: 4px;
}

/* Text field styling */
QLineEdit, QTextEdit {
    background-color: #2a2a2a;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 6px;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #4DB6AC;
}

/* Sidebar styling */
#sidebarApp {
    background-color: #1a1a1a;
    color: #ffffff;
}

#sidebarMenuApp QPushButton {
    background-color: transparent;
    color: #ffffff;
    text-align: left;
    border: none;
    border-radius: 0;
    padding: 10px;
}

#sidebarMenuApp QPushButton:hover {
    background-color: #2a2a2a;
}

#sidebarMenuApp QPushButton:checked {
    background-color: #4DB6AC;
    color: #ffffff;
}
EOF
```

### Calamares Main Configuration

Update the main Calamares configuration to use the Nanite branding:

```bash
# Create directories for Calamares configuration
mkdir -p config/includes.chroot/etc/calamares

# Create the main settings.conf file
cat > config/includes.chroot/etc/calamares/settings.conf << EOF
# Nanite Calamares Configuration
---
modules-search: [ local, /usr/lib/calamares/modules ]

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
    - bootloader-config
    - grubcfg
    - bootloader
    - packages
    - luksbootkeyfile
    - plymouthcfg
    - initramfscfg
    - initramfs
    - removeuser
    - umount

# Branding configuration
branding: nanite

# If this is set to true, the installer will show a prompt asking the user
# if they really want to quit right before quitting.
prompt-install: true

# If this is set to true, the installer will execute all target environment
# operations in the background, without blocking the UI.
dont-chroot: false
EOF
```

### Desktop Shortcut for Calamares

Create a desktop shortcut for the installer:

```bash
# Create the desktop shortcut
cat > config/includes.chroot/usr/share/applications/nanite-installer.desktop << EOF
[Desktop Entry]
Type=Application
Name=Install Nanite AI Linux
GenericName=System Installer
Comment=Install the system to your computer
Exec=sudo calamares
Icon=/etc/calamares/branding/nanite/logo.png
Terminal=false
StartupNotify=true
Categories=System;
Keywords=calamares;system;installer;
EOF
```

## Testing and Verification

To test the branding integration:

1. Build the ISO:

```bash
# Clean any previous build artifacts
sudo lb clean

# Build the ISO
sudo lb build
```

2. Test the ISO in a virtual machine:

```bash
# Test with QEMU
qemu-system-x86_64 -m 4096 -smp 2 -cdrom nanite-*.iso -boot d
```

3. Verify the branding elements:

- Check that the Plymouth boot splash appears correctly
- Verify that the GRUB menu is themed
- Confirm that the login screen uses the custom background
- Check that the desktop uses the default wallpaper
- Verify that the Calamares installer uses the Nanite branding

This guide provides detailed commands and code for integrating the created branding assets into both the Nanite Linux distribution and the Calamares installer. By following these steps, you can create a fully branded and customized Linux distribution with a consistent visual identity.
