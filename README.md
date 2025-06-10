
# 42 User Login Tracker

This Python script monitors a user’s login status on the 42 intra API and sends macOS notifications when the user logs in or logs out.

---

## Features

- Tracks a specified 42 user’s login or logout status
- Sends macOS desktop notifications using `pync`
- Supports two modes:
  - `loged` — notify when user logs in
  - `deloged` — notify when user logs out
- Colored terminal error messages for usage help

---

## Prerequisites

- Python 3.x
- macOS (because it uses `pync` for notifications)
- `requests` library
- `pync` library

---

## Setup

1. Clone or download the script and accompanying files.

2. Create a `.env` file in the same directory containing your 42 API credentials:

   ```
   <your_client_id>
   <your_client_secret>
   ```

3. Ensure you have a `requirements.txt` file with:

   ```
   requests
   pync
   ```

4. Run the `launch.sh` script to setup and launch the tracker:

   ```bash
   ./launch.sh <user_to_track> <loged/deloged>
   ```

This script will:

- Create and activate a Python virtual environment
- Upgrade pip
- Install dependencies from `requirements.txt`
- Run the Python script with your arguments

---

## Usage

Run the tracker with:

```bash
./launch.sh jbelkerf loged
```

Arguments:

- `<user_to_track>`: The 42 username to track
- `<loged/deloged>`: Mode to track:
  - `loged` — notify when user logs in
  - `deloged` — notify when user logs out

---

## How it works

- Authenticates with the 42 API using client credentials from `.env`.
- Polls the user’s info every 10 seconds.
- When the user logs in or logs out (based on the chosen mode), it sends a macOS notification and exits.

---

## Error Handling

If arguments are missing or invalid, the script prints a red usage message and exits:

```
usage: ./launch.sh <user_to_track> <loged/deloged>
```

---

## Notes

- The script currently works only on macOS due to the use of `pync` for notifications.
- You can customize the notification messages or polling interval in the script.

---

## License

This script is provided as-is, without warranty.
