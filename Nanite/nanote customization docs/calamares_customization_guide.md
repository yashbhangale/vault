# Calamares Installer Customization Guide

This comprehensive guide provides detailed instructions for customizing the Calamares installer for your Nanite Linux distribution. It covers branding, theming, slideshow customization, and post-installation scripts.

## Table of Contents

1. [Introduction to Calamares](#introduction-to-calamares)
2. [Directory Structure](#directory-structure)
3. [Branding Configuration](#branding-configuration)
4. [Slideshow Customization](#slideshow-customization)
5. [Theme and Style Customization](#theme-and-style-customization)
6. [Module Configuration](#module-configuration)
7. [Post-Installation Scripts](#post-installation-scripts)
8. [Integration with Live-build](#integration-with-live-build)
9. [Testing and Debugging](#testing-and-debugging)

## Introduction to Calamares

Calamares is a distribution-independent system installer used by many Linux distributions. It provides a modular architecture that allows for extensive customization of both appearance and functionality.

Key components for customization:
- **Branding**: Controls the visual identity (logos, colors, product name)
- **Slideshow**: Displayed during installation
- **Modules**: Functional components that handle specific installation tasks
- **Configuration**: YAML files that control the behavior of modules

## Directory Structure

The standard directory structure for Calamares customization in a Debian-based distribution:

```
/etc/calamares/
├── branding/
│   └── nanite/               # Your custom branding directory
│       ├── branding.desc     # Branding configuration
│       ├── logo.png          # Distribution logo
│       ├── show.qml          # Slideshow QML file
│       ├── slide1.png        # Slideshow images
│       ├── slide2.png
│       ├── slide3.png
│       └── stylesheet.qss    # Optional CSS styling
├── modules/                  # Module configurations
│   ├── bootloader.conf
│   ├── displaymanager.conf
│   ├── packages.conf
│   └── ...
└── settings.conf            # Main configuration file
```

## Branding Configuration

The `branding.desc` file is the core of your customization. It defines product information, window behavior, colors, and slideshow settings.

### Creating the Branding Directory

```bash
# Create the branding directory structure
mkdir -p /etc/calamares/branding/nanite
```

### Basic branding.desc Template

Create `/etc/calamares/branding/nanite/branding.desc`:

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
    productWelcome:      "welcome.png"
    # productWallpaper:    "wallpaper.png"  # Optional

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

### Detailed Color Configuration

For more detailed color customization, add these to the `style` section:

```yaml
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
    
    # Error colors
    errorBackground:      "#F44336"
    errorText:            "#FFFFFF"
    
    # Warning colors
    warningBackground:    "#FFC107"
    warningText:          "#000000"
```

## Slideshow Customization

The slideshow is displayed during the installation process. It can be created using QML or as a sequence of images.

### Basic QML Slideshow

Create `/etc/calamares/branding/nanite/show.qml`:

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

    // Second slide
    Slide {
        Image {
            id: background2
            source: "slide2.png"
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
            text: "AI-Powered Computing Environment"
            wrapMode: Text.WordWrap
            width: parent.width
            horizontalAlignment: Text.Center
        }
    }

    // Third slide
    Slide {
        Image {
            id: background3
            source: "slide3.png"
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
            text: "Integrated AI Models and Tools"
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

### Advanced QML Slideshow with Animation

For a more dynamic slideshow, you can add animations:

```qml
/* Nanite Installer Slideshow with Animations */
import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation {
    id: presentation
    property bool activatedInCalamares: false

    Timer {
        id: advanceTimer
        interval: 20000
        running: false
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }

    // First slide with animation
    Slide {
        Image {
            id: background1
            source: "slide1.png"
            width: 810
            height: 485
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
            opacity: 0
            
            // Fade in animation
            NumberAnimation on opacity {
                from: 0; to: 1
                duration: 1000
                running: true
            }
        }
        
        Text {
            id: slideText1
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 50
            font.pixelSize: 22
            color: "#ffffff"
            text: "Welcome to Nanite AI Linux"
            wrapMode: Text.WordWrap
            width: parent.width
            horizontalAlignment: Text.Center
            opacity: 0
            
            // Slide in animation
            NumberAnimation on opacity {
                from: 0; to: 1
                duration: 1000
                running: true
                easing.type: Easing.InOutQuad
            }
        }
    }

    // Additional slides with similar animations...

    // Functions called by Calamares
    function onActivate() {
        presentation.activatedInCalamares = true;
        advanceTimer.running = true;
    }
    
    function onLeave() {
        presentation.activatedInCalamares = false;
        advanceTimer.running = false;
    }

    Component.onCompleted: {
        if (!presentation.activatedInCalamares) {
            advanceTimer.running = true;
        }
    }
}
```

### Image-Only Slideshow

If you prefer not to use QML, you can configure a simple image slideshow in `branding.desc`:

```yaml
# Image slideshow configuration
slideshow: [
    "slide1.png",
    "slide2.png",
    "slide3.png"
]
```

## Theme and Style Customization

### CSS Stylesheet

Create `/etc/calamares/branding/nanite/stylesheet.qss` for additional styling:

```css
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
```

## Module Configuration

Calamares uses modules to perform specific installation tasks. Each module has its own configuration file.

### Main Configuration File

Create or modify `/etc/calamares/settings.conf`:

```yaml
# Nanite Calamares Configuration
---
# Modules can be job modules (with no UI) and view modules.
# They can be placed in two different paths:
# - modules/       - loaded at startup
# - local/modules/ - loaded at runtime
modules-search: [ local, /usr/lib/calamares/modules ]

# Phase 1 - prepare. Run before anything else.
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
    - nanite-post-install  # Custom post-installation script
    - umount

# Branding configuration
branding: nanite

# If this is set to true, the installer will show a prompt asking the user
# if they really want to quit right before quitting.
prompt-install: true

# If this is set to true, the installer will execute all target environment
# operations in the background, without blocking the UI.
dont-chroot: false
```

### Custom Module Configurations

#### Users Module

Create or modify `/etc/calamares/modules/users.conf`:

```yaml
# Users module configuration for Nanite
---
# Default username and hostname
defaultUserName: nanite
defaultHostName: nanite

# Auto-login by default
doAutoLogin: true

# Require strong passwords
requireStrongPasswords: false

# Allow weak passwords
allowWeakPasswords: true

# Allow weak passwords with warning
allowWeakPasswordsDefault: true

# Default user groups
defaultGroups:
    - users
    - lp
    - video
    - network
    - storage
    - wheel
    - audio
    - cdrom
```

#### Packages Module

Create or modify `/etc/calamares/modules/packages.conf`:

```yaml
# Packages module configuration for Nanite
---
backend: apt

# Update the system database before installing packages
update_db: true

# Operations to perform before installing packages
operations:
  - remove:
      - calamares
      - live-boot*
      - live-config*
      - live-tools

  - install:
      - nanite-branding
      - nanite-welcome
```

## Post-Installation Scripts

Custom scripts can be executed after installation to perform additional setup.

### Creating a Custom Module

1. Create the module directory:

```bash
mkdir -p /etc/calamares/modules/nanite-post-install
```

2. Create the module descriptor:

Create `/etc/calamares/modules/nanite-post-install/module.desc`:

```yaml
# Module metadata
---
type: "job"
name: "nanite-post-install"
interface: "python"
script: "main.py"
```

3. Create the Python script:

Create `/etc/calamares/modules/nanite-post-install/main.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import libcalamares

def run():
    """
    Nanite post-installation script.
    
    This script performs additional setup tasks after the main installation.
    """
    # Get the root mount point
    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    
    # Log the start of our custom operations
    libcalamares.utils.debug("Nanite post-installation: starting custom operations")
    
    # Create a welcome message
    create_welcome_message(root_mount_point)
    
    # Configure AI services
    configure_ai_services(root_mount_point)
    
    # Set up desktop shortcuts
    setup_desktop_shortcuts(root_mount_point)
    
    # Return success
    return None

def create_welcome_message(root_mount_point):
    """Create a welcome message for the user."""
    try:
        welcome_path = os.path.join(root_mount_point, "etc/profile.d/nanite-welcome.sh")
        with open(welcome_path, "w") as welcome_file:
            welcome_file.write("""#!/bin/bash
echo ""
echo -e "\033[1;36m"
echo "  _   _             _ _        _    _   _     _                  "
echo " | \\ | | __ _ _ __ (_) |_ ___ | |  (_) | |   (_)_ __  _   ___  __"
echo " |  \\| |/ _\` | '_ \\| | __/ _ \\| |  | | | |   | | '_ \\| | | \\ \\/ /"
echo " | |\\  | (_| | | | | | ||  __/| |__| | | |___| | | | | |_| |>  < "
echo " |_| \\_|\\__,_|_| |_|_|\\__\\___||_____/_| |_____|_| |_|\\__,_/_/\\_\\"
echo -e "\033[0m"
echo -e "\033[1;37mWelcome to Nanite AI Linux!\033[0m"
echo -e "\033[0;37mType 'nanite-help' to get started.\033[0m"
echo ""
""")
        os.chmod(welcome_path, 0o755)
        libcalamares.utils.debug("Created welcome message")
    except Exception as e:
        libcalamares.utils.debug(f"Error creating welcome message: {str(e)}")

def configure_ai_services(root_mount_point):
    """Configure AI services to start automatically."""
    try:
        # Enable Ollama service
        subprocess.run(["chroot", root_mount_point, "systemctl", "enable", "ollama.service"])
        
        # Enable Nanite AI assistant service
        subprocess.run(["chroot", root_mount_point, "systemctl", "enable", "nanite-assistant.service"])
        
        libcalamares.utils.debug("Configured AI services")
    except Exception as e:
        libcalamares.utils.debug(f"Error configuring AI services: {str(e)}")

def setup_desktop_shortcuts(root_mount_point):
    """Set up desktop shortcuts for AI tools."""
    try:
        # Create Desktop directory if it doesn't exist
        desktop_dir = os.path.join(root_mount_point, "etc/skel/Desktop")
        os.makedirs(desktop_dir, exist_ok=True)
        
        # Copy desktop shortcuts
        for app in ["nanite-assistant", "nanite-image-generator", "nanite-code-assistant"]:
            src = os.path.join(root_mount_point, f"usr/share/applications/{app}.desktop")
            dst = os.path.join(desktop_dir, f"{app}.desktop")
            if os.path.exists(src):
                subprocess.run(["cp", src, dst])
                os.chmod(dst, 0o755)
        
        libcalamares.utils.debug("Set up desktop shortcuts")
    except Exception as e:
        libcalamares.utils.debug(f"Error setting up desktop shortcuts: {str(e)}")
```

## Integration with Live-build

To integrate Calamares with Live-build, you need to include it in your package lists and copy your customizations into the live system.

### Adding Calamares to Package Lists

Create or modify `config/package-lists/installer.list.chroot`:

```
calamares
calamares-settings-debian
```

### Copying Custom Calamares Configuration

Create a hook to copy your custom Calamares configuration:

Create `config/hooks/live/0100-calamares-customization.hook.chroot`:

```bash
#!/bin/sh
set -e

# Create directories
mkdir -p /etc/calamares/branding/nanite
mkdir -p /etc/calamares/modules/nanite-post-install

# Copy branding files
cp -r /path/to/nanite_project/calamares/branding/nanite/* /etc/calamares/branding/nanite/

# Copy module configurations
cp -r /path/to/nanite_project/calamares/modules/* /etc/calamares/modules/

# Copy main configuration
cp /path/to/nanite_project/calamares/settings.conf /etc/calamares/

# Set permissions
chmod +x /etc/calamares/modules/nanite-post-install/main.py

# Update Calamares settings to use our branding
sed -i 's/^branding:.*/branding: nanite/' /etc/calamares/settings.conf

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0100-calamares-customization.hook.chroot
```

### Creating Desktop Shortcut for Calamares

Create `config/includes.chroot/usr/share/applications/nanite-installer.desktop`:

```
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
```

## Testing and Debugging

### Testing Calamares Configuration

To test your Calamares configuration without building a full ISO:

```bash
# Install Calamares
sudo apt install calamares calamares-settings-debian

# Copy your custom configuration
sudo cp -r /path/to/nanite_project/calamares/* /etc/calamares/

# Run Calamares in debug mode
sudo calamares -d
```

### Testing QML Slideshow

To test your QML slideshow without running the full installer:

```bash
# Install qmlscene
sudo apt install qtdeclarative5-dev-tools

# Test the slideshow
qmlscene -I /usr/share/calamares/qml /etc/calamares/branding/nanite/show.qml
```

### Common Issues and Solutions

1. **Slideshow not appearing**:
   - Check that the path in `branding.desc` is correct
   - Verify QML syntax with `qmlscene`
   - Check for missing image files

2. **Branding not applied**:
   - Verify that `settings.conf` points to your branding component
   - Check permissions on branding files

3. **Post-install script not running**:
   - Verify the module is included in the `exec` sequence in `settings.conf`
   - Check Python syntax and permissions

4. **UI styling issues**:
   - Check that `stylesheet.qss` is properly formatted
   - Verify that the style rules target the correct widgets

## Complete Example

Here's a complete example of the directory structure and files for Calamares customization:

```
/etc/calamares/
├── branding/
│   └── nanite/
│       ├── branding.desc
│       ├── logo.png
│       ├── show.qml
│       ├── slide1.png
│       ├── slide2.png
│       ├── slide3.png
│       ├── stylesheet.qss
│       └── welcome.png
├── modules/
│   ├── bootloader.conf
│   ├── displaymanager.conf
│   ├── packages.conf
│   ├── users.conf
│   └── nanite-post-install/
│       ├── module.desc
│       └── main.py
└── settings.conf
```

By following this guide, you can create a fully customized Calamares installer for your Nanite Linux distribution, complete with branded visuals, custom slideshow, and post-installation configuration.
