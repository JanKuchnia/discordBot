import discord
import asyncio
import random
import time
import re
import os
import sys
import io
import functools
import yt_dlp
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta
from discord.ext import tasks
from gtts import gTTS

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- INITIAL SETUP ---
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus('libopus.so.0')
    except:
        try:
            discord.opus.load_opus('opus')
        except: pass

# --- CONFIG ---
NAZWA_KANALU_SPONTU = "Kąćik szpątu"
NAZWA_KANALU_PIWNICA = "PIWNICA ♿"
NAZWA_KANALU_POBUDKA = "Pobudka⏰"
NAZWA_KANALU_BEZ_LIMITU = "🔊・Bez limitu"
NAZWA_KANALU_RIVALS ="Rivals"
NAZWA_KANALU_KACIK_GOONERKI ="kącik goonerski"
NAZWA_KANALU_DUO1 ="🔊・Duo#1"
NAZWA_KANALU_DUO2 ="🔊・Duo#2"
NAZWA_KANALU_TEAM2 ="🔊・Team#2"
NAZWA_KANALU_TEAM1 ="🔊・Team#1"

ID_KANALU_Z_CYTATAMI = 1440278981982162974

# --- MAPOWANIE ID UŻYTKOWNIKÓW ---
KISMET_ID  = "412962715103920138"
MICHAL_ID  = "1272860414304190468"
RHAAST_ID  = "1345484077121147002"
JAXER_ID   = "1211570401914658866"
ERYK_ID    = "924312924942643260"
HORDA_ID   = "1186023735656984697"
PAVELOS_ID = "710126890798678059"
DAVID_ID   = "962774833219895396"
LEI_ID     = "1289908823007563811"
DAREK_ID   = "1217483996611739738"
LUCJA_ID   = "1424069124191031399"
POLA_ID    = "1036708964739588156"
KUBA_ID    = "573064756366409729"
LESNIEW_ID = "726843563584782406"
TIXTER_ID  = "1312844505308987515"

# Lista osób, które bot ma czytać (na start pusta lub z Twoim ID)
OSOBY_DO_CZYTANIA = []

# Lista 12 osób do monitorowania wiadomości PV
OSOBY_MONITOROWANE = [
    KISMET_ID, MICHAL_ID, RHAAST_ID, JAXER_ID, ERYK_ID, HORDA_ID,
    PAVELOS_ID, DAVID_ID, LEI_ID, DAREK_ID, LUCJA_ID, KUBA_ID, TIXTER_ID
]
ID_PLECI = {
    KISMET_ID: "M",
    MICHAL_ID: "M",
    RHAAST_ID: "M",
    JAXER_ID: "M",
    ERYK_ID: "M",
    HORDA_ID: "K",
    PAVELOS_ID: "M",
    DAVID_ID: "M",
    LEI_ID: "K",
    DAREK_ID: "M",
    LUCJA_ID: "K",
    POLA_ID: "K",
    KUBA_ID: "M",
    LESNIEW_ID: "M",
    TIXTER_ID: "M"
}

# Słownik do tłumaczenia ID na imiona dla lektora
ID_TO_NAME = {
    KISMET_ID: "Kismet",
    MICHAL_ID: "Michał",
    RHAAST_ID: "Rast",
    JAXER_ID: "Jaxer",
    ERYK_ID: "Eryk",
    HORDA_ID: "Horda",
    PAVELOS_ID: "Pavelos",
    DAVID_ID: "Dawid",
    LEI_ID: "Lei",
    DAREK_ID: "Darek",
    LUCJA_ID: "Łucja",
    POLA_ID: "Pola",
    KUBA_ID: "Kuba",
    LESNIEW_ID: "Leśniew",
    TIXTER_ID: "Tixter"
}

# --- MAPOWANIE ID RÓL ---
ROLE_WLASCICIEL = "1339965713619615790"
ROLE_TATUS      = "1454123233954631894"
ROLE_CORKA      = "1455634844712173744"
ROLE_ADMIN      = "1339965713619615789"
ROLE_MODERATOR  = "1339965713619615788"
ROLE_PARA       = "1443706990898446366"
ROLE_CHLOPAK    = "1339965713401516039"
ROLE_DZIEWCZYNA = "1339965713401516038"
ROLE_ZNAJOMY    = "1339965713401516041"
ROLE_CZLONEK    = "1339965712969498701"
ROLE_18_PLUS    = "1339965713401516035"
ROLE_WIEK_17_18 = "1339965713401516034"
ROLE_WIEK_15_16 = "1339965713401516033"
ROLE_WIEK_13_14 = "1339965713401516032"

# --- USTAWIENIA 21:37 (BARKA) ---
GODZINA_BARKI_PL = "21:37" 
czas_barki_obj = datetime.strptime(GODZINA_BARKI_PL, "%H:%M") - timedelta(hours=4)
GODZINA_BARKI_BOT = czas_barki_obj.strftime("%H:%M")

# --- USTAWIENIA MUZYKI I VOLUME ---
DEFAULT_STREAMING_VOLUME = 0.4
DEFAULT_MUZYKA_VOLUME = 0.8
DEFAULT_POBUDKA_VOLUME = 0.9
DEFAULT_MAX_VOLUME = 2.0

# --- LIMITERY I CZASY ---
MAX_DM_REPEAT = 1000
CZAS_WYCISZENIA_JAXER = 90
CZAS_WYCISZENIA_RHAT = 120
CZAS_WYCISZENIA_DAVID = 67
CZAS_WYCISZENIA_HORDA = 30
CZAS_WYCISZENIA_MICHAL = 127

# --- CONFIG ŚPIOCHA (AUTO-POBUDKA) ---
CZAS_DO_POBUDKI = 900  # 15 minut w sekundach
spiochy = {}           # Słownik: {user_id: timestamp_wyciszenia}

# --- COOLDOWNS ---
COOLDOWN = {"s": 400, "zagraj": 2, "dm": 480, "pobudka": 250, "szponcik": 300, "oznacz_user": 60, "oznacz_admin": 5, "los": 25, "przenies": 5 ,"verstappen": 20, "syrena": 10, "przerwa": 5,"eryk":160,"wojfer":60,"crazy":60,"gejtos":60,"za_gorami_za_lasami":60}
custom_trigger_cooldowns = {}
CUSTOM_TRIGGER_COOLDOWN_TIME = 400
MAX_OZNACZEN_USER = 30
MAX_OZNACZEN_ADMIN = 20000
automat_piwnica_users = {}

# --- DATA / TRIGGERY ---
TRIGGERS = {
    MICHAL_ID: "https://cdn.discordapp.com/attachments/1339965713619615792/1444468797376561152/attachment.gif",
    LUCJA_ID: "https://cdn.discordapp.com/attachments/1089578033150693488/1391819603721584761/attachment.gif",
    DAREK_ID: "https://cdn.discordapp.com/attachments/1352653139303469197/1414338048010883237/DAREK.png",
    HORDA_ID: "https://cdn.discordapp.com/attachments/1339965714081251349/1434282714692845639/horda_i_kismet1.gif",
    KISMET_ID: "https://cdn.discordapp.com/attachments/1238095680959025163/1414312913765666857/image.png",
    DAVID_ID: "https://cdn.discordapp.com/attachments/1348240889423724596/1403488458361540738/david.png",
    RHAAST_ID: "https://cdn.discordapp.com/attachments/1238095680959025163/1414722515020025988/Adobe_Express_-_nwm.gif",
    KUBA_ID: "https://cdn.discordapp.com/attachments/1238095680959025163/1421230997055213729/image.png",
    ERYK_ID: "https://cdn.discordapp.com/attachments/1238095680959025163/1414322897320935525/latest.png",
    PAVELOS_ID: "https://cdn.discordapp.com/attachments/1339965713619615792/1461003580940095569/attachment.gif?ex=6968f91d&is=6967a79d&hm=8c8f577103763073457d033f205f37dfb751b935567c4cf0701bf6c72c004843&",
    LEI_ID: "https://cdn.discordapp.com/attachments/1339965714265673839/1443350160129130769/attachment.gif",
}

