# IsAnyoneInTheMine
![IsAnyoneInTheMine](docs\imgs\title.png)

 Checks if anyone is in minecraft realm

## Requirements
- Python 3+
- Microsoft Azure Application set up
  - Use [this wiki](https://wiki.vg/Microsoft_Authentication_Scheme#Microsoft_OAuth2_Flow) until you get to application setup
  - Application needs these settings:
    - `Personal Microsoft accounts only`
    - Redirect URI is http://localhost/auth/callback and type `Web`
  - On the App Page, navigate to "Certificates & secrets"
    - Generate a new client secret and save for later use
- Microsoft Bedrock Realm

## Server

Runs a flask web server hosting the API and handling auth.

Code inside `/server`

### Setup

1. Install requirements:
    - `pip install -r requirements.txt`
1. Create `.env` file
    - Copy `.env.template` and rename it `.env`
    - Populate it with Client (Application) ID and Secret you created in the requirements for Microsoft Azure

### Run Locally

`flask --app flask_app run`

### Usage

#### Homepage

Homepage will render text with YES or NO if any users are online in the realm.

![Homepage Screenshot](docs\imgs\homepage_screenshot.png)

#### Endpoint

`/api/isanyoneinthemine`

### Response

```json
{
    "isanyoneinthemine" : False
}
```

## Client

Local client turns a light on an ESP32 board if anyone is in the mine.

### Requirements
- ESP32 board (I use HiLetgo ESP-WROOM-32)
- Arduino IDE set up with ESP32 boards
    - [ESP32 Docs](https://docs.espressif.com/projects/arduino-esp32/en/latest/getting_started.html)

### Setup

1. Open `client/isanyoneinthemine.ino` in your Arduino IDE
2. Replace variables for your wifi network, server, etc.
3. Connect your ESP32 and flash it!
    - You may need to hold the `BOOT` or `IOO` button while it is uploading

### Run

Connect power and press the `EN` button!

## Resources
- API Reference https://wiki.vg/Bedrock_Realms
- Authentication Setup https://wiki.vg/Microsoft_Authentication_Scheme
- OpenXbox (used for first-time auth) https://github.com/OpenXbox/xbox-webapi-python
- ESP32 Docs https://docs.espressif.com/projects/arduino-esp32/en/latest/getting_started.html