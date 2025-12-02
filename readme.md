# TinyLangLLM

基于Minimind 2模型的轻量级大模型 **TinyLangLLM:26M**

pretrain和sft部分参考自[minimind](https://github.com/jingyaogong/minimind)

lora来自[这里](https://modelscope.cn/datasets/Moemuu/Muice-Dataset)

lora文件为[lora_N_512.pth](.\out\lora\TinyLangLLM\lora_N_512.pth),放置在`out\lora`下

## 直接使用
1.安装python3
2.去release下载下来，解压
3.
    ```bash
    pip install -r requirements.txt

    ```
直接使用部分的requirements会安装torch的CPU版本。

4.运行`start.py`

现在打开了一个适用于openai的接口，可以直接使用。或者：

5.运行`testAPI.py`

## 训练
1.安装python3
2.安装`pytorch`

3.
    ```bash
    pip install -r requirements.txt

    ```



lora训练集应该被命名为`lora_data.jsonl`放置在`.\dataset\`下

数据集格式

```json
{"conversations": [{"role": "user", "content": "如何集中精力做一件事情"}, {"role": "assistant", "content": "首当其冲的肯定是选择一个合适的地方啦，比如说图书馆之类的，如果你不想出去，那就找一个安静的地方吧。然后扔掉手机这类会让你分心的东西，或者关掉通知，确保你不会突然被打扰。明确你要做的事情，把它细化成分几步去完成，设置期限，任务完成之后放松放松。如果你感觉到累了不行了就去外面转转吧，喝一杯咖啡，思考让你停下来的地方，然后活力满满地继续接下来的工作。"}]}
{"conversations": [{"role": "user", "content": "低级ai不能涩涩，差评"}, {"role": "assistant", "content": "你什么意思？（大恼）"}]}
```

已经修改好了脚本，可以直接训练,但是除了lora之外的训练集需要自行下载

```bash
cd .\trainer\

train_pretrain.py
train_full_sft.py
train_lora.py

```

## 协议
训练模型使用的协议为[Apache 2.0](https://github.com/jingyaogong/minimind/blob/main/LICENSE)

lora训练集为CC-BY-NC-4.0。