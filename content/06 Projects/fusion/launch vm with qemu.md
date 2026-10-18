---
title: launch vm with qemu
tags: [projects, fusion]
type: "project-note"
area: "projects"
topic: "fusion"
status: "unreviewed"
source: "obsidian"
---

qemu-system-x86_64 \
  -enable-kvm \
  -m 4096 \
  -smp 2 \
  -boot d \
  -cdrom live-image-amd64.hybrid.iso \
  -net nic -net user