CUSTOM_TEXT_TRIGGERS = {
    "klatwa kastiego": {
        "action": "random_kick_voice",  
        "cooldown": 90,                
        "text": "🧙‍♂️ **Klątwa Kastiego** została rzucona..."
    },
    ("zakochana para", "{ROLE_PARA}"): {
        "action": ["ping_members_of_role", "ilosc_w(2)"],
        "role_ids": [ROLE_PARA],
        "text": "❤️❤️"
    },
    ("tata i curka", "{ROLE_TATUS} {ROLE_CORKA}", "{ROLE_CORKA} {ROLE_TATUS}"): {
        "action": "ping_members_of_role",
        "role_ids": [ROLE_TATUS, ROLE_CORKA],
        "text": " i "
    },
    # --- POPRAWIONE SEKCJE ---
    "wypierdalaj frajerze": {
        "action": "timeout_member",
        "timeout_user": int(MICHAL_ID),
        "timeout_duration": CZAS_WYCISZENIA_MICHAL,
        "text": f"Ochłoń na {CZAS_WYCISZENIA_MICHAL} sekund, Frajerze. 🧊",
        "cooldown": 180
    },
    "ochlon rhast": {
        "action": "timeout_member",
        "timeout_user": int(RHAAST_ID),
        "timeout_duration": CZAS_WYCISZENIA_RHAT,
        "text": f"Ochłoń na {CZAS_WYCISZENIA_RHAT} sekund, kolego. 🧊",
        "cooldown": 240
    },
    "stop horda": {
        "action": "timeout_member",
        "timeout_user": int(HORDA_ID),
        "timeout_duration": CZAS_WYCISZENIA_HORDA,
        "text": f"Ochłoń na {CZAS_WYCISZENIA_HORDA} sekund, kolego. 🧊",
        "cooldown": 240
    },
        "spokojnie dawid": {
        "action": "timeout_member",
        "timeout_user": int(DAVID_ID),
        "timeout_duration": CZAS_WYCISZENIA_DAVID,
        "text": f"Ochłoń na {CZAS_WYCISZENIA_DAVID} sekund, kolego. 🧊",
        "cooldown": 180
    },
    "przegioles pale jaxer": {
        "action": "timeout_member",
        "timeout_user": int(JAXER_ID),
        "timeout_duration": CZAS_WYCISZENIA_JAXER,
        "text": f"Przegiołeś pałę na {CZAS_WYCISZENIA_JAXER} sekund, kolego. 🧊",
        "cooldown": 420
    },
    # -------------------------
    "@kasia": "https://cdn.discordapp.com/attachments/1339965713619615792/1446226672369143969/ez.gif?ex=6933370c&is=6931e58c&hm=5bb9b45f02f1ab3fbcaaf89e4ecdb297d40d3459c8a5c6f8b89d71dfef528543&",
    "lei nie spimy": {
        "reply": "n",
        "dm": "Nie spimy, wstajemy",
        "dm_user": int(LEI_ID)
    },
    "67": {
        "action": "check_67_trigger",
        "text": "https://tenor.com/view/happycadogt-bang-pow-shooting-firing-gif-11168675231868030801"
    },
    "dzis jest ta noc": {
        "action": "random_ping",
        "text": "https://cdn.discordapp.com/attachments/1339965713619615792/1445861721188335626/attachment.gif?ex=6931e329&is=693091a9&hm=04a8240e6801cf263dcf2e52c440847769d15c3bfe9e72957abe929eacac828a&",
        "ids": [PAVELOS_ID, KUBA_ID, LEI_ID, HORDA_ID, RHAAST_ID, DAVID_ID, ERYK_ID, JAXER_ID, LUCJA_ID, KISMET_ID,DAREK_ID]
    },
    "czarnuch": "https://cdn.discordapp.com/attachments/1130980347245494365/1249092612913369199/racism.gif?ex=69314165&is=692fefe5&hm=09f1f4a5bb5e027372f1177037a11dba86934140907aa00e3df4c25c0fe3a8ac&",
    "@femboy": [f"<@{ERYK_ID}>", f"<@{KUBA_ID}>", f"<@{DAVID_ID}>"],
    "erys": "https://cdn.discordapp.com/attachments/1339965713619615792/1433550997178810498/attachment.gif?ex=69314427&is=692ff2a7&hm=767720768034ada858d610b83ddd9e3d983c6097d691610cbc3d3599eccea281&",
    "olej": "https://cdn.discordapp.com/attachments/1339965713619615792/1444470586909659256/attachment.gif",
    "graczligi": f"<@{MICHAL_ID}>",
    "kto jest rudy": f"https://cdn.discordapp.com/attachments/1238095680959025163/1428009971114840156/cmlk.png to ty <@{HORDA_ID}>",
    "dziewczyna pavelosa": ["@katarzyna", "@kasia"],
    "lazienka": {
        "action": "ilosc_w(10)",
        "text": f"<@{HORDA_ID}> <@{KISMET_ID}>"
    },
    "kismet": "https://cdn.discordapp.com/attachments/1238095680959025163/1423725663172427928/image.png",
    "schizofrenia": f"https://cdn.discordapp.com/attachments/1415753667562176512/1429894717352579144/att.0I2XMQXK7OKjn4KCQeSoPsikVIyFk6SsfgrCfIzHRag.png.jpg <@{KUBA_ID}>",
    "50%": ["{author}", "@everyone"],
    "sex": "NIE masturbuj sie w miejscu publicznym, {author}",
    ("lei i rhast", "rill"): "https://cdn.discordapp.com/attachments/1339965713619615792/1447287096233427196/attachment.gif?ex=693b0725&is=6939b5a5&hm=3440c723dd813ff9e526a91fe1e9bcfebaf5e39fbd8cfacd1db481e910154d6e&",
    "tata hordy": f"<@{PAVELOS_ID}>❤️",
    "wakey wakey": {
        "action": "ilosc_w([1,2,3,4,5])",
        "text": "@everyone",
        "admin_only": True
    },
    "losowanie": {
        "action": "losuj_dm",
        "dm_text": "zostales wylosowany na https://media.discordapp.net/attachments/1158788675325411351/1175608899768946780/zelekpistolet.gif",
        "dm_users": [PAVELOS_ID, KUBA_ID, LEI_ID, HORDA_ID, RHAAST_ID, DAVID_ID, ERYK_ID, JAXER_ID, LUCJA_ID, KISMET_ID]
    },
    "pobudka": {"action": "pobudka_sequence"},
    "najwiekszy furas": {
        "reply": "n",
        "dm": "Ktos tu jest największym furasem",
        "dm_user": int(KUBA_ID)
    },
    "jaxer": {
        "reply": "n",
        "dm": "WSTAWAJ WSTAWAJ WSTAWAJ",
        "dm_user": int(JAXER_ID)
    },
    "moneta": ["orzeł", "reszka"],
    "muzyka dla moich uszu": {"action": "play_muzyka_exact"},
    "verstappen": {"action": "play_verstappen"},
    "grecki pedal": {"action": "play_gejtos"},
    "zobaczymy jak bomba pierdolnie": {"action": "play_syrena"},
    "eryk skoncz pierdolic": {"action": "wycisz_eryk", "user": int(ERYK_ID)},
    "za gorami za lasami": {"action": "play_za_gorami_za_lasami"},
    "crazy": {"action": "play_crazy"},
    "silownia": {"action": "play_wojfer"},
    "spiderman":{"action": "play_spermaman"},
    "horda kiedy pavelos":{"action": "play_tatus"},
    "kuba femboy": {"action": "play_kuba_femboy"},
    "drzewo nds": "https://cdn.discordapp.com/attachments/1238095680959025163/1467948922684178564/drzewo.png?ex=69823d78&is=6980ebf8&hm=0dd65b10ff197d1008fb0f11d6123ebccec8a2c714db7c4982044aa0f4b0367c&",
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)
cooldowns = {action: {} for action in COOLDOWN.keys()}

# ==================== NOWA FUNKCJA: OBSŁUGA WIADOMOŚCI PV ====================
async def handle_private_message(message):
    """
    Obsługuje wiadomości prywatne.
    Czyta KAŻDĄ wiadomość od osób z listy OSOBY_MONITOROWANE.
    """
    # 1. Sprawdź czy nadawca jest na liście zaufanych
    sender_id_str = str(message.author.id)
    
    if sender_id_str not in OSOBY_MONITOROWANE:
        print(f"🔒 Zignorowano wiadomość od {message.author.name} (brak na liście).")
        return

    # Ignoruj puste wiadomości
    content = message.content.strip()
    if not content:
        return

    # --- NOWA LOGIKA WYCINANIA KOMENDY ---
    # Jeśli wiadomość zaczyna się od !wyslij, usuń to z tekstu do czytania
    if content.lower().startswith("!wyslij"):
        # Usuwamy pierwsze 7 znaków (!wyslij) i czyścimy spacje na początku
        clean_content = content[7:].strip()
    else:
        clean_content = content
    
    # Jeśli po wycięciu !wyslij nic nie zostało, nie ma co czytać
    if not clean_content:
        return
    # -------------------------------------

    print(f"📩 Otrzymano PV od {message.author.name}: {clean_content}")

    # 2. Ustalenie nazwy i płci
    sender_name = ID_TO_NAME.get(sender_id_str, message.author.name)
    plec = ID_PLECI.get(sender_id_str, "M") 
    
    akcja = "powiedziała" if plec == "K" else "powiedział"
    
    # Używamy clean_content zamiast content
    text_to_speak = f"{sender_name} {akcja}: {clean_content}"
# 3. Wybór kanału docelowego (Priorytety: Ty -> Największa grupa -> Piwnica)
    target_channel = None

    # PRIORYTET 1: Szukaj Ciebie (autora wiadomości PV) na wszystkich serwerach
    for guild in client.guilds:
        member = guild.get_member(message.author.id)
        if member and member.voice:
            target_channel = member.voice.channel
            print(f"📍 Znaleziono Cię na kanale: {target_channel.name}")
            break
    
    # PRIORYTET 2: Jeśli Ciebie nie ma, szukaj kanału z największą liczbą osób
    if not target_channel:
        all_channels = []
        for guild in client.guilds:
            all_channels.extend(guild.voice_channels)
        
        # Filtrujemy kanały, gdzie siedzą ludzie (pomijamy boty)
        active_channels = [c for c in all_channels if len([m for m in c.members if not m.bot]) > 0]
        
        if active_channels:
            target_channel = max(active_channels, key=lambda c: len([m for m in c.members if not m.bot]))
            print(f"📍 Wybrano największą grupę na: {target_channel.name}")

    # PRIORYTET 3: Jeśli wszędzie jest pusto, idź do "piwnica"
    if not target_channel:
        for guild in client.guilds:
            target_channel = discord.utils.get(guild.voice_channels, name="piwnica")
            if target_channel:
                print(f"📍 Pusto na serwerach, idę do piwnicy.")
                break

    # 4. Odtwarzanie za pomocą Twojej klasy TTSManager
    if target_channel:
        try:
            # Używamy Twojej metody speak, która sama połączy bota i odtworzy dźwięk
            await TTSManager.speak(target_channel, text_to_speak)
            await message.add_reaction("✅")
        except Exception as e:
            print(f"❌ Błąd podczas TTSManager.speak: {e}")
            await message.channel.send(f"Błąd: {e}")
    else:
        # Jeśli nawet kanał "piwnica" nie został znaleziony
        await message.channel.send("❌ Nie ma Cię na VC, nikt inny nie siedzi na kanałach i nie widzę kanału 'piwnica'.")
