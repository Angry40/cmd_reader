import os
import sys
import re

# 获取脚本所在文件夹路径
if getattr(sys, 'frozen', False):
    # 当前处于 "frozen" / 打包的可执行文件中
    script_dir = os.path.dirname(sys.executable)
else:
    # 当前处于脚本文件中
    script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义函数，将文本按指定长度分割
def cut_text(text,lenth):
    # 使用正则表达式，将文本按指定长度分割
    textArr = re.findall('.{'+str(lenth)+'}', text) 
    # 将剩余的文本添加到列表中
    textArr.append(text[(len(textArr)*lenth):]) 
    # 返回分割后的文本列表
    return textArr

# 读取书籍名称
book = input('Type the book name：')
# 如果书籍名称为空，则读取之前保存的书籍名称
if book == '' :
    book = open(os.path.join(script_dir, 'book.log'), 'r',encoding='utf-8',errors='ignore').read()
# 如果书籍名称不为空，则将书籍名称保存到文件中
else:
    with open(os.path.join(script_dir, 'book.log'),'w',encoding='utf-8') as fp:
        fp.write(str(book))

# 定义进度文件名
bookmark_file = os.path.join(script_dir, book + '.log')
# 尝试读取进度文件
try:
    # 读取进度文件中的当前页数
    old_bookmark = int(open(bookmark_file, 'r',encoding='utf-8',errors='ignore').read())
# 如果读取进度文件失败，则将当前页数设置为0
except:
    old_bookmark = 0

# 读取用户输入的关键字
keywords = input('Enter keyword search：')
# 初始化当前页数和搜索标志
new_bookmark = 0
search = True if bool(keywords) else False

length = input('Type the number of per line：')
if length == '': length = 12
else: length = int(length)

# 打开书籍文件
with open(os.path.join(script_dir, book+'.txt'), 'r' ,encoding='utf-8') as f :
    # 逐行读取书籍内容
    for line in f :
        # 当前页数加1
        new_bookmark = new_bookmark + 1
        # 去除行末的换行符和空格
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        # 如果搜索到关键字并且搜索标志为True
        if keywords in line and search:
            # 如果行长度小于等于指定长度，则直接输出
            if len(line) <= length:
                search_id = input(line)
            # 如果行长度大于指定长度，则按指定长度分割后输出
            else:
                search_id = input(cut_text(line,length)[0])
            # 如果用户输入's'，则将当前页数保存到进度文件中，并退出搜索
            if search_id == 's':
                with open(bookmark_file,'w',encoding='utf-8') as fp:
                    fp.write(str(new_bookmark))
                print('Bookmark updated successfully！')
                old_bookmark = new_bookmark
                search = False
        # 如果当前页数大于等于上次保存的页数并且搜索标志为False
        if new_bookmark >= old_bookmark and search == False:
            # 如果行长度小于等于指定长度，则直接输出
            if len(line) <= length:
                input(line)
            # 如果行长度大于指定长度，则按指定长度分割后输出
            else:
                for ii in cut_text(line,length):
                    input(ii)
            # 将当前页数保存到进度文件中
            with open(bookmark_file,'w',encoding='utf-8') as fp:
                fp.write(str(new_bookmark))