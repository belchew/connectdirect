import os
import base64
import re
import pandas as pd
import requests
import subprocess
from bs4 import BeautifulSoup

# === Конфигурация ===
SEARCH_URL = 'https://www.otustanausta.com/search.php'  # URL за търсене
SEARCH_WORD = 'pass'  # Търсена дума
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
index = text_result.find(SEARCH_WORD)
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
#==========================================================================


with open('key.txt', 'r') as f:
    password = f.read().strip()

# Channel mapping
channel_mapping = {
            '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&password&hash=',
            '#EXTINF:-1 tvg-name="bTV" tvg-logo="https://www.glebul.com/images/tv-logo/btv-hd.png" group-title="ЕФИРНИ" , bTV HD': 'https://www.seir-sanduk.com/?id=hd-btv-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Nova TV" tvg-logo="https://www.glebul.com/images/tv-logo/nova-tv-hd.png" group-title="ЕФИРНИ" , NovaTV': 'https://www.seir-sanduk.com/?id=hd-nova-tv-hd&password&hash=',
            '#EXTINF:-1 tvg-name="БНТ 2" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-2.png" group-title="ЕФИРНИ" , BNT 2': 'https://www.seir-sanduk.com/?id=bnt-2&password&hash=&hash=',
            '#EXTINF:-1 tvg-name="БНТ 3" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-3-hd.png" group-title="ЕФИРНИ" , BNT 3': 'https://www.seir-sanduk.com/?id=hd-bnt-3-hd&password&hash=',
            '#EXTINF:-1 tvg-name="БНТ 4" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-4.png" group-title="ЕФИРНИ" , BNT 4 HD': 'https://www.seir-sanduk.com/?id=bnt-4&password&hash=',
            '#EXTINF:-1 tvg-name="TV1" tvg-logo="https://www.glebul.com/images/tv-logo/tv-1.png" group-title="ЕФИРНИ" , TV1': 'https://www.seir-sanduk.com/?id=tv-1&password&hash=',
            '#EXTINF:-1 tvg-name="Kanal3" tvg-logo="https://www.glebul.com/images/tv-logo/kanal-3.png" group-title="ЕФИРНИ" , Kanal3': 'https://www.seir-sanduk.com/?id=kanal-3&password&hash=',
            '#EXTINF:-1 tvg-name="Evrokom" tvg-logo="https://www.glebul.com/images/tv-logo/evrokom.png" group-title="ЕФИРНИ" , Evrokom': 'https://www.seir-sanduk.com/?id=evrokom&password&hash=',
            '#EXTINF:-1 tvg-name="Skat" tvg-logo="https://www.glebul.com/images/tv-logo/skat.png" group-title="ЕФИРНИ" , Skat': 'https://www.seir-sanduk.com/?id=skat&password&hash=',
            '#EXTINF:-1 tvg-name="bgonair.bg" tvg-logo="https://www.glebul.com/images/tv-logo/bulgaria-on-air.png" group-title="ЕФИРНИ" , Bulgaria ON Air': 'https://www.seir-sanduk.com/?id=bulgaria-on-air&password&hash=',
            '#EXTINF:-1 tvg-name="Bloomberg" tvg-logo="https://www.glebul.com/images/tv-logo/bloomberg-tv.png" group-title="ЕФИРНИ" , Bloomberg TV Bulgaria': 'https://www.seir-sanduk.com/?id=bloomberg-tv&password&hash=&hash=',
            '#EXTINF:-1 tvg-name="Euronews Bulgaria" tvg-logo="https://www.glebul.com/images/tv-logo/euronews-bulgaria.png" group-title="ЕФИРНИ" , Euronews Bulgaria': 'https://www.seir-sanduk.com/?id=euronews-bulgaria&password&hash=',
            '#EXTINF:-1 tvg-name="Diema" tvg-logo="https://www.glebul.com/images/tv-logo/diema.png" group-title="Филмови" , Diema': 'https://www.seir-sanduk.com/?id=diema&password&hash=',
            '#EXTINF:-1 tvg-name="bTV Action" tvg-logo="https://www.glebul.com/images/tv-logo/btv-action-hd.png" group-title="Спортни"  , bTV Action HD': 'https://www.seir-sanduk.com/?id=hd-btv-action-hd&password&hash=',
            '#EXTINF:-1 tvg-name="bTV Cinema" tvg-logo="https://www.glebul.com/images/tv-logo/btv-cinema.png" group-title="Филмови" , bTV Cinema HD': 'https://www.seir-sanduk.com/?id=btv-cinema&password&hash=',
            '#EXTINF:-1 tvg-name="bTV Comedy" tvg-logo="https://www.glebul.com/images/tv-logo/btv-comedy.png" group-title="Филмови" , bTV Comedy HD': 'https://www.seir-sanduk.com/?id=btv-comedy&password&hash=',
            '#EXTINF:-1 tvg-name="bTV Story" tvg-logo="https://www.glebul.com/images/tv-logo/btv-story.png" group-title="Филмови" , bTV Story HD': 'https://www.seir-sanduk.com/?id=btv-story&password&hash=',
            '#EXTINF:-1 tvg-name="KinoNova" tvg-logo="https://www.glebul.com/images/tv-logo/kino-nova.png" group-title="Филмови" , KinoNova': 'https://www.seir-sanduk.com/?id=kino-nova&password&hash=',
            '#EXTINF:-1 tvg-name="id extra HD" tvg-logo="https://www.glebul.com/images/tv-logo/id-xtra-hd.png" group-title="Филмови" , ID Extra HD': 'https://www.seir-sanduk.com/?id=hd-id-xtra-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Diema Family" tvg-logo="https://www.glebul.com/images/tv-logo/diema-family.png" group-title="Филмови" , Diema Family': 'https://www.seir-sanduk.com/?id=diema-family&password&hash=',
            '#EXTINF:-1 tvg-name="STAR CHANNEL" tvg-logo="https://www.glebul.com/images/tv-logo/star-channel-hd.png" group-title="Филмови" , STAR CHANNEL HD': 'https://www.seir-sanduk.com/?id=hd-star-channel-hd&password&hash=',
            '#EXTINF:-1 tvg-name="STAR Life" tvg-logo="https://www.glebul.com/images/tv-logo/star-life-hd.png" group-title="Филмови" , STAR Life HD': 'https://www.seir-sanduk.com/?id=hd-star-life-hd&password&hash=',
            '#EXTINF:-1 tvg-name="STAR Crime " tvg-logo="https://www.glebul.com/images/tv-logo/star-crime-hd.png" group-title="Филмови" , STAR Crime HD': 'https://www.seir-sanduk.com/?id=hd-star-crime-hd&password&hash=',
            '#EXTINF:-1 tvg-name="7/8 TV" tvg-logo="https://www.glebul.com/images/tv-logo/78-tv-hd.png" group-title="ЕФИРНИ" , 7/8 TV HD': 'https://www.seir-sanduk.com/?id=hd-78-tv-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Nova Sport" tvg-logo="https://www.glebul.com/images/tv-logo/nova-sport-hd.png" group-title="Спортни" , Nova Sport HD': 'https://www.seir-sanduk.com/?id=hd-nova-sport-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Ring BG" tvg-logo="https://www.glebul.com/images/tv-logo/ring-bg-hd.png" group-title="Спортни" , Ring BG': 'https://www.seir-sanduk.com/?id=hd-ring-bg-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Diema Sport" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-hd.png" group-title="Спортни" , Diema Sport': 'https://www.seir-sanduk.com/?id=hd-diema-sport-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Diema Sport 2" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-2-hd.png" group-title="Спортни" , Diema Sport 2': 'https://www.seir-sanduk.com/?id=hd-diema-sport-2-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Diema Sport 3" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-3-hd.png" group-title="Спортни" , Diema Sport 3': 'https://www.seir-sanduk.com/?id=hd-diema-sport-3-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Max Sport 1 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-1-hd.png" group-title="Спортни" , Max Sport 1 HD': 'https://www.seir-sanduk.com/?id=hd-max-sport-1-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Max Sport 2 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-2-hd.png" group-title="Спортни" , Max Sport 2 HD': 'https://www.seir-sanduk.com/?id=hd-max-sport-2-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Max Sport 3 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-3-hd.png" group-title="Спортни" , Max Sport 3 HD': 'https://www.seir-sanduk.com/?id=hd-max-sport-3-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Max Sport 4 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-4-hd.png" group-title="Спортни" , Max Sport 4 HD': 'https://www.seir-sanduk.com/?id=hd-max-sport-4-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Eurosport" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-1-hd.png" group-title="Спортни" , Eurosport HD': 'https://www.seir-sanduk.com/?id=hd-eurosport-1-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Eurosport 2" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-2-hd.png" group-title="Спортни" , Eurosport 2 HD': 'https://www.seir-sanduk.com/?id=hd-eurosport-2-hd&password&hash=',
            #'#EXTINF:-1 tvg-id="FilmBox Stars" tvg-name="FilmBox Stars" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxplus.png" group-title="Филмови" , FilmBox Stars': '',
            #'#EXTINF:-1 tvg-id="FilmBox Extra" tvg-name="FilmBox Extra" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxextra.png" group-title="Филмови" , FilmBox Extra': '',
            #'#EXTINF:-1 tvg-id="MovieStar.bg" tvg-name="Moviestar HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/moviestar.png" group-title="Филмови" , Moviestar HD': '',
            #'#EXTINF:-1 tvg-id="amc.bg" tvg-name="AMC" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/amc.png" group-title="Филмови" , AMC': '',
            '#EXTINF:-1 tvg-id="AXN" tvg-name="AXN" tvg-logo="https://www.glebul.com/images/tv-logo/axn.png" group-title="Филмови" , AXN': 'https://www.seir-sanduk.com/?id=axn&password&hash=',
            '#EXTINF:-1 tvg-name="Discovery Channel" tvg-logo="https://www.glebul.com/images/tv-logo/discovery-channel-hd.png" group-title="Научни" , Discovery Channel HD': 'https://www.seir-sanduk.com/?id=hd-discovery-channel-hd&password&hash=',
            '#EXTINF:-1 tvg-name="NatGeo Wild" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-wild-hd.png" group-title="Научни" , Nat Geo Wild HD': 'https://www.seir-sanduk.com/?id=hd-nat-geo-wild-hd&password&hash=',
            #'#EXTINF:-1 tvg-id="HistoryChannel.bg" tvg-name="History Channel HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/history-1.png" group-title="Научни" , History Channel HD': '',
            #'#EXTINF:-1 tvg-id="DocuBox" tvg-name="DocuBox" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/docubox.png" group-title="Научни" , Docu Box HD': '',
            #'#EXTINF:-1 tvg-id="ViasatExplorer.bg" tvg-name="Viasat Explore HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_explore.png" group-title="Научни" , Viasat Explore HD': '',
            #'#EXTINF:-1 tvg-id="ViasatHistory.bg" tvg-name="Viasat History HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_history.png" group-title="Научни" , Viasat History HD': '',
            #'#EXTINF:-1 tvg-id="ViasatNature.bg" tvg-name="Viasat Nature HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_nature.png" group-title="Научни" , Viasat Nature HD': '',
            #'#EXTINF:-1 tvg-id="AnimalPlanet.bg" tvg-name="Animal Planet HD" tvg-logo="https://www.glebul.com/images/tv-logo/animal-planet.png" group-title="Научни" , Animal Planet HD': '',
            '#EXTINF:-1 tvg-name="DSTV" tvg-logo="https://www.glebul.com/images/tv-logo/dstv.png" group-title="Музикални" , DSTV': 'https://www.seir-sanduk.com/?id=dstv&password&hash=',
            #'#EXTINF:-1 tvg-id="Balkanika.bg" tvg-name="Balkanika HD" tvg-logo="https://www.glebul.com/images/tv-logo/balkanika-hd.png" group-title="Музикални" , Balkanika HD': '',
            '#EXTINF:-1 tvg-name="Planeta" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-hd.png" group-title="Музикални" , Planeta HD': 'https://www.seir-sanduk.com/?id=hd-planeta-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Planeta Folk" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-folk.png" group-title="Музикални" , Planeta Folk': 'https://www.seir-sanduk.com/?id=planeta-folk&password&hash=',
            '#EXTINF:-1 tvg-name="The Voice" tvg-logo="https://www.glebul.com/images/tv-logo/the-voice.png" group-title="Музикални" , The Voice': 'https://www.seir-sanduk.com/?id=the-voice&password&hash=',
            '#EXTINF:-1 tvg-name="City TV" tvg-logo="https://www.glebul.com/images/tv-logo/city-tv.png" group-title="Музикални" , City TV': 'https://www.seir-sanduk.com/?id=city-tv&password&hash=',
            '#EXTINF:-1 tvg-name="folklor-tv" tvg-logo="https://www.glebul.com/images/tv-logo/folklor-tv.png" group-title="Музикални" , Folklor TV': 'https://www.seir-sanduk.com/?id=folklor-tv&password&hash=',
            '#EXTINF:-1 tvg-name="Rodina TV" tvg-logo="https://www.glebul.com/images/tv-logo/rodina-tv.png" group-title="Музикални" , Rodina TV HD': 'https://www.seir-sanduk.com/?id=rodina-tv&password&hash=',
            '#EXTINF:-1 tvg-name="TiankovFolk" tvg-logo="https://www.glebul.com/images/tv-logo/tiankov-tv.png" group-title="Музикални" , Tiankov Folk': 'https://www.seir-sanduk.com/?id=tiankov-tv&password&hash=', 
            '#EXTINF:-1 tvg-name="Cartoon Network" tvg-logo="https://www.glebul.com/images/tv-logo/cartoon-network.png" group-title="Детски" , Cartoon Network HD': 'https://www.seir-sanduk.com/?id=cartoon-network&password&hash=',
            '#EXTINF:-1 tvg-name="Disney channel" tvg-logo="https://www.glebul.com/images/tv-logo/disney-channel.png" group-title="Детски" , Disney channel': 'https://www.seir-sanduk.com/?id=disney-channel&password&hash=',
            '#EXTINF:-1 tvg-name="Nickeldeon" tvg-logo="https://www.glebul.com/images/tv-logo/nickelodeon.png" group-title="Детски" , Nickelodeon': 'https://www.seir-sanduk.com/?id=nickelodeon&password&hash=',
            '#EXTINF:-1 tvg-name="Nick Jr." tvg-logo="https://www.glebul.com/images/tv-logo/nick-jr.png" group-title="Детски" , Nick Jr': 'https://www.seir-sanduk.com/?id=nick-jr&password&hash=',
            '#EXTINF:-1 tvg-name="EKids" tvg-logo="https://www.glebul.com/images/tv-logo/e-kids.png" group-title="Детски" , EKids': 'https://www.seir-sanduk.com/?id=e-kids&password&hash=',
            '#EXTINF:-1 tvg-name="Nicktoons" tvg-logo="https://www.glebul.com/images/tv-logo/nicktoons.png" group-title="Детски" , Nicktoons': 'https://www.seir-sanduk.com/?id=nicktoons&password&hash=',
            '#EXTINF:-1 tvg-name="National Geographic" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-hd.png" group-title="Научни" National Geographic HD': 'https://www.seir-sanduk.com/?id=hd-nat-geo-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Travel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-tv.png" group-title="Други" , Travel TV': 'https://www.seir-sanduk.com/?id=travel-tv&password&hash=',
            #'#EXTINF:-1 tvg-name="Magic" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/fantv.png" group-title="Музикални" , Magic TV': '',
            '#EXTINF:-1 tvg-name="VTK" tvg-logo="https://www.glebul.com/images/tv-logo/vtk.png" group-title="Други" , VTK': 'https://www.seir-sanduk.com/?id=vtk&password&hash=',
            '#EXTINF:-1 tvg-name="CodeFashion HD" tvg-logo="https://www.glebul.com/images/tv-logo/code-fashion-tv-hd.png" group-title="Други" , CodeFashion': 'https://www.seir-sanduk.com/?id=hd-code-fashion-tv-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Food Network" tvg-logo="https://www.glebul.com/images/tv-logo/food-network-hd.png" group-title="Други" , Food Network': 'https://www.seir-sanduk.com/?id=hd-food-network-hd&password&hash=', 
            '#EXTINF:-1 tvg-name="Epic Drama" tvg-logo="https://www.glebul.com/images/tv-logo/epic-drama-hd.png" group-title="Филмови" , Epic Drama': 'https://www.seir-sanduk.com/?id=hd-epic-drama-hd&password&hash=',
            '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD': 'https://www.seir-sanduk.com/?id=tlc&password&hash=',
            '#EXTINF:-1 tvg-name="24 Kitchen" tvg-logo="https://www.glebul.com/images/tv-logo/24-kitchen-hd.png" group-title="Други" , 24 Kitchen HD': 'https://www.seir-sanduk.com/?id=hd-24-kitchen-hd&password&hash=',
            '#EXTINF:-1 tvg-name="Travel Channel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-channel-hd.png" group-title="Научни" , Travel Channel': 'https://www.seir-sanduk.com/?id=hd-travel-channel-hd&password&hash=' 
        
            

    # Add more channels as needed
}

