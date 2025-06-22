# Nanite Live-Build Configuration Guide

This document provides a step-by-step walkthrough for creating the Live-build configuration for Nanite, a specialized Debian-based Linux distribution for AI engineers and Vibe Coders.

## Setting Up the Build Environment

First, we need to set up a proper build environment for creating our Nanite distribution:

```bash
# Create a build directory
mkdir -p nanite-build
cd nanite-build

# Install live-build and required packages
sudo apt update
sudo apt install -y live-build debootstrap squashfs-tools xorriso isolinux syslinux-common

# Initialize the live-build configuration
lb config
```

## Basic Configuration

Let's configure the basic settings for our Nanite distribution:

```bash
# Configure for a hybrid ISO image (works on USB and optical media)
lb config --binary-images iso-hybrid

# Set Debian as the base distribution (using the stable release)
lb config --distribution bookworm

# Configure architecture (amd64 for modern systems)
lb config --architectures amd64

# Set up the desktop environment (XFCE for lightweight yet customizable interface)
lb config --apt-recommends false
echo "task-xfce-desktop" > config/package-lists/desktop.list.chroot

# Enable firmware for better hardware support
lb config --firmware-binary true
lb config --firmware-chroot true

# Configure bootloader
lb config --bootappend-live "boot=live components locales=en_US.UTF-8"
```

## Package Selection

Now, let's define the packages to include in Nanite. We'll create several package list files to organize them by category:

### Core System Packages

Create `config/package-lists/core.list.chroot`:

```
# System essentials
sudo
apt-utils
curl
wget
git
build-essential
cmake
python3
python3-pip
python3-venv
python3-dev
htop
neofetch

# Hardware support
firmware-linux
firmware-linux-nonfree
nvidia-driver
amd64-microcode
intel-microcode

# Networking
network-manager
network-manager-gnome
wireless-tools
```

### AI and Development Packages

Create `config/package-lists/ai-dev.list.chroot`:

```
# Python data science and ML libraries
python3-numpy
python3-scipy
python3-matplotlib
python3-pandas
python3-sklearn
python3-tensorflow
python3-torch
python3-keras
python3-nltk
python3-spacy

# Development tools
code
jupyter-notebook
git-lfs
docker.io
docker-compose

# GPU support
nvidia-cuda-toolkit
nvidia-cuda-dev
```

### Desktop and UI Packages

Create `config/package-lists/desktop-extras.list.chroot`:

```
# XFCE extras
xfce4-goodies
xfce4-terminal
thunar
thunar-archive-plugin
thunar-media-tags-plugin

# Themes and appearance
arc-theme
papirus-icon-theme
fonts-noto
fonts-noto-color-emoji

# Multimedia
vlc
ffmpeg
gimp
inkscape
```

## Custom Scripts and Hooks

We'll create custom scripts to set up the AI components during the build process:

### Ollama Installation Script

Create `config/hooks/live/0100-install-ollama.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Installing Ollama for LLM support..."
curl -fsSL https://ollama.com/install.sh | sh

# Create directory for models
mkdir -p /usr/share/nanite/models
chmod 755 /usr/share/nanite/models

# Create systemd service for Ollama
cat > /etc/systemd/system/ollama.service << EOF
[Unit]
Description=Ollama Service
After=network.target

[Service]
ExecStart=/usr/bin/ollama serve
Restart=on-failure
User=root
Environment="OLLAMA_MODELS=/usr/share/nanite/models"

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
systemctl enable ollama.service

echo "Ollama installation completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0100-install-ollama.hook.chroot
```

### Python AI Libraries Installation Script

Create `config/hooks/live/0200-install-ai-libraries.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Installing Python AI libraries..."

# Create a requirements file
cat > /tmp/ai-requirements.txt << EOF
transformers
sentence-transformers
langchain
chromadb
llama-cpp-python
diffusers
accelerate
bitsandbytes
peft
optimum
onnxruntime
onnxruntime-gpu
EOF

# Install the requirements
pip3 install -r /tmp/ai-requirements.txt

echo "Python AI libraries installation completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0200-install-ai-libraries.hook.chroot
```

### Desktop Configuration Script

Create `config/hooks/live/0300-configure-desktop.hook.chroot`:

