import os
from flask import Flask, request, make_response

app = Flask(__name__)

FLAG = os.getenv("GZCTF_FLAG", "flag{00000000-0000-0000-0000-000000000000}")
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "SVUCTF"]

# 假设 Flag 格式为 flag{UUID}，总长度足够
part_length = len(FLAG) // len(ALLOWED_METHODS) + 1
FLAG_PARTS = {
    method: (i + 1, FLAG[i * part_length : (i + 1) * part_length])
    for i, method in enumerate(ALLOWED_METHODS)
}


@app.route("/", methods=ALLOWED_METHODS)
def challenge():
    method = request.method

    if method in ALLOWED_METHODS:
        part_number, flag_part = FLAG_PARTS[method]

        response = f"这是 Flag 的第 {part_number} 部分：{flag_part}"

        if method == "GET":
            response += f"<br>提示：完整的 flag 分为 {len(FLAG_PARTS)} 个部分，每个部分需要使用不同的 HTTP 方法获取。"
            response += "<br>已知的 HTTP 方法有：GET、POST、PUT、DELETE、OPTIONS，以及一个自定义方法。"

        elif method == "OPTIONS":
            resp = make_response(response)
            resp.headers["Allow"] = ", ".join(ALLOWED_METHODS)
            return resp

        elif method == "SVUCTF":
            response = "恭喜你找到了隐藏方法，" + response

        return response
    else:
        return "尝试不同的 HTTP 方法", 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
