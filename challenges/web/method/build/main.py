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
        if method == "OPTIONS":
            response = make_response(f"这是 Flag 的第 {part_number} 部分：{flag_part}")
            response.headers["Allow"] = ", ".join(ALLOWED_METHODS)
            return response
        elif method == "SVUCTF":
            return f"恭喜你找到了隐藏方法，这是第 {part_number} 部分：{flag_part}"
        else:
            return f"这是 Flag 的第 {part_number} 部分：{flag_part}"
    else:
        return "尝试不同的 HTTP 方法"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
