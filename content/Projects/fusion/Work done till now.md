---
title: work done till now
draft: "True"
---

```
sudo docker run --privileged -it -v /var/lib/docker/volumes/fusiondata/_data:/home/fusion fusionbuild1 /bin/bash

```

i want to make a custom linux distribution based on debain bookworm with live build tool please help me with that
distribution usecase : for ai, ml /ds engineers
based on : debain 12 bookworm
installer : Calamares

desktop environment : no desktop environment i want i3 window manager preinstalled
features : usb persisteance when boot through usb (that is memory must not loose after rebooting it)
every where it should replace debain as Fusion flux as an Distribution name
iso : 64bit amd64 iso



# prerequisites

To create a custom Linux distribution using the **Live Build** tool (commonly used for Debian-based distributions like Debian, Ubuntu, and their derivatives), you need to install several prerequisite packages. Here's a list of essential packages and a basic step-by-step guide for setting up the environment.

### Prerequisites for Using `live-build`:

1. **Debian/Ubuntu-based System:**
   Ensure you are working on a Debian or Ubuntu system, as `live-build` is designed for these distributions.

2. **Install Required Packages:**

   Open a terminal and run the following command to install the required tools:

   ```bash
   sudo apt-get update
   sudo apt-get install live-build debootstrap curl wget xorriso syslinux squashfs-tools genisoimage
   ```

   - **live-build**: The core tool to create live images.
   - **debootstrap**: Helps in creating a minimal base system (required for bootstrapping a Debian system).
   - **curl/wget**: For downloading additional files or packages during the build process.
   - **xorriso**: A command-line ISO 9660 editor and CD image creation tool, needed for making ISO files.
   - **syslinux**: For booting the system; used to configure boot loaders like ISOLINUX.
   - **squashfs-tools**: Tools to create a compressed filesystem, which is commonly used in live images.
   - **genisoimage**: Tool for creating the actual ISO image.

3. **Optional Packages:**
   Depending on the complexity of the custom distribution, you may need additional packages:

   - **apt-cacher-ng**: If you plan to cache packages during repeated builds.
     ```bash
     sudo apt-get install apt-cacher-ng
     ```

   - **git**: To manage repositories or pull specific configuration files.
     ```bash
     sudo apt-get install git
     ```

   - **locales**: To manage system locales if you want to customize them.
     ```bash
     sudo apt-get install locales
     ```

   - **schroot**: To manage chroots if you are building in an isolated environment.
     ```bash
     sudo apt-get install schroot
     ```

4. **Configure Live Build Environment:**

   After the necessary packages are installed, you can configure the build environment. For example:

   ```bash
   lb config
   ```

   This command sets up the default configuration for `live-build`. You can further customize it by adding options, such as specifying the distribution (Debian or Ubuntu version) or desktop environment.

5. **Build the Image:**

   Once the environment is configured, you can start building the ISO by running:

   ```bash
   sudo lb build
   ```

This process will generate a live ISO image that you can customize further by editing configuration files or adding packages as per your requirements.

### Key Files and Directories:

