# TikTok

Team Members: Kyal Sin Min Thet, Ian Freda Hariyanto, Teoh Tze Tzun, Jeffinson Darmawan, Pandu Caroko Adi

## Setup
On Mac/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## API Used
- APScheduler (https://apscheduler.readthedocs.io/en/stable/)
    - Used to schedule the background update of the database
- Flask (https://flask.palletsprojects.com/en/1.1.x/)
    - Used to create the web server
- Stripe (https://stripe.com/docs/api)
    - Used to handle payment

## Testing Web App Procedure (Creating Account)
- Choose a unique user name, password and phone number
- Use one of the following NRICs
    - ["S1111111A", "S000000A", "S222222A", "S1010101A"]
    - Each of the NRIC can only be used once
    - This is in compliance to our background authenticator