```bash
#!/bin/bash
set -e

echo "Configuring desktop environment..."

# Create Nanite-specific directories
mkdir -p /usr/share/nanite/backgrounds
mkdir -p /usr/share/nanite/icons
mkdir -p /usr/share/nanite/applications

# Set up default user configuration
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml

# Configure panel with AI assistant launcher
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-panel" version="1.0">
  <property name="panels" type="array">
    <value type="int" value="0"/>
    <property name="panel-0" type="empty">
      <property name="position" type="string" value="p=6;x=0;y=0"/>
      <property name="length" type="uint" value="100"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="2"/>
        <value type="int" value="3"/>
        <value type="int" value="4"/>
        <value type="int" value="5"/>
        <value type="int" value="6"/>
        <value type="int" value="7"/>
      </property>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="applicationsmenu"/>
    <property name="plugin-2" type="string" value="launcher">
      <property name="items" type="array">
        <value type="string" value="nanite-ai-assistant.desktop"/>
      </property>
    </property>
    <property name="plugin-3" type="string" value="tasklist"/>
    <property name="plugin-4" type="string" value="separator"/>
    <property name="plugin-5" type="string" value="systray"/>
    <property name="plugin-6" type="string" value="clock"/>
    <property name="plugin-7" type="string" value="actions"/>
  </property>
</channel>
EOF

# Create AI assistant launcher
cat > /usr/share/nanite/applications/nanite-ai-assistant.desktop << EOF
[Desktop Entry]
Name=Nanite AI Assistant
Comment=AI assistance powered by local LLMs
Exec=xfce4-terminal -e "ollama run mistral"
Icon=/usr/share/nanite/icons/ai-assistant.png
Terminal=false
Type=Application
Categories=Utility;AI;
EOF

# Copy the desktop file to applications directory
cp /usr/share/nanite/applications/nanite-ai-assistant.desktop /usr/share/applications/

echo "Desktop configuration completed."
```

Make the script executable:

```bash
chmod +x config/hooks/live/0300-configure-desktop.hook.chroot
```

## Custom Files and Resources

Let's add some custom files to our distribution:

### Create Directory Structure

```bash
mkdir -p config/includes.chroot/usr/share/nanite/backgrounds
mkdir -p config/includes.chroot/usr/share/nanite/icons
mkdir -p config/includes.chroot/usr/share/doc/nanite
```

### Create Documentation

Create `config/includes.chroot/usr/share/doc/nanite/README.md`:

```markdown
# Welcome to Nanite

Nanite is a specialized Linux distribution for AI engineers and Vibe Coders. It integrates various AI models, agents, and applications directly into the operating system, providing users with immediate access to AI assistance through Large Language Models (LLMs).

## Getting Started

1. **AI Assistant**: Access the AI assistant from the panel or by running `ollama run mistral` in the terminal.
2. **Installing Models**: Use `ollama pull <model-name>` to download additional models.
3. **Development Environment**: VSCode and JupyterLab are pre-installed for AI development.
4. **Documentation**: Find more documentation in `/usr/share/doc/nanite/`.

## Available Models

- Mistral: General-purpose LLM for various tasks
- Llama 3: Advanced reasoning and instruction following
- Phi-3: Lightweight model for basic tasks

## Support

For support and more information, visit our website or community forums.
```

### Create a Custom Welcome Script

Create `config/includes.chroot/usr/local/bin/nanite-welcome`:

```bash
#!/bin/bash

# Display welcome message
echo "Welcome to Nanite - AI-powered Linux Distribution"
echo "================================================="
echo ""
echo "System Information:"
neofetch
echo ""
echo "AI Models Status:"
ollama list
echo ""
echo "For help, type: less /usr/share/doc/nanite/README.md"
```

Make it executable:

```bash
chmod +x config/includes.chroot/usr/local/bin/nanite-welcome
```

Add it to the bash profile:

```bash
echo "# Run welcome script on login" >> config/includes.chroot/etc/skel/.bashrc
echo "if [ -f /usr/local/bin/nanite-welcome ]; then" >> config/includes.chroot/etc/skel/.bashrc
echo "    /usr/local/bin/nanite-welcome" >> config/includes.chroot/etc/skel/.bashrc
echo "fi" >> config/includes.chroot/etc/skel/.bashrc
```

## ISO Metadata Configuration

Configure the ISO metadata:

```bash
# Set the ISO volume ID
lb config --iso-volume "Nanite AI Linux"

# Set the ISO application ID
lb config --iso-application "Nanite AI Linux"

# Set the ISO publisher
lb config --iso-publisher "Nanite Project"
```

## Building the ISO

After setting up all the configuration, you can build the ISO:

```bash
# Clean any previous build artifacts
lb clean

# Build the ISO (requires root privileges)
sudo lb build
```

The build process will take some time, depending on your system's performance and internet connection. Once completed, you'll find the ISO file in the current directory, typically named something like `live-image-amd64.hybrid.iso`.

## Post-Build Steps

After building the ISO, you may want to:

1. Rename the ISO to something more descriptive:
   ```bash
   mv live-image-amd64.hybrid.iso nanite-ai-linux-$(date +%Y%m%d).iso
   ```

2. Calculate checksums for verification:
   ```bash
   sha256sum nanite-ai-linux-*.iso > nanite-ai-linux-$(date +%Y%m%d).sha256
   ```

3. Test the ISO in a virtual machine before distribution.

This configuration provides a solid foundation for Nanite, with the core system, AI components, and a customized desktop environment. You can further extend and customize it based on specific requirements and user feedback.
