import requests
from bs4 import BeautifulSoup

# === Конфигурация ===
LOGIN_URL = 'https://www.otustanausta.com/ucp.php?mode=login&redirect=index.php'
SEARCH_URL = 'https://www.otustanausta.com/search.php?keywords='
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

# === 4. Изпращаме заявка за търсене (примерно чрез GET) ===
search_params = {
    'q': SEARCH_WORD  # замени 'q' с правилното име на параметъра за търсене
}
search_response = session.get(SEARCH_URL, params=search_params)

if search_response.status_code != 200:
    print("❌ Търсенето се провали.")
    exit()

# === 5. Извличаме резултата ===
soup = BeautifulSoup(search_response.text, 'html.parser')

# Пример: взимаме текстовото съдържание
text_result = soup.get_text()

# === 6. Запис във файл ===
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(text_result)

print(f"📁 Резултатът е записан в {OUTPUT_FILE}")
