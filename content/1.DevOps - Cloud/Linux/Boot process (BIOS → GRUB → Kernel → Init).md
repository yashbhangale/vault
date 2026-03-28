Linux boot starts with BIOS/UEFI initializing hardware, then GRUB loads the kernel and initramfs, the kernel initializes the system, and finally systemd starts all user-space services.

Power ON
   ↓
BIOS/UEFI
   ↓
GRUB (Bootloader)
   ↓
Kernel (vmlinuz + initramfs)
   ↓
Init (systemd)
   ↓
Login Screen / Shell

