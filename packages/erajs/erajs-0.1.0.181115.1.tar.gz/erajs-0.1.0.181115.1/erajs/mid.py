# coding:utf-8
from . import engine as e

data = {}

engine = e.Engine()


class Mid():
    def __init__(self):
        engine.info('Initializing...')
        engine.info('├─ Fixing Path...')
        engine.fix_path()
        engine.info('├─ Checking Program Integrity...')
        engine.self_check()
        engine.info('├─ Loading Engine Configuration...')
        engine.load_config(['config/config.ini'])
        engine.info('├─ Registering Native API...')
        engine.info('│  └─ {} Native APIs Registered!'.format(
            engine.register_api()))
        engine.info('├─ Scanning Plugins...')
        engine.info('│  └─ {} Plugins Scanned!'.format(engine.scan_plugin()))
        engine.info('├─ Loading Plugins...')
        engine.info('│  └─ {} Plugins Loaded!'.format(engine.load_plugin()))
        engine.info('├─ Connecting Server...')
        engine.connect()
        engine.info('├─ Transfering Configuration to Server...')
        engine.send_config()
        engine.info('├─ Loading Data Files...')
        data = engine.load_data(engine.scan('data'))
        for each in data.keys():
            engine.data[each] = data[each]
        engine.info('│  └─ Data Files Loaded!')
        engine.info('├─ Scanning Scripts...')
        engine.info('│  └─ {} Scripts Scanned!'.format(engine.scan_script()))
        engine.info('├─ Loading Scripts...')
        engine.info('│  └─ {} Scripts Loaded!'.format(engine.load_script()))
        engine.info('├─ Scanning DLCs...')
        engine.info('│  └─ {} DLCs Scanned!'.format(engine.scan_dlc()))
        engine.info('├─ Loading DLCs...')
        engine.info('│  └─ {} DLCs Loaded!'.format(engine.load_dlc()))
        engine.info('├─ Scanning MODs...')
        engine.info('│  └─ {} MODs Scanned!'.format(engine.scan_mod()))
        engine.info('├─ Loading MODs...')
        engine.info('│  └─ {} MODs Loaded!'.format(engine.load_mod()))
        engine.info('├─ Transferring Loading Complete Signal...')
        engine.send_loaded()
        engine.info('└─ Initialize Complete!')

    def debug(self, text):
        return engine.debug(text)

    def info(self, text):
        return engine.info(text)

    def warn(self, text):
        return engine.warn(text)

    def error(self, text):
        return engine.error(text)

    def critical(self, text):
        return engine.critical(text)

    def get_data(self):
        return engine.data

    def title(self, text):
        engine.title(text)

    def t(self, text='', wait=False, color='default', bcolor='default'):
        engine.t(text, wait, color, bcolor)

    def b(self, text, func, *arg, **kw):
        engine.b(text, func, *arg, **kw)

    def h(self, text, rank=1, color='default', bcolor='default'):
        engine.h(text, rank, color, bcolor)

    def rate(self, now=0,  max=5, func=None, disabled=True):
        return engine.data['api']['rate'](now, max, func, disabled)

    def progress(self, now, max=100, length='100px'):
        return engine.data['api']['progress'](now, max, length)

    def radio(self, choice_list, default_index=0, func=None):
        return engine.data['api']['radio'](choice_list, default_index, func)

    def input(self, func=None):
        return engine.data['api']['input'](func)

    def divider(self, text=''):
        return engine.data['api']['divider'](text)

    def chart(self, chart_type, data, width=200, height=200):
        return engine.data['api']['chart'](chart_type, data, width, height)

    def page(self, color='default'):
        engine.page(color)

    def clear(self, last=False):
        engine.clear(last)

    def goto(self, func, *arg, **kw):
        engine.goto(func, *arg, **kw)

    def back(self, *arg, **kw):
        engine.back(*arg, **kw)

    def repeat(self, *arg, **kw):
        engine.repeat(*arg, **kw)

    def clear_gui(self, num=0):
        engine.clear_gui(num)

    def append_gui(self, func, *arg, **kw):
        engine.append_gui(func, *arg, **kw)

    def show_save_to_save(self):
        def save_to(save_num):
            engine.save_to(save_num)
            engine.repeat()
        # 获取列表
        save_file_list = engine.scan('save')
        # 弱加载
        for each in save_file_list:
            pass
        # 计算显示
        save_list = []
        current_num = 1
        while True:
            if len(save_file_list) == 0:
                save_list.append((current_num, '未使用'))
                break
            elif int(save_file_list[0].split('\\')[-1].split('.')[0]) == current_num:
                save_list.append((current_num, str(current_num)))
                save_file_list = save_file_list[1:]
                current_num += 1
        # 显示
        for each in save_list:
            engine.b(str(each[0])+'. '+each[1], save_to, each[0])
            engine.t()
        # 处理
        pass

    def show_save_to_load(self, func_after_load):
        def load_from(save_num):
            engine.load_from(save_num)
            engine.clear_gui()
            engine.goto(func_after_load)
        # 获取列表
        save_file_list = engine.scan('save')
        # 弱加载
        for each in save_file_list:
            pass
        # 计算显示
        save_list = []
        for each in save_file_list:
            save_list.append((int(each.split('\\')[-1].split('.')[0]), ''))
        # 显示
        for each in save_list:
            engine.b(str(each[0])+'. '+each[1], load_from, each[0])
            engine.t()
        # 处理
        pass

    def save(self, filename):
        pass

    def load_save(self, filename):
        pass

    def add(self, item):
        return engine.add(item)

    def get(self, pattern):
        return engine.get(pattern)

    def get_full_time(self):
        return engine.data['api']['get_full_time']()

    def tick(self):
        engine.data['api']['tick']()

    def new_hash(self):
        return e.new_hash()

    def exit(self, save=False):
        return engine.exit(save)


