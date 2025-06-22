# Live-build Branding and Customization Workflows

This document provides detailed, actionable workflows for customizing and branding a Debian-based Linux distribution using Live-build. It covers all aspects of visual and functional customization, from basic theming to boot splash screens and login managers.

## Directory Structure for Branding

When customizing a Debian Live system with branding elements, you'll work primarily with these directories:

```
nanite-build/
├── config/
│   ├── includes.chroot/     # Files for the live system
│   │   ├── etc/             # System configuration
│   │   ├── usr/             # Applications, themes, icons
│   │   └── var/             # Variable data
│   ├── includes.binary/     # Files for the boot medium
│   │   └── boot/            # Boot-related files
│   ├── hooks/
│   │   ├── live/            # Hooks for live system
│   │   │   ├── *.hook.chroot
│   │   │   └── *.hook.binary
│   │   └── normal/          # Hooks for normal system
│   ├── package-lists/       # Package selection
│   └── preseed/             # Package configuration
└── branding/                # Source branding assets
    ├── logos/
    ├── themes/
    └── wallpapers/
```

## 1. System Branding Elements

### 1.1 Distribution Name and Version

To change the distribution name and version information system-wide:

1. Create a custom `os-release` file:

```bash
mkdir -p config/includes.chroot/etc
```

Create `config/includes.chroot/etc/os-release` with the following content:

```
PRETTY_NAME="Nanite AI Linux"
NAME="Nanite"
VERSION_ID="1.0"
VERSION="1.0 (Quantum)"
VERSION_CODENAME=quantum
ID=nanite
ID_LIKE=debian
HOME_URL="https://nanite.ai/"
SUPPORT_URL="https://nanite.ai/support/"
BUG_REPORT_URL="https://nanite.ai/bugs/"
```

2. Create a custom `lsb-release` file:

Create `config/includes.chroot/etc/lsb-release`:

```
DISTRIB_ID=Nanite
DISTRIB_RELEASE=1.0
DISTRIB_CODENAME=quantum
DISTRIB_DESCRIPTION="Nanite AI Linux 1.0 (Quantum)"
```

3. Create a custom issue file:

Create `config/includes.chroot/etc/issue`:

```
Nanite AI Linux 1.0 \n \l
```

And `config/includes.chroot/etc/issue.net`:

```
Nanite AI Linux 1.0
```

### 1.2 Logo and Branding Assets

1. Create directories for branding assets:

```bash
mkdir -p config/includes.chroot/usr/share/nanite/branding
mkdir -p config/includes.chroot/usr/share/pixmaps
mkdir -p config/includes.chroot/usr/share/icons/hicolor/{16x16,22x22,24x24,32x32,48x48,64x64,128x128,256x256}/apps
```

2. Add your logo files:

```bash
# Copy logo to standard locations
cp branding/logos/nanite-logo.png config/includes.chroot/usr/share/pixmaps/nanite-logo.png
cp branding/logos/nanite-logo.svg config/includes.chroot/usr/share/nanite/branding/nanite-logo.svg

# Copy icons in various sizes
cp branding/logos/nanite-16.png config/includes.chroot/usr/share/icons/hicolor/16x16/apps/nanite.png
cp branding/logos/nanite-32.png config/includes.chroot/usr/share/icons/hicolor/32x32/apps/nanite.png
cp branding/logos/nanite-48.png config/includes.chroot/usr/share/icons/hicolor/48x48/apps/nanite.png
cp branding/logos/nanite-128.png config/includes.chroot/usr/share/icons/hicolor/128x128/apps/nanite.png
```

3. Update icon cache with a hook:

Create `config/hooks/live/0050-update-icon-cache.hook.chroot`:

```bash
#!/bin/sh
set -e

# Update icon cache
echo "Updating icon cache..."
gtk-update-icon-cache -f -t /usr/share/icons/hicolor

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0050-update-icon-cache.hook.chroot
```

## 2. Desktop Environment Customization (XFCE)

### 2.1 XFCE Theme and Appearance

1. Install required theme packages:

Create `config/package-lists/themes.list.chroot`:

```
arc-theme
papirus-icon-theme
fonts-noto
fonts-noto-color-emoji
```

