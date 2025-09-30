# magic import
from pip import main
from importlib.metadata import distributions
installed_packages = [dist.metadata['Name'] for dist in distributions()]
normal_import = __builtins__.__import__

def install(name, globals=None, locals=None, fromlist=(), level=0):
	__builtins__.__import__ = normal_import
	if name not in installed_packages:
		main(['install', '-U', name])
	name = normal_import(name, globals, locals, fromlist, level)
	__builtins__.__import__ = install
	return name

__builtins__.__import__ = install

# main.py

import requests, json, sys, traceback
from pyautogui import confirm

def conversation(contents, chat_mode=False):
  url = "https://api.360.cn/v1/chat/completions"
  payload = json.dumps({
    "model": "360/deepseek-r1",
    "messages": [
      {
        "role": "user",
        "content": contents
      }
    ],
    "stream": chat_mode,
    "temperature": 0.9,
    "max_tokens": 2048,
    "top_p": 0.5,
    "top_k": 0,
    "repetition_penalty": 1.05,
    "num_beams": 1,
    "user": "andy"
  })
  headers = {
    'Authorization': 'fk1357707141.BSCoDrkjDWq4N2aiATwpNRVnUL7WKimz726d4e68', # Replace it with your api key like this
    'Content-Type': 'application/json'
  }
  if not chat_mode:
    null = ''
    response = requests.request("POST", url, headers=headers, data=payload)
    return eval(response.text)['choices'][0]['message']['content']
  else:
    return requests.request("POST", url, headers=headers, data=payload, stream=True).iter_lines()


def execute(commands):
	global history
	Incorrect = True
	user_input = commands
	while Incorrect:
		try:
			RT = conversation(prompts+user_input)
			print('【AI】'+RT)
			commands = RT.split('```')[1::2]
			for item in commands:
				if item.startswith('python\n'):
					command = item[7:]
					if confirm(f'请问您要执行这个Python命令吗？\n{command}', 'AIGC脚本语言')=='OK':
						exec(command)
					else:
						user_input+='\n用户因为如下原因拒绝执行命令：'+input('【AIGC】请输入拒绝执行命令的原因：\n【我】')+'\n请你针对该要求，重新给出修正版的完整解决方案，不要输出之前的代码，直接输出你更正之后的代码'
						break

					Incorrect = False
		except:
			print('【出错，重新尝试中】')
			user_input+='\n实际执行过程中出错，报错信息如下：'+traceback.format_exc()+'\n请你针对错误，重新给出修正版的完整解决方案，不要输出之前的代码，直接输出你更正之后的代码'
	history += user_input
	history += '\n'

prompts = "现在，你拥有控制计算机的能力，你可以控制鼠标键盘，并且可以读取剪切板。在本平台中，你是中文编程语言的助手。用户输入中文命令，然后你必须用Markdown语法，回答以Python代码（只能使用Python语言，可以使用第三方库，而且优先考虑通过Python调用Linux终端），且不许提出多种解决方案（否则重复的命令会被执行2遍），然后直接执行用户的命令。如果你缺少相关的信息，你可以通过input函数向用户询问，但是只问你完全不知道的信息，你知道的信息你可以根据你的知识自动补充。\n以下是用户的命令：\n"

history = ''

if len(sys.argv) == 1:
	while True:
		execute(input('【我】'))
else:
	with open(sys.argv[1], encoding='utf-8') as scripts:
		execute(scripts.read())

