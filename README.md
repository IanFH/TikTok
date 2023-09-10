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

## Testing Procedures

### Registration
- Choose a unique user name, password and phone number
- Use one of the following NRICs
    - ["S000000A", "S222222A", "S1010101A"]
    - Each of the NRIC can only be used once
    - This is in compliance to our background authenticator
    - It might take up to 1 minute for the authenticator to authenticate the account, simulating real world conditions
- Make sure to include the word "Singapore" in the address as we are simulating the condition of allowing access only to Singapore. Clearly, this can be extended to other countries as well.
- Some possible unused phone numbers:
    ["00000000", "22222222", "10101010"]

### Login without Registration
- Use the following credentials
    - Username: Test User
    - Password: 12345
    - Phone Number: 11001100

### Usage
- Login with the account created
- To topup money into the account, click on the topup button 
    - Use the following card details
        - Card Number: 4242 4242 4242 4242
        - Expiry Date: Any date in the future
        - CVC: Any 3 digit number
        - Name on card: Any name
        - Email: Any email
        - Phone Number: Any SG phone number
        - Address: Any address