2. Create default XFCE configuration:

```bash
mkdir -p config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
```

3. Configure the XFCE appearance:

Create `config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xsettings" version="1.0">
  <property name="Net" type="empty">
    <property name="ThemeName" type="string" value="Arc-Dark"/>
    <property name="IconThemeName" type="string" value="Papirus-Dark"/>
    <property name="DoubleClickTime" type="empty"/>
    <property name="DoubleClickDistance" type="empty"/>
    <property name="DndDragThreshold" type="empty"/>
    <property name="CursorBlink" type="empty"/>
    <property name="CursorBlinkTime" type="empty"/>
    <property name="SoundThemeName" type="empty"/>
    <property name="EnableEventSounds" type="empty"/>
    <property name="EnableInputFeedbackSounds" type="empty"/>
  </property>
  <property name="Xft" type="empty">
    <property name="DPI" type="int" value="-1"/>
    <property name="Antialias" type="int" value="1"/>
    <property name="Hinting" type="int" value="1"/>
    <property name="HintStyle" type="string" value="hintslight"/>
    <property name="RGBA" type="string" value="rgb"/>
  </property>
  <property name="Gtk" type="empty">
    <property name="CanChangeAccels" type="empty"/>
    <property name="ColorPalette" type="empty"/>
    <property name="FontName" type="string" value="Noto Sans 10"/>
    <property name="MonospaceFontName" type="string" value="Noto Sans Mono 10"/>
    <property name="IconSizes" type="empty"/>
    <property name="KeyThemeName" type="empty"/>
    <property name="ToolbarStyle" type="string" value="icons"/>
    <property name="ToolbarIconSize" type="empty"/>
    <property name="MenuImages" type="bool" value="true"/>
    <property name="ButtonImages" type="bool" value="true"/>
    <property name="MenuBarAccel" type="empty"/>
    <property name="CursorThemeName" type="string" value="Adwaita"/>
    <property name="CursorThemeSize" type="empty"/>
    <property name="DecorationLayout" type="empty"/>
  </property>
</channel>
```

4. Configure the XFCE desktop:

Create `config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml`:

```xml
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
  <property name="desktop-icons" type="empty">
    <property name="style" type="int" value="0"/>
    <property name="file-icons" type="empty">
      <property name="show-home" type="bool" value="true"/>
      <property name="show-filesystem" type="bool" value="true"/>
      <property name="show-trash" type="bool" value="true"/>
      <property name="show-removable" type="bool" value="true"/>
    </property>
  </property>
</channel>
```

5. Configure the XFCE panel:

Create `config/includes.chroot/etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-panel" version="1.0">
  <property name="configver" type="int" value="2"/>
  <property name="panels" type="array">
    <value type="int" value="1"/>
    <property name="dark-mode" type="bool" value="true"/>
    <property name="panel-1" type="empty">
      <property name="position" type="string" value="p=8;x=0;y=0"/>
      <property name="length" type="uint" value="100"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="icon-size" type="uint" value="24"/>
      <property name="size" type="uint" value="36"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="2"/>
        <value type="int" value="3"/>
        <value type="int" value="4"/>
        <value type="int" value="5"/>
        <value type="int" value="6"/>
        <value type="int" value="7"/>
        <value type="int" value="8"/>
        <value type="int" value="9"/>
        <value type="int" value="10"/>
        <value type="int" value="11"/>
        <value type="int" value="12"/>
      </property>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="applicationsmenu">
      <property name="button-icon" type="string" value="nanite"/>
      <property name="button-title" type="string" value="Nanite"/>
      <property name="show-button-title" type="bool" value="true"/>
    </property>
    <property name="plugin-2" type="string" value="tasklist"/>
    <property name="plugin-3" type="string" value="separator">
      <property name="expand" type="bool" value="true"/>
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-4" type="string" value="systray"/>
    <property name="plugin-5" type="string" value="notification-plugin"/>
    <property name="plugin-6" type="string" value="indicator"/>
    <property name="plugin-7" type="string" value="statusnotifier"/>
    <property name="plugin-8" type="string" value="power-manager-plugin"/>
    <property name="plugin-9" type="string" value="pulseaudio">
      <property name="enable-keyboard-shortcuts" type="bool" value="true"/>
    </property>
    <property name="plugin-10" type="string" value="separator">
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-11" type="string" value="clock">
      <property name="digital-format" type="string" value="%a %d %b, %R"/>
    </property>
    <property name="plugin-12" type="string" value="actions">
      <property name="appearance" type="uint" value="0"/>
      <property name="items" type="array">
        <value type="string" value="-lock-screen"/>
        <value type="string" value="-switch-user"/>
        <value type="string" value="-separator"/>
        <value type="string" value="-suspend"/>
        <value type="string" value="-hibernate"/>
        <value type="string" value="-hybrid-sleep"/>
        <value type="string" value="-separator"/>
        <value type="string" value="-shutdown"/>
        <value type="string" value="-restart"/>
        <value type="string" value="-separator"/>
        <value type="string" value="+logout"/>
        <value type="string" value="-logout-dialog"/>
      </property>
    </property>
  </property>
</channel>
```

