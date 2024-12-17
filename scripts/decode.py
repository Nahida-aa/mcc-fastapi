import base64
import json

def decode_jwt(token):
    # 分割 JWT，获取 payload 部分
    payload = token.split('.')[1]
    
    # 添加必要的填充字符
    padding = '=' * (4 - len(payload) % 4)
    payload += padding
    
    # 解码 Base64 URL 安全编码的字符串
    decoded_bytes = base64.urlsafe_b64decode(payload)
    decoded_str = decoded_bytes.decode('utf-8')
    
    # 将 JSON 字符串转换为 Python 字典
    decoded_dict = json.loads(decoded_str)
    return decoded_dict

# 示例 JWT
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiTmFoaWRhLWFhIiwiaW1hZ2UiOiJodHRwczovL2F2YXRhcnMuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3UvOTYwODM5MjY_dj00IiwiZW1haWwiOiJ0ZXN0QGlvIiwibmlja25hbWUiOiIiLCJleHAiOjE3MzUxMTE3OTR9.00YDvEojL-L_teOj4WaHN0Cq5AsVdQ3che0vd28xNPM"

decoded_payload = decode_jwt(token)
print(decoded_payload)