SEVERITY_KEYWORDS = {
        "ERROR": [
            "error",
            "failed",
            "failure",
            "panic",
            "unable",
            "denied",
            "exception",
            "segfault",
            "fault",
            "critical",
        ],
        "WARNING": [
            "warning",
            "warn",
            "not found",
            "deprecated",
            "retry",
            "timeout",
        ],
        "SUCCESS": [
            "boot successful",
            "mounted",
            "started",
            "registered",
            "link is up",
            "online",
            "initialized",
            "detected",
        ],
    }

SUBSYSTEM_KEYWORDS = {
    "UART": [
        "uart",
        "tty",
        "serial",
    ],
    "NETWORK": [
        "eth",
        "network",
        "dhcp",
        "lan",
        "ipv4",
        "ipv6",
    ],
    "FILESYSTEM": [
        "ext4",
        "vfs",
        "filesystem",
        "mount",
        "rootfs",
        "mmcblk",
    ],
    "USB": [
        "usb",
        "keyboard",
        "mouse",
        "hub",
    ],
    "MEMORY": [
        "memory",
        "ram",
        "dma",
        "cache",
    ],
    "BOOT": [
        "boot",
        "init",
        "rcs",
        "/sbin/init",
    ],
}