# ==================== FUNKCJA POMOCNICZA: POBUDKA ====================
async def wykonaj_pobudke(guild, member):
    """
    Zoptymalizowana procedura pobudki z obsługą błędów i czyszczeniem sesji.
    """
    target_channel = await ChannelManager.znajdz_kanal_po_nazwie(guild, NAZWA_KANALU_POBUDKA)
    if not target_channel:
        print(f"❌ [BŁĄD] Brak kanału '{NAZWA_KANALU_POBUDKA}' na serwerze {guild.name}.")
        return

    # 1. Zabezpieczenie: Sprawdź czy użytkownik nadal jest na VC
    if not member.voice or not member.voice.channel:
        print(f"🏃 {member.name} uciekł z VC przed pobudką.")
        return

    original_channel = member.voice.channel
    path = "pobudka.mp3"

    if not os.path.exists(path):
        print(f"❌ [BŁĄD] Brak pliku {path}!")
        return

    # 2. Wyczyszczenie starego połączenia bota, jeśli istnieje
    if guild.voice_client:
        try:
            await guild.voice_client.disconnect(force=True)
            await asyncio.sleep(0.5)
        except: pass

    vc = None
    try:
        # 3. Przenieś ofiarę i wejdź botem
        await member.move_to(target_channel)
        vc = await target_channel.connect(timeout=10.0, reconnect=False)
        
        print(f"🔊 Procedura pobudki dla: {member.name}")
        
        # 4. Odtwarzanie dźwięku
        audio_source = discord.FFmpegPCMAudio(path, options=f"-vn -af volume={DEFAULT_POBUDKA_VOLUME}")
        vc.play(audio_source)

        # Czekaj aż skończy grać (max 15 sek, żeby bot nie utknął)
        timeout_play = 0
        while vc.is_playing() and timeout_play < 15:
            await asyncio.sleep(1)
            timeout_play += 1
            
    except Exception as e:
        print(f"⚠️ Problem w trakcie grania pobudki: {e}")
    finally:
        # 5. Sprzątanie: Rozłącz bota i odstaw użytkownika
        if vc:
            try: await vc.disconnect(force=True)
            except: pass
        
        await asyncio.sleep(0.5)
        
        # Odstawianie użytkownika z powrotem (jeśli nadal jest na serwerze)
        if member.voice:
            try:
                await member.move_to(original_channel)
                print(f"🔙 Odstawiono {member.name} na {original_channel.name}")
            except:
                # Jeśli kanał oryginalny zniknął, przenieś do piwnicy
                piwnica = await ChannelManager.znajdz_kanal_piwnica(guild)
                if piwnica: await member.move_to(piwnica)

        # 6. RESTART LICZNIKA (Jeśli nadal śpi po pobudce)
        await asyncio.sleep(1)
        if member.voice and member.voice.self_mute and not member.voice.self_deaf:
            spiochy[member.id] = time.time()

# ==================== SPOTIFY SCRAPER ====================
class SpotifyScraper:
    def is_spotify_link(self, query):
        return "spotify.com" in query or "spotify:" in query

    def get_youtube_query(self, url):
        clean_url = url.split('?')[0]
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            response = requests.get(clean_url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    clean = title_tag.text.replace(" | Spotify", "").replace(" - Single", "").strip()
                    if "playlist" in url:
                        clean = clean.split(" - song by")[0] if " - song by" in clean else clean
                    print(f"🎵 Spotify: {clean}")
                    return f"{clean} audio"
        except Exception as e:
            print(f"⚠️ Spotify Error: {e}")
        return url

spotify_scraper = SpotifyScraper()

# ==================== COOLDOWN MANAGER ====================
class CooldownManager:
    @staticmethod
    def is_on_cooldown(user_id, action_type):
        if action_type not in cooldowns or user_id not in cooldowns[action_type]: return False, 0
        last = cooldowns[action_type][user_id]
        diff = time.time() - last
        if diff < COOLDOWN.get(action_type, 0): return True, COOLDOWN.get(action_type, 0) - diff
        return False, 0

    @staticmethod
    def update_cooldown(user_id, action_type):
        if action_type not in cooldowns: cooldowns[action_type] = {}
        cooldowns[action_type][user_id] = time.time()

    @staticmethod
    def format_time(seconds): return int(seconds // 60), int(seconds % 60)

    @staticmethod
    def is_custom_trigger_on_cooldown(user_id, trigger, custom_time=None):
        if trigger in ["pobudka", "muzyka", "zagraj", "dm", "syrena"]: return False, 0
        key = f"{user_id}:{trigger}"
        if key not in custom_trigger_cooldowns: return False, 0
        
        diff = time.time() - custom_trigger_cooldowns[key]
        limit = custom_time if custom_time is not None else CUSTOM_TRIGGER_COOLDOWN_TIME
        if diff < limit: return True, limit - diff
        return False, 0

    @staticmethod
    def update_custom_trigger_cooldown(user_id, trigger):
        if trigger in ["pobudka", "muzyka", "zagraj", "dm", "syrena"]: return
        key = f"{user_id}:{trigger}"
        custom_trigger_cooldowns[key] = time.time()

class ChannelManager:
    @staticmethod
    async def znajdz_kanal_po_nazwie(guild, channel_name):
        return discord.utils.find(lambda c: channel_name.lower() in c.name.lower(), guild.voice_channels)

    @staticmethod
    async def znajdz_kanal_spontu(guild):
        return await ChannelManager.znajdz_kanal_po_nazwie(guild, NAZWA_KANALU_SPONTU)

    @staticmethod
    async def znajdz_kanal_piwnica(guild):
        return await ChannelManager.znajdz_kanal_po_nazwie(guild, NAZWA_KANALU_PIWNICA)

    @staticmethod
    async def przenies_uzytkownika(member, target_channel=None):
        try:
            if not target_channel:
                target_channel = await ChannelManager.znajdz_kanal_spontu(member.guild)
            if not target_channel: return False, None
            if member.voice and member.voice.channel and member.voice.channel.id != target_channel.id:
                await member.move_to(target_channel)
                return True, target_channel
            return False, target_channel
        except: return False, target_channel

    @staticmethod
    async def szponcik_przenies_wszystkich(guild):
        try:
            target = await ChannelManager.znajdz_kanal_spontu(guild)
            if not target: return False, 0, f"Nie znaleziono '{NAZWA_KANALU_SPONTU}'"
            przeniesieni = 0
            for channel in guild.voice_channels:
                if channel.id == target.id: continue
                for member in list(channel.members):
                    if not member.bot:
                        try:
                            await member.move_to(target)
                            przeniesieni += 1
                            await asyncio.sleep(0.5)
                        except: pass
            return True, przeniesieni, f"Przeniesiono {przeniesieni}"
        except Exception as e: return False, 0, f"Błąd: {e}"

# ==================== TTS MANAGER (POPRAWIONY) ====================
class TTSManager:
    @staticmethod
    async def speak(channel, text, lang='pl'):
        """Generuje mowę i odtwarza ją, zostając na kanale."""
        try:
            filename = "tts_output.mp3"
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)
            await asyncio.sleep(0.2)

            vc = channel.guild.voice_client
            if not vc:
                vc = await channel.connect()
            elif vc.channel.id != channel.id:
                await vc.move_to(channel)

            if vc.is_playing():
                vc.stop()

            audio_source = discord.FFmpegPCMAudio(filename, options=f"-vn -af volume={DEFAULT_MUZYKA_VOLUME}")
            vc.play(audio_source)

            while vc.is_playing():
                await asyncio.sleep(0.5)
            
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"❌ Błąd TTS speak: {e}")

    @staticmethod
    async def handle_lektor_command(message):
        """Obsługa komendy !wejdz - zarządzanie lektorem."""
        global OSOBY_DO_CZYTANIA
        content = message.content.strip()
        parts = content.split()
        
        # 1. !wejdz - włącza/wyłącza lektora dla Kismeta (domyślnie)
        if len(parts) == 1 and content.lower() == "!wejdz":
            if KISMET_ID in OSOBY_DO_CZYTANIA:
                OSOBY_DO_CZYTANIA.remove(KISMET_ID)
                await message.channel.send("🔇 Wyłączono lektora dla Kismeta.")
            else:
                OSOBY_DO_CZYTANIA.append(KISMET_ID)
                # Sprawdź czy Kismet jest na VC
                kismet_member = message.guild.get_member(int(KISMET_ID))
                if kismet_member and kismet_member.voice:
                    voice_channel = kismet_member.voice.channel
                    if message.guild.voice_client:
                        await message.guild.voice_client.move_to(voice_channel)
                    else:
                        await voice_channel.connect()
                    await message.channel.send(f"✅ Włączono lektora dla Kismeta. Wbiłem na jego kanał!")
                else:
                    await message.channel.send("✅ Włączono lektora dla Kismeta (ale nie jest on na VC).")
            return True
        
        # 2. !wejdz <@id> - dodaje/usuwa konkretną osobę
        elif len(parts) == 2 and parts[0].lower() == "!wejdz":
            pings = re.findall(r"<@!?(\d+)>", parts[1])
            if not pings:
                await message.channel.send("❌ Użycie: `!wejdz <@wzmianka>`")
                return True
            
            target_id = pings[0]
            target_member = message.guild.get_member(int(target_id))
            
            if not target_member:
                await message.channel.send("❌ Nie znaleziono użytkownika na serwerze.")
                return True
            
            if target_id in OSOBY_DO_CZYTANIA:
                OSOBY_DO_CZYTANIA.remove(target_id)
                await message.channel.send(f"🔇 Wyłączono lektora dla **{target_member.display_name}**.")
            else:
                OSOBY_DO_CZYTANIA.append(target_id)
                # Wejdź na kanał tej osoby jeśli jest na VC
                if target_member.voice:
                    voice_channel = target_member.voice.channel
                    if message.guild.voice_client:
                        await message.guild.voice_client.move_to(voice_channel)
                    else:
                        await voice_channel.connect()
                    await message.channel.send(f"✅ Włączono lektora dla **{target_member.display_name}**. Wbiłem na jego kanał!")
                else:
                    await message.channel.send(f"✅ Włączono lektora dla **{target_member.display_name}** (ale nie jest na VC).")
            return True
        
        # 3. !wejdz <@id1> <@id2> ... - dodaje kilka osób
        elif len(parts) >= 2 and parts[0].lower() == "!wejdz":
            pings = re.findall(r"<@!?(\d+)>", content)
            if not pings:
                await message.channel.send("❌ Użycie: `!wejdz <@wzmianka1> <@wzmianka2> ...`")
                return True
            
            added = []
            removed = []
            
            for ping_id in pings:
                target_member = message.guild.get_member(int(ping_id))
                if not target_member:
                    continue
                
                if ping_id in OSOBY_DO_CZYTANIA:
                    OSOBY_DO_CZYTANIA.remove(ping_id)
                    removed.append(target_member.display_name)
                else:
                    OSOBY_DO_CZYTANIA.append(ping_id)
                    added.append(target_member.display_name)
            
            # Wejdź na kanał pierwszego pingowanego który jest na VC
            for ping_id in pings:
                target_member = message.guild.get_member(int(ping_id))
                if target_member and target_member.voice:
                    voice_channel = target_member.voice.channel
                    if message.guild.voice_client:
                        await message.guild.voice_client.move_to(voice_channel)
                    else:
                        await voice_channel.connect()
                    break
            
            response = []
            if added:
                response.append(f"✅ **Dodano:** {', '.join(added)}")
            if removed:
                response.append(f"🔇 **Usunięto:** {', '.join(removed)}")
            
            if response:
                await message.channel.send("\n".join(response))
            return True
        
        return False

    @staticmethod
    async def process_tts(message):
        """Przetwarza wiadomości użytkowników z listy OSOBY_DO_CZYTANIA."""
        global OSOBY_DO_CZYTANIA
        
        if str(message.author.id) not in OSOBY_DO_CZYTANIA:
            return
        
        if message.author.voice and message.author.voice.channel:
            if not message.content.startswith(('!', 'http')):
                # Czyścimy pingi przed czytaniem
                text_to_read = message.content
                user_pings = re.findall(r"<@!?(\d+)>", text_to_read)
                for uid in user_pings:
                    name = ID_TO_NAME.get(uid, "użytkownik")
                    text_to_read = text_to_read.replace(f"<@{uid}>", name).replace(f"<@!{uid}>", name)
                
                await TTSManager.speak(message.author.voice.channel, text_to_read)

