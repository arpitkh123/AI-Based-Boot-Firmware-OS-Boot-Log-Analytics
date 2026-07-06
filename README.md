# AI-Based Boot Firmware and OS Boot Log Analytics

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Program](https://img.shields.io/badge/HPE-CPP--3-00B188)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%203B%2B-red)

> Intelligent, automated analysis of multi-stage embedded boot logs — from firmware initialization to kernel startup to OS service launch — for faster failure diagnosis and performance insight.

## About the Project

Modern embedded systems boot through several distinct stages — **firmware/bootloader initialization → kernel startup → OS service initialization** — and each stage generates its own stream of log data. When a boot fails or behaves abnormally, pinpointing *which* stage failed, *what kind* of failure it was, and *why* it happened, currently means manually scanning through large, dense, and inconsistently formatted log files. This is slow, error-prone, and doesn't scale as systems and deployments grow.

This project builds an **AI-based boot log analytics system** that ingests logs from every boot stage, automatically classifies failures and anomalies, and surfaces clear, actionable insights — including the likely root cause, the affected stage, and stage-wise performance metrics — turning hours of manual log-diving into minutes of guided diagnosis.

## Key Features

- **Multi-Stage Parsing**: Parses and correlates logs across multiple boot stages: firmware, bootloader, kernel, and OS services.
- **Hybrid Anomaly Detection**: Combines deterministic rule checking against an offline Knowledge Base with unsupervised Machine Learning (Isolation Forest) on log templates.
- **Probable Root Cause Identification**: Identifies probable root causes and provides detailed hardware/firmware resolution procedures for failed or delayed boot stages.
- **Boot Metrics Tracking**: Tracks stage-wise boot time and flags performance bottlenecks across boot cycles.
- **Baseline Comparison**: Detects abnormal patterns by comparing logs against historical "healthy boot" baselines.
- **Guided Diagnosis**: Presents findings through a clear, human-readable React-based dashboard instead of raw log dumps, with natural-language report generation powered by LLMs.

## Hardware Requirements

**Target device under test:** Raspberry Pi 3B+

| Component | Purpose |
|---|---|
| Raspberry Pi 3B+ | Embedded target whose boot logs are captured and analyzed |
| microSD card (32 GB+) | Hosts the Pi's bootloader and OS |
| 5V / 2.5A USB power supply | Stable power for repeated boot cycles |
| USB-to-TTL Serial (UART) cable | Captures firmware/bootloader logs over GPIO pins 8 & 10 from the earliest point of boot, before the network is available |
| HDMI monitor | Display output for direct interaction with the Raspberry Pi |
| Keyboard + Mouse | For direct input and interaction with the Raspberry Pi |

## Tech Stack

- **Language:** Python
- **Hybrid Analytics Engine**:
  - **Offline Knowledge-Base (KB) Engine**: Deterministic pattern matching using a signature database ([knowledge_base.json](file:///d:/yaya/HPE_CPP-3/ml-implementation/AI-Based-Boot-Firmware-OS-Boot-Log-Analytics/data/knowledge_base.json)) to resolve known firmware, memory, storage, and kernel crash signatures.
  - **Isolation Forest Model**: Unsupervised ML model trained on extracted log feature vectors to flag statistical anomalies and sequential variations.
  - **Confidence Fusion Engine**: Integrates KB matches, ML prediction confidence, log template counts, and boot milestones to output a weighted anomaly strength score.
- **Feature Engineering & Mining**:
  - **Template Extractor (Drain3)**: Clusters log messages into templates to reduce raw log dimensionality and map structural log trends.
  - **Feature Builder**: Constructs numeric features from log severity distributions, subsystem frequencies, boot duration, and milestone completion.
- **Web Application Stack**:
  - **Backend**: FastAPI (Python) hosting analytics API endpoints and routing parsing and AI inference requests.
  - **Frontend**: React (Vite, TypeScript, TailwindCSS) providing an interactive analytics dashboard, historical log viewer, and comparative charts.
  - **Database**: SQLite (SQLAlchemy ORM) storing analysis reports and run histories.
- **LLM Integration**: Integrates Large Language Models (Gemini/Vertex AI APIs) to summarize complex failure vectors and generate targeted, plain-text recovery instructions when offline resolutions require broader context.
- **Data Handling**: Pandas, NumPy, Scikit-learn.
- **Log Sources**: U-Boot/firmware logs, Linux kernel `dmesg`, `systemd`/`journalctl` service logs.

## How It Works

1. **Capture** — Boot logs are collected from the target Raspberry Pi 3B+ at each stage (firmware/bootloader via UART serial console, and kernel via `dmesg`).
2. **Preprocess & Parse** — Raw logs are normalized and parsed (timestamp, boot stage, severity, messages) into structured streams.
3. **Analyze & Extract** — Log messages are clustered into structural templates via Drain3. The system maps boot milestones (kernel started, rootfs mounted, systemd init loaded) and builds a numeric feature vector representing the boot cycle.
4. **Detect & Match**:
   - The log stream is matched against the **Knowledge-Base Engine**. If a matching signature (such as a kernel panic or SD card read timeout) is hit, it immediately retrieves pre-configured recovery resolutions.
   - The feature vector is passed to the **Isolation Forest Model** to check for statistical deviations against healthy boot baselines.
5. **Confidence Fusion** — The outputs of both engines are combined along with boot success metadata, severity summaries, and template similarities to calculate a final confidence/severity score.
6. **Report** — If a known signature is matched, the KB resolution is outputted immediately. Otherwise, the results are processed by the LLM explainer to generate a natural-language report, surfaced directly on the React dashboard.

## Error and Fault Injection Methodology

To validate the classification and anomaly detection accuracy of our Hybrid Engine, we systematically injected failures across different boot stages of the Raspberry Pi 3B+:

### 1. Device Tree Overlay (DTO) Failures
- **Method**: Modifying `/boot/config.txt` to apply invalid or mismatched device tree overlays.
- **Injected Faults**:
  - Specifying invalid target phandles or missing nodes in fragment targets.
  - Feeding mismatched parameter types to overlay properties (e.g. integer parameters configured as strings).
- **Resulting Log Signature**: `platform 3f215040.serial: probe of 3f215040.serial failed with error -22` or `error -EINVAL: unable to register 8250 port`.

### 2. Kernel Boot Argument (bootargs) Corruptions
- **Method**: Intentionally introducing typos and syntax issues into `cmdline.txt` (or U-Boot's `bootargs` variable).
- **Injected Faults**:
  - Adding whitespace within configuration tokens (e.g. `console=ttyS0, 115200` instead of `console=ttyS0,115200`).
  - Specifying an invalid root block device (e.g. `root=/dev/mmcblk0p3` instead of `/dev/mmcblk0p2`).
- **Resulting Log Signature**: `Warning: unable to open an initial console` or `Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(179,3)`.

### 3. Boot Asset Tampering
- **Method**: Deleting or renaming critical files located on the FAT boot partition.
- **Injected Faults**:
  - Renaming/removing the Device Tree Blob (DTB) (`bcm2710-rpi-3-b-plus.dtb`).
  - Corrupting or renaming the kernel image (`kernel8.img` / `kernel7.img`).
- **Resulting Log Signature**: U-Boot output: `no bootable image found` or standard Broadcom bootloader watchdog resets.

### 4. Filesystem Corruption Simulation
- **Method**: Introducing software-level failures within the ext4 root filesystem.
- **Injected Faults**:
  - Truncating or deleting `/sbin/init` or critical systemd binaries.
  - Forcing dirty shutdowns or corrupting metadata blocks on the ext4 journal.
- **Resulting Log Signature**: `Kernel panic - not syncing: Attempted to kill init! exitcode=0x00000100` or system-wide systemd service crashes.

## Project Status

This project is under active development as part of the HPE CPP-3 program. The features and architecture above reflect the current scope and will evolve as development progresses.

## Acknowledgement

This project has been developed as part of the **HPE CPP-3 program**, under the guidance and mentorship of **Mr. Arunachalam Somasundaram** (HPE Mentor) and **Mr. Ankur Raj** (JECRC University Mentor). We sincerely thank both our mentors for their continuous guidance and support, and HPE for the opportunity and resources extended throughout this project.

## Team Members

1. Arpit Khandelwal
2. Vrinda Sharma
3. Nishtha Kasliwal
4. Yug Borana
5. Priyansh Porwal
