# Live-build Documentation for Nanite Project

## Overview
Live-build is a set of scripts used to build Debian Live systems. It's the official tool for creating custom Debian-based distributions and is maintained by the Debian Live team.

## Installation

To install live-build on a Debian system:

```bash
sudo apt-get update
sudo apt-get install live-build
```

## Basic Workflow

The basic workflow for creating a custom Debian Live system consists of:

1. **Create a build directory**:
   ```bash
   mkdir nanite-build && cd nanite-build
   ```

2. **Configure the build**:
   ```bash
   lb config
   ```

3. **Build the image**:
   ```bash
   sudo lb build
   ```

## Build Stages

The build process is divided into four main stages:

1. **Bootstrap Stage**: Initial phase of populating the chroot directory with packages to make a barebones Debian system.

2. **Chroot Stage**: Completes the construction of the chroot directory, populating it with all packages listed in the configuration and other materials. Most customization occurs in this stage.

3. **Binary Stage**: Builds a bootable image, using the contents of the chroot directory to construct the root filesystem for the Live system.

4. **Source Stage**: If enabled, builds a source tarball after the live image is built.

## Configuration Structure

Live-build uses a configuration directory structure under `config/`:

- `config/bootstrap/`: Configuration for the bootstrap stage
- `config/chroot/`: Configuration for the chroot stage
- `config/binary/`: Configuration for the binary stage
- `config/source/`: Configuration for the source stage

## Key Configuration Files

- **Package Lists**: `config/package-lists/*.list.chroot` - Define packages to include
- **Hooks**: 
  - `config/hooks/live/*.hook.chroot` - Scripts run during the chroot stage
  - `config/hooks/live/*.hook.binary` - Scripts run during the binary stage
- **Includes**: 
  - `config/includes.chroot/` - Files to include in the live system
  - `config/includes.binary/` - Files to include in the binary image

## Image Types

Live-build can create several types of images:

1. **ISO Hybrid**: Most versatile, can be used on virtual machines, optical media, or USB drives
   ```bash
   lb config --binary-images iso-hybrid
   ```

2. **HDD**: For specific use cases, creates a disk image
   ```bash
   lb config --binary-images hdd
   ```

3. **Netboot**: For network booting
   ```bash
   lb config --binary-images netboot
   ```

## Customization Options

### Build-time vs. Boot-time Configuration

- **Build-time options**: Applied during image creation
- **Boot-time options**: Applied when the live system boots
  - Early boot options: Applied by `live-boot` package
  - Later boot options: Applied by `live-config` package

### Package Selection

To specify custom package lists:

```bash
echo "package1 package2 package3" > config/package-lists/custom.list.chroot
```

### Custom Content

To include custom files in the live system:

```bash
mkdir -p config/includes.chroot/path/to/destination
cp /path/to/source/file config/includes.chroot/path/to/destination/
```

### Custom Scripts (Hooks)

To run custom scripts during build:

```bash
mkdir -p config/hooks/live
cat > config/hooks/live/custom.hook.chroot << EOF
#!/bin/sh
# Custom script to run during chroot stage
echo "Running custom hook"
# Add your commands here
EOF
chmod +x config/hooks/live/custom.hook.chroot
```

## Advanced Configuration

### Preseed Files

For automated installations:

```bash
mkdir -p config/includes.installer
cp preseed.cfg config/includes.installer/
```

### Boot Parameters

To set default boot parameters:

```bash
lb config --bootappend-live "boot=live components locales=en_US.UTF-8"
```

## Best Practices

1. **Start Simple**: Begin with a minimal configuration and add features incrementally
2. **Version Control**: Keep your configuration in a version control system
3. **Test Frequently**: Build and test images frequently to catch issues early
4. **Document Changes**: Document all customizations for future reference
5. **Use Auto Scripts**: For reproducible builds, use auto scripts to apply configuration changes

## Troubleshooting

- Check build logs in `binary.log`
- For failed builds, examine the state of the chroot directory
- Use `lb clean` to clean up before rebuilding
- For specific package issues, try installing them manually in the chroot environment

## References

- [Debian Live Manual](https://live-team.pages.debian.net/live-manual/html/live-manual/index.en.html)
- [Live-build Examples](https://live-team.pages.debian.net/live-manual/html/live-manual/examples.en.html)