# ==================== MUSIC MANAGER ====================
class MusicManager:
    YDL_OPTS = {
        'format': 'bestaudio[protocol^=http]/bestaudio/best', 
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0', 
        'extractor_args': {'youtube': {'player_client': ['ios']}},
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'nocheckcertificate': True,
        'socket_timeout': 30,
        # WAŻNE: Obsługa cookies, żeby YouTube nie blokował
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None, 
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel error',
        'options': '-vn'
    }

    music_queue = {}

    @staticmethod
    def get_guild_data(guild_id):
        if guild_id not in MusicManager.music_queue:
            MusicManager.music_queue[guild_id] = {
                'queue': [], 'loop': False, 'voice_client': None, 'now_playing': None
            }
        return MusicManager.music_queue[guild_id]

    @staticmethod
    async def get_audio_source(url_or_query):
        loop = asyncio.get_event_loop()
        query = url_or_query.strip()
        
        if spotify_scraper.is_spotify_link(query):
            query = spotify_scraper.get_youtube_query(query)
            if not query.startswith("http") and not query.startswith("ytsearch:"):
                query = f"ytsearch:{query}"

        if not query.startswith(('http://', 'https://')):
            query = f"ytsearch:{query}"

        print(f"[YT-DLP] Szukam: {query}")

        try:
            ydl = yt_dlp.YoutubeDL(MusicManager.YDL_OPTS)
            func = functools.partial(ydl.extract_info, query, download=False)
            data = await asyncio.wait_for(loop.run_in_executor(None, func), timeout=45.0)

            if not data: raise Exception("Brak danych z YT")
            if 'entries' in data: data = data['entries'][0]
            
            source_url = data.get('url')
            title = data.get('title', 'Nieznany')
            if not source_url: raise Exception("Brak URL")
            
            print(f"[YT-DLP] Znaleziono: {title}")
            source = discord.FFmpegPCMAudio(source_url, executable='ffmpeg', **MusicManager.FFMPEG_OPTIONS)
            return discord.PCMVolumeTransformer(source, volume=DEFAULT_STREAMING_VOLUME), title

        except Exception as e:
            print(f"[YT ERROR] {e}")
            raise e

    @staticmethod
    async def start_playback(guild_id):
        guild_data = MusicManager.get_guild_data(guild_id)
        guild = client.get_guild(guild_id)
        
        if not guild or not guild.voice_client or not guild.voice_client.is_connected():
            guild_data['queue'] = []
            return

        vc = guild.voice_client
        if not guild_data['queue']:
            guild_data['now_playing'] = None
            asyncio.run_coroutine_threadsafe(MusicManager.disconnect_after_delay(vc), client.loop)
            return

        track = guild_data['queue'].pop(0)
        try:
            source, title = await MusicManager.get_audio_source(track['query'])
        except Exception as e:
            if 'text_channel' in track:
                try: await track['text_channel'].send(f"⚠️ Błąd: {e}")
                except: pass
            await asyncio.sleep(1)
            await MusicManager.start_playback(guild_id)
            return

        guild_data['now_playing'] = title
        if 'text_channel' in track:
            try: await track['text_channel'].send(f"▶️ **{title}**")
            except: pass

        def _after(error):
            fut = MusicManager._on_track_end(guild_id, track, error)
            asyncio.run_coroutine_threadsafe(fut, client.loop)

        try:
            if vc.is_playing(): vc.stop()
            vc.play(source, after=_after)
        except Exception as e:
            await MusicManager._on_track_end(guild_id, track, e)

    @staticmethod
    async def _on_track_end(guild_id, finished_track, error):
        guild = client.get_guild(guild_id)
        if not guild or not guild.voice_client or not guild.voice_client.is_connected():
            MusicManager.get_guild_data(guild_id)['queue'] = []
            return

        guild_data = MusicManager.get_guild_data(guild_id)
        if guild_data.get('loop'): guild_data['queue'].append(finished_track)

        if guild_data['queue']:
            await asyncio.sleep(0.5)
            await MusicManager.start_playback(guild_id)
        else:
            guild_data['now_playing'] = None
            asyncio.run_coroutine_threadsafe(MusicManager.disconnect_after_delay(guild.voice_client), client.loop)

    @staticmethod
    async def disconnect_after_delay(vc, delay=300):
        await asyncio.sleep(delay)
        try:
            if vc and vc.is_connected() and not vc.is_playing(): await vc.disconnect()
        except: pass

    @staticmethod
    async def add_and_play(message, url_or_query):
        guild_id = message.guild.id
        guild_data = MusicManager.get_guild_data(guild_id)

        if not message.author.voice: return "❌ Wejdź na kanał!", False
        await message.channel.send("🔎 Szukam...")
        
        try:
            _, title = await MusicManager.get_audio_source(url_or_query)
        except Exception as e: return f"❌ Błąd YT: {e}", False

        vc = message.guild.voice_client
        try:
            if not vc or not vc.is_connected():
                vc = await message.author.voice.channel.connect(timeout=20.0, reconnect=True)
                await asyncio.sleep(1.5)
            elif vc.channel.id != message.author.voice.channel.id:
                await vc.move_to(message.author.voice.channel)
        except Exception as e: return f"❌ Błąd łączenia: {e}", False

        track = {'query': url_or_query, 'title': title, 'text_channel': message.channel}
        guild_data['queue'].append(track)

        if vc.is_playing(): return f"🎵 Dodano: **{title}** ({len(guild_data['queue'])})", True
        await MusicManager.start_playback(guild_id)
        return f"▶️ Gram: **{title}**", True

    @staticmethod
    async def stop_music(guild_id):
        guild_data = MusicManager.get_guild_data(guild_id)
        guild = client.get_guild(guild_id)
        vc = guild.voice_client if guild else None
        guild_data['queue'] = []
        guild_data['now_playing'] = None
        if vc:
            if vc.is_playing(): vc.stop()
            try: await vc.disconnect(force=True)
            except: pass
            return "⏹️ Zatrzymano"
        return "❌ Bot nie gra"

    @staticmethod
    def skip_track(guild_id):
        guild = client.get_guild(guild_id)
        vc = guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            return "⏭️ Pominięto"
        return "❌ Nic nie gra"

    @staticmethod
    def toggle_loop(guild_id):
        guild_data = MusicManager.get_guild_data(guild_id)
        guild_data['loop'] = not guild_data['loop']
        status = "✅" if guild_data['loop'] else "❌"
        return f"🔁 Pętla: {status}"

