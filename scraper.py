import webbrowser

# Линкът, който искаш да отвориш
url = "https://www.seir-sanduk.com/linkzagledane.php?parola=aeagaDs3AdKaAf2"

# Извлича частта след "?" в URL-то
if "?" in url:
    url_part = url.split("?")[1]  # Разделя URL-то по "?" и взема частта след него
else:
    url_part = ""

# Отваря линка в браузъра
webbrowser.open(url)

# Записва частта от URL в result.txt
with open("result.txt", "w") as file:
    file.write(url_part)

print("Частта от URL-то е записана в result.txt")
