# rfid_wallet
Script to store/retrieve crypto wallet Recovery Phrase to/from RFID tag, using **Raspberry Pi** and **RFID-RC522 Module**.

## Prerequisites
* Install mfrc522 library with `sudo pip install mfrc522` (or using `pip3`)
* Active SPI Interface in `sudo raspi-config`
* RPi library is included with Raspberry OS. Just update (you know, `sudo apt update` -> `sudo apt upgrade`)
* Run scripts using python 3.x

This is the pin configuration for RFID-RC522 Module:

  | RC522 Pin	| RaspPi Pin |
  |-----------|------------|
  |3.3V	| Pin 1 |
  | RST | Pin 22 |
  | GND | Pin 6	|
  | MISO | Pin 21 |
  | MOSI | Pin 19 |
  | SCK	| Pin 23 |
  | SDA	| Pin 24 |

 > Give me an RFID tag and I'll control the world —Gengis Kan
