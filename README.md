this doc serves as a documentation during development, all intermediate steps should leave a photo / screenshot inside `./screenshots/` folder for reference to make the tutorial later.

# Hardware configuration

ESP-32-S3 board with camera module.

For reference, we are using Seeed Studio XIAO ESP32S3 Sense module.

## IDE setup

We are using Arduino with ESP32 configuration set.

1. Install the [lastest version](https://www.arduino.cc/en/software) of Arduino IDE

2. Insert Additional Board Manager

   - For Windows
   - Navigate to File > Preferences, and fill "Additional Boards Manager URLs" with the url below:

```plaintext
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

- For MacOS
- Navigate to Arduino IDE > Preferences, and fill "Additional Boards Manager URLs" with the url below:

```plaintext
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

3. Navigate to Tools > Board > Boards Manager..., type the keyword esp32 in the search box, select the latest version of esp32, and install it.

4. Select Board and Port

   - Select XIAO_ESP32S3 and the corresponding port number

5. Navigate to Tools > PSRAM > Select `OPI PSRAM`

## Code compilation and upload to board

1. Click to open the esp32 project at `./cam/cam.ino`

2. Insert your own credentials

   - Get your own WIFI credentials by copying credential.h.template, and rename it into credential.h, then fill your WIFI credential in it.

3. Upload the program to your board!

# Computer-side software configuration

## Connections to made

1. Ensure your computer is connected to the same Wifi as your board, and use a usb lable to connect your board with your computer both for power supply and serial communication purposes. The images are sent via Wifi from the esp32 board to your computer, however, the communication from your computer back to the board to indicate the presence is currently using serial for simplicity of demonstration and extendability.

## Configurations

1. The repo of the software is located under `./home_server/`, copy and paste `custom_config.py.template` to create your own version of `custom_config.py`, and fillin the fields correspondingly.

## Python env setup

```shell
conda create -n smart-cam python=3.9 -y
conda activate smart-cam
pip install -r home_server/requirements.txt
python home_server/main.py
```

# References

[Seeed Studio's tutorial](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

[DroneBot's Video](https://www.youtube.com/watch?v=qNzlytUdB_Q)
