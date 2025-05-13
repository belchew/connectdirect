import requests
from bs4 import BeautifulSoup

# === Конфигурация ===
LOGIN_URL = 'https://www.otustanausta.com/ucp.php?mode=login&redirect=index.php'      # Заменете с истинския URL за логин
SEARCH_URL = 'https://www.otustanausta.com/search.php?keywords='    # Заменете с URL-то за търсене
USERNAME = 'itv'
PASSWORD = 'P@r0la'
SEARCH_WORD = 'pass'
OUTPUT_FILE = 'key.txt'

# === 1. Създаваме сесия ===
session = requests.Session()

# === 2. Данни за вход (провери имената на полетата) ===
login_data = {
    'username': USERNAME,
    'password': PASSWORD
}

# === 3. Изпращане на POST заявка за логин ===
login_response = session.post(LOGIN_URL, data=login_data)

if login_response.status_code != 200:
    print("❌ Грешка при логване.")
    exit()

print("✅ Успешен вход.")

# === 4. Изпращаме заявка за търсене ===
search_params = {
    'q': SEARCH_WORD  # заменете 'q' с правилното име на параметъра за търсене
}
search_response = session.get(SEARCH_URL, params=search_params)

if search_response.status_code != 200:
    print("❌ Търсенето се провали.")
    exit()

# === 5. Извличане на резултата от страницата ===
soup = BeautifulSoup(search_response.text, 'html.parser')
text_result = soup.get_text()

# === 6. Намиране на "pass" и следващите 25 символа ===
index = text_result.find("pass")
if index != -1:
    # Вземаме "pass" и следващите 25 символа
    extracted_text = text_result[index:index+30]  # "pass" + 25 символа
    print(f"✅ Намерено: {extracted_text}")
    
    # === 7. Записване в key.txt ===
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    print(f"💾 Резултатът е записан в {OUTPUT_FILE}")
else:
    print("⚠️ Не беше намерено 'pass' в резултата.")
