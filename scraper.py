import requests

# Линкът, който искаш да отвориш
url = "https://www.seir-sanduk.com/linkzagledane.php?parola=aeagaDs3AdKaAf2"

# Изпраща HTTP GET заявка и следи за пренасочване
response = requests.get(url, allow_redirects=True)

# Взима крайния URL (след всички пренасочвания)
new_url = response.url

# Записва новия URL в result.txt
with open("result.txt", "w") as file:
    file.write(new_url)

# Отпечатва новия URL
print(f"Новият URL е: {new_url}")
