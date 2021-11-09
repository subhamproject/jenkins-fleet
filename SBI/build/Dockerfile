FROM python:3.9.7
RUN pip3 install boto3 click
RUN mkdir -p /data
WORKDIR /data
COPY ./SBI/script/fleet.py .
ADD entry.sh .
ENTRYPOINT [ "/data/entry.sh" ]