# ==================== HANDLERY KOMEND ====================
class CommandHandler:
    
    @staticmethod
    async def handle_check_67_trigger(message):
        """Obsługa triggery '67' - nie działa na same pingi."""
        # Sprawdź czy to tylko pingi + 67
        content_without_pings = re.sub(r'<@!?\d+>', '', message.content)
        content_without_pings = re.sub(r'<@&\d+>', '', content_without_pings)
        content_without_pings = content_without_pings.strip()
        
        # Usuń też zwykłe spacje i sprawdź czy zostaje tylko "67"
        if content_without_pings.replace(' ', '') == "67":
            await message.channel.send("https://tenor.com/view/happycadogt-bang-pow-shooting-firing-gif-11168675231868030801")
            return True
        return False

    @staticmethod
    async def handle_za_gorami_za_lasami(message):
        if not message.author.voice: 
            return
        
        path = "lasy.mp3"
        if not os.path.exists(path): 
            print(f"❌ Brak pliku: {path}")
            return

        # Rozłącz bota jeśli już gdzieś siedzi
        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            # Używamy DEFAULT_MUZYKA_VOLUME dla spójności
            vc.play(discord.FFmpegPCMAudio(path, options=f"-vn -af volume={DEFAULT_MUZYKA_VOLUME}"))
            print(f"🔊 Gram za górami za lasami dla: {message.author.name}")
            
            while vc.is_playing(): 
                await asyncio.sleep(1)
            await vc.disconnect()
        except Exception as e:
            print(f"Błąd odtwarzania lasy.mp3: {e}")

    @staticmethod
    async def handle_obudz(message):
        if not message.author.guild_permissions.move_members and not message.author.guild_permissions.administrator:
            await message.channel.send("❌ Nie masz uprawnień do budzenia ludzi.")
            return

        match = re.search(r'\d+', message.content)
        if not match:
            await message.channel.send("❌ Podaj ID lub oznacz użytkownika: `!obudz <ID/wzmianka>`")
            return
            
        target_id = int(match.group(0))
        member = message.guild.get_member(target_id)
        
        if not member:
            await message.channel.send("❌ Nie znaleziono użytkownika na serwerze.")
            return
        if not member.voice:
            await message.channel.send("❌ Użytkownik nie jest połączony z żadnym kanałem głosowym.")
            return

        kanal_spont = await ChannelManager.znajdz_kanal_spontu(message.guild)
        kanal_piwnica = await ChannelManager.znajdz_kanal_piwnica(message.guild)

        if not kanal_spont or not kanal_piwnica:
            await message.channel.send(f"❌ Nie znaleziono kanałów: '{NAZWA_KANALU_SPONTU}' lub '{NAZWA_KANALU_PIWNICA}'")
            return

        loops = random.choice([4, 5, 6, 7, 8])
        await message.channel.send(f"😈 Rozpoczynam procedurę budzenia dla: {member.mention} ({loops} cykli)")

        for i in range(loops):
            try:
                if not member.voice:
                    await message.channel.send("🏃 Użytkownik uciekł z VC!")
                    break
                await member.move_to(kanal_spont)
                await asyncio.sleep(0.6)
                await member.move_to(kanal_piwnica)
                await asyncio.sleep(0.6)
            except discord.Forbidden:
                await message.channel.send("❌ Bot nie ma uprawnień do przenoszenia tego użytkownika.")
                break
            except Exception as e:
                print(f"Critical error obudz: {e}")
                break
        
        await message.channel.send(f"✅ Zakończono budzenie {member.mention}.")

    @staticmethod
    async def handle_colon_trigger(message):
        content = message.content
        if ":" not in content: return False
        parts = content.split(":", 1)
        key = parts[0].strip().lower()
        value = parts[1].strip()

        if key in CUSTOM_TEXT_TRIGGERS and not isinstance(CUSTOM_TEXT_TRIGGERS[key], dict):
            user_id = str(message.author.id)
            on_cd, remaining = CooldownManager.is_custom_trigger_on_cooldown(user_id, key)
            if on_cd:
                mins, secs = CooldownManager.format_time(remaining)
                await message.channel.send(f"⏱️ Czekaj {mins}m {secs}s")
                return True
            CooldownManager.update_custom_trigger_cooldown(user_id, key)
            await message.channel.send(value)
            return True
        return False

    @staticmethod
    async def handle_zagraj(message):
        user_id = str(message.author.id)
        on_cd, rem = CooldownManager.is_on_cooldown(user_id, "zagraj")
        if on_cd: return
        query = message.content[len("!zagraj"):].strip()
        if not query: return
        CooldownManager.update_cooldown(user_id, "zagraj")
        resp, _ = await MusicManager.add_and_play(message, query)
        await message.channel.send(resp)

    @staticmethod
    async def handle_loop(message):
        resp = MusicManager.toggle_loop(message.guild.id)
        await message.channel.send(resp)

    @staticmethod
    async def handle_stop_music(message):
        resp = await MusicManager.stop_music(message.guild.id)
        await message.channel.send(resp)

    @staticmethod
    async def handle_skip(message):
        resp = MusicManager.skip_track(message.guild.id)
        await message.channel.send(resp)

    @staticmethod
    async def handle_pobudka_sequence(message):
        user_id = str(message.author.id)
        on_cd, remaining = CooldownManager.is_on_cooldown(user_id, "pobudka")
        if on_cd:
            mins, secs = CooldownManager.format_time(remaining)
            await message.channel.send(f"⏱️ Czekaj {mins}m {secs}s")
            return
        
        numbers = re.findall(r'\d+', message.content)
        if not numbers:
            await message.channel.send("❌ Składnia: `pobudka <ID>`")
            return
            
        target_id = int(numbers[0])
        target_member = message.guild.get_member(target_id)
        
        if not target_member:
            await message.channel.send("❌ Brak usera")
            return
        if not target_member.voice:
            await message.channel.send("❌ User nie jest na kanale")
            return

        CooldownManager.update_cooldown(user_id, "pobudka")
        
        await message.channel.send(f"🔊 POBUDKA! {target_member.mention}")
        await wykonaj_pobudke(message.guild, target_member)

    @staticmethod
    async def handle_muzyka_exact(message):
        if not message.author.voice: return
        path = "muzyka.mp3"
        if not os.path.exists(path): return
        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass
        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options=f"-vn -af volume={DEFAULT_MUZYKA_VOLUME}"))
            while vc.is_playing(): await asyncio.sleep(1)
            await vc.disconnect()
        except: pass

    @staticmethod
    async def handle_verstappen(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_on_cooldown(user_id, "verstappen")
        if on_cd: return
        CooldownManager.update_cooldown(user_id, "verstappen")

        if not message.author.voice: return
        path = "max.mp3"
        if not os.path.exists(path): return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass
        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options=f"-vn -af volume={DEFAULT_MAX_VOLUME}"))
            while vc.is_playing(): await asyncio.sleep(1)
            await vc.disconnect()
        except Exception as e: print(f"Błąd max: {e}")

    @staticmethod
    async def handle_syrena(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_on_cooldown(user_id, "syrena")
        if on_cd: return
        CooldownManager.update_cooldown(user_id, "syrena")

        if not message.author.voice:
             await message.channel.send("❌ Wejdź na kanał głosowy, żeby usłyszeć syrenę.")
             return
             
        path = "syrena.mp3"
        if not os.path.exists(path):
            print("❌ Brak pliku syrena.mp3")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass
        
        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options=f"-vn -af volume=2.0"))
            await message.channel.send("💣 **ZOBACZYMY JAK BOMBA PIERDOLNIE**")
            while vc.is_playing(): await asyncio.sleep(1)
            await vc.disconnect()
        except Exception as e: print(f"Błąd syreny: {e}")

    @staticmethod
    async def handle_crazy(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "Crazy")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "Crazy")

        if not message.author.voice: return

        path = "Crazy.mp3"
        if not os.path.exists(path):
            print(f"❌ Brak pliku: {path} w katalogu bota.")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=1.0"))
            print(f"🤪 Gram Crazy.mp3 dla: {message.author.name}")

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            
        except Exception as e:
            print(f"⚠️ Błąd podczas odtwarzania Crazy: {e}")
            if message.guild.voice_client:
                try: await message.guild.voice_client.disconnect(force=True)
                except: pass

    @staticmethod
    async def handle_wojfer(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "wojfer")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "wojfer")

        if not message.author.voice: return

        path = "wojfer.mp3"
        if not os.path.exists(path):
            print(f"❌ Brak pliku: {path} w katalogu bota.")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=1.0"))
            print(f"🤪 Gram wojfer.mp3 dla: {message.author.name}")

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            
        except Exception as e:
            print(f"⚠️ Błąd podczas odtwarzania krzyki: {e}")
            if message.guild.voice_client:
                try: await message.guild.voice_client.disconnect(force=True)
                except: pass



    @staticmethod
    async def handle_spermaman(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "spermaman")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "spermaman")

        if not message.author.voice: return

        path = "SpermaMan.mp3"
        if not os.path.exists(path):
            print(f"❌ Brak pliku: {path} w katalogu bota.")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=1.0"))
            print(f"🤪 Gram SpermaMan.mp3 dla: {message.author.name}")

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            
        except Exception as e:
            print(f"⚠️ Błąd podczas odtwarzania krzyki: {e}")
            if message.guild.voice_client:
                try: await message.guild.voice_client.disconnect(force=True)
                except: pass            

    @staticmethod
    async def handle_tatus(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "tatus")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "tatus")

        if not message.author.voice: return

        path = "tatus.mp3"
        if not os.path.exists(path):
            print(f"❌ Brak pliku: {path} w katalogu bota.")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=2.0"))
            print(f"🤪 Gram tatus.mp3 dla: {message.author.name}")

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            
        except Exception as e:
            print(f"⚠️ Błąd podczas odtwarzania krzyki: {e}")
            if message.guild.voice_client:
                try: await message.guild.voice_client.disconnect(force=True)
                except: pass            
    @staticmethod
    async def handle_kuba_femboy(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "kuba_femboy")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "kuba_femboy")
        if not message.author.voice: return

        path = "kuba_femboy.mp3"
        if not os.path.exists(path):
            print(f"❌ Brak pliku: {path} w katalogu bota.")
            return

        if message.guild.voice_client:
            try: await message.guild.voice_client.disconnect(force=True)
            except: pass

        try:
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=2.0"))
            print(f"🤪 Gram kuba_femboy.mp3 dla: {message.author.name}")

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            
        except Exception as e:
            print(f"⚠️ Błąd podczas odtwarzania krzyki: {e}")
            if message.guild.voice_client:
                try: await message.guild.voice_client.disconnect(force=True)
                except: pass            

    @staticmethod
    async def handle_gejtos(message):
        user_id = str(message.author.id)
        on_cd, _ = CooldownManager.is_custom_trigger_on_cooldown(user_id, "gejtos")
        if on_cd: return
        CooldownManager.update_custom_trigger_cooldown(user_id, "gejtos")

        url = "https://soundcloud.com/erdo-626977992/gejtos-antyczny-napaleniec?si=85df33291d6d4bd29e087eda86165738&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"
        resp, success = await MusicManager.add_and_play(message, url)
        if success:
            await message.channel.send("🇬🇷 " + resp)
        else:
            await message.channel.send(resp)

    @staticmethod
    async def handle_dm_command(message):
        if not message.author.guild_permissions.administrator: return
        
        try:
            match = re.search(r'!dm\s*[\[\(]?([0-9,\s]+)[\]\)]?\s+(.+)', message.content, re.DOTALL)
            
            if not match:
                await message.channel.send("❌ Użycie: `!dm (id1, id2) treść [ilość]`")
                return

            raw_ids_group = match.group(1)
            rest_of_message = match.group(2).strip()

            target_ids = []
            for item in raw_ids_group.split(','):
                clean_id = "".join(filter(str.isdigit, item))
                if clean_id:
                    target_ids.append(int(clean_id))
            
            if not target_ids:
                await message.channel.send("❌ Nie wykryto żadnych poprawnych ID.")
                return

            parts = rest_of_message.split()
            count = 1
            content = rest_of_message

            if len(parts) > 1 and parts[-1].isdigit():
                count = int(parts[-1])
                content = rest_of_message.rsplit(' ', 1)[0]
            
            if count > MAX_DM_REPEAT: count = MAX_DM_REPEAT

            await message.channel.send(f"📬 Wysyłam do {len(target_ids)} osób ({count}x)...")

            for uid in target_ids:
                user_obj = None
                try:
                    user_obj = await client.fetch_user(uid)
                except discord.NotFound:
                    await message.channel.send(f"⚠️ ID {uid}: Nie znaleziono użytkownika.")
                    continue
                except Exception:
                    continue

                try:
                    for _ in range(count):
                        await user_obj.send(content)
                        if count > 1: await asyncio.sleep(0.7)
                except discord.Forbidden:
                    await message.channel.send(f"❌ {user_obj.name}: Zablokowane DM.")
                except Exception as e:
                    print(f"Błąd DM {uid}: {e}")

            await message.channel.send("✅ Zakończono.")
        except Exception as e:
            await message.channel.send(f"❌ Błąd krytyczny: {e}")

    @staticmethod
    async def handle_role_substitution(message):
        content = message.content
        role_map = {
            "ROLE_TATUS": ROLE_TATUS, "ROLE_CORKA": ROLE_CORKA, "ROLE_PARA": ROLE_PARA,
            "ROLE_ADMIN": ROLE_ADMIN, "ROLE_MODERATOR": ROLE_MODERATOR
        }
        
        new_content = content
        replaced = False
        
        for kw, rid in role_map.items():
            if kw in new_content:
                new_content = new_content.replace(kw, f"<@&{rid}>")
                replaced = True
                
        if replaced:
            return False 
        return False

    @staticmethod
    async def handle_custom_text_triggers(message):

        def normalize(text):
            replacements = {
                'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
                'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
            }
            for pl, latin in replacements.items():
                text = text.replace(pl, latin)
            return text

        raw_content = message.content
        lower_content = message.content.lower()
        user_id = str(message.author.id)

        processed_content = lower_content
        if message.mentions:
            for mention in message.mentions:
                user_string = f"@{mention.name.lower()}"
                processed_content = processed_content.replace(f"<@{mention.id}>", user_string).replace(f"<@!{mention.id}>", user_string)
        if message.role_mentions:
            for role in message.role_mentions:
                role_string = f"@{role.name.lower()}"
                processed_content = processed_content.replace(f"<@&{role.id}>", role_string)
        processed_content = re.sub(r'https?://\S+', '', processed_content)
        normalized_content = normalize(processed_content)
        
        role_id_mapping = {
            "{ROLE_TATUS}": ROLE_TATUS, "{ROLE_CORKA}": ROLE_CORKA, "{ROLE_PARA}": ROLE_PARA,
            "{ROLE_WLASCICIEL}": ROLE_WLASCICIEL, "{ROLE_ADMIN}": ROLE_ADMIN, "{ROLE_MODERATOR}": ROLE_MODERATOR,
            "{ROLE_CHLOPAK}": ROLE_CHLOPAK, "{ROLE_DZIEWCZYNA}": ROLE_DZIEWCZYNA, "{ROLE_ZNAJOMY}": ROLE_ZNAJOMY,
            "{ROLE_CZLONEK}": ROLE_CZLONEK, "{ROLE_18_PLUS}": ROLE_18_PLUS, "{ROLE_WIEK_17_18}": ROLE_WIEK_17_18,
            "{ROLE_WIEK_15_16}": ROLE_WIEK_15_16, "{ROLE_WIEK_13_14}": ROLE_WIEK_13_14
        }
        role_text_mapping = {
            "{ROLE_TATUS}": "tatus", "{ROLE_CORKA}": "curka", "{ROLE_PARA}": "para",
            "{ROLE_WLASCICIEL}": "właściciel", "{ROLE_ADMIN}": "admin", "{ROLE_MODERATOR}": "moderator",
            "{ROLE_CHLOPAK}": "chłopak", "{ROLE_DZIEWCZYNA}": "dziewczyna"
        }

        for key, value in CUSTOM_TEXT_TRIGGERS.items():
            trigger_found = False
            cooldown_key = str(key)
            triggers_list = key if isinstance(key, tuple) else [key]

            for trigger in triggers_list:
                trigger_with_ids = trigger
                replaced_ids = False
                for placeholder, role_id in role_id_mapping.items():
                    if placeholder in trigger_with_ids:
                        trigger_with_ids = trigger_with_ids.replace(placeholder, f"<@&{role_id}>")
                        replaced_ids = True
                
                if replaced_ids and trigger_with_ids in raw_content:
                    trigger_found = True
                    break

                trigger_text = trigger.lower()
                for ph, txt in role_text_mapping.items():
                    trigger_text = trigger_text.replace(ph.lower(), txt)
                trigger_normalized = normalize(trigger_text)

                if (trigger_text in lower_content or 
                    trigger_text in processed_content or 
                    trigger_normalized in normalized_content):
                    trigger_found = True
                    break

            if not trigger_found:
                continue

            if isinstance(value, dict):
                if value.get("admin_only") and not message.author.guild_permissions.administrator:
                    continue

            actions = []
            if isinstance(value, dict):
                raw_action = value.get("action")
                if isinstance(raw_action, list): actions = raw_action
                elif raw_action: actions = [raw_action]

            special_actions = [
                "pobudka_sequence", "play_muzyka_exact", "play_verstappen", "play_gejtos", 
                "play_syrena", "play_za_gorami_za_lasami", "wycisz_eryk", "random_kick_voice", 
                "play_crazy", "play_wojfer", "check_67_trigger","play_spermaman","play_tatus","play_kuba_femboy"
            ]
            
            # SPECJALNA OBSŁUGA DLA 67
            if "check_67_trigger" in actions:
                result = await CommandHandler.handle_check_67_trigger(message)
                if result:
                    return True
                else:
                    continue
            
            if not any(act in special_actions for act in actions):
                custom_time = None
                if isinstance(value, dict): custom_time = value.get("cooldown")
                on_cd, remaining = CooldownManager.is_custom_trigger_on_cooldown(user_id, cooldown_key, custom_time)
                if on_cd:
                    mins, secs = CooldownManager.format_time(remaining)
                    await message.channel.send(f"⏱️ Czekaj {mins}m {secs}s")
                    return True
                CooldownManager.update_custom_trigger_cooldown(user_id, cooldown_key)

            if isinstance(value, dict) and "ping_members_of_role" in actions and "role_ids" in value:
                loop_count = 1
                for act in actions:
                    if isinstance(act, str) and act.startswith("ilosc_w"):
                        match = re.search(r'ilosc_w\((.*?)\)', act)
                        if match:
                            try:
                                inner = match.group(1).strip()
                                if inner.startswith('[') and inner.endswith(']'):
                                    nums = [int(n.strip()) for n in inner[1:-1].split(',') if n.strip().isdigit()]
                                    if nums: loop_count = random.choice(nums)
                                else: loop_count = int(inner)
                            except: pass
                if loop_count > 100: loop_count = 100
                
                role_ids = value["role_ids"]
                if not isinstance(role_ids, list): role_ids = [role_ids]
                all_mentions = []
                for rid in role_ids:
                    role = message.guild.get_role(int(rid))
                    if role:
                        role_mentions = [m.mention for m in role.members if not m.bot]
                        if role_mentions: all_mentions.append(" ".join(role_mentions))
                
                if all_mentions:
                    separator = f" {value.get('text', '')} " if "text" in value else " "
                    response_text = separator.join(all_mentions)
                    for _ in range(loop_count):
                        await message.channel.send(response_text)
                        if loop_count > 1: await asyncio.sleep(0.8)
                return True

            if isinstance(value, dict):
                if "random_kick_voice" in actions:
                    on_cd, remaining = CooldownManager.is_custom_trigger_on_cooldown(user_id, cooldown_key, value.get("cooldown", 60))
                    if on_cd:
                        mins, secs = CooldownManager.format_time(remaining)
                        await message.channel.send(f"⏱️ Klątwa ładuje się... ({mins}m {secs}s)")
                        return True
                    CooldownManager.update_custom_trigger_cooldown(user_id, cooldown_key)

                    TARGET_CHANNEL_NAMES = [
                        NAZWA_KANALU_SPONTU, NAZWA_KANALU_PIWNICA, NAZWA_KANALU_POBUDKA,
                        NAZWA_KANALU_BEZ_LIMITU, NAZWA_KANALU_RIVALS, NAZWA_KANALU_KACIK_GOONERKI,
                        NAZWA_KANALU_DUO1, NAZWA_KANALU_DUO2, NAZWA_KANALU_TEAM2, NAZWA_KANALU_TEAM1
                    ]
                    
                    potential_victims = []
                    for ch_name in TARGET_CHANNEL_NAMES:
                        channel = discord.utils.find(lambda c: ch_name.lower() in c.name.lower(), message.guild.voice_channels)
                        if channel:
                            for member in channel.members:
                                if not member.bot:
                                    potential_victims.append(member)
                    
                    if potential_victims:
                        victim = random.choice(potential_victims)
                        try:
                            await victim.move_to(None)
                            await message.channel.send(f"🧙‍♂️ **Klątwa Kastiego** dosięgła {victim.mention}! Wypierdalaj z VC. 💀")
                        except discord.Forbidden:
                            await message.channel.send("❌ Bot nie ma uprawnień do wyrzucania ludzi (Move Members).")
                        except Exception as e:
                            await message.channel.send(f"❌ Coś poszło nie tak: {e}")
                    else:
                        await message.channel.send("❌ Nikogo nie ma na przeklętych kanałach. Duchy śpią. 👻")
                    return True

                if "play_za_gorami_za_lasami" in actions:
                    await CommandHandler.handle_za_gorami_za_lasami(message)
                    return True
                if "pobudka_sequence" in actions:
                    await CommandHandler.handle_pobudka_sequence(message)
                    return True
                if "play_muzyka_exact" in actions:
                    await CommandHandler.handle_muzyka_exact(message)
                    return True
                if "play_verstappen" in actions:
                    await CommandHandler.handle_verstappen(message)
                    return True
                if "play_gejtos" in actions:
                    await CommandHandler.handle_gejtos(message)
                    return True
                if "play_syrena" in actions:
                    await CommandHandler.handle_syrena(message)
                    return True
                if "play_crazy" in actions:
                    await CommandHandler.handle_crazy(message)
                    return True
                if "play_wojfer" in actions:
                    await CommandHandler.handle_wojfer(message)
                    return True
                if "play_spermaman" in actions:
                    await CommandHandler.handle_spermaman(message)
                    return True
                if "play_tatus" in actions:
                    await CommandHandler.handle_tatus(message)
                    return True
                if "play_kuba_femboy" in actions:
                    await CommandHandler.handle_kuba_femboy(message)
                    return True
                
                if "wycisz_eryk" in actions:
                    if message.author.id == 924312924942643260:
                        await message.channel.send("Nie masz tu władzy.")
                        return True
                    on_cd, rem = CooldownManager.is_on_cooldown(user_id, "eryk")
                    if on_cd:
                        await message.channel.send(f"⏱️ Eryk musi odpocząć ({int(rem)}s)")
                        return True
                    CooldownManager.update_cooldown(user_id, "eryk")
                    target_id = value.get("user")
                    target_member = message.guild.get_member(target_id)
                    if target_member and target_member.voice:
                        try:
                            await target_member.edit(mute=True)
                            await target_member.move_to(None)
                            await message.channel.send(f"🔇 <@{target_id}> uciszony i wyrzucony.")
                            async def unmute_later(mem, delay):
                                await asyncio.sleep(delay)
                                try: await mem.edit(mute=False)
                                except: pass
                            asyncio.create_task(unmute_later(target_member, CZAS_WYCISZENIA_JAXER))
                        except: await message.channel.send("❌ Brak uprawnień.")
                    return True
    
                if "disconnect_from_voice" in actions:
                    try:
                        # Pobierz listę użytkowników do rozłączenia
                        disconnect_users = value.get("disconnect_user", [])
                        if not isinstance(disconnect_users, list):
                            disconnect_users = [disconnect_users]
                        
                        # Przejdź przez wszystkich użytkowników na liście
                        disconnected_count = 0
                        disconnected_names = []
                        
                        for target_id in disconnect_users:
                            target_member = message.guild.get_member(int(target_id))
                            
                            if target_member:
                                if target_member.voice and target_member.voice.channel:
                                    try:
                                        # Rozłącz użytkownika z kanału głosowego
                                        await target_member.move_to(None)
                                        disconnected_count += 1
                                        disconnected_names.append(target_member.mention)
                                        
                                    except discord.Forbidden:
                                        await message.channel.send(f"❌ Bot nie ma uprawnień do rozłączania {target_member.mention}.")
                                    except Exception as e:
                                        await message.channel.send(f"❌ Błąd podczas rozłączania {target_member.mention}: {e}")
                                else:
                                    await message.channel.send(f"❌ {target_member.mention} nie jest na żadnym kanale głosowym.")
                            else:
                                await message.channel.send(f"❌ Nie znaleziono użytkownika o ID {target_id} na serwerze.")
                        
                        # Wyślij podsumowanie jeśli kogoś rozłączono
                        if disconnected_count > 0:
                            disconnect_text = value.get("text", "Użytkownicy zostali wyrzuceni z kanałów.")
                            # Dodaj wzmianki o rozłączonych osobach
                            if disconnected_names:
                                disconnect_text = f"{disconnect_text} {', '.join(disconnected_names)}"
                            await message.channel.send(disconnect_text)
                        else:
                            # Jeśli nikogo nie rozłączono, wyślij informację
                            await message.channel.send("❌ Nikogo z listy nie udało się rozłączyć (nikt nie był na VC lub błąd uprawnień).")
                            
                    except Exception as e:
                        print(f"❌ Błąd w akcji disconnect_from_voice: {e}")
                        await message.channel.send(f"❌ Wystąpił błąd: {e}")
                    
                    return True

                if "timeout_member" in actions and "timeout_user" in value:
                    try:
                        raw_ud = value["timeout_user"]
                        t_id = random.choice(raw_ud) if isinstance(raw_ud, list) else raw_ud
                        t_time = value.get("timeout_duration", 60)
                        t_mem = message.guild.get_member(int(t_id))
                        
                        if t_mem:
                            success_timeout = False
                            try:
                                await t_mem.timeout(timedelta(seconds=t_time))
                                success_timeout = True
                                if "text" in value: 
                                    await message.channel.send(f"{value['text']} {t_mem.mention}")
                                else: 
                                    await message.channel.send(f"🤐 {t_mem.mention} poleciał na timeout ({t_time}s).")
                            except discord.Forbidden:
                                print(f"⚠️ Nie mam uprawnień do timeoutowania {t_mem.name} (za wysoka rola?).")
                            except Exception as e:
                                print(f"⚠️ Błąd timeout: {e}")

                            if not success_timeout and t_mem.voice:
                                await message.channel.send(f"🛡️ {t_mem.mention} ma immunitet na timeout, ale leci **KICK Z VC**!")
                                try:
                                    await t_mem.edit(mute=True)
                                    await t_mem.move_to(None)
                                    
                                    async def unmutef(m, d):
                                        await asyncio.sleep(d)
                                        try: await m.edit(mute=False)
                                        except: pass
                                    
                                    asyncio.create_task(unmutef(t_mem, t_time))
                                except Exception as e:
                                    print(f"❌ Nie udało się nawet wyrzucić z VC: {e}")
                        else:
                            print(f"⚠️ Nie znaleziono użytkownika o ID {t_id}")
                    except Exception as fatal_e: 
                        print(f"❌ Krytyczny błąd w logice timeout: {fatal_e}")
                    
                    return True

                if any("dm" in str(act) for act in actions) and "dm_user" in value and "losuj_dm" not in actions: 
                    try:
                        t = await client.fetch_user(value["dm_user"])
                        msg_c = random.choice(value["dm"]) if isinstance(value["dm"], list) else value["dm"]
                        await t.send(msg_c)
                    except: pass
                    if "reply" in value and value["reply"] == "n": return True

                loop_count = 1
                for act in actions:
                    if isinstance(act, str) and act.startswith("ilosc_w"):
                        match = re.search(r'ilosc_w\((.*?)\)', act)
                        if match:
                            try:
                                inner = match.group(1).strip()
                                if inner.startswith('[') and inner.endswith(']'):
                                    nums = [int(n.strip()) for n in inner[1:-1].split(',') if n.strip().isdigit()]
                                    if nums: loop_count = random.choice(nums)
                                else: loop_count = int(inner)
                            except: pass
                if loop_count > 100: loop_count = 100
                
                target_dm_user = None
                if "losuj_dm" in actions and "dm_users" in value:
                    try:
                        w_id = random.choice(value["dm_users"])
                        target_dm_user = await client.fetch_user(int(w_id))
                    except: pass

                final_dm_txt = "Pozdro"
                if "dm_text" in value:
                    final_dm_txt = random.choice(value["dm_text"]) if isinstance(value["dm_text"], list) else value["dm_text"]

                should_send_channel = "text" in value and value["text"]
                final_channel_txt = ""
                if should_send_channel:
                    final_channel_txt = random.choice(value["text"]) if isinstance(value["text"], list) else value["text"]

                for _ in range(loop_count):
                    if should_send_channel:
                        msg_s = final_channel_txt
                        if "random_ping" in actions and "ids" in value:
                            try:
                                w_k = random.choice(value["ids"])
                                msg_s += f" <@{w_k}>"
                            except: pass
                        await message.channel.send(msg_s)
                    if target_dm_user:
                        try: await target_dm_user.send(final_dm_txt)
                        except: pass
                    if loop_count > 1: await asyncio.sleep(0.8)
                return True

            elif isinstance(value, list):
                await message.channel.send(random.choice(value).replace("{author}", message.author.mention))
                return True
            else:
                await message.channel.send(str(value).replace("{author}", message.author.mention))
                return True

        return False
    
    @staticmethod
    async def handle_triggered_responses(message):
        user_ids = re.findall(r"<@!?(\d+)>", message.content)
        if len(user_ids) == 1 and message.content.strip() == f"<@{user_ids[0]}>":
            uid = user_ids[0]
            if uid in TRIGGERS:
                await message.channel.send(TRIGGERS[uid])
                return True
        return False

    @staticmethod
    async def handle_oznacz(message):
        if not message.mentions: return
        user_id = str(message.author.id)
        ctype = "oznacz_admin" if message.author.guild_permissions.administrator else "oznacz_user"
        if CooldownManager.is_on_cooldown(user_id, ctype)[0]: return
        CooldownManager.update_cooldown(user_id, ctype)
        cnt = 5
        try: cnt = int(message.content.split()[2])
        except: pass
        for i in range(min(cnt, MAX_OZNACZEN_ADMIN if "admin" in ctype else MAX_OZNACZEN_USER)):
            await message.channel.send(f"{message.mentions[0].mention} {i+1}")
            await asyncio.sleep(0.5)

    @staticmethod
    async def handle_los(message):
        user_id = str(message.author.id)
        if CooldownManager.is_on_cooldown(user_id, "los")[0]: return
        CooldownManager.update_cooldown(user_id, "los")
        mems = [m for m in message.guild.members if not m.bot]
        if mems: await message.channel.send(f"🎰 {random.choice(mems).mention}")

    @staticmethod
    async def handle_przenies(message):
        user_id = str(message.author.id)
        if CooldownManager.is_on_cooldown(user_id, "przenies")[0]: return
        if not message.author.voice: return
        CooldownManager.update_cooldown(user_id, "przenies")
        res, _ = await ChannelManager.przenies_uzytkownika(message.author)
        if res: await message.channel.send("✅ Przeniesiono")

    @staticmethod
    async def handle_przenies_innego(message):
        if not message.author.guild_permissions.move_members: return
        if not message.mentions: return
        res, _ = await ChannelManager.przenies_uzytkownika(message.mentions[0])
        if res: await message.channel.send(f"✅ Przeniesiono {message.mentions[0].mention}")

    @staticmethod
    async def handle_szponcik(message):
        if not message.author.guild_permissions.administrator: return
        user_id = str(message.author.id)
        if CooldownManager.is_on_cooldown(user_id, "szponcik")[0]: return
        CooldownManager.update_cooldown(user_id, "szponcik")
        res, n, _ = await ChannelManager.szponcik_przenies_wszystkich(message.guild)
        if res: await message.channel.send(f"✅ Szponcik: {n}")

    @staticmethod
    async def handle_automat_piwnica(message):
        global automat_piwnica_users
        if not message.author.guild_permissions.administrator: return
        cnt = message.content.lower()
        if cnt.startswith("!wlacz"):
            if "wszyscy" in cnt:
                automat_piwnica_users = {"wszyscy": True}
                await message.channel.send("✅ Automat włączony dla: **WSZYSCY**")
                return
            targets = message.mentions
            if not targets: targets = [message.author]
            if "wszyscy" in automat_piwnica_users: automat_piwnica_users = {}
            added_names = []
            for member in targets:
                automat_piwnica_users[str(member.id)] = True
                added_names.append(member.display_name)
            await message.channel.send(f"✅ Automat włączony dla: **{', '.join(added_names)}**")
        elif cnt.startswith("!wylacz"):
            if "wszyscy" in cnt or not message.mentions:
                automat_piwnica_users = {}
                await message.channel.send("⛔ Automat całkowicie **WYŁĄCZONY**.")
                return
            removed_names = []
            for member in message.mentions:
                uid = str(member.id)
                if uid in automat_piwnica_users:
                    del automat_piwnica_users[uid]
                    removed_names.append(member.display_name)
            if removed_names: await message.channel.send(f"⛔ Usunięto z automatu: **{', '.join(removed_names)}**")
            else: await message.channel.send("⚠️ Tych osób nie było na liście.")
        
