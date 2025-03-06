## 🖼️ Image Hosting Bot

![Image host](https://envs.sh/pqu.jpg)

Welcome to the Image Hosting Bot, a powerful and user-friendly Telegram bot designed to help you easily upload images and receive instant links to share with your friends and family! 🚀

## 👨‍💻 Developers

This bot is brought to you by Alpha Bots, a passionate team dedicated to creating innovative and efficient tools for the community. We strive to make technology accessible and enjoyable for everyone!

Developers:

Utkarsh 🇮🇳

Adarsh 🇮🇳

## ✨ Features

- ![Feature](https://img.shields.io/badge/Feature-Seamless%20Image%20Uploads-brightgreen) Upload images directly to the bot and get a shareable link instantly! 📤
- ![Feature](https://img.shields.io/badge/Feature-User%20Friendly%20Interface-blue) With inline buttons for help and support, using the bot is a breeze. 🛠️
- ![Feature](https://img.shields.io/badge/Feature-MongoDB%20Integration-yellow) All uploaded image URLs are stored securely for easy access. 🔒

## 🌍 Languages Used

- ![Python](https://img.shields.io/badge/Language-Python-blue) The primary language used for development, providing a robust and flexible framework. 🐍

## 🚀 Deployment

Click the button below to see various deployment options:

[![Deploy](https://img.shields.io/badge/Deploy-Now%21-brightgreen)]()

### 🌈 Heroku Deployment

1. Click on the deploy button. 🌟
2. Set your environment variables:

<a href="https://heroku.com/deploy?template=https://github.com/utkarshdubey2008/imagehost">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" style="width: 200px; height: auto;">
</a>

### 🐳 Docker Deployment

1. Build your Docker image:

```bash
docker build -t imagehost .
```

2. Run your Docker container:

```bash
docker run -e API_ID -e API_HASH -e BOT_TOKEN -e MONGO_URI imagehost
```

### ☁️ Koyeb Deployment

1. Click on the button below 👇.☁️
2. Set your environment variables as mentioned above.
3. Use the button below to deploy to Koyeb:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?name=imagehost&type=git&repository=THEALPHABOTZ%2Fimagehost&branch=main&builder=buildpack&env%5[...)

---

## 🛠️ Installation

### 📦 Prerequisites

Make sure you have the following installed:

- ![Python](https://img.shields.io/badge/Python-3.9%20or%20later-blue) 🐍
- ![pip](https://img.shields.io/badge/pip-Python%20package%20installer-blue) 📦

### ⚙️ Setup Instructions

1. Clone this repository:

```bash
git clone https://github.com/yourusername/imagehost.git
cd imagehost
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file or set environment variables for:

```plaintext
API_ID='YOUR_API_ID'
API_HASH='YOUR_API_HASH'
BOT_TOKEN='YOUR_BOT_TOKEN'
MONGO_URL='YOUR_MONGODB_URL'
ADMIN_ID='YOUR_ID'
BOT_IMAGE_URL='YOUR_BOT_IMAGE' (For Start message use @quick_img_bot for link)
```

4. Run the bot:

```bash
python bot.py
```

## ⚠️ Troubleshooting

If you face any issues or errors during setup or usage, please feel free to contact our support via [Support Link](https://t.me/alphabotzchat). We are happy to help you get things sorted!

For the latest updates, check out our [Updates Channel](https://t.me/Thealphabotz).

## 🤝 Contributing

We welcome contributions! If you want to improve the bot or add new features, feel free to fork the repository and submit a pull request. 🙌

## 📞 Support

If you encounter any issues or need help, please reach out to us via our [Support Chat](https://t.me/alphabotzchat). 💬

## 🔗 Links

- [GitHub Repository](https://github.com/utkarshdubey2008/imagehost)
- [Updates Channel](https://t.me/Thealphabotz)

Thank you for using the Image Hosting Bot! Happy sharing! 🎉
