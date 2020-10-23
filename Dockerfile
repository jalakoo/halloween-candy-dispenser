ARG ALWAYSAI_HW="default"
FROM alwaysai/edgeiq:${ALWAYSAI_HW}-0.16.1
RUN sudo -H apt-get update && sudo -H apt-get install -y libasound2-dev && sudo -H apt-get install -y rpi.gpio