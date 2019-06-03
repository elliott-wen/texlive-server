FROM ubuntu:18.04
RUN   apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -q -y wget texlive texlive-science texlive-publishers \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-recommended \
    texlive-plain-extra \
    python3 \
    python3-pip \
    git
RUN git clone https://github.com/SwiftLaTeX/texmf-server.git /app && \
    pip3 install -r /app/requirements.txt && echo "0.4"
COPY pdflatex.fmt /app/
WORKDIR /app
CMD ["python3", "WSGI.py"]
