echo "creating virtual envirment..."
python3 -m venv ~/myvenv

echo "activating virtual environment..."
source ~/myvenv/bin/activate

echo "upgrading pip..."
python3 -m pip install --upgrade pip

echo "installing dependencies..."
pip install -r requirements.txt

python3 is_peer_loged.py