echo "creating virtual envirment..."
python3 -m venv ~/myvenv

echo "activating virtual environment..."
source ~/myvenv/bin/activate

echo "upgrading pip..."
python3 -m pip install --upgrade pip 2>/dev/null > /dev/null

echo "installing dependencies..."
pip install -r requirements.txt 2>/dev/null > /dev/null

python3 is_peer_loged.py $1 $2