### 2.2 Custom Wallpapers

1. Create directories for wallpapers:

```bash
mkdir -p config/includes.chroot/usr/share/nanite/backgrounds
```

2. Add your wallpapers:

```bash
cp branding/wallpapers/default.png config/includes.chroot/usr/share/nanite/backgrounds/
cp branding/wallpapers/nanite-*.png config/includes.chroot/usr/share/nanite/backgrounds/
```

3. Create a hook to set default wallpaper:

Create `config/hooks/live/0060-set-wallpaper.hook.chroot`:

```bash
#!/bin/sh
set -e

# Set default wallpaper for all users
echo "Setting default wallpaper..."
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml << EOF
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
EOF

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0060-set-wallpaper.hook.chroot
```

### 2.3 Custom Application Menu

1. Create a custom menu entry for Nanite Assistant:

```bash
mkdir -p config/includes.chroot/usr/share/applications
```

Create `config/includes.chroot/usr/share/applications/nanite-assistant.desktop`:

```
[Desktop Entry]
Name=Nanite AI Assistant
Comment=AI assistance powered by local LLMs
Exec=xfce4-terminal -e "ollama run nanite-assistant"
Icon=nanite
Terminal=false
Type=Application
Categories=Utility;AI;
StartupNotify=true
```

2. Create a custom menu category for AI tools:

Create `config/includes.chroot/etc/xdg/menus/applications-merged/nanite-ai.menu`:

```xml
<!DOCTYPE Menu PUBLIC "-//freedesktop//DTD Menu 1.0//EN"
 "http://www.freedesktop.org/standards/menu-spec/1.0/menu.dtd">
<Menu>
  <Name>Applications</Name>
  <Menu>
    <Name>AI Tools</Name>
    <Directory>nanite-ai.directory</Directory>
    <Include>
      <Category>AI</Category>
    </Include>
  </Menu>
</Menu>
```

3. Create the directory file:

```bash
mkdir -p config/includes.chroot/usr/share/desktop-directories
```

Create `config/includes.chroot/usr/share/desktop-directories/nanite-ai.directory`:

```
[Desktop Entry]
Name=AI Tools
Comment=Artificial Intelligence Tools
Icon=nanite
Type=Directory
```

## 3. Boot Splash Customization (Plymouth)

### 3.1 Installing Plymouth

1. Add Plymouth to your package list:

Create or edit `config/package-lists/boot.list.chroot`:

```
plymouth
plymouth-themes
plymouth-x11
```

### 3.2 Creating a Custom Plymouth Theme

1. Create directories for the Plymouth theme:

```bash
mkdir -p config/includes.chroot/usr/share/plymouth/themes/nanite
```

2. Create the theme files:

Create `config/includes.chroot/usr/share/plymouth/themes/nanite/nanite.plymouth`:

```
[Plymouth Theme]
Name=Nanite
Description=Nanite AI Linux boot splash
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/nanite
ScriptFile=/usr/share/plymouth/themes/nanite/nanite.script
```

3. Create the Plymouth script:

Create `config/includes.chroot/usr/share/plymouth/themes/nanite/nanite.script`:

```
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
```

4. Add the theme assets:

