import telebot
import os

bot = telebot.TeleBot(os.environ['TELEGRAM_BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.reply_to(message, "Bot aktif!")

bot.infinity_polling()

AKUN_FILE = "poinku.txt"
SUKSES_FILE = "login_sukses.txt"

# Load akun dari file
def load_akun():
    akun = []
    if not os.path.exists(AKUN_FILE):
        return akun
    with open(AKUN_FILE, "r") as f:
        for line in f:
            data = line.strip().split(":")
            if len(data) >= 2:
                akun.append({"no_hp": data[0], "password": data[1]})
    return akun

# Login dan ambil token
def login_poinku(no_hp, password):
    try:
        r = requests.post("https://indomaretpoinku.id/api/sso/login",
                          json={"username": no_hp, "password": password}, timeout=10)
        if r.status_code == 200 and "access_token" in r.text:
            return r.json().get("access_token")
    except:
        pass
    return None

# Ambil info member
def get_info(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get("https://indomaretpoinku.id/api/member", headers=headers)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Selamat datang di TUZD Poinku Bot!\nGunakan /login untuk mulai.")

@bot.message_handler(commands=['login'])
def login_semua(message):
    akun_list = load_akun()
    sukses, gagal = 0, 0
    hasil = []

    for akun in akun_list:
        token = login_poinku(akun['no_hp'], akun['password'])
        if token:
            info = get_info(token)
            if info:
                nama = info.get("nama")
                poin = info.get("poin")
                sukses += 1
                hasil.append(f"[+] {akun['no_hp']} ({nama}) - {poin} poin")
                with open(SUKSES_FILE, "a") as f:
                    f.write(f"{akun['no_hp']}:{token} - {datetime.now()}\n")
            else:
                gagal += 1
        else:
            gagal += 1

    res = f"[✓] Login selesai.\nBerhasil: {sukses} | Gagal: {gagal}\n\n" + "\n".join(hasil)
    bot.reply_to(message, res)

print("[BOT] TUZD Poinku Bot is running...")
bot.infinity_polling()
