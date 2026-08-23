"""
Canonical Raspberry Pi / Linux Boot Events.

This file acts as the single source of truth for the
Boot Event Engine.

Every boot stage, parser, feature builder,
dashboard and ML model should reference these
constants instead of hardcoding event names.
"""

BOOT_EVENTS = {

    # --------------------------------------------------
    # Bootloader
    # --------------------------------------------------

    "UBOOT_START": {
        "stage": "UBOOT",
        "description": "U-Boot execution started."
    },

    "KERNEL_LOAD": {
        "stage": "UBOOT",
        "description": "Linux kernel image loaded."
    },

    "DTB_LOAD": {
        "stage": "UBOOT",
        "description": "Device Tree loaded."
    },

    # --------------------------------------------------
    # Kernel
    # --------------------------------------------------

    "KERNEL_START": {
        "stage": "KERNEL",
        "description": "Linux kernel started."
    },

    "MEMORY_INIT": {
        "stage": "KERNEL",
        "description": "Memory initialization."
    },

    "CPU_INIT": {
        "stage": "KERNEL",
        "description": "CPU initialization."
    },

    "IRQ_INIT": {
        "stage": "KERNEL",
        "description": "Interrupt controller initialization."
    },

    "DMA_INIT": {
        "stage": "KERNEL",
        "description": "DMA initialization."
    },

    "DRIVER_INIT": {
        "stage": "KERNEL",
        "description": "Kernel driver initialization."
    },

    "USB_INIT": {
        "stage": "KERNEL",
        "description": "USB subsystem initialization."
    },

    "NETWORK_INIT": {
        "stage": "KERNEL",
        "description": "Network subsystem initialization."
    },

    # --------------------------------------------------
    # Filesystem
    # --------------------------------------------------

    "ROOTFS_MOUNT": {
        "stage": "FILESYSTEM",
        "description": "Root filesystem mounted."
    },

    # --------------------------------------------------
    # Userspace
    # --------------------------------------------------

    "INIT_START": {
        "stage": "INIT",
        "description": "Init process started."
    },

    "SYSTEMD_START": {
        "stage": "INIT",
        "description": "systemd started."
    },

    "LOGIN_PROMPT": {
        "stage": "LOGIN",
        "description": "Login prompt displayed."
    },

    "BOOT_COMPLETE": {
        "stage": "LOGIN",
        "description": "Boot completed successfully."
    }
}