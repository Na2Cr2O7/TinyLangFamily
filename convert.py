import json
import os

# 输入文件路径
input_file = 'distill_r1_110k_sft.jsonl'
# 输出文件路径 (改为 .jsonl 格式)
output_file = 'lora_dataDeepThinking.jsonl'
maxLines=100
maxLength=512
lineCount=0
try:
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line_num, line in enumerate(infile, start=1):
            try:
                data = json.loads(line)
                user = data.get('instruction', '')
                assistant = data.get('output', '')
                if len(user)>maxLength or len(assistant)>maxLength: continue
                # 构造新的对话格式并序列化为一行 JSON 文本

                lineCount+=1
                new_entry = {
                    "conversations": [
                        {"role": "user", "content": user},
                        {"role": "assistant", "content": assistant}
                    ]
                }
                outfile.write(json.dumps(new_entry, ensure_ascii=False) + '\n')
                if lineCount>=maxLines: break
            except json.JSONDecodeError as e:
                print(f"[第{line_num}行] JSON解析失败: {e}")
            except KeyError as e:
                print(f"[第{line_num}行] 缺少必要字段: {e}")
            except Exception as e:
                print(f"[第{line_num}行] 处理时发生未知错误: {e}")


    print(f"成功转换并写入 {output_file}")

except FileNotFoundError:
    print(f"输入文件 {input_file} 不存在，请检查路径是否正确。")
except Exception as e:
    print(f"读取或写入文件过程中出现异常: {e}")