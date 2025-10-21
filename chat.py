#!/usr/bin/env python3

import os
from openai import OpenAI
import sys
import argparse

client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")

def chat_mode(content):
    messages = [{"role": "user", "content": content}]
    return get_ai_response_stream(messages)

def dictionary_mode(word, field=None):
    if field:
        messages = [{"role": "user", "content": f"给我解释一下这个词在{field}领域的含义，请以可以在终端中直接显示的格式输出，{word}"}]
    else:
        messages = [{"role": "user", "content": f"给我查这个词的字典释义，请以可以在终端中直接显示的格式输出，{word}"}]
    return get_ai_response_stream(messages)

def translate_mode(content):
    messages = [{"role": "user", "content": f"翻译以下内容：{content}"}]
    return get_ai_response_stream(messages)

def get_ai_response_stream(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True 
    )
    
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    
    print()
    return full_response

def main():
    parser = argparse.ArgumentParser(
        description='chat tools',
        epilog='''
Example:
  python script.py -c "Hello"
  python script.py -d "reciprocal" 
  python script.py -d "receptive field" -f "神经科学"
  python script.py -t "Hello world"
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--chat', help='Chat mode')
    group.add_argument('-d', '--dictionary', help='Dictionary mode')
    group.add_argument('-t', '--translate', help='Translate mode')
    
    parser.add_argument('-f', '--field', help='Field')
    args = parser.parse_args()
    
    try:
        if args.chat:
            result = chat_mode(args.chat)
        
        elif args.dictionary:
            result = dictionary_mode(args.dictionary, args.field)
        
        elif args.translate:
            result = translate_mode(args.translate)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