@staticmethod
async def handle_czysc(message):
    """Rozłącza bota z VC i czyści kolejkę muzyki."""
    guild_id = message.guild.id
    
    # Zatrzymaj muzykę i wyczyść kolejkę
    if guild_id in MusicManager.music_queue:
        MusicManager.music_queue[guild_id]['queue'] = []
        MusicManager.music_queue[guild_id]['now_playing'] = None
    
    # Rozłącz bota jeśli jest na VC
    if message.guild.voice_client:
        try:
            vc = message.guild.voice_client
            if vc.is_playing():
                vc.stop()
            await vc.disconnect(force=True)
            await message.channel.send("✅ **Bot opuścił kanał głosowy. Kolejka wyczyszczona.**")
        except Exception as e:
            await message.channel.send(f"❌ Błąd: {e}")
    else:
        await message.channel.send("✅ **Kolejka wyczyszczona.** (Bot nie był na VC)")

# --- ZADANIE 1: 21:37 (BARKA) ---
@tasks.loop(minutes=1)
async def harmonogram_barka():
    now = datetime.now()
    aktualna_godzina = now.strftime("%H:%M")
    if aktualna_godzina == GODZINA_BARKI_BOT:
        for guild in client.guilds:
            target_channel = discord.utils.find(lambda c: NAZWA_KANALU_PIWNICA.lower() in c.name.lower(), guild.voice_channels)
            if target_channel:
                try:
                    if guild.voice_client:
                        try: await guild.voice_client.disconnect(force=True)
                        except: pass
                    vc = await target_channel.connect()
                    path = "barka.mp3"
                    if os.path.exists(path):
                        vc.play(discord.FFmpegPCMAudio(path, options="-vn -af volume=1.0"))
                        while vc.is_playing(): await asyncio.sleep(1)
                        await vc.disconnect()
                    else:
                        print("❌ Nie znaleziono pliku barka.mp3")
                        await vc.disconnect()
                except Exception as e: print(f"Błąd barki: {e}")

