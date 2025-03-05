this doc serves as a documentation during development, all intermediate steps should leave a photo / screenshot inside `./screenshots/` folder for reference to make the tutorial later.

# Hardware configuration

ESP-32-S3 board with camera module.

For reference, we are using Seeed Studio XIAO ESP32S3 Sense module.

# IDE configuration

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

6. Open the project at `./cam`

7. Insert your own credentials

   - Get your own WIFI credentials by copying credential.h.template, and rename it into credential.h, then fill your WIFI credential in it.
   - ! DO NOT CHANGE THE TEMPLATE FILE.

8. Upload to your board!

# References

[Seeed Studio's tutorial](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

[DroneBot's Video](https://www.youtube.com/watch?v=qNzlytUdB_Q)
