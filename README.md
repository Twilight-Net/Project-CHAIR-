# 🪑 Project Chair

> A self-hosted local network hub with mini apps — built for privacy, built for your LAN.

![Status](https://img.shields.io/badge/status-active-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.8+-yellow)

---

## What is Project Chair?

**Project Chair** is a personal local-network suite that runs entirely on your machine — no internet required, no accounts, no tracking. It's a collection of self-hosted mini apps organized under a single hub called **Twilight Net**, designed with a clean, minimal UI inspired by Android 16's Material You design language.

Think of it as your own private internet, running at home.

---

## Architecture

```
Project Chair
└── Twilight Net (hub)          → localhost:8080
    ├── 🎬 Local Tube           → localhost:3001
    ├── 🤖 Local AI             → localhost:3002  [coming soon]
    ├── 💬 Local Chat           → localhost:3003  [coming soon]
    └── ☁️  Local Cloud          → localhost:3004  [coming soon]
```

---

## Apps

### 🌆 Twilight Net — The Hub
The main dashboard for the entire suite. Displays all mini apps as cards, provides quick navigation, and has an admin panel to add or remove apps dynamically.

**Features:**
- Android 16-style dark AMOLED UI
- App grid with icons and descriptions
- Live clock and uptime display
- Admin panel (PIN protected) to add/delete apps
- Apps persist across sessions via localStorage

---

### 🎬 Local Tube
A private YouTube-like video platform for your local network. Only admins can upload and manage content — everyone on the LAN can watch, like, and follow channels.

**Features:**
- Home feed (videos) and Shorts (vertical format)
- Channels with follow system
- Like system — per user, persistent
- View count tracking
- Thumbnail support for all content
- Search across videos and shorts
- Upload progress bar
- Auto channel creation on first upload
- Admin-only upload and delete (PIN protected)

**Stack:** Python (Flask) + Vanilla HTML/CSS/JS + JSON flat-file DB

---

## Getting Started

### Requirements
- Python 3.8+
- pip

### Install dependencies
```bash
pip install flask
```

### Run Twilight Net (hub)
```bash
cd twilight_net
python server.py
# → http://localhost:8080
```

### Run Local Tube
```bash
cd local_tube
python server.py
# → http://localhost:3001
```

---

## File Structure

```
project-chair/
│
├── twilight_net/
│   ├── server.py          # Python HTTP server (port 8080)
│   └── index.html         # Hub UI — app grid, admin panel
│
└── local_tube/
    ├── server.py          # Flask backend (port 3001)
    ├── index.html         # Frontend UI
    ├── db.json            # Auto-generated flat-file database
    └── uploads/
        ├── videos/        # Full-length video files
        ├── shorts/        # Short-form video files
        └── thumbnails/    # Thumbnail images
```

---

## Admin System

All apps in Project Chair share a unified admin PIN: **`1258`**

| App | Admin Access | Admin Can |
|-----|-------------|-----------|
| Twilight Net | PIN via admin button | Add / remove apps from grid |
| Local Tube | PIN via profile icon | Upload videos, delete videos |

Admin sessions are client-side only — no tokens, no cookies. The PIN is verified per action on the server for destructive operations.

---

## Design Philosophy

Project Chair follows the **Android 16 / Material You** design language:

- AMOLED dark backgrounds (`#0a0a0c`)
- Rounded cards with large corner radii
- Surface layering for depth without shadows
- Google Sans typography
- Minimal chrome — content first
- Bottom sheet modals instead of popups
- Pill-shaped chips and action buttons
- Subtle animations with `cubic-bezier` easing

---

## Roadmap

- [x] Twilight Net hub
- [x] Local Tube (videos + shorts + likes + follows)
- [ ] Local AI — on-device LLM interface
- [ ] Local Chat — real-time LAN messaging (WebSocket)
- [ ] Local Cloud — personal file storage and sharing
- [ ] Unified admin dashboard across all apps
- [ ] Dark/light theme toggle
- [ ] Mobile PWA support

---

## Privacy

Project Chair is 100% local. Nothing leaves your machine or LAN:
- No telemetry
- No external API calls
- No user accounts or passwords (only PIN)
- No cookies beyond localStorage for user identity
- All data stored in local JSON files and the filesystem

---

## License

MIT — use it, fork it, make it yours.

---

*Built with 🪑 and zero cloud dependencies.*