# --- ZADANIE 2: SPRAWDZANIE ŚPIOCHÓW (NOWE) ---
@tasks.loop(seconds=30)
async def check_sleeping_users_task():
    now = time.time()
    IMMUNITET_ID = 412962715103920138

    for user_id, start_time in list(spiochy.items()):
        if user_id == IMMUNITET_ID:
            if user_id in spiochy: del spiochy[user_id]
            continue

        duration = now - start_time
        
        if duration > CZAS_DO_POBUDKI:
            found_member = None
            for guild in client.guilds:
                m = guild.get_member(user_id)
                if m and m.voice:
                    found_member = m
                    break
            
            if found_member:
                print(f"⏰ Koniec spania dla {found_member.name}. Czas: {int(duration/60)} min.")
                if user_id in spiochy: del spiochy[user_id]
                asyncio.create_task(wykonaj_pobudke(found_member.guild, found_member))
            else:
                if user_id in spiochy: del spiochy[user_id]

@client.event
async def on_ready():
    print(f"✅ Zalogowano: {client.user}")
    
    if not harmonogram_barka.is_running():
        harmonogram_barka.start()
        
    if not check_sleeping_users_task.is_running():
        check_sleeping_users_task.start()
        print("🕵️ Monitorowanie śpiochów uruchomione.")
    
    print(f"📊 Bot monitoruje {len(OSOBY_MONITOROWANE)} osób w wiadomościach PV.")
    print("📋 Osoby monitorowane:")
    for person_id in OSOBY_MONITOROWANE:
        name = ID_TO_NAME.get(person_id, "Nieznany")
        print(f"  - {name} ({person_id})")

