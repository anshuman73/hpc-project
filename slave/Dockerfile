FROM tensorflow/tensorflow:2.3.0

COPY slave_requirements.txt /home/slave_requirements.txt
COPY slave.config /home/slave.config
COPY slave.py /home/slave.py
COPY run.sh /home/run.sh
RUN chmod a+x /home/run.sh

WORKDIR /home
RUN pip3 install -r slave_requirements.txt

ENTRYPOINT ["./run.sh"]
