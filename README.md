# tgboticcup


## Installation
0. ** Install packet (Debian)
    sudo apt install pip python3.13-venv

1. **Clone the repository and navigate to the project directory:**
   ```sh
   git clone <repository-URL>
   cd tgboticcup
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv myenv
   source myenv/bin/activate  # for Windows: myenv\Scripts\activate
   ```

3. **Install dependencies Python ≤3.11.:**
   ```sh
   pip install -r requirements.txt
   ```
   **Install dependencies Python 3.12+ :**
   ```sh
   pip install -r requirements-12.txt
   ```

4. **Create a configuration file:**
    - Copy `config.py.example` to `config.py` (if an example is provided).
    - Enter your Telegram bot token in the `token` variable in the `config.py` file.

## Running the Telegram Bot

```sh
python main.py
```

## Running the Web Application (Admin Panel)

```sh
python app.py
```

## Requirements

- Python 3.8+
- All dependencies are listed in [requirements.txt]

## License

MIT License

