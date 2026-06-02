# 42 Login Tracker

A small CLI tool that watches the 42 intra API and notifies you the moment a user logs in or logs out — no refreshing the intra page, no guessing.

---

## Why use it

At 1337 / 42 schools, knowing when someone is logged in matters more than you'd think:

- **Watching for an evaluator** — you're waiting on a correction and need to know the second your evaluator shows up at a workstation so you can ping them or head to their cluster.
- **Tracking yourself** — useful if you're debugging a session issue or want to confirm your own location got registered correctly.
- **Tracking a peer** — waiting for a teammate to arrive before starting a group session, or just need to know when they're available in-campus.

Instead of refreshing the intra every few minutes, you run one command and get a desktop notification the moment the status changes.

---

## Setup

Clone the repo and enter it:

```bash
git clone https://github.com/jbelkerf/42-login-tracker.git
cd 42-login-tracker
```

That's all the setup you need. The launch script handles the Python virtual environment and dependencies automatically on first run.

---

## Usage

```bash
./launch.sh <login> <logged|delogged>
```

**Examples:**

Wait until `jbelkerf` logs in:
```bash
./launch.sh jbelkerf logged
```

Wait until `jbelkerf` logs out:
```bash
./launch.sh jbelkerf delogged
```

On first run (and whenever your token expires), a browser window will open automatically for 42 OAuth. Log in once, and the tracker starts polling.

---

## Use cases

| Situation | Command |
|-----------|---------|
| Waiting for your evaluator to arrive at campus | `./launch.sh <evaluator_login> logged` |
| Watching until your evaluator leaves (e.g. to catch them between sessions) | `./launch.sh <evaluator_login> delogged` |
| Confirming your own session registered on intra | `./launch.sh <your_login> logged` |
| Waiting for a teammate to show up before starting a project session | `./launch.sh <peer_login> logged` |
| Noticing when a peer wraps up their session | `./launch.sh <peer_login> delogged` |

---

## How it works

1. `./launch.sh` sets up a Python venv and installs dependencies for your OS (Linux or macOS).
2. It opens your browser to authenticate via 42 OAuth — no credentials are stored locally.
3. The script polls the 42 intra API every 10 seconds, checking the `location` field of the target user.
4. When the condition is met (user appears or disappears), you get a desktop notification and the script exits.

---

## Requirements

- Linux or macOS
- Python 3
- A 42 intra account (for OAuth)


---

## Notes

- The token is obtained fresh each run via browser OAuth. If it expires mid-session, the script will tell you to re-run it.
- If the target login doesn't exist on intra, the script exits with an error immediately.
- Ctrl+C stops the tracker at any time.
