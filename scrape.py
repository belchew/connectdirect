import os
import base64
import re
import pandas as pd
import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

# Channel mapping
channel_mapping = {
            '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-bnt-1-hd&pass=',
            '#EXTINF:-1 tvg-name="bTV" tvg-logo="https://www.glebul.com/images/tv-logo/btv-hd.png" group-title="ЕФИРНИ" , bTV HD': 'https://www.seir-sanduk.com/?player=3&id=hd-btv-hd&pass=',
            '#EXTINF:-1 tvg-name="Nova TV" tvg-logo="https://www.glebul.com/images/tv-logo/nova-tv-hd.png" group-title="ЕФИРНИ" , NovaTV': 'https://www.seir-sanduk.com/?player=3&id=hd-nova-tv-hd&pass=',
            '#EXTINF:-1 tvg-name="БНТ 2" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-2.png" group-title="ЕФИРНИ" , BNT 2': 'https://www.seir-sanduk.com/?id=bnt-2&pass=&hash=',
            '#EXTINF:-1 tvg-name="БНТ 3" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-3-hd.png" group-title="ЕФИРНИ" , BNT 3': 'https://www.seir-sanduk.com/?player=3&id=hd-bnt-3-hd&pass=',
            '#EXTINF:-1 tvg-name="БНТ 4" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-4.png" group-title="ЕФИРНИ" , BNT 4 HD': 'https://www.seir-sanduk.com/?player=3&id=bnt-4&pass=',
            '#EXTINF:-1 tvg-name="TV1" tvg-logo="https://www.glebul.com/images/tv-logo/tv-1.png" group-title="ЕФИРНИ" , TV1': 'https://www.seir-sanduk.com/?player=3&id=tv-1&pass=',
            '#EXTINF:-1 tvg-name="Kanal3" tvg-logo="https://www.glebul.com/images/tv-logo/kanal-3.png" group-title="ЕФИРНИ" , Kanal3': 'https://www.seir-sanduk.com/?player=3&id=kanal-3&pass=',
            '#EXTINF:-1 tvg-name="Evrokom" tvg-logo="https://www.glebul.com/images/tv-logo/evrokom.png" group-title="ЕФИРНИ" , Evrokom': 'https://www.seir-sanduk.com/?player=3&id=evrokom&pass=',
            '#EXTINF:-1 tvg-name="Skat" tvg-logo="https://www.glebul.com/images/tv-logo/skat.png" group-title="ЕФИРНИ" , Skat': 'https://www.seir-sanduk.com/?player=3&id=skat&pass=',
            '#EXTINF:-1 tvg-name="bgonair.bg" tvg-logo="https://www.glebul.com/images/tv-logo/bulgaria-on-air.png" group-title="ЕФИРНИ" , Bulgaria ON Air': 'https://www.seir-sanduk.com/?player=3&id=bulgaria-on-air&pass=',
            '#EXTINF:-1 tvg-name="Bloomberg" tvg-logo="https://www.glebul.com/images/tv-logo/bloomberg-tv.png" group-title="ЕФИРНИ" , Bloomberg TV Bulgaria': 'https://www.seir-sanduk.com/?id=bloomberg-tv&pass=&hash=',
            '#EXTINF:-1 tvg-name="Euronews Bulgaria" tvg-logo="https://www.glebul.com/images/tv-logo/euronews-bulgaria.png" group-title="ЕФИРНИ" , Euronews Bulgaria': 'https://www.seir-sanduk.com/?player=3&id=euronews-bulgaria&pass=',
            '#EXTINF:-1 tvg-name="Diema" tvg-logo="https://www.glebul.com/images/tv-logo/diema.png" group-title="Филмови" , Diema': 'https://www.seir-sanduk.com/?player=3&id=diema&pass=',
            '#EXTINF:-1 tvg-name="bTV Action" tvg-logo="https://www.glebul.com/images/tv-logo/btv-action-hd.png" group-title="Спортни"  , bTV Action HD': 'https://www.seir-sanduk.com/?player=3&id=hd-btv-action-hd&pass=',
            '#EXTINF:-1 tvg-name="bTV Cinema" tvg-logo="https://www.glebul.com/images/tv-logo/btv-cinema.png" group-title="Филмови" , bTV Cinema HD': 'https://www.seir-sanduk.com/?player=3&id=btv-cinema&pass=',
            '#EXTINF:-1 tvg-name="bTV Comedy" tvg-logo="https://www.glebul.com/images/tv-logo/btv-comedy.png" group-title="Филмови" , bTV Comedy HD': 'https://www.seir-sanduk.com/?player=3&id=btv-comedy&pass=',
            '#EXTINF:-1 tvg-name="bTV Story" tvg-logo="https://www.glebul.com/images/tv-logo/btv-story.png" group-title="Филмови" , bTV Story HD': 'https://www.seir-sanduk.com/?player=3&id=btv-story&pass=',
            '#EXTINF:-1 tvg-name="KinoNova" tvg-logo="https://www.glebul.com/images/tv-logo/kino-nova.png" group-title="Филмови" , KinoNova': 'https://www.seir-sanduk.com/?player=3&id=kino-nova&pass=',
            '#EXTINF:-1 tvg-name="id extra HD" tvg-logo="https://www.glebul.com/images/tv-logo/id-xtra-hd.png" group-title="Филмови" , ID Extra HD': 'https://www.seir-sanduk.com/?player=3&id=hd-id-xtra-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Family" tvg-logo="https://www.glebul.com/images/tv-logo/diema-family.png" group-title="Филмови" , Diema Family': 'https://www.seir-sanduk.com/?player=3&id=diema-family&pass=',
            '#EXTINF:-1 tvg-name="STAR CHANNEL" tvg-logo="https://www.glebul.com/images/tv-logo/star-channel-hd.png" group-title="Филмови" , STAR CHANNEL HD': 'https://www.seir-sanduk.com/?player=3&id=hd-star-channel-hd&pass=',
            '#EXTINF:-1 tvg-name="STAR Life" tvg-logo="https://www.glebul.com/images/tv-logo/star-life-hd.png" group-title="Филмови" , STAR Life HD': 'https://www.seir-sanduk.com/?player=3&id=hd-star-life-hd&pass=',
            '#EXTINF:-1 tvg-name="STAR Crime " tvg-logo="https://www.glebul.com/images/tv-logo/star-crime-hd.png" group-title="Филмови" , STAR Crime HD': 'https://www.seir-sanduk.com/?player=3&id=hd-star-crime-hd&pass=',
            '#EXTINF:-1 tvg-name="7/8 TV" tvg-logo="https://www.glebul.com/images/tv-logo/78-tv-hd.png" group-title="ЕФИРНИ" , 7/8 TV HD': 'https://www.seir-sanduk.com/?player=3&id=hd-78-tv-hd&pass=',
            '#EXTINF:-1 tvg-name="Nova Sport" tvg-logo="https://www.glebul.com/images/tv-logo/nova-sport-hd.png" group-title="Спортни" , Nova Sport HD': 'https://www.seir-sanduk.com/?player=3&id=hd-nova-sport-hd&pass=',
            '#EXTINF:-1 tvg-name="Ring BG" tvg-logo="https://www.glebul.com/images/tv-logo/ring-bg-hd.png" group-title="Спортни" , Ring BG': 'https://www.seir-sanduk.com/?player=3&id=hd-ring-bg-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-hd.png" group-title="Спортни" , Diema Sport': 'https://www.seir-sanduk.com/?player=3&id=hd-diema-sport-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport 2" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-2-hd.png" group-title="Спортни" , Diema Sport 2': 'https://www.seir-sanduk.com/?player=3&id=hd-diema-sport-2-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport 3" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-3-hd.png" group-title="Спортни" , Diema Sport 3': 'https://www.seir-sanduk.com/?player=3&id=hd-diema-sport-3-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 1 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-1-hd.png" group-title="Спортни" , Max Sport 1 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-1-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 2 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-2-hd.png" group-title="Спортни" , Max Sport 2 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-2-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 3 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-3-hd.png" group-title="Спортни" , Max Sport 3 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-3-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 4 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-4-hd.png" group-title="Спортни" , Max Sport 4 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-max-sport-4-hd&pass=',
            '#EXTINF:-1 tvg-name="Eurosport" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-1-hd.png" group-title="Спортни" , Eurosport HD': 'https://www.seir-sanduk.com/?player=3&id=hd-eurosport-1-hd&pass=',
            '#EXTINF:-1 tvg-name="Eurosport 2" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-2-hd.png" group-title="Спортни" , Eurosport 2 HD': 'https://www.seir-sanduk.com/?player=3&id=hd-eurosport-2-hd&pass=',
            #'#EXTINF:-1 tvg-id="FilmBox Stars" tvg-name="FilmBox Stars" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxplus.png" group-title="Филмови" , FilmBox Stars': '',
            #'#EXTINF:-1 tvg-id="FilmBox Extra" tvg-name="FilmBox Extra" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxextra.png" group-title="Филмови" , FilmBox Extra': '',
            #'#EXTINF:-1 tvg-id="MovieStar.bg" tvg-name="Moviestar HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/moviestar.png" group-title="Филмови" , Moviestar HD': '',
            #'#EXTINF:-1 tvg-id="amc.bg" tvg-name="AMC" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/amc.png" group-title="Филмови" , AMC': '',
            '#EXTINF:-1 tvg-id="AXN" tvg-name="AXN" tvg-logo="https://www.glebul.com/images/tv-logo/axn.png" group-title="Филмови" , AXN': 'https://www.seir-sanduk.com/?player=3&id=axn&pass=',
            '#EXTINF:-1 tvg-name="Discovery Channel" tvg-logo="https://www.glebul.com/images/tv-logo/discovery-channel-hd.png" group-title="Научни" , Discovery Channel HD': 'https://www.seir-sanduk.com/?player=3&id=hd-discovery-channel-hd&pass=',
            '#EXTINF:-1 tvg-name="NatGeo Wild" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-wild-hd.png" group-title="Научни" , Nat Geo Wild HD': 'https://www.seir-sanduk.com/?player=3&id=hd-nat-geo-wild-hd&pass=',
            #'#EXTINF:-1 tvg-id="HistoryChannel.bg" tvg-name="History Channel HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/history-1.png" group-title="Научни" , History Channel HD': '',
            #'#EXTINF:-1 tvg-id="DocuBox" tvg-name="DocuBox" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/docubox.png" group-title="Научни" , Docu Box HD': '',
            #'#EXTINF:-1 tvg-id="ViasatExplorer.bg" tvg-name="Viasat Explore HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_explore.png" group-title="Научни" , Viasat Explore HD': '',
            #'#EXTINF:-1 tvg-id="ViasatHistory.bg" tvg-name="Viasat History HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_history.png" group-title="Научни" , Viasat History HD': '',
            #'#EXTINF:-1 tvg-id="ViasatNature.bg" tvg-name="Viasat Nature HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_nature.png" group-title="Научни" , Viasat Nature HD': '',
            #'#EXTINF:-1 tvg-id="AnimalPlanet.bg" tvg-name="Animal Planet HD" tvg-logo="https://www.glebul.com/images/tv-logo/animal-planet.png" group-title="Научни" , Animal Planet HD': '',
            '#EXTINF:-1 tvg-name="DSTV" tvg-logo="https://www.glebul.com/images/tv-logo/dstv.png" group-title="Музикални" , DSTV': 'https://www.seir-sanduk.com/?player=3&id=dstv&pass=',
            #'#EXTINF:-1 tvg-id="Balkanika.bg" tvg-name="Balkanika HD" tvg-logo="https://www.glebul.com/images/tv-logo/balkanika-hd.png" group-title="Музикални" , Balkanika HD': '',
            '#EXTINF:-1 tvg-name="Planeta" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-hd.png" group-title="Музикални" , Planeta HD': 'https://www.seir-sanduk.com/?player=3&id=hd-planeta-hd&pass=',
            '#EXTINF:-1 tvg-name="Planeta Folk" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-folk.png" group-title="Музикални" , Planeta Folk': 'https://www.seir-sanduk.com/?player=3&id=planeta-folk&pass=',
            '#EXTINF:-1 tvg-name="The Voice" tvg-logo="https://www.glebul.com/images/tv-logo/the-voice.png" group-title="Музикални" , The Voice': 'https://www.seir-sanduk.com/?player=3&id=the-voice&pass=',
            '#EXTINF:-1 tvg-name="City TV" tvg-logo="https://www.glebul.com/images/tv-logo/city-tv.png" group-title="Музикални" , City TV': 'https://www.seir-sanduk.com/?player=3&id=city-tv&pass=',
            '#EXTINF:-1 tvg-name="folklor-tv" tvg-logo="https://www.glebul.com/images/tv-logo/folklor-tv.png" group-title="Музикални" , Folklor TV': 'https://www.seir-sanduk.com/?player=3&id=folklor-tv&pass=',
            '#EXTINF:-1 tvg-name="Rodina TV" tvg-logo="https://www.glebul.com/images/tv-logo/rodina-tv.png" group-title="Музикални" , Rodina TV HD': 'https://www.seir-sanduk.com/?player=3&id=rodina-tv&pass=',
            '#EXTINF:-1 tvg-name="TiankovFolk" tvg-logo="https://www.glebul.com/images/tv-logo/tiankov-tv.png" group-title="Музикални" , Tiankov Folk': 'https://www.seir-sanduk.com/?player=3&id=tiankov-tv&pass=', 
            '#EXTINF:-1 tvg-name="Cartoon Network" tvg-logo="https://www.glebul.com/images/tv-logo/cartoon-network.png" group-title="Детски" , Cartoon Network HD': 'https://www.seir-sanduk.com/?player=3&id=cartoon-network&pass=',
            '#EXTINF:-1 tvg-name="Disney channel" tvg-logo="https://www.glebul.com/images/tv-logo/disney-channel.png" group-title="Детски" , Disney channel': 'https://www.seir-sanduk.com/?player=3&id=disney-channel&pass=',
            '#EXTINF:-1 tvg-name="Nickeldeon" tvg-logo="https://www.glebul.com/images/tv-logo/nickelodeon.png" group-title="Детски" , Nickelodeon': 'https://www.seir-sanduk.com/?player=3&id=nickelodeon&pass=',
            '#EXTINF:-1 tvg-name="Nick Jr." tvg-logo="https://www.glebul.com/images/tv-logo/nick-jr.png" group-title="Детски" , Nick Jr': 'https://www.seir-sanduk.com/?player=3&id=nick-jr&pass=',
            '#EXTINF:-1 tvg-name="EKids" tvg-logo="https://www.glebul.com/images/tv-logo/e-kids.png" group-title="Детски" , EKids': 'https://www.seir-sanduk.com/?player=3&id=e-kids&pass=',
            '#EXTINF:-1 tvg-name="Nicktoons" tvg-logo="https://www.glebul.com/images/tv-logo/nicktoons.png" group-title="Детски" , Nicktoons': 'https://www.seir-sanduk.com/?player=3&id=nicktoons&pass=',
            '#EXTINF:-1 tvg-name="National Geographic" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-hd.png" group-title="Научни" National Geographic HD': 'https://www.seir-sanduk.com/?player=3&id=hd-nat-geo-hd&pass=',
            '#EXTINF:-1 tvg-name="Travel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-tv.png" group-title="Други" , Travel TV': 'https://www.seir-sanduk.com/?player=3&id=travel-tv&pass=',
            #'#EXTINF:-1 tvg-name="Magic" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/fantv.png" group-title="Музикални" , Magic TV': '',
            '#EXTINF:-1 tvg-name="VTK" tvg-logo="https://www.glebul.com/images/tv-logo/vtk.png" group-title="Други" , VTK': 'https://www.seir-sanduk.com/?player=3&id=vtk&pass=',
            '#EXTINF:-1 tvg-name="CodeFashion HD" tvg-logo="https://www.glebul.com/images/tv-logo/code-fashion-tv-hd.png" group-title="Други" , CodeFashion': 'https://www.seir-sanduk.com/?player=3&id=hd-code-fashion-tv-hd&pass=',
            '#EXTINF:-1 tvg-name="Food Network" tvg-logo="https://www.glebul.com/images/tv-logo/food-network-hd.png" group-title="Други" , Food Network': 'https://www.seir-sanduk.com/?player=3&id=hd-food-network-hd&pass=', 
            '#EXTINF:-1 tvg-name="Epic Drama" tvg-logo="https://www.glebul.com/images/tv-logo/epic-drama-hd.png" group-title="Филмови" , Epic Drama': 'https://www.seir-sanduk.com/?player=3&id=hd-epic-drama-hd&pass=',
            '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD': 'https://www.seir-sanduk.com/?player=3&id=tlc&pass=',
            '#EXTINF:-1 tvg-name="24 Kitchen" tvg-logo="https://www.glebul.com/images/tv-logo/24-kitchen-hd.png" group-title="Други" , 24 Kitchen HD': 'https://www.seir-sanduk.com/?player=3&id=hd-24-kitchen-hd&pass=',
            '#EXTINF:-1 tvg-name="Travel Channel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-channel-hd.png" group-title="Научни" , Travel Channel': 'https://www.seir-sanduk.com/?player=3&id=hd-travel-channel-hd&pass=' 
            

    # Add more channels as needed
}

