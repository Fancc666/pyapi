from http.server import BaseHTTPRequestHandler
# from http.server import HTTPServer
import requests
import re
import json
from urllib.parse import unquote
import urllib3


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        urllib3.disable_warnings()

        self.reply = {
            'code': 0,
            'msg': "",
            'v_link': ""
        }

        bv_num = self.get_para("bv")
        if bv_num != "":
            bv_num = unquote(bv_num, 'utf-8')
            try:
                req_text = self.get_html("https://m.bilibili.com/video/" + bv_num)
                v_link = re.findall(r"\"readyVideoUrl\":\"(.*?)\"", req_text)
                if len(v_link) > 0:
                    self.reply['msg'] = "ok"
                    self.reply['v_link'] = v_link[0]
                else:
                    self.err("can not find video link")
                self.end()
            except Exception as e:
                self.err("access is invalid")
                self.end()
        else:
            self.err("parameter is missing")
            self.end()

        return
    def show_text(self, text):
        self.wfile.write(str(text).encode('utf-8'))
    def get_para(self, name):
        f = re.findall(r"(?:\&|\?)"+name+r"=(.*?)(?:\&|$)", self.path)
        if len(f) > 0:
            return f[0]
        else:
            return ""
    def get_html(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) \
                        AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        req = requests.get(url, verify=False, headers=headers)
        req.encoding = "utf-8"
        return req.text
    def err(self, msg):
        self.reply['code'] = 1
        self.reply['msg'] = msg
    def end(self):
        self.show_text("api_response=")
        self.show_text(json.dumps(self.reply))


# if __name__ == "__main__":
#     s = HTTPServer(('localhost', 8888), handler)
#     print("server is running...")
#     s.serve_forever()
