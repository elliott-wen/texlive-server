FROM python:3.7.3-stretch
RUN   apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -q -y wget texlive texlive-science texlive-publishers \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    texlive-latex-recommended \
    texlive-plain-extra \
    git
RUN git clone https://github.com/SwiftLaTeX/texmf-server.git /app && \
    pip3 install -r /app/requirements.txt && echo "0.5"
COPY pdflatex.fmt /app/
COPY fonts/* /app/fonts/
WORKDIR /app
CMD ["python3", "wsgi.py"]
