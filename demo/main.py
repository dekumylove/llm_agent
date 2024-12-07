# agent entrance
import time
from tools import tools_map
from prompt import generate_prompt, user_prompt
from model_provider import ModelProvider
'''
todo:
  1、环境变量设置
  2、工具的引入
  3、prompt模版
  4、模型的初始化
'''

mp = ModelProvider()

def parser_thoughts(response):
  """
    response:
    {
      "action": {
        "name": "action name",
        "args": {
          "arg name": "arg value"
        }
      },
      "thoughts": {
        "text": "thought",
        "plan": "plan",
        "criticism": "criticism",
        "speak": "speak", 当前步骤，返回给用户的总结
        "reasoning": ""
      },
      "observation": "The overall progress of the current task"
    }
  """
  try:
    thoughts = response.get('thoughts')
    plan = thoughts['plan']
    reasoning = thoughts['reasoning']
    criticism = thoughts['criticism']
    observation = response.get('observation')
    prompt = f"plan:{plan}\nreasoning:{reasoning}\ncriticism:{criticism}\nobservation:{observation}"

    return prompt
  except Exception as err:
    print(f'parse thought err:{err}')
    return "".format(err) # err转换成string类型

# 大模型运行
def agent_excute(query, max_request_time = 10):
  current_request_time = 0
  chat_history = [] # 用于记录历史信息（内容、时间...）
  agent_scratch = '' # 用于记录llm的反思、思考
  while current_request_time < max_request_time:
    current_request_time += 1
    """
    如果返回结果达到预期，则直接返回
    """
    prompt = generate_prompt(query, agent_scratch)

    # 大模型调用时间
    start_time = time.time()

    # call llm
    # print(f'chat history: {chat_history}')
    response = mp.chat(prompt = prompt, chat_history = chat_history)

    end_time = time.time()
    print(f'llm call time: {end_time - start_time}', flush = True)

    if not response or not isinstance(response, dict):
      print(f'llm call error, please try again: {response}')
      continue
    
    """
    response:
    {
      "action": {
        "name": "action name",
        "args": {
          "arg name": "arg value"
        }
      },
      "thoughts": {
        "text": "thought",
        "plan": "plan",
        "self-criticism": "criticism",
        "speak": "speak", current step, conclusion for user
        "reasoning": ""
      }
    }
    """
    action_info = response.get("action")
    action_name = action_info['name']
    action_args = action_info['args']
    print(f'action name:{action_name}, args:{action_args}')

    if action_name == 'finish':
      final_answer = action_args.get('answer')
      print(f'final_answer:{final_answer}')
      break

    observation = response.get('observation')
    print(f'observation:{observation}')
    try:
      # 将action_name映射到对应的工具函数
      func = tools_map.get(action_name)
      tool_result = func(**action_args)
    except Exception as err:
      print(f'call tool error: {err}')

    agent_scratch = agent_scratch + f'\nobservation:{observation}\ntool_result:{tool_result}'

    assistant_msg = parser_thoughts(response)
    chat_history.append([user_prompt, assistant_msg])

    if current_request_time == max_request_time:
      print(f'llm call times over {max_request_time}, task failed')
    else:
      print(f'llm call times: {current_request_time}')

def main():
  # 支持用户的多轮输入
  max_request_time = 20
  while True:
    query = input("please input your goal:")
    if query == "exit":
      return
    agent_excute(query, max_request_time)

if __name__ == "__main__":
  main()