```bash
cp branding/plymouth/background.png config/includes.chroot/usr/share/plymouth/themes/nanite/
cp branding/plymouth/logo.png config/includes.chroot/usr/share/plymouth/themes/nanite/
```

5. Create a hook to set the Plymouth theme:

Create `config/hooks/live/0070-set-plymouth-theme.hook.chroot`:

```bash
#!/bin/sh
set -e

# Set Plymouth theme
echo "Setting Plymouth theme..."
plymouth-set-default-theme nanite
update-initramfs -u

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0070-set-plymouth-theme.hook.chroot
```

## 4. Login Screen Customization (LightDM)

### 4.1 Installing LightDM

1. Add LightDM to your package list:

Create or edit `config/package-lists/display-manager.list.chroot`:

```
lightdm
lightdm-gtk-greeter
lightdm-gtk-greeter-settings
```

### 4.2 Customizing LightDM

1. Create directories for LightDM configuration:

```bash
mkdir -p config/includes.chroot/etc/lightdm
```

2. Configure LightDM:

Create `config/includes.chroot/etc/lightdm/lightdm.conf`:

```
[Seat:*]
greeter-session=lightdm-gtk-greeter
user-session=xfce
```

3. Configure LightDM GTK Greeter:

Create `config/includes.chroot/etc/lightdm/lightdm-gtk-greeter.conf`:

```
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
```

4. Add login background:

```bash
cp branding/wallpapers/login-background.png config/includes.chroot/usr/share/nanite/backgrounds/
```

## 5. GRUB Bootloader Customization

### 5.1 Installing GRUB Theme

1. Create directories for GRUB theme:

```bash
mkdir -p config/includes.chroot/boot/grub/themes/nanite
```

2. Create the GRUB theme:

Create `config/includes.chroot/boot/grub/themes/nanite/theme.txt`:

```
# Nanite GRUB theme

# Global properties
title-text: "Nanite AI Linux"
title-color: "#ffffff"
title-font: "DejaVu Sans Regular 18"
desktop-image: "background.png"
desktop-color: "#000000"
terminal-box: "terminal_box_*.png"
terminal-font: "DejaVu Sans Mono Regular 12"

# Boot menu
+ boot_menu {
    left = 15%
    width = 70%
    top = 30%
    height = 40%
    item_font = "DejaVu Sans Regular 12"
    item_color = "#cccccc"
    selected_item_color = "#ffffff"
    selected_item_font = "DejaVu Sans Bold 12"
    icon_width = 32
    icon_height = 32
    item_height = 36
    item_padding = 5
    item_spacing = 10
    selected_item_pixmap_style = "select_*.png"
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
    bar_style = "progress_bar_*.png"
}

# Logo
+ image {
    left = 50%-128
    top = 10%
    width = 256
    height = 64
    file = "logo.png"
}
```

3. Add GRUB theme assets:

```bash
cp branding/grub/background.png config/includes.chroot/boot/grub/themes/nanite/
cp branding/grub/logo.png config/includes.chroot/boot/grub/themes/nanite/
cp branding/grub/select_*.png config/includes.chroot/boot/grub/themes/nanite/
cp branding/grub/progress_bar_*.png config/includes.chroot/boot/grub/themes/nanite/
cp branding/grub/terminal_box_*.png config/includes.chroot/boot/grub/themes/nanite/
```

4. Configure GRUB to use the theme:

Create `config/includes.chroot/etc/default/grub.d/nanite-theme.cfg`:

```
# Nanite GRUB theme configuration
GRUB_THEME="/boot/grub/themes/nanite/theme.txt"
GRUB_BACKGROUND="/boot/grub/themes/nanite/background.png"
GRUB_DISTRIBUTOR="Nanite"
GRUB_TIMEOUT=5
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```

5. Create a hook to update GRUB:

Create `config/hooks/live/0080-update-grub.hook.chroot`:

```bash
#!/bin/sh
set -e

# Update GRUB
echo "Updating GRUB configuration..."
update-grub

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0080-update-grub.hook.chroot
```

## 6. System-wide Branding Integration

### 6.1 Browser Homepage and Bookmarks

1. Create a custom Firefox profile:

