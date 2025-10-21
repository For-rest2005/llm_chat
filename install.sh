#!/bin/bash

# Install script for DeepSeek Chat

sudo cp chat.py /usr/local/bin/deepseek-chat
sudo chmod +x /usr/local/bin/deepseek-chat

echo "Enter your DeepSeek API key:"
read -s api_key
echo "export DEEPSEEK_API_KEY=\"$api_key\"" >> ~/.bashrc
source ~/.bashrc

echo "Installation done. Use 'deepseek-chat' command."
