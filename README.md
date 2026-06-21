# AI-Based Boot Firmware and OS Boot Log Analytics

![Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Program](https://img.shields.io/badge/HPE-CPP--3-00B188)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%203B%2B-red)

> Intelligent, automated analysis of multi-stage embedded boot logs — from firmware initialization to kernel startup to OS service launch — for faster failure diagnosis and performance insight.

## About the Project

Modern embedded systems boot through several distinct stages — **firmware/bootloader initialization → kernel startup → OS service initialization** — and each stage generates its own stream of log data. When a boot fails or behaves abnormally, pinpointing *which* stage failed, *what kind* of failure it was, and *why* it happened, currently means manually scanning through large, dense, and inconsistently formatted log files. This is slow, error-prone, and doesn't scale as systems and deployments grow.

This project builds an **AI-based boot log analytics system** that ingests logs from every boot stage, automatically classifies failures and anomalies, and surfaces clear, actionable insights — including the likely root cause, the affected stage, and stage-wise performance metrics — turning hours of manual log-diving into minutes of guided diagnosis.

## Key Features

- Parses and correlates logs across multiple boot stages: firmware, bootloader, kernel, and OS services.
- Automatically classifies boot failures and anomalies using ML/NLP-based log analysis.
- Identifies probable root causes for failed or delayed boot stages.
- Tracks stage-wise boot time and flags performance bottlenecks across boot cycles.
- Detects abnormal patterns by comparing logs against historical "healthy boot" baselines.
- Presents findings through a clear, human-readable dashboard instead of raw log dumps.

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
- **ML Models:** LSTM (to learn sequential patterns in boot logs and pick up on failure trends over time) and Isolation Forest (for unsupervised anomaly detection on log data)
- **Frontend:** React (for the analytics dashboard)
- **LLM Integration:** The structured output produced by the ML models is sent via an API request to a Large Language Model (LLM), which converts it into a clear, plain-text summary that's easy for engineers to read and act on
- **Data Handling:** Pandas, NumPy
- **Log Sources:** U-Boot/firmware logs, Linux kernel `dmesg`, `systemd`/`journalctl` service logs

*(This stack reflects the current direction and will be updated as implementation progresses.)*

## How It Works

1. **Capture** — Boot logs are collected from the Raspberry Pi at each stage: firmware/bootloader via UART serial console and kernel via `dmesg`.
2. **Preprocess** — Raw logs are cleaned, parsed, and structured into a consistent format (timestamp, boot stage, severity, message).
3. **Analyze** — ML/NLP models classify each entry as normal or anomalous, detect failure patterns, and compute stage-wise timing.
4. **Report** — Results are presented on a dashboard highlighting failed stages, anomaly types, root-cause hints, and performance trends across boot cycles.

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