```bash
mkdir -p config/includes.chroot/etc/skel/.mozilla/firefox/nanite.default
```

Create `config/includes.chroot/etc/skel/.mozilla/firefox/profiles.ini`:

```
[Profile0]
Name=default
IsRelative=1
Path=nanite.default
Default=1
```

2. Create a custom homepage:

```bash
mkdir -p config/includes.chroot/usr/share/nanite/homepage
```

Create `config/includes.chroot/usr/share/nanite/homepage/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Nanite AI Linux</title>
    <style>
        body {
            font-family: 'Noto Sans', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #f0f0f0;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .logo {
            max-width: 200px;
            margin-bottom: 20px;
        }
        h1 {
            font-size: 36px;
            margin: 0;
            color: #4db6ac;
        }
        h2 {
            font-size: 24px;
            margin: 30px 0 15px;
            color: #4db6ac;
        }
        p {
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .card {
            background-color: #2a2a2a;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .links {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 15px;
            margin-top: 30px;
        }
        .link-item {
            background-color: #333;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
            transition: transform 0.2s;
        }
        .link-item:hover {
            transform: translateY(-3px);
            background-color: #444;
        }
        a {
            color: #64ffda;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="/usr/share/nanite/branding/nanite-logo.svg" alt="Nanite Logo" class="logo">
            <h1>Welcome to Nanite AI Linux</h1>
            <p>Your AI-powered computing environment</p>
        </div>
        
        <div class="card">
            <h2>Getting Started</h2>
            <p>Nanite AI Linux integrates various AI models, agents, and applications directly into the operating system, providing immediate access to AI assistance through Large Language Models (LLMs).</p>
            <p>To access the AI assistant, click the Nanite icon in the panel or press <strong>Alt+A</strong>.</p>
        </div>
        
        <div class="card">
            <h2>Quick Links</h2>
            <div class="links">
                <a href="file:///usr/share/doc/nanite/README.md" class="link-item">Documentation</a>
                <a href="https://nanite.ai/community" class="link-item">Community</a>
                <a href="https://nanite.ai/support" class="link-item">Support</a>
                <a href="https://nanite.ai/tutorials" class="link-item">Tutorials</a>
            </div>
        </div>
    </div>
</body>
</html>
```

3. Configure Firefox to use the custom homepage:

Create `config/includes.chroot/etc/skel/.mozilla/firefox/nanite.default/prefs.js`:

```javascript
// Nanite Firefox preferences
user_pref("browser.startup.homepage", "file:///usr/share/nanite/homepage/index.html");
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.startup.page", 1);
user_pref("browser.newtabpage.enabled", false);
```

### 6.2 Terminal Customization

1. Create a custom bashrc:

Create `config/includes.chroot/etc/skel/.bashrc.d/nanite-prompt.sh`:

```bash
# Nanite custom prompt
export PS1="\[\033[38;5;81m\]\u\[\033[38;5;245m\]@\[\033[38;5;81m\]nanite\[\033[38;5;245m\]:\[\033[38;5;39m\]\w\[\033[00m\] $ "

# Nanite welcome message
echo -e "\033[1;36m"
echo "  _   _             _ _        _    _   _     _                  "
echo " | \ | | __ _ _ __ (_) |_ ___ | |  (_) | |   (_)_ __  _   ___  __"
echo " |  \| |/ _\` | '_ \| | __/ _ \| |  | | | |   | | '_ \| | | \ \/ /"
echo " | |\  | (_| | | | | | ||  __/| |__| | | |___| | | | | |_| |>  < "
echo " |_| \_|\__,_|_| |_|_|\__\___||_____/_| |_____|_| |_|\__,_/_/\_\\"
echo -e "\033[0m"
echo -e "\033[1;37mWelcome to Nanite AI Linux!\033[0m"
echo -e "\033[0;37mType 'nanite-help' to get started.\033[0m"
echo ""
```

2. Create a help script:

Create `config/includes.chroot/usr/local/bin/nanite-help`:

