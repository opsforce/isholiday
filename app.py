import datetime
import json
import pytz

from flask import Flask, jsonify, redirect, abort, url_for

app = Flask(__name__)


with open('isholiday/legal_holidays.json', 'r') as f:
    lh = json.loads(f.read())


@app.route('/')
@app.route('/today')
def today():
    date = datetime.datetime.now() + datetime.timedelta(hours=8)
    date_str = date.strftime("%Y-%m-%d")
    date_weekday = date.isoweekday()  # 周几，1-7

    _dict = {}

    if date_str in lh:
        _dict[date_str] = lh[date_str]
    else:
        if date_weekday == 6 or date_weekday == 7:
            _dict[date_str] = True
        else:
            _dict[date_str] = False

    return jsonify(_dict)  # 返回字典，并 header: application/json


@app.route('/yesterday')
def yesterday():
    interval = datetime.timedelta(days=-1)
    date = datetime.datetime.now() + datetime.timedelta(hours=8) + interval
    date_str = date.strftime("%Y-%m-%d")
    date_weekday = date.isoweekday()  # 周几，1-7

    _dict = {}

    if date_str in lh:
        _dict[date_str] = lh[date_str]
    else:
        if date_weekday == 6 or date_weekday == 7:
            _dict[date_str] = True
        else:
            _dict[date_str] = False

    return jsonify(_dict)


@app.route('/tomorrow')
def tomorrow():
    interval = datetime.timedelta(days=1)
    date = datetime.datetime.now() + datetime.timedelta(hours=8) + interval
    date_str = date.strftime("%Y-%m-%d")
    date_weekday = date.isoweekday()  # 周几，1-7

    _dict = {}

    if date_str in lh:
        _dict[date_str] = lh[date_str]
    else:
        if date_weekday == 6 or date_weekday == 7:
            _dict[date_str] = True
        else:
            _dict[date_str] = False

    return jsonify(_dict)


@app.route('/<someday>')
def index(someday):
    if someday:
        try:
            date = datetime.datetime.strptime(someday, "%Y-%m-%d")
            date_str = date.strftime("%Y-%m-%d")
            date_weekday = date.isoweekday()  # 周几，1-7

            _dict = {}

            if date_str in lh:
                _dict[date_str] = lh[date_str]
            else:
                if date_weekday == 6 or date_weekday == 7:
                    _dict[date_str] = True
                else:
                    _dict[date_str] = False

            return jsonify(_dict)
        except Exception as e:
            app.logger.error(e)
            return """开发完成：
0. 只支持本年内日期查询
1. 支持常见日子查询：昨天、今天、明天
2. 支持某个日期查询，且只支持特定日期格式：2021-01-01

开发中：
0. 支持常见日子查询：前天、后天
1. 支持查询上个月、本月、下个月
2. 支持查询某年、某月
3. 支持查询前年、去年、今年、明年（不一定准确）、后年（不一定准确）
4. 支持某个日期查询，且支持多种日期格式"""

    # else:
    #     return redirect(url_for('/'))

    # if not _items:
    #     abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
