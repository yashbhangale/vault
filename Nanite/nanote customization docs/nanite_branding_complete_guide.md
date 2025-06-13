# Nanite Linux: Complete Branding and Customization Guide

This comprehensive guide provides detailed instructions for customizing and branding Nanite Linux, a specialized Debian-based distribution for AI engineers and Vibe Coders. It covers all aspects of branding, from OS customization to Calamares installer theming.

## Table of Contents

1. [Introduction](#introduction)
2. [Branding Requirements](#branding-requirements)
3. [Live-build Branding Workflows](#live-build-branding-workflows)
4. [Calamares Installer Customization](#calamares-installer-customization)
5. [Branding Assets](#branding-assets)
6. [Integration Guide](#integration-guide)
7. [Testing and Validation](#testing-and-validation)
8. [Additional Resources](#additional-resources)

## Introduction

Nanite Linux is a specialized distribution designed for AI engineers and Vibe Coders, integrating various AI models, agents, and applications directly into the operating system. This guide provides a complete walkthrough for customizing and branding Nanite Linux to create a professional, cohesive user experience.

The branding process involves several key components:
- Visual identity (logos, colors, wallpapers)
- Boot experience (GRUB, Plymouth)
- Desktop environment
- Installer experience (Calamares)

By following this guide, you'll be able to create a fully branded Nanite Linux distribution with a consistent look and feel across all components.

## Branding Requirements

Before starting the customization process, it's important to understand the branding requirements for Nanite Linux:

- **Base Distribution**: Debian
- **Build System**: Live-build
- **Installer**: Calamares
- **Primary Colors**: Teal blue (#4DB6AC) and dark gray (#1a1a1a)
- **Target Audience**: AI engineers and Vibe Coders
- **Key Features**: Integrated AI models, agents, and applications
- **Deliverables**: ISO format and VM images (VMware/VirtualBox)

The branding should reflect the technical, cutting-edge nature of AI development while maintaining a clean, professional appearance. The visual identity should incorporate neural network and circuit-like patterns to symbolize the AI focus.

## Live-build Branding Workflows

Live-build is the primary tool for creating Nanite Linux. It provides a flexible framework for customizing Debian-based distributions.

### Setting Up Live-build

First, install the necessary packages:

```bash
sudo apt update
sudo apt install live-build live-config live-boot
```

Create a new live-build configuration directory:

```bash
mkdir -p nanite-live
cd nanite-live
lb config --distribution bullseye --archive-areas "main contrib non-free" --binary-images iso-hybrid
```

### Directory Structure

Live-build uses a specific directory structure for customization:

```
nanite-live/
├── auto/
│   └── config
├── config/
│   ├── hooks/
│   │   ├── live/
│   │   └── normal/
│   ├── includes.chroot/
│   │   └── usr/
│   │       ├── share/
│   │       └── local/
│   ├── includes.binary/
│   ├── package-lists/
│   └── archives/
└── build/
```

### Customization Hooks

Hooks are scripts that run at different stages of the build process. They are essential for customizing the live system.

Create a hook for installing branding packages:

```bash
mkdir -p config/hooks/live
cat > config/hooks/live/0010-install-branding-packages.hook.chroot << 'EOF'
#!/bin/sh
set -e

# Install required packages
apt-get update
apt-get install -y --no-install-recommends \
  plymouth \
  plymouth-themes \
  lightdm \
  lightdm-gtk-greeter \
  grub-common \
  grub-pc \
  imagemagick

# Exit successfully
exit 0
EOF

chmod +x config/hooks/live/0010-install-branding-packages.hook.chroot
```

### Package Lists

Create package lists to include necessary software:

```bash
mkdir -p config/package-lists
cat > config/package-lists/desktop.list.chroot << EOF
xfce4
xfce4-terminal
xfce4-goodies
lightdm
lightdm-gtk-greeter
plymouth
plymouth-themes
grub2-common
calamares
calamares-settings-debian
EOF
```

### Custom Configuration Files

You can include custom configuration files in the live system:

```bash
mkdir -p config/includes.chroot/etc/skel/.config
```

This directory structure allows you to place files that will be included in the live system and the installed system.

## Calamares Installer Customization

Calamares is a distribution-independent system installer used by many Linux distributions. It provides a modular architecture that allows for extensive customization of both appearance and functionality.

### Directory Structure

The standard directory structure for Calamares customization:

```
/etc/calamares/
├── branding/
│   └── nanite/               # Your custom branding directory
│       ├── branding.desc     # Branding configuration
│       ├── logo.png          # Distribution logo
│       ├── show.qml          # Slideshow QML file
│       ├── slide1.png        # Slideshow images
│       └── stylesheet.qss    # Optional CSS styling
├── modules/                  # Module configurations
│   ├── bootloader.conf
│   ├── displaymanager.conf
│   ├── packages.conf
│   └── ...
└── settings.conf            # Main configuration file
```

### Branding Configuration

The `branding.desc` file is the core of your customization. It defines product information, window behavior, colors, and slideshow settings.

Example `branding.desc`:

```yaml
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
    donateUrl:           "https://nanite.ai/donate/"

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
    sidebarBackground:    "#1a1a1a"
    sidebarText:          "#FFFFFF"
    sidebarTextHighlight: "#4DB6AC"
    sidebarSelect:        "#4DB6AC"
```

### QML Slideshow

The slideshow is displayed during the installation process. It can be created using QML:

```qml
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
```

### Module Configuration

Calamares uses modules to perform specific installation tasks. Each module has its own configuration file.

Example `settings.conf`:

```yaml
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
```

## Branding Assets

The following branding assets have been created for Nanite Linux:

### Logos

- **Main Logo**: A minimalist logo featuring a stylized "N" with circuit-like patterns in teal blue (#4DB6AC)
- **Plymouth Logo**: A simplified version of the main logo for the boot splash

### Wallpapers

- **Desktop Wallpaper**: A modern, abstract wallpaper with neural network patterns and circuit-like designs
- **Login Background**: A blurred version of the desktop wallpaper optimized for the login screen

### Plymouth Boot Splash

- **Background**: A black background with subtle circuit patterns in the corners
- **Logo**: The simplified Nanite logo for the boot splash

### Calamares Slideshow

- **Slide Images**: Professional images showing the Nanite desktop environment with AI tools

## Integration Guide

This section provides detailed commands and code for integrating the branding assets into both the OS and installer.

### Logo Integration

```bash
# Create directories for the logo
mkdir -p config/includes.chroot/usr/share/nanite/branding
mkdir -p config/includes.chroot/usr/share/pixmaps
mkdir -p config/includes.chroot/usr/share/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128,256x256}/apps

# Copy the logo
cp nanite_project/branding_assets/logos/nanite-logo.png config/includes.chroot/usr/share/nanite/branding/

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

### Wallpaper Integration

```bash
# Create directories for wallpapers
mkdir -p config/includes.chroot/usr/share/nanite/backgrounds

# Copy the wallpapers
cp nanite_project/branding_assets/wallpapers/default.png config/includes.chroot/usr/share/nanite/backgrounds/
cp nanite_project/branding_assets/wallpapers/login-background.png config/includes.chroot/usr/share/nanite/backgrounds/

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

```bash
# Create directories for Plymouth theme
mkdir -p config/includes.chroot/usr/share/plymouth/themes/nanite

# Copy the Plymouth assets
cp nanite_project/branding_assets/plymouth/background.png config/includes.chroot/usr/share/plymouth/themes/nanite/
cp nanite_project/branding_assets/plymouth/logo.png config/includes.chroot/usr/share/plymouth/themes/nanite/

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

### Calamares Installer Integration

```bash
# Create directories for Calamares branding
mkdir -p config/includes.chroot/etc/calamares/branding/nanite

# Copy the branding assets
cp nanite_project/branding_assets/logos/nanite-logo.png config/includes.chroot/etc/calamares/branding/nanite/logo.png
cp nanite_project/branding_assets/calamares/slide1.png config/includes.chroot/etc/calamares/branding/nanite/slide1.png

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
EOF

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
EOF
```

## Testing and Validation

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

## Additional Resources

- [Live-build Manual](https://live-team.pages.debian.net/live-manual/html/live-manual/index.en.html)
- [Calamares Documentation](https://github.com/calamares/calamares/wiki)
- [Plymouth Theming Guide](https://www.freedesktop.org/wiki/Software/Plymouth/Documentation/)
- [GRUB Theming Guide](https://www.gnu.org/software/grub/manual/grub/html_node/Theme-file-format.html)

---

By following this comprehensive guide, you can create a fully branded Nanite Linux distribution with a consistent visual identity across all components, from boot to desktop to installer.