mid = Mid()


# def init():
#     print('[DEBG]Initializing...')
#     print('[DEBG]├─ Fixing Path...', end='')
#     engine.fix_path()
#     print('OK')
#     print('[DEBG]├─ Checking Program Integrity...', end='')
#     engine.self_check()
#     print('OK')
#     print('[DEBG]├─ Loading Engine Configuration...', end='')
#     engine.load_config(['config/config.ini'])
#     print('OK')
#     print('[DEBG]├─ Registering Native API...')
#     print('[FINE]│  └─ {} Native APIs Registered!'.format(engine.register_api()))
#     print('[DEBG]├─ Scanning Plugins...')
#     print('[FINE]│  └─ {} Plugins Scanned!'.format(engine.scan_plugin()))
#     print('[DEBG]├─ Loading Plugins...')
#     print('[FINE]│  └─ {} Plugins Loaded!'.format(engine.load_plugin()))
#     print('[DEBG]├─ Connecting Server...', end='')
#     engine.connect()
#     print('OK')
#     print('[DEBG]├─ Transfering Configuration to Server...', end='')
#     engine.send_config()
#     print('OK')
#     print('[DEBG]├─ Loading Data Files...')
#     data = engine.load_data(engine.scan('data'))
#     for each in data.keys():
#         engine.data[each] = data[each]
#     print('[FINE]│  └─ Data Files Loaded!')
#     print('[DEBG]├─ Scanning Scripts...')
#     print('[FINE]│  └─ {} Scripts Scanned!'.format(engine.scan_script()))
#     print('[DEBG]├─ Loading Scripts...')
#     print('[FINE]│  └─ {} Scripts Loaded!'.format(engine.load_script()))
#     print('[DEBG]├─ Scanning DLCs...')
#     print('[FINE]│  └─ {} DLCs Scanned!'.format(engine.scan_dlc()))
#     print('[DEBG]├─ Loading DLCs...')
#     print('[FINE]│  └─ {} DLCs Loaded!'.format(engine.load_dlc()))
#     print('[DEBG]├─ Scanning MODs...')
#     print('[FINE]│  └─ {} MODs Scanned!'.format(engine.scan_mod()))
#     print('[DEBG]├─ Loading MODs...')
#     print('[FINE]│  └─ {} MODs Loaded!'.format(engine.load_mod()))
#     print('[DEBG]├─ Transferring Loading Complete Signal...', end='')
#     engine.send_loaded()
#     print('OK')
#     print('[FINE]└─ Initialize Complete!')
#     return engine.data


# def title(text):
#     engine.title(text)


# def t(text='', wait=False):
#     engine.t(text, wait)


# def b(text, func, *arg, **kw):
#     engine.b(text, func, *arg, **kw)


# def h(text, rank=1):
#     engine.h(text, rank)


# def rate(now=0,  max=5, func=None):
#     return engine.data['api']['rate'](now, max, func)


# def progress(now, max=100, length=100):
#     return engine.data['api']['progress'](now, max, length)


# def radio(choice_list, default_index=0, func=None):
#     return engine.data['api']['radio'](choice_list, default_index, func)


# def input(func=None):
#     return engine.data['api']['input'](func)


# def divider(text=''):
#     return engine.data['api']['divider'](text)


# def page():
#     engine.page()


# def clear(last=False):
#     engine.clear(last)


# def goto(func, *arg, **kw):
#     engine.goto(func, *arg, **kw)


# def back(*arg, **kw):
#     engine.back(*arg, **kw)


# def repeat(*arg, **kw):
#     engine.repeat(*arg, **kw)


# def clear_gui(num=1):
#     engine.clear_gui(num)


# def show_save_to_save():
#     def save_to(save_num):
#         engine.save_to(save_num)
#         engine.repeat()
#     # 获取列表
#     save_file_list = engine.scan('save')
#     # print(save_file_list)
#     # 弱加载
#     for each in save_file_list:
#         pass
#     # 计算显示
#     save_list = []
#     current_num = 1
#     while True:
#         if len(save_file_list) == 0:
#             save_list.append((current_num, '未使用'))
#             break
#         elif int(save_file_list[0].split('\\')[-1].split('.')[0]) == current_num:
#             save_list.append((current_num, str(current_num)))
#             save_file_list = save_file_list[1:]
#             current_num += 1
#     # 显示
#     for each in save_list:
#         engine.b(str(each[0])+'. '+each[1], save_to, each[0])
#         engine.t()
#     # 处理
#     pass


# def show_save_to_load(func_after_load):
#     def load_from(save_num):
#         engine.load_from(save_num)
#         engine.clear_gui()
#         engine.goto(func_after_load)
#     # 获取列表
#     save_file_list = engine.scan('save')
#     # 弱加载
#     for each in save_file_list:
#         pass
#     # 计算显示
#     save_list = []
#     for each in save_file_list:
#         save_list.append((int(each.split('\\')[-1].split('.')[0]), ''))
#     # 显示
#     for each in save_list:
#         engine.b(str(each[0])+'. '+each[1], load_from, each[0])
#         engine.t()
#     # 处理
#     pass


# def save(filename):
#     pass


# def load_save(filename):
#     pass


# def add(item):
#     return engine.add(item)


# def get(pattern):
#     return engine.get(pattern)


# def get_full_time():
#     return engine.data['api']['get_full_time']()


# def tick():
#     engine.data['api']['tick']()


# def _______________________________________________________():
#     pass


# def new_hash():
#     return e.new_hash()
