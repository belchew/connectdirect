import requests
from urllib.parse import urlparse, parse_qs

# Линкът, който искаш да отвориш
url = "https://www.seir-sanduk.com/linkzagledane.php?parola=aeagaDs3AdKaAf2"

# Изпраща HTTP GET заявка и следи за пренасочване
response = requests.get(url, allow_redirects=True)

# Взима крайния URL след всички пренасочвания
final_url = response.url

# Извлича частта от URL след "pass="
parsed_url = urlparse(final_url)
query_params = parse_qs(parsed_url.query)

# Проверява дали параметърът "pass" съществува
if '?/' in query_params:
    pass_value = query_params['?/'][0]
else:
    pass_value = ""  # Ако параметърът "pass" не съществува, оставяме празно

# Записва стойността след "pass=" в result.txt
with open("result.txt", "w") as file:
    file.write(pass_value)

# Отпечатва стойността след "pass="
print(f"Паролата е: {pass_value}")
