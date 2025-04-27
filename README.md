# 🚀 Image Adjuster Deployment Guide

This guide covers **building** and **deploying** the **Image Adjuster** application (Frontend + Backend) using **Docker**.

- **Frontend**: React + Vite (served via Nginx)
- **Backend**: FastAPI (Python 3.11 + Uvicorn)
- **Deployment Modes**:
  - **Local Development**: Docker Compose (multi-container orchestration)
  - **Production Deployment**: Docker run commands (isolated, simplified)

---

## 📁 Sub-project READMEs

- [Frontend README](./frontend/README.md) — Build instructions for **React UI**.
- [Backend README](./backend/README.md) — Build instructions for **FastAPI backend**.

---

## 🖥️ 1. Local Deployment (Docker Compose)

### 🛠️ Build & Run Locally

```bash
docker-compose up --build
```

### 🌐 Access Locally

- **Frontend UI**: [http://localhost:3000](http://localhost:3000)
- **Backend API (Swagger docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 📄 Docker Compose Overview

- **Services**:
  - `image-adjuster-frontend` (React UI via Nginx)
  - `image-adjuster-backend` (FastAPI backend)
- **Network**: `image-adjuster-network`
- **Volumes**:
  - `image-adjuster-uploads`
  - `image-adjuster-outputs`

This setup allows **quick multi-container orchestration** for **local development**.

---

## ☁️ 2. Production Deployment (Docker Run)

### 🛠️ Build Docker Images

1. **Backend**:

```bash
cd backend
docker build -t your-dockerhub-username/image-adjuster-backend:latest .
```

2. **Frontend**:

```bash
cd frontend
export VITE_BACKEND_URL=http://<server-ip>:8000  # Backend API URL for production
docker build -t your-dockerhub-username/image-adjuster-frontend:latest .
```

_For detailed build instructions, refer to the sub-project READMEs._

---

### 📦 Push Images to Docker Hub

```bash
docker push your-dockerhub-username/image-adjuster-backend:latest
docker push your-dockerhub-username/image-adjuster-frontend:latest
```

---

### 🚀 Run Containers on Linux Server

1. **Backend**:

```bash
docker run -d \
  --name image-adjuster-backend \
  -p 8000:8000 \
  -v image-adjuster-uploads:/app/uploads \
  -v image-adjuster-outputs:/app/outputs \
  your-dockerhub-username/image-adjuster-backend:latest
```

2. **Frontend**:

```bash
docker run -d \
  --name image-adjuster-frontend \
  -p 3000:80 \
  your-dockerhub-username/image-adjuster-frontend:latest
```

---

### 🌐 Access on Production Server

- **Frontend UI**: `http://<server-ip>:3000`
- **Backend API**: `http://<server-ip>:8000`

---

## 🛡️ Optional Enhancements

- **Reverse Proxy (Nginx/Traefik)** for **custom domains** and **SSL/TLS** support.
- **Systemd unit files** for **auto-restarting containers** on reboot.
- **Docker healthchecks** for service monitoring.

---

## 🚨 Common Docker Commands

- **Stop containers**:

```bash
docker stop image-adjuster-backend image-adjuster-frontend
```

- **Remove containers**:

```bash
docker rm image-adjuster-backend image-adjuster-frontend
```

- **View logs**:

```bash
docker logs image-adjuster-backend
docker logs image-adjuster-frontend
```

- **Inspect volumes**:

```bash
docker volume ls
docker volume inspect image-adjuster-uploads
docker volume inspect image-adjuster-outputs
```

---

Let me know if you'd like to integrate **CI/CD workflows**, **reverse proxy configs**, or other **deployment optimizations**! 🚀
