import requests
from bs4 import BeautifulSoup

# URL адреси
login_url = "https://www.otustanausta.com/ucp.php?mode=login"
inbox_url = "https://www.otustanausta.com/ucp.php?i=pm&folder=inbox"
base_url = "https://www.otustanausta.com/"

# Създаваме сесия
session = requests.Session()

# Вземаме login страницата
response = session.get(login_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Взимаме form_token
form_token = soup.find('input', {'name': 'form_token'})
form_token = form_token['value'] if form_token else ''

# Данни за логин (замени със свои!)
payload = {
    'username': 'itv',
    'password': 'P@r0la',
    'login': 'Вход',
    'redirect': 'index.php',
    'form_token': form_token,
}

# Изпращаме заявка за логин
login_response = session.post(login_url, data=payload)

# Проверка за логин
if "Изход [" in login_response.text or "logout" in login_response.text.lower():
    print("Успешен логин!")

    # Влизаме в inbox
    inbox_response = session.get(inbox_url)
    inbox_soup = BeautifulSoup(inbox_response.text, 'html.parser')

    # Намираме линковете към съобщенията
    message_links = inbox_soup.select("a.topictitle")

    if message_links:
        print(f"Намерени {len(message_links)} съобщения.\n")

        with open("result.txt", "w", encoding="utf-8") as file:
            for link in message_links:
                href = link.get("href")
                if href:
                    if href.startswith("./"):
                        href = href.replace("./", "")
                    full_url = base_url + href

                    print(f"Зареждам съобщение: {full_url}")

                    # Записваме само частта след "/?" или "?" в result.txt
                    url_part = full_url.split("?", 1)[-1]
                    file.write(url_part + "\n")

                    # Зареждаме съобщението
                    msg_response = session.get(full_url)
                    msg_soup = BeautifulSoup(msg_response.text, 'html.parser')

                    # Извличаме съдържанието на съобщението
                    post_body = msg_soup.select_one("div.postbody div.content")
                    if post_body:
                        print("Съдържание:\n")
                        print(post_body.text.strip())
                    else:
                        print("Не успях да намеря съдържание.")

                    print("\n" + "-"*60 + "\n")
        print("Частите от URL-ите са записани в result.txt")
    else:
        print("Няма намерени съобщения.")
else:
    print("Неуспешен логин.")
