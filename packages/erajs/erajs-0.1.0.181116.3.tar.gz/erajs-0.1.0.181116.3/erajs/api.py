# coding:utf-8
from . import mid

m = mid.mid
version = '0.1.0'
data = {}

# 显示控制


def init():
    """
    初始化Era.js引擎。\n
    该语句必须在以下所有语句调用之前使用。\n
    """
    global data
    data = m.get_data()


def debug(text):
    """
    调试用输出。\n
    """
    global m
    return m.debug(text)


def info(text):
    """
    调试用输出。\n
    """
    global m
    return m.info(text)


def warn(text):
    """
    调试用输出。\n
    """
    global m
    return m.warn(text)


def error(text):
    """
    调试用输出。\n
    """
    global m
    return m.error(text)


def critical(text):
    """
    调试用输出。\n
    """
    global m
    return m.critical(text)


def title(text):
    """
    更改游戏窗口标题。\n
    """
    global m
    m.title(text)


def page(color='default'):
    """
    新建页面。\n
    """
    global m
    m.page(color)


def t(text='', wait=False, color='default', bcolor='default'):
    """
    显示 text。\n
    当 text 为 "" 时，换行（所有控件间均可以使用该方法换行）；\n
    当 wait 为 True 时，停在当前地方，直到点击鼠标左键或鼠标右键。\n
    左键跳过一句，右键跳过一段。\n
    """
    global m
    m.t(text, wait, color, bcolor)


def b(text, func, *arg, **kw):
    """
    显示按钮，其内容为 text。\n
    func 为 返回函数，当按钮按下时，func 执行，且其执行参数为 *arg 和 **kw ；\n
    常见用法：api.b('TEST_BUTTON', api.goto, NEXT_PAGE_FUNC)\n
    注意：若向该参数显式传递参数 disabled=True 时，会生成一个被禁用的按钮\n
    """
    global m
    m.b(text, func, *arg, **kw)


def h(text, rank=1, color='default', bcolor='default'):
    """
    显示标题，其内容为 text。\n
    """
    global m
    m.h(text, rank, color, bcolor)


def rate(now=0,  max=5, func=None, disabled=True):
    """
    显示评级，其内容为 text。\n
    func 为 返回函数，当评级的数值改变时，func 执行，且其执行参数为：\n
    {
        "value": 【改变后的评级数值】
    }\n
    """
    global m
    return m.rate(now, max, func, disabled)


def progress(now, max=100, length=100):
    """
    显示进度条，其长度为 length。\n
    now 表示当前值；max 表示最大值。\n
    """
    global m
    return m.progress(now, max, length)


def radio(choice_list, default_index=0, func=None):
    """
    显示单选。\n
    choice_list 表示显示内容，如["低", "中", "高"]；\n
    default_index 表示默认选中的内容，如 1 表示 “中” 默认被选中。\n
    func 是返回函数，当单选的状态被改变时触发，其参数为：\n
    {
        "value": 【当前选中的内容】
    }\n
    """
    global m
    return m.radio(choice_list, default_index, func)


def input(func=None):
    """
    显示输入框。\n
    func 是返回函数，当输入框的内容被改变时触发，其参数为：\n
    {
        "value": 【改变后的内容】
    }\n
    Tips：可与按钮连用进行自定义文本的输入。\n
    """
    global m
    return m.input(func)


def divider(text=''):
    """
    显示横线。\n
    Bug：显示文字暂时有Bug。\n
    """
    global m
    return m.divider(text)


def chart(chart_type, data, width=200, height=200):
    global m
    return m.chart(chart_type, data, width, height)


def clear(last=False):
    """
    清除所有显示。\n
    """
    global m
    m.clear(last)


def goto(func, *arg, **kw):
    """
    【界面逻辑函数】\n
    进入其中的页面。\n
    """
    global m
    m.goto(func, *arg, **kw)


def back(*arg, **kw):
    """
    【界面逻辑函数】\n
    退回到上一个浏览的页面。\n
    """
    global m
    m.back(*arg, **kw)


def repeat(*arg, **kw):
    """
    【界面逻辑函数】\n
    重复当前的页面。\n
    Tips：刷新数据时常用\n
    """
    global m
    m.repeat(*arg, **kw)


def clear_gui(num=0):
    """
    【界面逻辑函数】\n
    清除所有界面逻辑关系。\n
    """
    global m
    m.clear_gui(num)


def append_gui(func, *arg, **kw):
    """
    【界面逻辑函数】\n
    向界面链的末尾增加一个界面（但不触发）。\n
    """
    global m
    m.append_gui(func, *arg, **kw)


def show_save_to_save():
    """
    显示当前存档（存档用）。\n
    """
    global m
    m.show_save_to_save()


def show_save_to_load(func_after_load):
    """
    显示当前存档（读档用）。\n
    """
    global m
    m.show_save_to_load(func_after_load)


def mode():
    """
    改变显示模式。\n
    """
    global m
    pass


def exit(save=False):
    """
    改变显示模式。\n
    """
    global m
    m.exit(save)

# 资源控制


def add(item):
    global m
    return m.add(item)


def get(pattern):
    global m
    return m.get(pattern)


# EraTime
def get_full_time():
    """
    以文本方式返回当前时间（全部）。\n
    """
    global m
    return m.get_full_time()


def tick():
    """
    时间流逝一个单位。\n
    """
    global m
    m.tick()


def ________________________________________________________________():
    pass


def new_hash():
    """
    返回一个HASH字符串。\n
    Tips：可用于索引和标记。\n
    """
    global m
    return m.new_hash()
