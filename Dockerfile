FROM python:3.11-slim

# Install Firefox and dependencies
RUN apt-get update && \
    apt-get install -y firefox-esr wget gnupg2 xvfb && \
    rm -rf /var/lib/apt/lists/*

# Install geckodriver
RUN GECKODRIVER_VERSION=$(wget -qO- https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep '"tag_name":' | sed -E 's/.*"v([^"]+)".*/\1/') && \
    wget -O /tmp/geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz" && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    rm /tmp/geckodriver.tar.gz

# Set display number for Xvfb
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your test script
COPY main.py .

# Run the test using Xvfb for headless display
CMD ["sh", "-c", "Xvfb :99 -screen 0 1920x1080x24 & python main.py"]