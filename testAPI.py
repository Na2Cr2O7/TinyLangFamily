import load
load.start_loading()
import requests
url = "http://localhost:8000/v1/chat/completions"
load.stop_loading()
print('TinyLangLLM-DeepThinking:36M 测试')
messages=[{"role": "user", "content": input("请输入：")}]
while True:
    payload = {
        "model": "tinylangllm",
        "messages": messages
    }
    
    load.start_loading()
    response = requests.post(url, json=payload)
    load.stop_loading()

    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print("模型回复：")
        print(reply)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": input("请输入：")})
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)