```bash
#!/bin/bash

echo -e "\033[1;36mNanite AI Linux - Help\033[0m"
echo -e "\033[1;37m=====================\033[0m"
echo ""
echo -e "\033[1;37mAI Commands:\033[0m"
echo -e "  \033[0;36mnanite-ask\033[0m <question>    - Ask the AI assistant a question"
echo -e "  \033[0;36mnanite-image-gen\033[0m         - Generate images from text descriptions"
echo -e "  \033[0;36mnanite-code-assist\033[0m       - Get AI-powered coding help"
echo -e "  \033[0;36mnanite-rag\033[0m               - Use Retrieval-Augmented Generation"
echo -e "  \033[0;36mnanite-speech\033[0m            - Speech recognition and synthesis"
echo ""
echo -e "\033[1;37mSystem Commands:\033[0m"
echo -e "  \033[0;36mnanite-system-info\033[0m       - Display system information"
echo -e "  \033[0;36mnanite-update\033[0m            - Update the system"
echo -e "  \033[0;36mnanite-settings\033[0m          - Open system settings"
echo ""
echo -e "\033[1;37mDocumentation:\033[0m"
echo -e "  Full documentation is available at \033[0;36mfile:///usr/share/doc/nanite/\033[0m"
echo ""
```

Make it executable:

```bash
chmod +x config/includes.chroot/usr/local/bin/nanite-help
```

### 6.3 Custom System Information

Create `config/includes.chroot/usr/local/bin/nanite-system-info`:

```bash
#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Logo
echo -e "${CYAN}"
echo "  _   _             _ _        _    _   _     _                  "
echo " | \ | | __ _ _ __ (_) |_ ___ | |  (_) | |   (_)_ __  _   ___  __"
echo " |  \| |/ _\` | '_ \| | __/ _ \| |  | | | |   | | '_ \| | | \ \/ /"
echo " | |\  | (_| | | | | | ||  __/| |__| | | |___| | | | | |_| |>  < "
echo " |_| \_|\__,_|_| |_|_|\__\___||_____/_| |_____|_| |_|\__,_/_/\_\\"
echo -e "${NC}"

# System info
echo -e "${BOLD}SYSTEM INFORMATION${NC}"
echo -e "${BLUE}Hostname:${NC} $(hostname)"
echo -e "${BLUE}Distribution:${NC} Nanite AI Linux $(cat /etc/nanite-version 2>/dev/null || echo "1.0")"
echo -e "${BLUE}Kernel:${NC} $(uname -r)"
echo -e "${BLUE}Uptime:${NC} $(uptime -p | sed 's/up //')"
echo -e "${BLUE}Shell:${NC} $SHELL"

# Hardware info
echo -e "\n${BOLD}HARDWARE INFORMATION${NC}"
echo -e "${GREEN}CPU:${NC} $(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | sed 's/^[ \t]*//')"
echo -e "${GREEN}Memory:${NC} $(free -h | grep Mem | awk '{print $3 " used of " $2 " total"}')"
echo -e "${GREEN}Disk:${NC} $(df -h / | awk 'NR==2 {print $3 " used of " $2 " total (" $5 " used)"}')"

# GPU info
if command -v nvidia-smi &> /dev/null; then
    GPU=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    echo -e "${GREEN}GPU:${NC} $GPU"
elif command -v lspci &> /dev/null; then
    GPU=$(lspci | grep -i 'vga\|3d\|2d' | head -1 | sed 's/.*: //')
    echo -e "${GREEN}GPU:${NC} $GPU"
fi

# AI models
echo -e "\n${BOLD}AI MODELS${NC}"
if command -v ollama &> /dev/null; then
    echo -e "${CYAN}Available models:${NC}"
    ollama list 2>/dev/null | awk '{print "  - " $1 " (" $2 ")"}'
else
    echo -e "${RED}Ollama not found. AI models may not be available.${NC}"
fi

# Network info
echo -e "\n${BOLD}NETWORK INFORMATION${NC}"
IP=$(ip -4 addr show scope global | grep inet | awk '{print $2}' | cut -d'/' -f1 | head -1)
if [ -n "$IP" ]; then
    echo -e "${YELLOW}IP Address:${NC} $IP"
else
    echo -e "${YELLOW}IP Address:${NC} Not connected"
fi

echo -e "\nFor more information, visit the Nanite documentation."
```

Make it executable:

