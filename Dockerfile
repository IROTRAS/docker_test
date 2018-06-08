# Python Base Image from https://hub.docker.com/r/arm32v7/python/
#FROM arm32v7/python:3.6.4-stretch 
FROM arm32v7/python:2.7.14-stretch

# Intall the rpi.gpio python module
RUN pip install --no-cache-dir rpi.gpio
RUN pip install --no-cache paho-mqtt

# Copy the Python Script to blink LED
COPY led_blinker.py ./


# Trigger Python script
CMD ["python", "./led_blinker.py"]
