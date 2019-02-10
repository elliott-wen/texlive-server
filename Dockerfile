FROM ubuntu:18.04
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git
COPY texmf-dist /app/
RUN git clone https://github.com/SwiftLaTeX/texmf-server.git /app && \
    pip3 install -r /app/requirements.txt && echo "0.4"

WORKDIR /app
CMD ["python3", "WSGI.py"]
