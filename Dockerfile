# Gunakan image Python terbaru
FROM python:3.12-slim

# Install dependencies sistem yang dibutuhkan oleh Chrome
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
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

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d'.' -f1) \
    && wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip" \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Set Workdir
WORKDIR /app

# Copy semua file ke container
COPY . .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python", "bot.py"]
