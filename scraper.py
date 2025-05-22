import requests
from bs4 import BeautifulSoup

login_url = "https://www.otustanausta.com/ucp.php?mode=login"
inbox_url = "https://www.otustanausta.com/ucp.php?i=pm&folder=inbox"
base_url = "https://www.otustanausta.com/"

# Създаваме сесия
session = requests.Session()

# Вземаме login страницата
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Извличаме всички hidden input полета от login формата
login_form = soup.find("form", {"id": "login"})
hidden_fields = login_form.find_all("input", {"type": "hidden"})
form_data = {field.get("name"): field.get("value", "") for field in hidden_fields}

# Добавяме нашите логин данни
form_data.update({
    "username": "itv",
    "password": "P@r0la",
    "login": "Вход",  # това може да е 'Login' или друг текст — виж точния value на бутона
})

# Изпращаме POST заявка
login_response = session.post(login_url, data=form_data)

# Проверка за логин
if "Изход [" in login_response.text or "logout" in login_response.text.lower():
    print("✅ Успешен логин!")
else:
    print("❌ Неуспешен логин.")
    # Записваме HTML за преглед
    with open("debug_login.html", "w", encoding="utf-8") as f:
        f.write(login_response.text)
    print("📄 Записах отговора от сървъра в debug_login.html. Отвори го и провери за грешка.")
