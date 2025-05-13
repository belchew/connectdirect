import requests
from bs4 import BeautifulSoup

# === Конфигурация ===
SEARCH_URL = 'https://www.otustanausta.com/search.php?keywords=pass'  # Заменете с истинското URL за търсене
SEARCH_WORD = 'pass'  # Търсим думата "pass"
OUTPUT_FILE = 'key.txt'

# === 1. Изпращаме заявка за търсене ===
search_params = {
    'keywords': SEARCH_WORD  # Задаваме думата "pass" в параметъра 'keywords'
}

search_response = requests.get(SEARCH_URL, params=search_params)

if search_response.status_code != 200:
    print("❌ Търсенето се провали.")
    exit()

# === 2. Извличане на резултата от страницата ===
soup = BeautifulSoup(search_response.text, 'html.parser')
text_result = soup.get_text()

# === 3. Намиране на "pass" и следващите 25 символа ===
index = text_result.find("pass")
if index != -1:
    # Вземаме "pass" и следващите 25 символа
    extracted_text = text_result[index:index+30]  # "pass" + 25 символа
    print(f"✅ Намерено: {extracted_text}")
    
    # === 4. Записване в key.txt ===
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(extracted_text)

    print(f"💾 Резултатът е записан в {OUTPUT_FILE}")
else:
    print("⚠️ Не беше намерено 'pass' в резултата.")
    
