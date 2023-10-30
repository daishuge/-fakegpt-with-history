import time
from fake_api import fake_api
from token_count import token_count
import config
import random

print('''
作者: daishuge袋鼠哥
项目地址: https://github.com/daishuge/fakegpt_with_history
''')
print("加载分词中...\n")
token_count("1")    #初始化jieba
print("\n")

history = []    #历史记录储存

def main():

    if config.if_pandora:
        print("尝试向pandora发送测试文本...")

        try:
            fake_api("hi", 2500,True,1,config.if_pandora)
        except:
            config.if_pandora=False
            print("pandora 连接错误, 尝试官方api")

    elif not config.if_pandora:
        config.if_pandora=False

    time.sleep(1)

    print(f'''

    起始设置
    是否使用pandora:   {config.if_pandora}
    是否启用概括:      {config.long_text}
    到达此token则概括: {config.max_token}
    概括成此单词数:    {config.smaller_text}
    openai_api:        {config.openai_api}
    pandora_api:       {config.pandora_api}
    base_url:          {config.base_url}
    ''')

    while True:
        query = input("\n\nYou: ")
        if query == "clear":
            history.clear()
            print("历史记录已清空!")
            continue

        history.append("user:" + query)
        history_string="".join(history)
        full_result = fake_api(history_string, 2500,True,1,config.if_pandora)

        history.append("chatgpt: " + full_result)

        history_string="".join(history)

        if config.long_text:
            print("")
            tokens=token_count(history_string)

            if tokens>config.max_token:
                    print("概括中...")

                    history_string="".join(history)

                    gaikuo=fake_api("请把这段文字概括成"+str(config.smaller_text)+"个英文单词以内,不要有多余内容,特别注意千万不要超过单词数: "+history_string,600,True,0.3,config.if_pandora)
                    
                    history.clear()

                    history.append("history:"+gaikuo)

if __name__ == '__main__':
    main()