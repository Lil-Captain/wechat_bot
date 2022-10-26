# author: lian
# date: 2022/6/9
import requests
import json
from datetime import datetime

def webhook():
    # 和风天气：https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
    qweather_key = "f7cc78d23ddf471092c5db239ce58c19"
    wuchang_location = 101200111
    weather_header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
    ignore_list = ["晴", "多云"]
    try:
        response = requests.get(
            url=f"https://devapi.qweather.com/v7/weather/3d?location={wuchang_location}&key={qweather_key}",
            headers=weather_header)
    except Exception as e:
        body = {
            "msgtype": "text",
            "text": {
                "content": "信息获取失败",
                "mentioned_mobile_list": ["13277377368"]
            }
        }
        return body

    if response.status_code == 200:
        try:
            weather_data = json.loads(response.text).get("daily")[1]
            if weather_data['textDay'] in ignore_list:
                body = {
                    "msgtype": "markdown",
                    "markdown": {
                        "content": f"下面播报武昌区明日天气情况：\n"
                                   f">天气：{weather_data['textDay']}\n"
                                   f">最高温：{weather_data['tempMax']}\n"
                                   f">最低温：{weather_data['tempMin']}\n",
                    }
                }
            else:
                body = {
                    "msgtype": "text",
                    "text": {
                        "content": f"下面播报武昌区明日天气情况：\n"
                                   f"天气：{weather_data['textDay']}\n"
                                   f"最高温：{weather_data['tempMax']}\n"
                                   f"最低温：{weather_data['tempMin']}\n"
                                   f"出门前请做好充足准备！",
                        "mentioned_mobile_list": ["@all"]
                    }
                }
        except Exception as e:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('/home/ln/log/weather_log.txt', 'a') as f:
                f.write(now + "：" + str(response.text) + "\n")
            body = {
                "msgtype": "text",
                "text": {
                    "content": "信息获取失败",
                    "mentioned_mobile_list": ["13277377368"]
                }
            }
            return body
    else:
        body = {
            "msgtype": "text",
            "text": {
                "content": "访问出错",
                "mentioned_mobile_list": ["13277377368"]
            }
        }
    return body


if __name__ == '__main__':
    body = webhook()
    wechat_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=91e7f6c0-74f8-4d8e-ae42-9f32da330b88"
    wechat_header = {'Content-Type': 'application/json; charset=UTF-8'}
    requests.post(url=wechat_url, json=body, headers=wechat_header)