async def rosyjska_ruletka_z_kanalu(message):
    """Pobiera losową wiadomość z kanału cytatów i czyta ją na VC."""
    channel_cytaty = client.get_channel(ID_KANALU_Z_CYTATAMI)
    if not channel_cytaty:
        print(f"❌ Nie znaleziono kanału cytatów o ID: {ID_KANALU_Z_CYTATAMI}")
        return

    # Pobieranie ostatnich 150 wiadomości
    quotes = []
    async for msg in channel_cytaty.history(limit=150):
        if msg.content and not msg.author.bot:
            quotes.append(msg.content)

    if not quotes:
        await message.channel.send("❌ Kanał z cytatami jest pusty.")
        return

    wybrany_cytat = random.choice(quotes)

    # Logika wyboru kanału głosowego (Twoje priorytety)
    target_channel = None
    if message.author.voice:
        target_channel = message.author.voice.channel

    if not target_channel:
        all_vcs = [c for g in client.guilds for c in g.voice_channels]
        active_vcs = [c for c in all_vcs if len([m for m in c.members if not m.bot]) > 0]
        if active_vcs:
            target_channel = max(active_vcs, key=lambda c: len([m for m in c.members if not m.bot]))

    if not target_channel:
        for guild in client.guilds:
            target_channel = discord.utils.get(guild.voice_channels, name=NAZWA_KANALU_PIWNICA)
            if target_channel: break

    if target_channel:
        await message.channel.send(f"🎲 **Rosyjska ruletka!** Wbijam na {target_channel.name}...")
        # Wykorzystujemy Twoją klasę TTSManager
        await TTSManager.speak(target_channel, wybrany_cytat)
    else:
        await message.channel.send("❌ Nawet w piwnicy nikogo nie ma.")

# --- OBSŁUGA WIADOMOŚCI PV ---
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Komenda ruletki działająca na każdym kanale
    if message.content.lower() == "ruletka":
        await rosyjska_ruletka_z_kanalu(message)
        return
    # Najpierw obsłuż wiadomości prywatne
    if isinstance(message.channel, discord.DMChannel):
        await handle_private_message(message)
        return
    
    # Reszta obsługi wiadomości na serwerze
    if message.author.bot: return
    
    # 1. Obsługa komendy !wejdz (zarządzanie lektorem)
    if message.content.lower().startswith("!wejdz"):
        if await TTSManager.handle_lektor_command(message):
            return
    
    # 2. Przetwarzanie TTS dla osób z listy
    await TTSManager.process_tts(message)
    
    # 3. Obsługa podmiany ról na wzmianki (np. ROLE_TATUS)
    if any(role_keyword in message.content for role_keyword in ["ROLE_TATUS", "ROLE_CORKA", "ROLE_ADMIN", "ROLE_MODERATOR", "ROLE_PARA", "ROLE_"]):
        if await CommandHandler.handle_role_substitution(message):
            return

    cnt = message.content.lower()

    # 4. Mini-komendy (Sloty, Szansa, Gej)
    if cnt == "!sloty":
        slots = ['🍒', '🍋', '🍇', '🍉', '💎', '7️⃣']
        a, b, c = random.choice(slots), random.choice(slots), random.choice(slots)
        msg = f"🎰 | {a} | {b} | {c} | 🎰"
        if a == b == c: msg += "\n💰 JACKPOT! WYGRAŁEŚ ŻYCIE!"
        elif a == b or b == c or a == c: msg += "\n💵 Było blisko..."
        else: msg += "\n💩 Przegrałeś, biedaku."
        await message.channel.send(msg)
        return

    if cnt.startswith("!szansa"):
        await message.channel.send(f"🔮 Szansa na to wynosi: **{random.randint(0,100)}%**")
        return

    if cnt.startswith("!gej"):
        proc = random.randint(0, 100)
        user = message.mentions[0].mention if message.mentions else message.author.mention
        msg = f"🏳️‍🌈 **{user}** jest gejem w **{proc}%**."
        if proc > 90: msg += " (Potężny Pedał)"
        elif proc < 10: msg += " (Sigma)"
        await message.channel.send(msg)
        return

    # 5. Główne komendy
    if cnt.startswith("!wlacz") or cnt.startswith("!wylacz"):
        await CommandHandler.handle_automat_piwnica(message)
        return

    if cnt.startswith("!zagraj"):
        await CommandHandler.handle_zagraj(message)
        return
        
    if cnt.startswith("!loop"):
        await CommandHandler.handle_loop(message)
        return
        
    if cnt == "!stop":
        await CommandHandler.handle_stop_music(message)
        return
        
    if cnt == "!skip":
        await CommandHandler.handle_skip(message)
        return

    if cnt == "!czysc" or cnt == "!wyjdz" or cnt == "!clear":
        await CommandHandler.handle_czysc(message)
        return
        
    if cnt.startswith("!oznacz"):
        await CommandHandler.handle_oznacz(message)
        return
        
    if cnt == "!los":
        await CommandHandler.handle_los(message)
        return
        
    if cnt.startswith("!przenies "):
        await CommandHandler.handle_przenies_innego(message)
        return
        
    if cnt == "!szponcik":
        await CommandHandler.handle_szponcik(message)
        return
        
    if cnt.startswith("!obudz"):
        await CommandHandler.handle_obudz(message)
        return

    if cnt.startswith("!pobudka"):
        await CommandHandler.handle_pobudka_sequence(message)
        return
        
    if cnt in ["!spont", "!kącik", "!szpont"]:
        await CommandHandler.handle_przenies(message)
        return
        
    if cnt.startswith("!dm"):
        await CommandHandler.handle_dm_command(message)
        return

    # 6. Triggery i reakcje (ostatnia deska ratunku)
    if await CommandHandler.handle_triggered_responses(message): return
    if await CommandHandler.handle_custom_text_triggers(message): return
    if await CommandHandler.handle_colon_trigger(message): return

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot: return
    user_id = member.id
    IMMUNITET_ID = int(KISMET_ID)

    # 1. LOGIKA ŚPIOCHA
    if not after.channel:
        if user_id in spiochy: del spiochy[user_id]
    else:
        spi_poprawnie = after.self_mute and not after.self_deaf
        
        if spi_poprawnie:
            if user_id == IMMUNITET_ID:
                pass 
            elif user_id not in spiochy:
                spiochy[user_id] = time.time()
                print(f"💤 {member.name} zasypia (MUTE: ON, SŁUCHAWKI: ON). Start licznika.")
        else:
            if user_id in spiochy:
                del spiochy[user_id]
                status = "włączył mikrofon" if not after.self_mute else "wyłączył słuchawki"
                print(f"👀 {member.name} reset licznika ({status}).")

    # 2. LOGIKA PIWNICY I BEZ LIMITU
    if automat_piwnica_users:
        uid = str(member.id)
        if "wszyscy" in automat_piwnica_users or uid in automat_piwnica_users:
            if after.channel:
                kp = await ChannelManager.znajdz_kanal_piwnica(member.guild)
                kbl = await ChannelManager.znajdz_kanal_po_nazwie(member.guild, NAZWA_KANALU_BEZ_LIMITU)

                zakazane_kanaly_ids = []
                if kp: zakazane_kanaly_ids.append(kp.id)
                if kbl: zakazane_kanaly_ids.append(kbl.id)

                if after.channel.id in zakazane_kanaly_ids:
                    print(f"🚨 Automat: Wyłapano {member.name} na kanale '{after.channel.name}'")
                    await asyncio.sleep(0.5)
                    await ChannelManager.przenies_uzytkownika(member)

# --- URUCHAMIANIE ---
if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    try:
        if TOKEN: client.run(TOKEN)
        else: print("❌ Brak tokenu! Ustaw DISCORD_TOKEN w pliku .env")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
