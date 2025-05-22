import requests
from bs4 import BeautifulSoup

# 🔗 URL-и
login_url = "https://www.otustanausta.com/ucp.php?mode=login"
inbox_url = "https://www.otustanausta.com/ucp.php?i=pm&folder=inbox"
base_url = "https://www.otustanausta.com/"

# 🔒 Данни за логин (замени с реални)
USERNAME = "itv"
PASSWORD = "P@r0la"

# 👉 Създаваме сесия
session = requests.Session()

# 1. Вземаме login страницата
response = session.get(login_url)
soup = BeautifulSoup(response.text, "html.parser")

# 2. Извличаме всички hidden input полета от login формата
login_form = soup.find("form", {"id": "login"})
hidden_fields = login_form.find_all("input", {"type": "hidden"})
form_data = {field.get("name"): field.get("value", "") for field in hidden_fields}

# 3. Добавяме потребител и парола
form_data.update({
    "username": USERNAME,
    "password": PASSWORD,
    "login": "Вход",  # понякога е "Login" — провери ако не тръгне
})

# 4. Изпращаме POST заявка
login_response = session.post(login_url, data=form_data)

# 5. Проверка за логин
if "Изход [" in login_response.text or "logout" in login_response.text.lower():
    print("✅ Успешен логин!")

    # 6. Отваряме Inbox
    inbox_response = session.get(inbox_url)
    inbox_soup = BeautifulSoup(inbox_response.text, "html.parser")

    message_links = inbox_soup.select("a.topictitle")

    if message_links:
        print(f"📨 Намерени съобщения: {len(message_links)}\n")

        with open("result.txt", "w", encoding="utf-8") as file:
            for link in message_links:
                href = link.get("href")
                if href.startswith("./"):
                    href = href.replace("./", "")
                full_url = base_url + href

                # Записваме параметрите от URL-а
                url_part = full_url.split("?", 1)[-1]
                file.write(url_part + "\n")

                # Изтегляме и показваме съдържанието
                msg_response = session.get(full_url)
                msg_soup = BeautifulSoup(msg_response.text, "html.parser")

                post_body = msg_soup.select_one("div.postbody div.content")
                print(f"📌 Съобщение от {full_url}:\n")
                if post_body:
                    print(post_body.text.strip())
                else:
                    print("⚠️ Не успях да намеря съдържание.")
                print("\n" + "-" * 60 + "\n")
        print("📁 Записано в result.txt")
    else:
        print("⚠️ Не бяха намерени съобщения в входящата кутия.")
else:
    print("❌ Неуспешен логин.")
