import streamlit as st
import requests
import re
from io import StringIO

st.set_page_config(page_title="Proxy Converter & Checker", layout="centered")

st.title("🛠️ Proxy Converter & Checker Tool")

input_text = st.text_area("Nhập danh sách proxy:", height=300, placeholder="Ví dụ:\n14.190.107.199:37434:66an:stt46mtk\nhttp://66an:stt46mtk@14.190.107.199:37434")

convert_option = st.radio("Chọn kiểu chuyển đổi:", ("IP:PORT:USER:PASS ➜ http", "http ➜ IP:PORT:USER:PASS"))

check_live = st.checkbox("✅ Kiểm tra proxy live/die")

timeout = st.slider("⏱️ Timeout khi kiểm tra (giây)", min_value=1, max_value=10, value=5)

# Hàm chuyển đổi định dạng proxy
def convert_line(line, mode):
    if mode == "IP:PORT:USER:PASS ➜ http":
        parts = line.strip().split(":")
        if len(parts) == 4:
            ip, port, user, pwd = parts
            return f"http://{user}:{pwd}@{ip}:{port}"
    elif mode == "http ➜ IP:PORT:USER:PASS":
        match = re.match(r"http://(.*?):(.*?)@(.*?):(.*)", line.strip())
        if match:
            user, pwd, ip, port = match.groups()
            return f"{ip}:{port}:{user}:{pwd}"
    return None

# Hàm kiểm tra proxy live hay die
def is_proxy_live(proxy_url, timeout=5):
    try:
        proxies = {"http": proxy_url, "https": proxy_url}
        r = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=timeout)
        return r.status_code == 200
    except:
        return False

# Xử lý khi nhấn nút
if st.button("🔥 Bắt đầu xử lý"):
    lines = input_text.strip().splitlines()
    results = []
    live_list = []
    dead_list = []

    for line in lines:
        conv = convert_line(line, convert_option)
        if conv:
            if check_live:
                if is_proxy_live(conv, timeout):
                    status = "✅ LIVE"
                    live_list.append(conv)
                else:
                    status = "❌ DIE"
                    dead_list.append(conv)
            else:
                status = ""
            results.append(f"{conv} {status}".strip())
        else:
            results.append(f"❗ Sai định dạng: {line}")

    result_text = "\n".join(results)
    st.text_area("🎯 Kết quả:", result_text, height=300)

    st.download_button("📥 Tải tất cả kết quả", data=result_text, file_name="converted_proxies.txt", mime="text/plain")

    # Nếu có bật kiểm tra live
    if check_live:
        live_text = "\n".join(live_list)
        die_text = "\n".join(dead_list)

        st.subheader("✅ Proxy Live")
        st.text_area("Live", live_text, height=200)
        st.download_button("📥 Tải Live Proxy", data=live_text, file_name="live_proxies.txt", mime="text/plain")

        st.subheader("❌ Proxy Die")
        st.text_area("Die", die_text, height=200)
        st.download_button("📥 Tải Die Proxy", data=die_text, file_name="dead_proxies.txt", mime="text/plain")
