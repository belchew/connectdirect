import requests
from bs4 import BeautifulSoup

login_url = "https://www.otustanausta.com/ucp.php?mode=login"

# 🔒 Твоите данни
USERNAME = "itv"
PASSWORD = "P@r0la"

# Създаваме сесия
session = requests.Session()

# Вземаме login страницата
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")

# Взимаме формата и скритите полета
login_form = soup.find("form", {"id": "login"})
hidden_fields = login_form.find_all("input", {"type": "hidden"})
form_data = {field.get("name"): field.get("value", "") for field in hidden_fields}

# Добавяме нашите данни
form_data.update({
    "username": USERNAME,
    "password": PASSWORD,
    "login": "Login",  # ⚠️ смени на "Вход" или "Влез", ако не работи!
})

# 🐞 Дебъг: показваме какво пращаме
print("🔍 POST данни за логин:")
for key, val in form_data.items():
    print(f"  {key}: {val}")

# Изпращаме заявка
login_response = session.post(login_url, data=form_data)

# Проверка
if "Изход [" in login_response.text or "logout" in login_response.text.lower():
    print("✅ Успешен логин!")
else:
    print("❌ Неуспешен логин.")
    with open("debug_login.html", "w", encoding="utf-8") as f:
        f.write(login_response.text)
    print("📄 Записах отговора в debug_login.html. Провери какво пише вътре.")