# Функция за намиране на m3u8 линкове
def update_links(channel, source_link):
    with requests.Session() as session:
        response = session.get(source_link)
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
        if match:
            m3u_link = match.group(0)
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None

# Събиране на линковете
data_list = []
m3u_links = []


for channel, source_link in channel_mapping.items():
    source_link = source_link.replace('password', password)  # Заместваме password
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:
        m3u_links.append(f"{channel}\n{fetched_link}")

#for channel, source_link in channel_mapping.items():
#    fetched_link = update_links(channel, source_link)
#    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
#    if fetched_link:
#        m3u_links.append(f"{channel}\n{fetched_link}")

#channel_df = pd.DataFrame(data_list)

# Запис във файла sources.m3u
file_path = 'sources.m3u'

with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n\n')  # Добавен \n за нов ред
    for link in m3u_links:
        file.write(link + '\n')

print(f"Файлът {file_path} беше обновен с новите линкове.")

# 🔁 Замяна на .m3u8 с .mmpeg
with open(file_path, 'r') as file:
    content = file.read()

# Замени разширението
updated_content = content.replace('https://cdn2.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn3.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn4.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn5.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn6.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn7.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn8.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('https://cdn9.glebul.com/hls/', 'https://cdn11.glebul.com/dvr/').replace('index.m3u8?', 'tracks-v1a1/index.m3u8?')

# Запиши отново файла с променените линкове
with open(file_path, 'w') as file:
    file.write(updated_content)

print(f"Всички .m3u8 линкове бяха заменени с .mmpeg в {file_path}.")
