# 🤖 Bot README

## Komendy z `!`

### 🎵 Muzyka
| Komenda | Opis |
|--------|------|
| `!zagraj <query/link>` | Odtwarza muzykę z YouTube lub Spotify na VC |
| `!stop` | Zatrzymuje muzykę i rozłącza bota z VC |
| `!skip` | Pomija aktualny utwór |
| `!loop` | Włącza / wyłącza pętlę aktualnego utworu |
| `!czysc` / `!wyjdz` / `!clear` | Rozłącza bota z VC i czyści kolejkę |

### 🚀 Przenoszenie
| Komenda | Opis |
|--------|------|
| `!spont` / `!kącik` / `!szpont` | Przenosi siebie na kanał spontu |
| `!przenies <@user>` | Przenosi wskazanego użytkownika na kanał spontu |
| `!szponcik` | Przenosi **wszystkich** na kanał spontu *(admin)* |

### 🔔 Budzenie
| Komenda | Opis |
|--------|------|
| `!obudz <ID>` | Przenosi użytkownika między kanałami (budzenie manualne) |
| `!pobudka <ID>` | Odtwarza `pobudka.mp3` ofierze na kanale Pobudka |

### 🛠️ Moderacja / Admin
| Komenda | Opis |
|--------|------|
| `!oznacz <@user> [ilość]` | Oznacza użytkownika X razy |
| `!dm (id1, id2) <treść> [ilość]` | Wysyła DM do podanych użytkowników *(admin)* |
| `!wlacz` / `!wlacz wszyscy` | Włącza automat piwnicy *(admin)* |
| `!wylacz` / `!wylacz wszyscy` | Wyłącza automat piwnicy *(admin)* |

### 🗣️ Lektor TTS
| Komenda | Opis |
|--------|------|
| `!wejdz` | Włącza / wyłącza lektora TTS dla Kismeta |
| `!wejdz <@user>` | Włącza / wyłącza lektora TTS dla konkretnej osoby |

### 🎲 Minigry
| Komenda | Opis |
|--------|------|
| `!sloty` | Jednoręki bandyta z emoji |
| `!szansa` | Losuje procent szansy na coś |
| `!gej <@user>` | Losuje % gejowości użytkownika |
| `!los` | Losuje losowego członka serwera |

---

## 🎤 Text triggery

### 🔊 Dźwiękowe (odtwarza mp3 na VC)
| Trigger | Plik |
|--------|------|
| `verstappen` | `max.mp3` |
| `muzyka dla moich uszu` | `muzyka.mp3` |
| `zobaczymy jak bomba pierdolnie` | `syrena.mp3` |
| `za gorami za lasami` | `lasy.mp3` |
| `crazy` | `Crazy.mp3` |
| `silownia` | `wojfer.mp3` |
| `spiderman` | `SpermaMan.mp3` |
| `horda kiedy pavelos` | `tatus.mp3` |
| `kuba femboy` | `kuba_femboy.mp3` |
| `grecki pedal` | Stream z SoundCloud (gejtos) |

### ⚖️ Timeout / Moderacja
| Trigger | Akcja |
|--------|-------|
| `wypierdalaj frajerze` | Timeout Michała (127s) |
| `ochlon rhast` | Timeout Rhaasta (120s) |
| `stop horda` | Timeout Hordy (30s) |
| `spokojnie dawid` | Timeout Dawida (67s) |
| `przegioles pale jaxer` | Timeout Jaxera (90s) |
| `eryk skoncz pierdolic` | Wycisza i wyrzuca Eryka z VC |
| `klatwa kastiego` | Wyrzuca **losową** osobę z VC |

### 📣 Pingi / DM
| Trigger | Akcja |
|--------|-------|
| `lei nie spimy` | DM do Lei |
| `najwiekszy furas` | DM do Kuby |
| `jaxer` | DM do Jaxera: *"WSTAWAJ WSTAWAJ WSTAWAJ"* |
| `dzis jest ta noc` | Losowy ping z listy + GIF |
| `losowanie` | DM do losowej osoby z listy |
| `pobudka` | Sekwencja pobudki |
| `zakochana para` | Pinguje wszystkich z roli Para |
| `tata i curka` | Pinguje Tatusia i Córkę |
| `wakey wakey` | @everyone losową ilość razy *(admin)* |
| `lazienka` | Pinguje Hordę i Kismeta |

### 🖼️ Obrazki / GIFy
| Trigger | Odpowiedź |
|--------|-----------|
| `kismet` | Obrazek Kismeta |
| `erys` | GIF Eryka |
| `olej` | GIF |
| `@kasia` | GIF |
| `67` | GIF (tylko bez samych pingów) |
| `drzewo nds` | Obrazek drzewa |
| `kto jest rudy` | Obrazek + ping Hordy |
| `schizofrenia` | Obrazek + ping Kuby |
| `moneta` | Orzeł lub reszka |
| `sex` | Odpowiedź tekstowa |
| `50%` | Ping autora lub @everyone |
| `graczligi` | Ping Michała |
| `@femboy` | Losowy ping: Eryk / Kuba / Dawid |
| `lei i rhast` / `rill` | GIF |
| `tata hordy` | Ping Pavelosa |
| `dziewczyna pavelosa` | `@katarzyna` / `@kasia` |

### 👤 Ping konkretnego usera
Jeśli wyślesz **samą wzmiankę** jednej z poniższych osób (nic więcej), bot odpowie ich przypisanym obrazkiem / GIFem:

Michał, Łucja, Darek, Horda, Kismet, Dawid, Rhaast, Kuba, Eryk, Pavelos, Lei

---

## 🎙️ Komendy głosowe / PV

| Trigger | Akcja |
|--------|-------|
| `ruletka` | Losuje cytat z kanału cytatów i czyta go TTS na VC |
| Wiadomość PV od monitorowanej osoby | Bot czyta ją TTS na VC (opcjonalnie z `!wyslij` na początku) |

---

## ⚙️ Automatyczne zachowania

| Zachowanie | Opis |
|-----------|------|
| **21:37 codziennie** | Odtwarza `barka.mp3` na kanale PIWNICA |
| **Lektor TTS** | Czyta wiadomości tekstowe osób z listy `OSOBY_DO_CZYTANIA` gdy są na VC |
| **Śpioch** | Jeśli ktoś wejdzie na MUTE (bez deafa) przez 15 minut → automatyczna pobudka |
| **Automat piwnicy** | Jeśli włączony, przenosi wskazanych userów z Piwnicy / Bez limitu na Spont gdy tam wejdą |

---

## 🔊 Pliki dźwiękowe

Bot wymaga następujących plików `.mp3` w katalogu głównym:

```
pobudka.mp3
barka.mp3
muzyka.mp3
max.mp3
syrena.mp3
Crazy.mp3
wojfer.mp3
lasy.mp3
tatus.mp3
kuba_femboy.mp3
SpermaMan.mp3
```

> `tts_output.mp3` jest generowany dynamicznie przez gTTS — nie musisz go dodawać.

---

## 🛠️ Konfiguracja

Plik `.env` (lub zmienna środowiskowa na Pterodactyl):

```env
DISCORD_TOKEN=twój_token_tutaj
```
