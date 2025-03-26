# ESP32-CAM Meets Vision Language Models: Building an Intelligent Vision System with Cloud LLMs

# Introduction

TODO: Explain the problem, context, and goals of the tutorial.

# Prerequisites

TODO: List required knowledge, tools, or equipment.

# Steps

TODO: Detailed instructions with diagrams, screenshots, or code
snippets.

## Hardware preperation

In this tutorial, we are going to use Seeed Studio XIAO ESP32S3 Sense module. This board is very tiny, and has a tiny camera extension as well, that can be connected with the main board with a socket with no effort.

![alt text](screenshots/hardware-configuration/xiao-with-camera.png)

![alt text](screenshots/hardware-configuration/xiao.png)

![alt text](screenshots/hardware-configuration/hardware-antenna.jpg)

![alt text](screenshots/hardware-configuration/hardware-with-cam.jpg)

### IDE setup

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

### Compile the code and upload to board

1. Click to open the esp32 project at `./cam/cam.ino`

2. Insert your own credentials

   - Get your own WIFI credentials by copying credential.h.template, and rename it into credential.h, then fill your WIFI credential in it.

3. Upload the program to your board!

## Computer side software configuration

Personal computer is used as a server to receive the images captured by the camera, then python scripts and various libraries can be used to do movement detection, and only upload to LLM if the image changed quite a bit to reduce LLM points used, image post-processing (object segmentation, mono-colorize for better performance of LLM input, image compression for lower cost introduced).

Then the image is sent via internet to vision LLMs for interpretation, with a configurable detection target.

### Connections to made

1. Ensure your computer is connected to the same Wifi as your board, and use a usb lable to connect your board with your computer both for power supply and serial communication purposes. The images are sent via Wifi from the esp32 board to your computer, however, the communication from your computer back to the board to indicate the presence is currently using serial for simplicity of demonstration and extendability.

2. Open up the browser and input the ip address `http://192.168.8.189/`

![alt text](screenshots/excecution/browser.png)

3. Reduce the resolution to 128x128 for more stable image transfer.

### Configurations

1. The repo of the software is located under `./home_server/`, copy and paste `custom_config.py.template` to create your own version of `custom_config.py`, and fillin the fields correspondingly.

### Python environment setup

```shell
conda create -n smart-cam python=3.9 -y
conda activate smart-cam
pip install -r home_server/requirements.txt
python home_server/main.py
```

## Demonstration

TODO: Showcase results, simulations, or examples.

## Conclusion

TODO: Summarize key takeaways and suggest further reading or
applications.

## References

TODO: List any articles, books, or resources you used. All work must be
original and properly cited.

[Seeed Studio's tutorial](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)

[DroneBot's Video](https://www.youtube.com/watch?v=qNzlytUdB_Q)

## Acknowledgement

TODO: Acknowledge any sources for help, including AI tools. A
contribution statement is required if the tutorial is a teamwork.
