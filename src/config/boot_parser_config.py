
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



BOOT_STAGE_PATTERNS = {
    "UBOOT": [
        "U-Boot",
        "Hit any key to stop autoboot",
        "=>",
        "Loading",
        "Bad Linux",
        "Wrong Image Format",
        "device tree",
        "DTB",
        "booti",
        "bootm",
        "bootz"
    ],

    "KERNEL": [
        "Booting Linux",
        "Linux version",
        "Kernel command line",
        "CPU:",
        "Memory:",
        "VFS:",
        "Freeing unused kernel memory"
    ],

    "INIT": [
        "Run /init",
        "Starting init",
        "init:",
        "systemd",
        "BusyBox"
    ],

    "LOGIN": [
        "login:",
        "login successful",
        "Welcome",
        "Password:",
        "Last login",
        "Boot Successful!"
    ]
}






# =============================================================================
# Failure Detection Keywords
# =============================================================================

IRQ_FAILURE_KEYWORDS = [
    "irqchip: unreachable",
    "irq mismatch",
    "failed to request irq",
    "unable to handle irq",
    "no irq domain",
    "irq initialization failed",
    "unexpected irq"
]

DMA_FAILURE_KEYWORDS = [
    "dma allocation failed",
    "failed to allocate dma",
    "cma allocation failed",
    "dma mapping error",
    "out of dma memory",
    "dma init failed"
]

ROOTFS_FAILURE_KEYWORDS = [
    "unable to mount root fs",
    "cannot open root device",
    "vfs: unable to mount root fs",
    "kernel panic - not syncing: vfs",
    "wrong root partition",
    "root device not found"
]

DTB_FAILURE_KEYWORDS = [
    "missing dtb",
    "wrong dtb",
    "bad dtb",
    "unable to load dtb",
    "device tree blob",
    "fdt error",
    "could not find dtb"
]

OOM_KEYWORDS = [
    "oom-killer",
    "out of memory",
    "killed process",
    "memory exhausted",
    "cannot allocate memory"
]

INIT_FAILURE_KEYWORDS = [
    "no working init found",
    "failed to execute /init",
    "requested init failed",
    "init process exited",
    "kernel panic - not syncing: no working init found"
]

CPU_FAILURE_KEYWORDS = [
    "failed to boot secondary cpu",
    "secondary processor failed",
    "cpu bringup failed",
    "unable to start cpu",
    "cpu stalled",
    "cpu panic"
]

FILESYSTEM_FAILURE_KEYWORDS = [
    "ext4-fs error",
    "filesystem corruption",
    "journal checksum error",
    "superblock error",
    "read-only file system",
    "i/o error",
    "failed to mount filesystem"
]







# =============================================================================
# Failure Priority
#
# Highest priority failures appear first.
# The parser reports the first detected failure as the primary root cause.
# =============================================================================

FAILURE_PRIORITY = [

    {
        "name": "DTB_FAILURE",
        "keywords": DTB_FAILURE_KEYWORDS,
        "reason": "Device Tree Blob (DTB) could not be loaded."
    },

    {
        "name": "ROOTFS_FAILURE",
        "keywords": ROOTFS_FAILURE_KEYWORDS,
        "reason": "Root filesystem could not be mounted."
    },

    {
        "name": "INIT_FAILURE",
        "keywords": INIT_FAILURE_KEYWORDS,
        "reason": "Init process could not be started."
    },

    {
        "name": "DMA_FAILURE",
        "keywords": DMA_FAILURE_KEYWORDS,
        "reason": "DMA allocation failed."
    },

    {
        "name": "IRQ_FAILURE",
        "keywords": IRQ_FAILURE_KEYWORDS,
        "reason": "Interrupt initialization failed."
    },

    {
        "name": "CPU_FAILURE",
        "keywords": CPU_FAILURE_KEYWORDS,
        "reason": "CPU initialization failed."
    },

    {
        "name": "FILESYSTEM_FAILURE",
        "keywords": FILESYSTEM_FAILURE_KEYWORDS,
        "reason": "Filesystem corruption or I/O failure detected."
    },

    {
        "name": "OOM",
        "keywords": OOM_KEYWORDS,
        "reason": "Out Of Memory condition detected."
    },

    {
        "name": "KERNEL_PANIC",
        "keywords": KERNEL_PANIC_KEYWORDS,
        "reason": "Kernel panic detected."
    },

    {
        "name": "UART_ERROR",
        "keywords": UART_ERROR_KEYWORDS,
        "reason": "UART registration or pin control failure detected."
    },
]