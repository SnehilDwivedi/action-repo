# Webhook Receiver - GitHub Event Listener

This repository implements a **Flask-based Webhook Receiver** for listening to GitHub Webhook events such as:

- Push
- Pull Request
- Merge (bonus)

Incoming events are stored in **MongoDB** and retrieved every 15 seconds for display via a frontend UI.

---

## 🔁 Application Flow



---

## 📦 Tech Stack

- **Backend:** Python, Flask
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript (Polling every 15 seconds)
- **Webhook Source:** GitHub (via GitHub Webhooks)

---

## 📬 Webhook Endpoint

> **POST** `/webhook`

This endpoint accepts GitHub event payloads and stores them in MongoDB in the following format:

### MongoDB Schema

| Field        | Type      | Description                                              |
|--------------|-----------|----------------------------------------------------------|
| `id`         | ObjectId  | MongoDB default                                          |
| `request_id` | String    | Git commit hash (or PR ID for Pull Requests)            |
| `author`     | String    | GitHub username                                         |
| `action`     | Enum      | One of: `["PUSH", "PULL_REQUEST", "MERGE"]`             |
| `from_branch`| String    | Source branch (e.g., `dev`)                             |
| `to_branch`  | String    | Target branch (e.g., `main`)                            |
| `timestamp`  | ISO String| UTC timestamp of the event                              |

---

## 🧪 Events Format (UI Display)

- **Push:**  
  `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC`

- **Pull Request:**  
  `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC`

- **Merge:**  
  `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC`

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
