"""
1. write files
2. read files
3. append contents in files
4. web search for specialized knowledge
"""
import os
from langchain_community.tools.tavily_search import TavilySearchResults

# 定义工作目录
def _get_workdir_root():
  workdir_root = os.environ.get("WORKDIR_ROOT", "./data/llm_result")
  return workdir_root
workdir_root = _get_workdir_root()

def read_file(filename):
  global workdir_root
  filename = os.path.join(workdir_root, filename)
  if not os.path.exists(filename):
    return f'{filename} does not exist, please check whether file exists before read'
  with open(filename, 'r') as f:
    return "\n".join(f.readlines)
  
def append_to_file(filename, content = "\n"):
  global workdir_root
  filename = os.path.join(workdir_root, filename)
  if not os.path.exists(filename):
    return f'{filename} does not exist, please check whether file exists before append'
  with open(filename, 'a') as f:
    f.write(content)
  return "append content to file successfully!"

def write_file(filename, content = ""):
  global workdir_root
  filename = os.path.join(workdir_root, filename)
  if not os.path.exists(workdir_root):
    os.makedirs(workdir_root)

  with open(filename, 'w') as f:
    f.write(content)
  return "write content to file successfully!"

def search_web(query):
  TavilySearchResults(max_results)