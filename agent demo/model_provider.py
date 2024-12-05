import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompt import user_prompt

class ModelProvider(object):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL_NAME")
        self._client = OpenAI(
            api_key=self.api_key, 
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        self.max_retry_times = 3

    def chat(self, prompt, chat_history = None):
        current_retry_times = 0
        while current_retry_times < self.max_retry_times:
            current_retry_times += 1
            try:
                messages = [{'role': 'system', 'content': prompt}]
                if chat_history:
                    for his in chat_history:
                        messages.append({'role': 'user','content': his[0]})
                        messages.append({'role': 'assistant','content': his[1]})
                messages.append({'role': 'user','content': user_prompt})
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                )
                """
                {
                    "id":"chatcmpl-1dde4d20-99d2-96d5-b321-c9847b80cf19",
                    "choices":[
                        {
                            "finish_reason":"stop",
                            "index":0,
                            "logprobs":null,
                            "message":
                            {
                                "content":"I am Qwen, a large language model created by Alibaba Cloud. I'm designed to assist users in generating various types of text, such as articles, stories, poems, and answering questions across a wide range of topics. How can I assist you today?",
                                "refusal":null,
                                "role":"assistant",
                                "audio":null,
                                "function_call":null,
                                "tool_calls":null
                            }
                        }
                    ],
                    "created":1733405490,
                    "model":"qwen-plus",
                    "object":"chat.completion",
                    "service_tier":null,
                    "system_fingerprint":null,
                    "usage":{
                        "completion_tokens":52,
                        "prompt_tokens":33,
                        "total_tokens":85,
                        "completion_tokens_details":null,
                        "prompt_tokens_details":null
                    }
                }
                """
                content = json.loads(response['choices'][0]['message']['content'])
                return content
            except Exception as error:
                print(f"调用大模型失败: {error}")
            return {}