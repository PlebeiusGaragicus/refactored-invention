import torch
from transformers import pipeline


pipe = pipeline("text-generation",
                # model="/teamspace/studios/this_studio/alignment-handbook/sos-v01-dpo",
                model="LaierTwoLabsInc/Satoshi-7B",
                # torch_dtype=torch.bfloat16, device_map="auto")
                device_map="auto")
                # torch_dtype=torch.bfloat16, device_map="cpu")


messages = [

    {"role": "user", "content":"Is taxtation theft??"},
]
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
outputs = pipe(prompt, max_new_tokens=512, do_sample=True, temperature=0.5, top_k=50, top_p=0.5)

print(outputs[0]["generated_text"])
