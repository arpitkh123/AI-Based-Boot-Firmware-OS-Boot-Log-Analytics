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



# Boot - Related Logs
# ==========================================================
# BOOT PARSER CONFIGURATION
# ==========================================================

KERNEL_START_KEYWORDS = [
    "booting linux",
    "linux version",
    "starting kernel",
]

ROOTFS_KEYWORDS = [
    "mounted root",
    "vfs: mounted root",
    "ext4-fs",
    "root filesystem",
    "rootfs",
]

INIT_KEYWORDS = [
    "run /sbin/init as init process",
    "/sbin/init",
    "busybox",
    "init process",
]

LOGIN_KEYWORDS = [
    "login:",
    "busybox login",
    "please press enter to activate this console",
    # "#",
    # "$",
]

BOOT_SUCCESS_KEYWORDS = [
    "boot successful!",
]

BOOT_FAILURE_KEYWORDS = [
    "kernel panic",
    "oops",
    "unable to mount root fs",
    "unable to mount root filesystem",
    "no init found",
    "segmentation fault",
    "fatal exception",
    "system halted",
]

KERNEL_PANIC_KEYWORDS = [
    "kernel panic",
    "oops",
    "call trace",
    "stack trace",
    "fatal exception",
]

# ==========================================================
# HARDWARE INITIALIZATION
# ==========================================================

HARDWARE_INIT_KEYWORDS = [
    "acpi",
    "pci",
    "nvme",
    "ahci",
    "usb device found",
    "new high speed",
    "new low speed",
    "manufacturer:",
    "product:",
    "detected vipt",
]

# ==========================================================
# DRIVER / MODULE EVENTS
# ==========================================================

MODULE_DRIVER_KEYWORDS = [
    "loading",
    "insmod",
    "firmware: direct-loading",
    "driver registered",
    "registered new interface driver",
]

MODULE_DRIVER_FAILURE_KEYWORDS = [
    "failed",
    "probe failed",
    "unable to register",
    "failed to load",
    "error -",
    "module not found",
]

# ==========================================================
# NETWORK EVENTS
# ==========================================================

NETWORK_INIT_KEYWORDS = [
    "link is up",
    "link is down",
    "configuring for phy",
    "dhcp",
    "ip address",
    "network unreachable",
    "no carrier",
    "timed out",
    "eth0",
    "lan78xx",
]

# ==========================================================
# SYSTEMD / SERVICE EVENTS
# (Useful for Ubuntu, RHEL, HPE Servers)
# ==========================================================

SYSTEMD_SERVICE_KEYWORDS = [
    "reached target",
    "starting",
    "started",
    "activating",
    "dependency failed",
    "timeout",
    "service",
]

# ==========================================================
# CRITICAL WARNINGS
# ==========================================================

CRITICAL_WARNING_KEYWORDS = [
    "out of memory",
    "oom-killer",
    "i/o error",
    "corruption",
    "read-only",
    "warning",
    "stack trace",
    "filesystem error",
    "segmentation fault",
]

# ==========================================================
# FILESYSTEM FAILURES
# ==========================================================

FILESYSTEM_ERROR_KEYWORDS = [
    "unable to mount root fs",
    "unable to mount root filesystem",
    "ext4-fs error",
    "vfs error",
    "i/o error",
    "read-only filesystem",
    "filesystem corruption",
]

# ==========================================================
# UART FAILURES
# ==========================================================

UART_ERROR_KEYWORDS = [
    "unable to register 8250 port",
    "probe failed",
    "tty error",
    "uart error",
    "serial error",
]

# ==========================================================
# MEMORY FAILURES
# ==========================================================

MEMORY_ERROR_KEYWORDS = [
    "out of memory",
    "oom-killer",
    "memory corruption",
    "dma error",
    "allocation failure",
]