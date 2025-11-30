# TinyLangLLM

基于Minimind 2模型的轻量级大模型 **TinyLangLLM:26M**

pretrain和sft部分参考自[minimind](https://github.com/jingyaogong/minimind)

lora来自[这里](https://modelscope.cn/datasets/Moemuu/Muice-Dataset)

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

已经修改好了脚本，可以直接训练,但是除了lora之外的训练集需要自行下载

```bash

.\trainer\train_pretrain.py
.\trainer\train_full_sft.py
.\trainer\train_lora.py

```

## 协议
训练模型使用的协议为[Apache 2.0](https://github.com/jingyaogong/minimind/blob/main/LICENSE)

lora训练集为CC-BY-NC-4.0。