```bash
chmod +x config/includes.chroot/usr/local/bin/nanite-system-info
```

### 6.4 Custom About Dialog

Create `config/includes.chroot/usr/share/applications/nanite-about.desktop`:

```
[Desktop Entry]
Name=About Nanite
Comment=Information about Nanite AI Linux
Exec=nanite-about
Icon=nanite
Terminal=false
Type=Application
Categories=System;
```

Create `config/includes.chroot/usr/local/bin/nanite-about`:

```bash
#!/bin/bash

# Use zenity to display about dialog
zenity --info \
  --title="About Nanite AI Linux" \
  --width=400 \
  --height=300 \
  --text="<span size='large'><b>Nanite AI Linux</b></span>\n\nVersion 1.0 (Quantum)\n\nNanite is a specialized Linux distribution for AI engineers and Vibe Coders. It integrates various AI models, agents, and applications directly into the operating system.\n\n<b>Website:</b> https://nanite.ai\n<b>Support:</b> https://nanite.ai/support\n\n© 2025 Nanite Project" \
  --icon-name="nanite"
```

Make it executable:

```bash
chmod +x config/includes.chroot/usr/local/bin/nanite-about
```

## 7. Integrating Branding into Live-build

### 7.1 Creating a Branding Package

1. Create a directory structure for the package:

```bash
mkdir -p config/packages.chroot/nanite-branding/DEBIAN
mkdir -p config/packages.chroot/nanite-branding/usr/share/nanite
```

2. Create the control file:

Create `config/packages.chroot/nanite-branding/DEBIAN/control`:

```
Package: nanite-branding
Version: 1.0
Section: misc
Priority: optional
Architecture: all
Maintainer: Nanite Team <team@nanite.ai>
Description: Nanite branding package
 This package contains branding elements for Nanite AI Linux.
```

3. Create a postinst script:

Create `config/packages.chroot/nanite-branding/DEBIAN/postinst`:

```bash
#!/bin/sh
set -e

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor
fi

# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    update-desktop-database
fi

# Create version file
echo "1.0" > /etc/nanite-version

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/packages.chroot/nanite-branding/DEBIAN/postinst
```

4. Build the package with a hook:

Create `config/hooks/live/0010-build-branding-package.hook.chroot`:

```bash
#!/bin/sh
set -e

# Build the branding package
echo "Building nanite-branding package..."
cd /config/packages.chroot
dpkg-deb --build nanite-branding
apt-get install -y ./nanite-branding.deb

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0010-build-branding-package.hook.chroot
```

### 7.2 Applying Branding to ISO

1. Create a hook to customize the ISO boot menu:

Create `config/hooks/live/0090-customize-isolinux.hook.binary`:

```bash
#!/bin/sh
set -e

# Customize isolinux boot menu
echo "Customizing isolinux boot menu..."

# Set menu title
sed -i 's/Debian GNU\/Linux/Nanite AI Linux/g' binary/isolinux/menu.cfg
sed -i 's/Debian GNU\/Linux/Nanite AI Linux/g' binary/isolinux/stdmenu.cfg

# Set boot parameters
sed -i 's/boot=live components/boot=live components quiet splash/g' binary/isolinux/menu.cfg

# Copy splash image if it exists
if [ -f /usr/share/nanite/branding/isolinux-splash.png ]; then
    cp /usr/share/nanite/branding/isolinux-splash.png binary/isolinux/splash.png
fi

# Exit successfully
exit 0
```

Make it executable:

```bash
chmod +x config/hooks/live/0090-customize-isolinux.hook.binary
```

2. Configure ISO metadata:

```bash
lb config --iso-volume "Nanite AI Linux" \
          --iso-application "Nanite AI Linux" \
          --iso-publisher "Nanite Project" \
          --iso-preparer "Nanite Build System"
```

## 8. Complete Build Command

After setting up all the customization and branding elements, build the ISO with:

```bash
# Clean any previous build artifacts
sudo lb clean

# Build the ISO
sudo lb build
```

This comprehensive guide provides detailed, actionable workflows for customizing and branding a Debian-based Linux distribution using Live-build. By following these steps, you can create a fully branded and customized distribution that reflects your organization's identity and meets your specific requirements.
