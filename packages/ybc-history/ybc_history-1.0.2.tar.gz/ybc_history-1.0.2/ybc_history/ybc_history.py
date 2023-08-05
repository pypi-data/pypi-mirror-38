import datetime

import requests

import ybc_config

__PREFIX = ybc_config.config['prefix']
__HISTORY_URL = __PREFIX + ybc_config.uri + '/history'


def history_info(month=datetime.datetime.today().month, day=datetime.datetime.today().day, number=3, type='string'):
    """
    功能：获取历史上的今天。

    参数：month，day：日期，默认今天
         number：事件条数，超出则返回当天所有事件
         type：返回值类型，输入list返回列表，其他则返回string

    返回：历史上的今天事件
    """
    days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    error_flag = 1
    # 参数类型正确性判断
    error_msg = ""
    if not isinstance(month, int):
        error_flag = -1
        error_msg = "'month'"
    if not isinstance(day, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'day'"
    if not isinstance(number, int):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'number'"
    if not isinstance(type, str):
        if error_flag == -1:
            error_msg += "、"
        error_flag = -1
        error_msg += "'type'"
    if error_flag == -1:
        return "history_info方法" + error_msg + "参数类型错误: 请输入正确的参数类型 "

    # 参数取值正确性判断
    error_msg = "history_info方法使用错误: "
    if (day < 1) | (month < 1) | (month > 12) | (day > days[month - 1]):
        error_flag = -1
        error_msg += "输入日期不存在"
    if number <= 0:
        if error_flag == -1:
            error_msg += ";"
        error_flag = -1
        error_msg += "历史事件数输入错误"
    if error_flag == -1:
        return error_msg

    params = {
        "month": month,
        "day": day,
        "number": number
    }

    url = __HISTORY_URL
    for i in range(3):
        r = requests.get(url, params)
        if r.status_code == 200:
            res = r.json()
            if number > len(res):
                print("history_info方法使用提示: 超出该天记录事件数，已展示所有事件")

            if type == 'list':
                return res
            else:
                return "\n".join(res)

    return "history_info方法调用失败: 请稍后再试"


def main():
    result = history_info(1, 1, 3, "list")
    print(result)


if __name__ == '__main__':
    main()
