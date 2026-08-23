"""
Boot Event Detection Patterns.

Maps raw log messages to canonical boot events.

This file contains detection rules only.

The Boot Event Engine uses these rules to generate
a boot timeline.
"""

BOOT_EVENT_PATTERNS = {

    # ============================================================
    # Bootloader
    # ============================================================

    "UBOOT_START": {

        "stage": "UBOOT",
        "previous_stage": None,

        "patterns": [

            "u-boot",

            "starting kernel",

            "bootloader"
        ]
    },

    "KERNEL_LOAD": {

        "stage": "UBOOT",
        "previous_stage": "UBOOT",

        "patterns": [

            "loading kernel",

            "kernel image",

            "starting kernel"
        ]
    },

    "DTB_LOAD": {

        "stage": "UBOOT",
        "previous_stage": "UBOOT",

        "patterns": [

            "device tree",

            "fdt",

            "dtb"
        ]
    },

    # ============================================================
    # Kernel
    # ============================================================

    "KERNEL_START": {

        "stage": "KERNEL",
        "previous_stage": "UBOOT",

        "patterns": [

            "booting linux",

            "linux version"
        ]
    },

    "MEMORY_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",


        "patterns": [

            "memory:",

            "reserved memory",

            "cma",

            "mem:"
        ]
    },

    "CPU_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "cpu features",

            "smp",

            "booted secondary processor",

            "detected vipt"
        ]
    },

    "IRQ_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "irq",

            "irqchip"
        ]
    },

    "DMA_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "dma:"
        ]
    },

    "DRIVER_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "driver",

            "registered",

            "loading"
        ]
    },

    "USB_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "usb",

            "usbcore"
        ]
    },

    "NETWORK_INIT": {

        "stage": "KERNEL",
        "previous_stage": "KERNEL",

        "patterns": [

            "eth0",

            "lan78xx",

            "network",

            "link is up"
        ]
    },

    # ============================================================
    # Filesystem
    # ============================================================

    "ROOTFS_MOUNT": {

        "stage": "FILESYSTEM",
        "previous_stage": "KERNEL",

        "patterns": [

            "mounted root",

            "root filesystem",

            "vfs"
        ]
    },

    # ============================================================
    # Userspace
    # ============================================================

    "INIT_START": {

        "stage": "INIT",
        "previous_stage": "FILESYSTEM",

        "patterns": [

            "run /init",

            "systemd",

            "starting"
        ]
    },

    "LOGIN_PROMPT": {

        "stage": "LOGIN",
        "previous_stage": "INIT",

        "patterns": [

            "login:",

            "raspberrypi login",

            "ubuntu login",

            "debian login"
        ]
    },

    "BOOT_COMPLETE": {
        
        "stage": "LOGIN",
        "previous_stage": "LOGIN",

        "patterns": [

            "boot successful",

            "login:"
        ]
    }

}