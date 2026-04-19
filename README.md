# 📸 Snap Viewer

A self-hosted web app for browsing and downloading exported Snapchat story and highlight data. Built with Python and Flask, deployed on a personal cloud server with Nginx, HTTPS, and systemd.

🔗 **Live Demo:** [snap.unocloud.us](https://snap.unocloud.us)

---

## Features

- 📂 Browse exported Snapchat stories and highlights by profile
- 🖼️ Lightbox viewer for photos and videos
- ⬇️ Download individual media or bulk-download entire sections
- 🔍 Search history browser
- 🕐 Timestamps displayed for each snap
- 📱 Responsive layout

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Frontend | HTML, CSS, JavaScript |
| Web Server | Nginx (reverse proxy) |
| HTTPS | Let's Encrypt via Certbot |
| Process Manager | systemd |
| Hosting | AWS EC2 (Ubuntu 22.04) |

---

## Project Structure

```
snap-viewer/
├── app.py            # Flask application
├── write_html.py     # HTML generation helpers
├── templates/        # Jinja2 HTML templates
└── .gitignore
```

---

## Deployment

This app runs as a systemd service behind Nginx on an AWS EC2 instance.

### 1. Clone the repo

```bash
git clone https://github.com/uno-1096/snap-viewer.git
cd snap-viewer
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### 3. Run locally

```bash
python app.py
# App runs on http://localhost:5001
```

### 4. Production (systemd)

Create `/etc/systemd/system/snapviewer.service`:

```ini
[Unit]
Description=Snap Viewer Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/snapchat-viewer
ExecStart=/home/ubuntu/snapchat-viewer/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable snapviewer
sudo systemctl start snapviewer
```

### 5. Nginx config

```nginx
server {
    server_name snap.unocloud.us;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then enable HTTPS:

```bash
sudo certbot --nginx -d snap.unocloud.us
```

---

## About

Built as part of a self-hosted cloud homelab project. The full infrastructure (VPC, EC2, DNS, Nginx, SSL) was provisioned using Terraform and is documented in [terraform-vpc-project](https://github.com/uno-1096/terraform-vpc-project).
