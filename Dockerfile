# Gunakan image Python terbaru
FROM python:3.12-slim

# Install dependencies sistem yang dibutuhkan oleh Chrome
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    ca-certificates \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-glib-1-2 \
    libxcomposite1 \
    libxrandr2 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxss1 \
    libxtst6 \
    libglib2.0-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# Tambahkan kunci GPG Chrome (metode baru)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | tee /etc/apt/keyrings/google-chrome.asc > /dev/null

# Tambahkan repository Chrome
RUN echo "deb [signed-by=/etc/apt/keyrings/google-chrome.asc] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver yang sesuai dengan versi Chrome
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Set Workdir
WORKDIR /app

# Copy semua file ke container
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python", "bot.py"]
