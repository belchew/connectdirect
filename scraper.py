import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Данни за вход
login_url = "https://www.otustanausta.com/ucp.php?mode=login"
inbox_url = "https://www.otustanausta.com/ucp.php?i=pm&folder=inbox"
username = "itv"
password = "P@r0la"

# Създаваме сесия
session = requests.Session()

# Първо зареждаме login формата, за да вземем токените
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, 'html.parser')

# Намираме необходимите скрити полета за вход (като form_token)
form_token = soup.find('input', {'name': 'form_token'})
form_token_value = form_token['value'] if form_token else ''

# Подготвяме payload за логин
payload = {
    'username': username,
    'password': password,
    'login': 'Вход',  # Това може да е 'Login' на английския интерфейс
    'form_token': form_token_value,
    'redirect': 'index.php',  # обикновено така е по подразбиране
    'autologin': 'on'
}

# Изпращаме POST заявка за логин
response = session.post(login_url, data=payload)

# Проверяваме дали входът е успешен
if "Излез" in response.text or "Logout" in response.text:
    print("[✓] Успешно влязохме в профила.")

    # Зареждаме страницата с входящите съобщения
    inbox_response = session.get(inbox_url)
    soup = BeautifulSoup(inbox_response.text, 'html.parser')

    # Търсим линк, който започва с https://www.seir-sanduk
    link_tag = soup.find('a', href=lambda href: href and href.startswith("https://www.seir-sanduk"))

    if link_tag:
        target_url = link_tag['href']
        print(f"[i] Намерен линк: {target_url}")

        # Отваряме линка
        final_response = session.get(target_url)

        # Взимаме всичко след "/?"
        parsed_url = urlparse(final_response.url)
        query_part = parsed_url.query

        if query_part:
            with open("result.txt", "w", encoding="utf-8") as file:
                file.write(query_part + "\n")
            print(f"[✓] Извлечено и записано в result.txt:\n{query_part}")
        else:
            print("[!] В URL-а няма част след '/?'")
    else:
        print("[!] Не е намерен линк, започващ с 'https://www.seir-sanduk'")
else:
    print("[!] Входът е неуспешен – провери потребителско име/парола или токен")

