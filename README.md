# AlbionMonitor 📊

![Monitor](https://github.com/SEU_USUARIO/AlbionMonitor/actions/workflows/monitor.yml/badge.svg)
![Coverage](https://github.com/SEU_USUARIO/AlbionMonitor/actions/workflows/coverage.yml/badge.svg)

AlbionMonitor is a market analysis tool for [Albion Online](https://albiononline.com/), built in Python. It monitors item prices via the public Albion API and sends alerts via Telegram for arbitrage opportunities and price trends.

---

## 🚀 Features

- Detects arbitrage opportunities between cities
- Sends Telegram alerts with detailed price breakdowns and trend charts
- Automatically generates and removes historical price graphs
- Supports full automation via Docker and GitHub Actions

---

## 📦 Requirements

- Python 3.11+
- `requests`, `matplotlib`, `python-dotenv`
- Optional: Docker, Make, GitHub Actions

---

## 🔧 Setup

1. Clone this repository.
2. Create your own `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```
