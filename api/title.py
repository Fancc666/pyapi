from http.server import BaseHTTPRequestHandler
import requests
import re
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        self.reply = {
            'code': 0,
            'msg': "",
            'title': ""
        }

        l = self.get_para("link")
        if l != "":
            # try:
            #     req_text = self.get_html(l)
            #     tit = re.findall(r"<title>(.*?)</title>", req_text)
            #     if len(tit) > 0:
            #         self.reply['msg'] = "ok"
            #         self.reply['title'] = tit[0]
            #     else:
            #         self.err("there is no title in the site")
            #     self.end()
            # except:
            #     self.err("access is invalid")
            #     self.end()
            self.show_text(self.get_html(l))
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
        req = requests.get(url)
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
