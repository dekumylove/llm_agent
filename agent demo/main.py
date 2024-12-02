# agent entrance
import time
'''
todo:
  1、环境变量设置
  2、工具的引入
  3、prompt模版
  4、模型的初始化
'''

# 调用大模型
def call_llm():


# 生成prompt
def generate_prompt(query, agent_scratch):
  """
    prompt：
      1、人物描述
      2、工具描述
      3、用户的输入user_msg
      4、assistant_msg
      5、限制
      6、通过反思，给出更好实践的描述
  """

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
      }
    }
  """
  try:
    thoughts = response.get('thoughts')
    plan = thoughts['plan']
    reasoning = thoughts['reasoning']
    criticism = thoughts['criticism']
    observation = thoughts['speak']
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
    response = call_llm(prompt)

    end_time = time.time()
    print(f'大模型调用时间：{end_time - start_time}', flush = True)

    if not response or not isinstance(response, dict):
      print(f'大模型调用错误，请重试：', response)
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
        "speak": "speak", 当前步骤，返回给用户的总结
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

    observation = response.get('thoughts')['speak']
    try:
      # 将action_name映射到对应的工具函数
      tools_map = {

      }
      func = tools_map,get(action_name)
      observation = func(**action_args)
    except Exception as err:
      print(f'调用工具失败：{err}')

    agent_scratch = agent_scratch + "\n" + observation

    user_msg = "决定使用哪个工具"
    assistant_msg = parser_thoughts(response)
    chat_history.append([user_msg, assistant_msg])

def main():
  # 支持用户的多轮输入
  max_request_time = 10
  while True:
    query = input("请输入您的目标")
    if query == "exit":
      return
    agent_excute(query, max_request_time)

if __name__ == "__main__":
  main()