def update_links(channel, source_link):
    try:
        from urllib.parse import urljoin
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            m3u8_link = None
            ts_link = None

            def handle_response(response):
                nonlocal m3u8_link, ts_link
                url = response.url
                print(f"📡 Response: {url}")

                if ".m3u8" in url and not m3u8_link:
                    m3u8_link = url
                    print(f"✅ Found m3u8 for {channel[:40]}...: {url}")

                elif ".ts" in url and not ts_link:
                    ts_link = url
                    print(f"🧪 Found .ts segment for {channel[:40]}...: {url}")

            print(f"🌐 Visiting: {source_link}")
            page.goto(source_link, timeout=30000)

            page.on("response", handle_response)
            for frame in page.frames:
                try:
                    frame.on("response", handle_response)
                except:
                    pass

            try:
                page.wait_for_selector("video", timeout=5000)
                page.click("video")
                print("🎬 Clicked video element")
            except:
                try:
                    page.keyboard.press("Space")
                    print("🎬 Pressed Space to start video")
                except:
                    print("⚠️ No video interaction")

            page.wait_for_timeout(10000)
            browser.close()

            # Ако не е открит .m3u8, но имаме .ts линк, правим опит да съставим базов плейлист линк
            if not m3u8_link and ts_link:
                # Примерно преобразуване: премахваме след segment, и добавяме playlist.m3u8
                base_url = ts_link.rsplit('/', 1)[0]
                possible_m3u8 = urljoin(base_url + "/", "playlist.m3u8")
                print(f"🧩 Reconstructed m3u8 guess from .ts: {possible_m3u8}")
                return possible_m3u8

            return m3u8_link

    except Exception as e:
        print(f"🚨 Error fetching link for {channel[:40]}...: {e}")
        return None

# 📦 Обработка и запис
data_list = []
m3u_links = []

def process_channel(channel, source_link):
    link = update_links(channel, source_link)
    data_list.append({
        'Channel': channel,
        'SourceLink': source_link,
        'LinkToUpdate': link
    })
    if link:
        m3u_links.append(f"{channel}\n{link}")

# 🚀 Стартираме паралелно извличане
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(lambda item: process_channel(item[0], item[1]), channel_mapping.items())

# 📝 Записваме .m3u файл
file_path = 'sources.m3u'
with open(file_path, 'w', encoding='utf-8') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')
    for link in m3u_links:
        file.write(link + '\n')

# 🗃️ CSV лог за дебъг
df = pd.DataFrame(data_list)
df.to_csv('m3u_links_log.csv', index=False)

print(f"\n✅ Готово! Записахме {len(m3u_links)} линка в {file_path} и лог в m3u_links_log.csv")
