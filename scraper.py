import requests
from bs4 import BeautifulSoup

login_url = "https://www.otustanausta.com/ucp.php?mode=login"
inbox_url = "https://www.otustanausta.com/ucp.php?i=pm&folder=inbox"
base_url = "https://www.otustanausta.com/"

USERNAME = "itv"
PASSWORD = "P@r0la"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": login_url,
    "Content-Type": "application/x-www-form-urlencoded",
}

# 1. Вземаме login страницата
response = session.get(login_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2. Събираме скритите полета
login_form = soup.find("form", {"id": "login"})
hidden_fields = login_form.find_all("input", {"type": "hidden"})
form_data = {field.get("name"): field.get("value", "") for field in hidden_fields}

# 3. Добавяме нашите данни
form_data.update({
    "username": USERNAME,
    "password": PASSWORD,
    "login": "Login",  # важно е да съвпада с value на бутона
})

# 4. Изпращаме заявка с headers
login_response = session.post(login_url, data=form_data, headers=headers)

# 5. Проверка
if "Изход [" in login_response.text or "logout" in login_response.text.lower():
    print("✅ Успешен логин!")
else:
    print("❌ Неуспешен логин.")
    with open("debug_login.html", "w", encoding="utf-8") as f:
        f.write(login_response.text)
    print("📄 Провери debug_login.html за съобщение от сайта.")