- **config/package-lists/**: You can place custom package lists here to include specific software in the build.
- **config/includes.chroot/**: You can add custom files or scripts to be included in the final system.

By ensuring these prerequisites are installed and following the steps above, you'll be able to create a custom Linux distribution using `live-build`.




# 0th Config file

```
#!/bin/sh

set -e

lb config noauto \
    --distribution bookworm \
    --architecture amd64 \
    --debian-installer false \
    --debian-installer-gui false \
    --bootappend-live "boot=live components persistence" \
    --linux-flavours amd64 \
    --iso-publisher "Fusion Flux" \
    --iso-volume "Fusion Flux Live" \
    --iso-application "Fusion Flux AI/ML Distribution" \
    --apt-indices false \
    --firmware-binary true \
    --firmware-chroot true \
    --archive-areas "main contrib non-free non-free-firmware" \
    "${@}"

```

# 1st build (basic)

Creating a custom Linux distribution based on Debian, with the ability to boot from a USB (using tools like Rufus or Ventoy) and install directly from the BIOS like other popular distributions (such as Kali), involves several steps and key configurations. Here’s a breakdown of the major components and steps you'll need to follow:

### 1. **Choose a Base (Debian) Version**
   - Select the correct **Debian base version** (e.g., Debian 11 "Bullseye" or 12 "Bookworm").
   - Make sure to use the **amd64 architecture** as you mentioned.

### 2. **Debian Live Build System**
   - Use **Debian live-build** tools, which are designed for creating live systems and installing them.
     - Install the `live-build` tool to generate the ISO:
       ```bash
       sudo apt-get install live-build
       ```
     - Live-build allows customization of the system, including packages, scripts, and configurations, which you need for the live boot and installation.

### 3. **Configure the Live Boot**
   - The live boot system is essential for creating an image that can be tested in live mode (before installation).
   - Steps:
     1. Create a working directory:
        ```bash
        mkdir custom-linux
        cd custom-linux
        ```
     2. Start the live build process with a minimal Debian system template:
        ```bash
        lb config --architecture amd64
        ```
     3. Customize configurations:
        - Set up **live boot** settings (optional configurations can be added in the `auto/config` file):
          ```bash
          lb config \
          --distribution bullseye \
          --architecture amd64 \
          --debian-installer true \
          --bootappend-live "boot=live components" \
          --iso-publisher "YourLinux v1.0" \
          --iso-volume "YourLinux" \
          --iso-application "YourLinux Live Installer"
          ```
     4. Generate the live image:
        ```bash
        sudo lb build
        ```
     This will create an `.iso` file, which you can use with Rufus or Ventoy to boot into a live session.

### 4. **Include a Debian Installer**
   - To install the OS from the BIOS directly (as is done with Kali Linux), you need to enable the **Debian installer**.
     - You can enable the Debian installer using the `--debian-installer true` option in live-build as shown above.
     - This ensures that your custom OS includes a full installation option alongside the live boot.

### 5. **Custom Packages and Pre-installed Software**
   - Use the `packages.chroot` file to specify the software you want installed in the live system (and also installed post-install).
   - Example: Add specific software packages to the live system like this:
     ```bash
     echo "kali-linux-default" >> config/package-lists/custom.list.chroot
     echo "gnome-core" >> config/package-lists/custom.list.chroot
     echo "curl" >> config/package-lists/custom.list.chroot
     ```

### 6. **Custom Branding (Optional)**
   - Add custom logos, backgrounds, and boot menus.
   - Modify the boot menu using GRUB configuration in `/config/bootloaders/grub` or the `grub-pc` package for BIOS compatibility.

### 7. **BIOS Compatibility**
   - Make sure your ISO is **hybrid** (so it works for both BIOS and UEFI systems). You can achieve this by ensuring your `lb config` command uses the `--debian-installer true` option.
   - Hybrid ISO configurations will make the boot media compatible across different systems, including BIOS and UEFI boot modes.
   - Verify the ISO can be booted using Rufus and Ventoy in both **MBR and GPT** partition schemes.

### 8. **Persistent Storage (Optional)**
   - If you want the live boot environment to support **persistence** (i.e., save changes to the USB), enable persistence via custom configurations:
     - Modify the boot command line (in `syslinux` or `grub`):
       ```bash
       boot=live components persistence
       ```
     - The persistence file or partition needs to be named properly (e.g., `persistence.conf` in the root of the USB drive).

### 9. **Testing and Debugging**
   - Test your custom live image on **virtual machines** like VirtualBox or QEMU.
   - Boot the ISO with tools like Rufus, Ventoy, or BalenaEtcher to verify it works both in **live mode** and **installation mode**.
   - Ensure that the system installs correctly and that custom packages/software are properly configured post-installation.

### 10. **Optional Tools for Simplified Building**
   - **Refracta Tools**: If live-build feels complex, you can use **Refracta** tools. They simplify the process of creating a live system and installer. These tools can create a live ISO and provide an easy-to-use graphical installer.

     Install Refracta Tools:
     ```bash
     sudo apt-get install refractasnapshot refractainstaller refractainstaller-base
     ```

### 11. **ISO Testing and Finalization**
   - Ensure the ISO is well-tested on multiple devices with different BIOS and UEFI settings.
   - Verify boot compatibility on different systems (BIOS/UEFI) using tools like Rufus or Ventoy for creating bootable USBs.

### Additional Considerations:
   - **File system support**: Ensure the system supports ext4, Btrfs, or other file systems commonly used on Linux.
   - **Secure Boot support**: If needed, configure secure boot support for UEFI systems.
   - **Kernel options**: Customize the kernel if specific features or drivers are needed.
   - **Documentation**: Provide good documentation for users who will install your custom distro, especially if it has unique tools or configurations.

### Example of a Customized Command for Building:
```bash
lb config \
--architecture amd64 \
--debian-installer true \
--distribution bullseye \
--bootappend-live "boot=live components persistence" \
--iso-application "Custom Linux OS" \
--iso-publisher "YourOS Publisher" \
--iso-volume "YourOS Installer" \
--debian-installer true \
--mirror-bootstrap "http://deb.debian.org/debian/" \
--archive-areas "main contrib non-free"
```

This process will create a Debian-based custom ISO with live boot and installation options, BIOS/UEFI compatibility, and custom software configurations.


# 2nd via prompt

To create a custom Linux distribution based on **Debian 12 "Bookworm"** using the **live-build tool**, tailored for AI, ML/DS engineers, and using the **i3 window manager** without a desktop environment, here’s how you can go about it. You also want the installer to be **Calamares**, with **USB persistence** support and custom branding replacing **Debian** with the name **Fusion Flux**.

Below are the detailed steps to guide you through the process:

---

## 1. **Install Required Tools**

First, you need to install the necessary tools on your build machine (which should ideally be a Debian 12 "Bookworm" system):

```bash
sudo apt update
sudo apt install live-build calamares git
```

- `live-build`: Tool for building live systems (ISO images).
- `calamares`: A modular installer framework.

## 2. **Set Up the Build Directory**

Create a new directory for your custom distribution:

```bash
mkdir fusion-flux
cd fusion-flux
```

## 3. **Configure Live Build**

You'll need to configure `live-build` to create your base system with i3, custom branding, persistence, and other features.

### **Base Configuration Command:**
Run the following command to set the basic options for the live-build system:

```bash
lb config \
--distribution bookworm \
--architecture amd64 \
--debian-installer false \
--debian-installer-gui false \
--bootappend-live "boot=live components persistence" \
--linux-flavours amd64 \
--iso-publisher "Fusion Flux" \
--iso-volume "Fusion Flux Live" \
--iso-application "Fusion Flux AI/ML Distribution" \
--apt-indices false \
--firmware-binary true \
--firmware-chroot true \
--archive-areas "main contrib non-free"
```

Here’s what each option does:
- **`--distribution bookworm`**: Specifies the Debian 12 Bookworm base.
- **`--architecture amd64`**: Sets 64-bit architecture.
- **`--bootappend-live "boot=live components persistence"`**: Enables persistence.
- **`--debian-installer false`**: Disables the default Debian installer (you'll be using Calamares instead).
- **`--firmware-binary` and `--firmware-chroot`**: Ensures firmware is available for hardware support.
- **`--archive-areas "main contrib non-free"`**: Enables access to additional repositories for non-free and contrib software.

### **Customizing the Build:**

1. **Window Manager Configuration (i3)**
   Create a `config/package-lists/custom.list.chroot` file and add the packages you want preinstalled in the system:

   ```bash
   mkdir -p config/package-lists
   echo "i3" >> config/package-lists/custom.list.chroot
   echo "lightdm" >> config/package-lists/custom.list.chroot  # For a lightweight display manager
   echo "xterm" >> config/package-lists/custom.list.chroot
   echo "git" >> config/package-lists/custom.list.chroot
   echo "python3" >> config/package-lists/custom.list.chroot
   echo "python3-pip" >> config/package-lists/custom.list.chroot
   echo "python3-venv" >> config/package-lists/custom.list.chroot
   echo "jupyterlab" >> config/package-lists/custom.list.chroot
   echo "neovim" >> config/package-lists/custom.list.chroot
   echo "scikit-learn" >> config/package-lists/custom.list.chroot
   echo "tensorflow" >> config/package-lists/custom.list.chroot
   echo "pytorch" >> config/package-lists/custom.list.chroot
   ```

   This list ensures that the **i3 window manager** is installed, alongside AI/ML-related tools (e.g., `scikit-learn`, `tensorflow`, `pytorch`, and Jupyter).

2. **Add Calamares Installer**
   Calamares is a modular and customizable installer used by various Linux distributions.

   - In your `config/package-lists/`, create a list for Calamares:
     ```bash
     echo "calamares" >> config/package-lists/installer.list.chroot
     echo "calamares-settings-debian" >> config/package-lists/installer.list.chroot
     ```

   - To configure Calamares, you need to create custom settings. Create the following directory:
     ```bash
     mkdir -p config/includes.chroot/etc/calamares/modules
     ```

   - You can find default configurations for Calamares modules in the Debian repository. Customize the installer for your distribution’s needs. For example, place the following configuration in the `netinstall.conf` for Calamares:

     ```bash
     echo "
     ---
     name: netinstall
     welcome: true
     pre_install:
         - initramfs-update
     installation:
         - install
         - configure-base
     post_install:
         - initramfs-update
     " >> config/includes.chroot/etc/calamares/modules/netinstall.conf
     ```

3. **Custom Branding (Replace "Debian" with "Fusion Flux")**
   - Replace any **Debian** branding with **Fusion Flux**. This involves replacing logos, system messages, and installer text.
   - Update the GRUB menu and any logos found in `/boot/grub/themes` and `/usr/share/plymouth/themes` to reflect your distribution’s branding.
   - You can customize `/etc/lsb-release` to define the release version:
     ```bash
     echo "DISTRIB_ID=FusionFlux" > config/includes.chroot/etc/lsb-release
     echo "DISTRIB_DESCRIPTION='Fusion Flux AI/ML Distribution'" >> config/includes.chroot/etc/lsb-release
     ```

4. **Persistence Configuration**
   To ensure USB persistence, ensure the **boot command** includes the persistence option (already included in `--bootappend-live`). Additionally, when users create a live USB with persistence, they need to set up a persistence partition named `persistence`.

   - Modify the live boot files to include support for persistence:
     ```bash
     echo "/ union" > config/includes.binary/persistence.conf
     ```

## 4. **Build the ISO**

Once the configuration is ready, build the ISO using the following command:

```bash
sudo lb build
```

This will create a 64-bit `amd64` ISO image in the current directory.

- The build process can take some time depending on the size of the packages you’ve included.
- Check for any errors or missing packages and modify `config/package-lists/custom.list.chroot` as needed.

## 5. **Test Your ISO**

After the build process is complete, you will have a `.iso` file ready for testing.

### Test the ISO in VirtualBox or QEMU:

You can test the live boot and installation process using a virtual machine before trying it on real hardware. If everything works, you can create a bootable USB.

### Create a Bootable USB with Persistence:

Use **Rufus**, **Ventoy**, or **BalenaEtcher** to create a bootable USB from the ISO.

If you are using persistence, make sure to create a second partition on the USB labeled `persistence` and a file named `persistence.conf` with the following content:

```
/ union
```

This will ensure that changes made in the live session (e.g., saved files or installed packages) are persistent.

## 6. **Final Touches**

Once your ISO is fully functional, you may want to:
- Further tweak configurations for the installer.
- Add more advanced AI/ML tools based on feedback from users or your own preferences.
- Ensure all branding elements (logos, texts, etc.) reflect the **Fusion Flux** identity.

---

By following these steps, you will have created a custom **Debian Bookworm**-based Linux distribution named **Fusion Flux**, with i3 preinstalled, **Calamares** as the installer, and **USB persistence**. This distribution will be optimized for AI, ML, and Data Science workflows, and should work smoothly when booted from a USB or installed on a system.


# 3rd firmware error

I understand you're encountering an error while building your Fusion Linux distribution. The error message indicates that the package 'firmware-linux' is not available. This is a common issue when working with Debian-based distributions, especially when dealing with non-free firmware. Let's troubleshoot this step by step:

1. First, ensure that you have the non-free and contrib repositories enabled. In your lb config command, add the following if you haven't already:

   ```
   lb config --distribution bookworm --archive-areas "main contrib non-free non-free-firmware"
   ```

2. The package 'firmware-linux' has been replaced by more specific packages in recent Debian versions. Instead of 'firmware-linux', you should use 'firmware-linux-free' and possibly 'firmware-linux-nonfree'. Update your package list to include these:

   Edit your `config/package-lists/live.list.chroot` file and replace 'firmware-linux' with:

   ```
   firmware-linux-free
   firmware-misc-nonfree
   ```

3. Make sure your system is up to date:

   ```
   sudo apt update
   sudo apt upgrade
   ```

4. Clean your build environment before rebuilding:

   ```
   sudo lb clean
   ```

5. Rebuild your live system:

   ```
   sudo lb build
   ```

If you're still encountering issues, here are a few more things to try:

6. Check if you have the correct sources list. Create or edit the file `config/archives/debian.list.chroot`:

   ```
   deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
   deb http://deb.debian.org/debian-security/ bookworm-security main contrib non-free non-free-firmware
   deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware
   ```

7. If you're behind a proxy, make sure it's correctly configured in your build environment.

8. If the issue persists, you might want to try using a newer version of live-build:

   ```
   sudo apt install live-build/bookworm-backports
   ```

After making these changes, clean and rebuild your system. If you're still facing issues, please provide the full output of the build process, and I'll be happy to help you troubleshoot further.



# test with qemu 

```
qemu-system-x86_64 -cdrom '/home/yash/Desktop/live-image-amd64.hybrid.iso' -boot d -m 3000
```


# building and modififing chroot

Using `chroot` allows you to enter a filesystem environment (in this case, the filesystem of your live-build) and interact with it as if it were the root of your system. This is very useful for testing changes like adding or removing programs without having to rebuild the entire ISO.

Here's a step-by-step guide on how to use `chroot` in the context of a live-build:

### Steps to Use `chroot` with Live-build

1. **Prepare the Build Environment**
   Make sure you have your live-build setup ready, and you have at least done the `lb build` command once to create the base filesystem. If you haven't built the image yet, run:
   ```bash
   lb build
   ```
   This will create a `chroot/` directory in your live-build project where the root filesystem resides.

2. **Entering the `chroot` Environment**
   Once the `chroot` directory is ready, you can enter it:
   ```bash
   sudo chroot path/to/chroot/
   ```
   For example, if you're in your live-build directory, it might be:
   ```bash
   sudo chroot chroot/
   ```
   Now you're inside the filesystem as if it's the root of your system.

3. **Update Package Lists**
   Inside the `chroot`, you’ll want to update the package list to make sure it has access to the latest repositories:
   ```bash
   apt-get update
   ```

4. **Installing Packages**
   You can now install any packages you want to add to the final ISO. For example:
   ```bash
   apt-get install your-package
   ```

5. **Removing Packages**
   Similarly, you can remove packages:
   ```bash
   apt-get remove your-package
   ```

6. **Testing and Configuring**
   You can also modify and test configurations inside the `chroot` environment. You are working within the actual environment that will be part of your live system, so this allows you to test changes immediately.

7. **Exiting the `chroot`**
   Once you're done making changes, you can simply exit the `chroot` environment:
   ```bash
   exit
   ```

8. **Repack the ISO (if needed)**
   If you are satisfied with the changes made in the `chroot`, you can rebuild the binary part of the ISO (not the full rebuild) to integrate the changes:
   ```bash
   lb clean --binary
   lb build
   ```

   This will regenerate the ISO but keep the same base environment, making it faster.

### Additional Notes:
- **Mount proc, sys, and dev**: Some services or scripts inside `chroot` may require access to `/proc`, `/sys`, or `/dev`. You can mount these as follows before entering `chroot`:
   ```bash
   sudo mount -o bind /proc chroot/proc
   sudo mount -o bind /sys chroot/sys
   sudo mount -o bind /dev chroot/dev
   ```
   After you're done, unmount them:
   ```bash
   sudo umount chroot/proc
   sudo umount chroot/sys
   sudo umount chroot/dev
   ```

Using `chroot` allows you to make changes quickly without needing to rebuild the entire image. This can save a lot of time when testing packages or configurations.


# add set users, change os name , and configure calamares


### 1. **Add default username (`fusion`) and password (`fusion`), and make `fusion` user a sudoer**

You can achieve this by editing the configuration of `live-build` to create a user with the required credentials. You'll modify the hooks to add the user and set up sudo permissions.

- Create a `chroot` hook file:
  ```bash
  mkdir -p config/hooks/live
  nano config/hooks/live/01-create-user.hook.chroot
  ```

- Add the following content to create the `fusion` user, set the password, and add it to the `sudo` group:
  ```bash
  #!/bin/bash

  # Add 'fusion' user with password 'fusion'
  useradd -m -s /bin/bash fusion
  echo 'fusion:fusion' | chpasswd

  # Add 'fusion' to sudoers
  echo 'fusion ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/fusion
  chmod 0440 /etc/sudoers.d/fusion
  ```

- Make the hook executable:
  ```bash
  chmod +x config/hooks/live/01-create-user.hook.chroot
  ```

### 2. **Add root user and set the password to `root`**

You can add the `root` password within the same hook created in Step 1 or in a separate hook file.

- In the same hook file (`01-create-user.hook.chroot`), add the following line:
  ```bash
  # Set root password to 'root'
  echo 'root:root' | chpasswd
  ```

### 3. **Change OS name to `fusion` instead of Debian**

To rebrand the OS, you will need to modify certain files that show the OS name.

- Create another hook to replace all occurrences of `Debian` with `fusion`:
  ```bash
  nano config/hooks/live/02-change-os-name.hook.chroot
  ```

- Add the following commands to replace Debian with Fusion in key files:
  ```bash
  #!/bin/bash

  # Change OS name from Debian to fusion
  sed -i 's/Debian/fusion/g' /etc/issue
  sed -i 's/Debian/fusion/g' /etc/os-release
  sed -i 's/Debian/fusion/g' /etc/motd
  ```

- Make the hook executable:
  ```bash
  chmod +x config/hooks/live/02-change-os-name.hook.chroot
  ```

### 4. **Auto-start Calamares installer on booting the live OS**

To automatically start the Calamares installer when the live system boots, you can configure an autostart file or a systemd service.

- Create a file to handle Calamares autostart:
  ```bash
  mkdir -p config/includes.chroot/etc/xdg/autostart/
  nano config/includes.chroot/etc/xdg/autostart/calamares.desktop
  ```

- Add the following content to auto-start Calamares:
  ```bash
  [Desktop Entry]
  Type=Application
  Exec=calamares
  Hidden=false
  NoDisplay=false
  X-GNOME-Autostart-enabled=true
  Name=Calamares Installer
  Comment=Start Calamares Installer
  ```

### 5. **Remove Calamares installer after installing the distribution**

Once the OS is installed, you will want to remove Calamares from the target system (the installed system). You can create a post-installation script for this purpose.

- Create a new hook to remove Calamares after installation:
  ```bash
  nano config/hooks/post/03-remove-calamares.hook.postinst
  ```

- Add the following content to the hook to remove Calamares after the installation process:
  ```bash
  #!/bin/bash

  # Remove Calamares after installation
  apt-get purge --yes calamares
  ```

- Make the hook executable:
  ```bash
  chmod +x config/hooks/post/03-remove-calamares.hook.postinst
  ```

### Building the Live ISO

Once you have completed all these customizations, you can build your custom Linux distribution using the `live-build` tool.

- First, ensure everything is set up correctly, then start the build process:
  ```bash
  sudo lb build
  ```

This will generate the ISO for your custom Linux distribution with all the changes.

---

### Summary of Changes

1. **User Setup:**
   - `fusion` user is created with sudo privileges.
   - `root` user is set up with the password `root`.

2. **OS Branding:**
   - OS name is changed from `Debian` to `fusion`.

3. **Installer Autostart:**
   - Calamares installer is set to autostart when the live system boots.

4. **Post-Installation Cleanup:**
   - Calamares is removed from the system after installation to prevent it from being present in the installed system.

This setup allows you to fully customize the live distribution as per your requirements!