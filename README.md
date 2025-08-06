# 🔄 Nexus Updater

![Python](https://img.shields.io/badge/Built%20With-Python%203-blue)
![Systemd Timer](https://img.shields.io/badge/Scheduled%20By-Systemd%20Timer-brightgreen)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

> Automated updater for [`nexus-cli`](https://cli.nexus.xyz/) that checks for new releases every hour, installs the latest version if needed, and restarts it safely in a `screen` session.

---

## ✨ Features

- Checks GitHub Releases for the latest `nexus-cli` version
- Compares against the installed version (`nexus-cli -V`)
- If versions differ:
  - Stops current `nexus-cli` process in `screen`
  - Installs the latest release via one-line install script
  - Restarts `nexus-cli` in a detached screen session
- Runs automatically **every hour** using a `systemd` timer
- All actions are logged to `/opt/nexus-updater/updater.log`

---

## ⚙️ Requirements

- Linux system with `systemd`
- Python 3.x
- `screen` installed (`sudo apt install screen`)
- `curl` installed
- Root access (`sudo`) for installing services to `/opt/`

---

## 🚀 Installation

```bash
git clone https://github.com/seventhlegend/nexus-network-updater.git
cd nexus-network-updater
sudo bash install.sh

```

### Verify:

```bash
sudo systemctl status nexus-updater.timer
tail -f /opt/nexus-updater/updater.log
```

---

## 🛠 How It Works

1. Fetches the latest release from:
   `https://api.github.com/repos/nexus-xyz/nexus-cli/releases/latest`
2. Removes any `v` prefix from version string (`v0.10.4` → `0.10.4`)
3. Compares with the local version from:

   ```bash
   nexus-cli -V  # e.g. "nexus-network 0.10.3"
   ```

4. If different:

   - Sends `Q` and `Ctrl+C` to stop the `screen` session
   - Runs the install script:

     ```bash
     curl https://cli.nexus.xyz/ | sh
     ```

   - Starts `nexus-cli` again inside a `screen` session
   - Detaches it with `ctrl+a d`

---

## 📄 Logs & Monitoring

```bash
tail -f /opt/nexus-updater/updater.log
journalctl -u nexus-updater.service
```

---

## 🧩 Self-Updating the Nexus Updater

You can safely reinstall and update the Nexus Updater itself (including systemd timer/service files) by running:

```bash
bash update-nexus-updater.sh
```

### What it does:

- Stops and disables the `nexus-updater.timer`
- Deletes the current local copy of the project
- Clones the latest version from GitHub
- Re-runs `install.sh`
- Restarts the systemd timer

This ensures your `nexus-updater` instance is always clean and in sync with the latest version of this repository.

### Important:

- Make sure you run this command **from within the cloned repo directory**
- You **must have `sudo` access**
- Any custom modifications will be **overwritten**

---

## ❌ Uninstall

```bash
sudo bash uninstall.sh
```

---

## 💼 File Structure

```text
nexus-updater/
├── nexus_updater.py           # Main update logic
├── install.sh                 # One-line installer
├── uninstall.sh              # Clean uninstaller
├── nexus-updater.service     # systemd service
├── nexus-updater.timer       # systemd timer
├── README.md                  # This file
└── .gitignore
```

---

## 🔐 Security Considerations

- The update process relies on a remote shell script: `curl https://cli.nexus.xyz/ | sh`
- Only use this tool if you trust the source
- You can inspect the installer manually before proceeding

---

## 🤝 Support This Project

If you found this tool helpful and want to support future open-source development, consider donating via one of the addresses below:

| Network               | Address                                        |
| --------------------- | ---------------------------------------------- |
| 💼 **EVM (MetaMask)** | `0x44a0c2aBA5F216719d8DEa221843D5f821728bAb`   |
| 🌊 **Solana**         | `556RHbKnCfsbvbr5Zjo1ZNaiWtBB15btMGuppyfEKHTo` |
| 🔄 **TRON (TRX)**     | ``                                             |
| ₿ **Bitcoin (BTC)**   | ``                                             |

> Every little bit helps me spend more time building useful tools like this. Thank you! 🙏

---

## 📄 License

This project is licensed under the terms of the **GNU General Public License v3.0 (GPL-3.0)**.  
You are free to use, modify, and redistribute this software under the same license.

- 📜 Full license text: [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)
- ⚠️ All derivative works must also be open source and licensed under GPL-3.0

---

## 🙋‍♂️ Contributions

Pull requests, issues, suggestions and improvements are welcome.
If you'd like to extend this tool to other CLI apps, feel free to fork and adapt.

---

## ⚠️ Disclaimer

This script is intended for users running `nexus-cli start` inside a `screen` session named `nexus`.  
If your setup is different, the script **may not function as expected**.

Use this tool at your own risk.  
No warranties or guarantees are provided.  
Please review the code before running it on production systems.

