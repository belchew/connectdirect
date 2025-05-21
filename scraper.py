from urllib.parse import urlparse

def extract_after_questionmark(url):
    parsed_url = urlparse(url)
    return parsed_url.query  # Връща всичко след "/?"

# === Пример за използване ===
url = "https://www.seir-sanduk.com/?pass=xxxxxxxxxxxx"

result = extract_after_questionmark(url)

if result:
    with open("result.txt", "w", encoding="utf-8") as file:
        file.write(result + "\n")
    print("[✓] Извлечено и записано в result.txt:")
    print(result)
else:
    print("Няма нищо след '/?' в URL-а.")
