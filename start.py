import time
from colorama import Fore

import load
load.start_loading()

import warnings
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from model.model_minimind import MiniMindConfig, MiniMindForCausalLM
from model.model_lora import *

        



try:
    import torch_directml  # type: ignore

    device = torch_directml.device(0) # GPU 0 (intel HD Graphics 520)
    print(Fore.GREEN + 'Using DirectML for GPU acceleration')
except ImportError:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print(Fore.GREEN + f'Using device: {device}')

hidden_size = 512
num_hidden_layers = 8

use_moe = False
top_p = 0.85
tokenizer = AutoTokenizer.from_pretrained('./model/')
ckp = f'./out/full_sft_{hidden_size}.pth'
model = MiniMindForCausalLM(MiniMindConfig(
            hidden_size=hidden_size,
            num_hidden_layers=num_hidden_layers,
            use_moe=use_moe
        ))
model.load_state_dict(torch.load(ckp, map_location=device), strict=True)
apply_lora(model)

load.stop_loading()
selected=input('选择模型:\n1:TinyLangLLM2\n2:TinyLangLLM-DeepThinking\n3.氯铂酸喵第三代\n4.NaCl-Platinum:')
modelSelect={'1':'lora_TinyLangLLM2_512',
             '2':'lora_DeepThinking_512',
             '3':'lora_3_512',
             '4':'lora_4_512'
}
    
load_lora(model, f'./out/lora/{modelSelect[selected]}.pth')
load.start_loading()

streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

model=model.to(device)
model.eval()

def predict(messages):
    global model, tokenizer,loading
    loading=True
    startTime=time.time()
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)
    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=340,
        do_sample=True,
        top_p=top_p,
        temperature=0.7
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    endTime = time.time()
    loading=False
    print()
    
    print("time:", endTime - startTime)
    
    return tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]



from flask import Flask, request, jsonify
import json
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "TinyLangLLM 12M ",
        "endpoint": "/v1/chat/completions"
    })




@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    print('Chat')
    # headers = dict(request.headers)
    
    # # 获取并解析请求体
    # try:
    #     body = request.get_json(force=True)
    # except Exception as e:
    #     return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
    
    try:
        data = request.get_json()
        print(data)
        if not data or 'messages' not in data:
            return jsonify({"error": "Missing 'messages'"}), 400
        messages = data['messages']
        if not isinstance(messages, list) or len(messages) == 0:
            return jsonify({"error": "'messages' must be a non-empty list"}), 400

        response_text = predict(messages)
        print(response_text)

        response = {
            "id": "chatcmpl-" + str(np.random.randint(1000000, 9999999)),
            "object": "chat.completion",
            "created": int(time.time()),
            "model": f"tinylangllm-{hidden_size}M",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 1
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

load.stop_loading()
if __name__ == '__main__':
    print("🚀 启动 TinyLangLLM OpenAI api 服务器")
    print("监听地址: http://localhost:8000/v1/chat/completions")
    print("请在 config.ini 中设置:")
    print("  server_url = http://localhost:8000/v1")
    print("  API_KEY = 任意值（如 test-key）")
    # print("\n等待请求中...（按 Ctrl+C 停止）\n")
    try:
        app.run(host='127.0.0.1', port=8000, debug=False)
    except:
        loadingShouldStop = True
        th.join()