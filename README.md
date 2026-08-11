# Ishonchli Usta — Ishchi va Ish beruvchi platformasi (Django)

Santexnik, elektrik, suvoqchi va boshqa ustalarni — ularga ish beruvchi mijozlar bilan bog'laydigan,
lokatsiya, reyting va real vaqtga yaqin chat funksiyasiga ega ikki tomonlama platforma.

## Umumiy imkoniyatlar

- **Splash-animatsiya** — saytga birinchi marta kirganda chiroyli animatsion bosh sahifa
- **To'liq ro'yxatdan o'tish** — login, ism, parol, telefon (`+998` bilan boshlanishi **shart**, tekshiriladi)
- Ro'yxatdan o'tishda **rol tanlanadi**: 🛠️ Ishchi (Usta) yoki 🧑‍💼 Ish beruvchi
- Ishchi tanlansa, **kasb kategoriyasi** (santexnik, elektrik, suvoqchi, g'isht teruvchi va h.k. — 20+ tayyor kategoriya) va tajriba yili so'raladi
- Kirgandan keyin **shaxsiylashtirilgan bosh sahifa** — tezkor havolalar, so'nggi e'lonlar/ustalar
- **"🗂️ Kategoriyalar" tugmasi** — navbar'da va bosh sahifada doim ko'rinadi, bosilganda barcha kasb turlari ro'yxati bilan oyna (modal) ochiladi; kategoriyani tanlash to'g'ridan-to'g'ri tegishli ro'yxatga (ish e'lonlari yoki ustalar) olib boradi
- **Qidiruv** — ishchi ish e'lonlarini nomi, tavsifi **yoki kategoriya nomi** bo'yicha qidiradi; ish beruvchi ustalarni ismi **yoki kasbi** bo'yicha qidiradi
- **GPS-lokatsiya** — foydalanuvchi tizimga kirganda brauzer orqali avtomatik lokatsiyasi so'raladi va saqlanadi; ishchiga eng yaqin ish beruvchilar, ish beruvchiga eng yaqin ustalar birinchi bo'lib ko'rsatiladi (masofa km da hisoblanadi)
- **Profilni tahrirlash**: rasm yuklash, ism o'zgartirish, o'zi haqida yozish
- **Hisobni butunlay o'chirish** imkoniyati
- **Kimning profili ekanligi har doim aniq ko'rinadi** — o'z profilingizda yashil banner ("bu sizning profilingiz"), boshqa birovning profilida ko'k banner ("boshqa foydalanuvchi profilini ko'ryapsiz")
- **To'liq mobilga moslashgan** — kichik ekranlarda navbar "hamburger" menyuga aylanadi, barcha kartalar va formalar telefon ekraniga moslashadi
- Zamonaviy, tushunarli va yorqin dizayn (gradient sarlavhalar, soyali kartalar, katta va kichik ekranlarga moslashgan)

## 🛠️ Ishchi (Usta) uchun

- O'z profilida kasbi, tajribasi, reytingi ko'rinadi
- **Ishchi postlari** — bajargan ishlarini **rasm yoki video** (MP4/WebM/MOV, maksimal 50 MB) shaklida joylaydi (ish beruvchi buni ko'radi)
- **"Ish qidirish"** bo'limi — o'z kasbiga mos, unga eng yaqin ish e'lonlarini ko'radi
- Har bir ish beruvchi bilan **chat** orqali bog'lanadi
- Baholarini va sharhlarini o'z profilida ko'radi

## 🧑‍💼 Ish beruvchi uchun

- **"Ustalar"** bo'limi — kategoriya bo'yicha filtrlab, o'ziga eng yaqin ustalarni topadi
- **"Mening e'lonlarim"** — ish e'loni joylaydi, yopadi/o'chiradi
- **"⭐ Reyting"** bo'limi — eng yuqori baholangan ustalar reytingini (leaderboard) ko'radi
- Yollagan ustasini **ishi tugagach baholaydi** (1-5 yulduz + izoh) — bu ustaning umumiy reytingini oshiradi/pasaytiradi
- Har bir usta bilan **chat** orqali bog'lanadi, ustaning profilidagi postlarini ko'radi

## 💬 Chat

- Har bir profilda (ishchi yoki ish beruvchi) pastda **"Chat"** tugmasi bor
- **Matn xabarlar**
- **Stikerlar** (emoji-stikerlar to'plami)
- **GIF** — demo rejimida animatsion-hissiy emoji to'plami sifatida ishlaydi (haqiqiy GIF-lar uchun pastga qarang)
- **Ovozli xabarlar** — brauzer mikrofoni orqali yozib, yuborish mumkin (MediaRecorder API)
- Xabarlar har 3 soniyada avtomatik yangilanadi (polling asosida, real vaqtga yaqin)
- **Endi chat sahifasi ekranga to'liq moslashadi** — kompyuterda ham, telefonda ham (JS orqali dinamik balandlik hisoblanadi)
- Har bir yangi xabar yumshoq animatsiya bilan paydo bo'ladi
- **"📍 Jonli lokatsiya"** tugmasi — suhbat ichida ikkala tomonning joriy joylashuvini bitta xaritada, real vaqtga yaqin (har 8 soniyada) ko'rish

> **Haqiqiy GIF integratsiyasi haqida:** hozirgi versiyada tashqi GIF-provayder (Tenor/Giphy) ulanmagan — ular bepul API kaliti talab qiladi va tashqi tarmoqqa chiqishni talab qiladi. `chat/views.py` dagi `conversation_view` funksiyasidagi `GIFS` ro'yxatini kengaytirib yoki Tenor/Giphy API bilan almashtirib, haqiqiy GIF qidiruvini ulash mumkin.

## 📍 GPS va xarita imkoniyatlari (to'liq)

- **Avtomatik GPS-aniqlash** — kirganda brauzer orqali lokatsiya so'raladi va saqlanadi
- **Doimiy (jonli) kuzatuv** — ilova `watchPosition` orqali lokatsiyani uzluksiz kuzatadi va har 15 soniyada serverga yuboradi, shu orqali ikki tomon bir-birini deyarli real vaqtda ko'radi
- **Interaktiv xarita** — har bir profilida (agar lokatsiya bo'lsa) OpenStreetMap/Leaflet.js orqali xarita ko'rinadi, joylashuv nuqta bilan belgilanadi (bepul, API kalit talab qilmaydi)
- **"🧭 Yo'nalish olish" tugmasi** — bosilganda Google Maps ochilib, u yergacha yo'nalishni ko'rsatadi
- **Qo'lda lokatsiya belgilash** (`/lokatsiya/belgilash/`) — agar GPS ishlamasa yoki foydalanuvchi boshqa joyni ko'rsatmoqchi bo'lsa:
  - Xaritadan istalgan nuqtaga bosib belgilash (marker'ni sudrab ham surish mumkin)
  - **Manzil matni bo'yicha qidirish** — masalan "Chilonzor, Toshkent" deb yozib, OpenStreetMap Nominatim (bepul geokodlash xizmati) orqali avtomatik topish
  - Qayta "📡 GPS orqali aniqlash" tugmasi
- **Radius bo'yicha filtrlash** — Ustalar va Ish e'lonlari sahifalarida "5 / 10 / 20 / 50 km ichida" filtri, faqat shu radius ichidagilarni ko'rsatadi
- **GPS rad etilsa** — pastki burchakda "Qo'lda belgilash" havolasi bilan yumshoq bildirishnoma chiqadi (majburlamaydi, lekin eslatadi)

> **Nominatim (geokodlash) haqida eslatma:** bu — OpenStreetMap loyihasining bepul, ochiq geokodlash xizmati, API kalit talab qilmaydi. Lekin ularning **foydalanish siyosati** past hajmdagi (shaxsiy/kichik loyihalar) so'rovlarni nazarda tutadi — soatiga juda ko'p so'rov yuborilsa, IP vaqtincha bloklanishi mumkin. Katta miqyosdagi/tijorat loyihasi uchun production'da o'z serveringizda Nominatim joylashtirish yoki pullik xizmat (Google Geocoding API, Mapbox) ga o'tish tavsiya etiladi.

> **"Jonli kuzatuv" haqida muhim cheklov:** bu faqat ikkala foydalanuvchi ham brauzerda ilovani ochiq tutgan va lokatsiyaga ruxsat bergan paytda ishlaydi — bu veb-ilovalar uchun tabiiy chegara (fon rejimida GPS kuzatish uchun maxsus mobil ilova — Android/iOS native app — kerak bo'ladi, veb-brauzer orqali bu imkonsiz). Demo/MVP maqsadida bu yondashuv yetarli.

## 🎨 Dizayn

- Barcha tugmalar bosilganda/hover qilinganda yumshoq animatsiya bilan javob beradi (ko'tarilish, soya kuchayishi, bosilganda siqilish effekti)
- Splash-animatsiya — suzib yuruvchi fon shakllari, puls effektli belgi, silliq matn animatsiyalari bilan
- Kartalar va tezkor tugmalar (quick-tile) sichqoncha ustiga borganda ko'tarilib, ikonkasi biroz aylanadigan animatsiyaga ega

## Xavfsizlik

- Parollar Django'ning standart xavfsiz hash tizimi orqali saqlanadi (hech qachon ochiq matnda emas)
- Barcha formalar **CSRF-himoyalangan**
- Telefon raqami serverda ham qattiq tekshiriladi (faqat frontendda emas)
- Fayl yuklash hajmi cheklangan (60 MB, video postlar uchun) — server yuklanishini himoya qiladi
- `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff` kabi asosiy HTTP xavfsizlik sarlavhalari yoqilgan
- Foydalanuvchi faqat **o'z** post/e'lon/xabarlarini o'chira oladi (ownership tekshiruvi barcha view'larda mavjud)
- Production'ga chiqarishda albatta: `DEBUG=False`, yangi `SECRET_KEY`, HTTPS va `ALLOWED_HOSTS` cheklanishi kerak (pastga qarang)

## 🗄️ Ma'lumotlar bazasi — PostgreSQL (tayyor holatda SQLite bilan ishga tushadi)

Loyiha **PostgreSQL** bilan ishlashga to'liq moslangan, lekin sizga qulay bo'lishi uchun `.env` faylida hozircha `USE_SQLITE=True` qilib qo'yilgan — ya'ni **hech narsa sozlamasdan darhol ishga tushadi** (tayyor `db.sqlite3` fayli, admin akkount bilan). PostgreSQL'ga o'tishni xohlaganingizda, quyidagi qadamlarni bajarasiz.

### PostgreSQL o'rnatish (agar hali o'rnatilmagan bo'lsa)

**Windows:** https://www.postgresql.org/download/windows/ dan yuklab o'rnating (o'rnatish jarayonida `postgres` foydalanuvchisi uchun parol so'raladi — shuni **albatta eslab qoling**, keyin `.env`ga aynan shu parolni yozasiz).

**macOS:** `brew install postgresql@16 && brew services start postgresql@16`

**Ubuntu/Linux:** `sudo apt install postgresql postgresql-contrib`

### Baza va foydalanuvchi yaratish

O'rnatgach, terminalda (Windows'da "SQL Shell (psql)" dasturini oching, Enter bosib standart qiymatlarni tanlab, o'rnatishda qo'ygan parolingizni kiriting):

```sql
CREATE DATABASE ishonchliusta_db;
```

### `.env` faylini PostgreSQL'ga o'tkazish

`.env` faylini Notepad (yoki boshqa matn muharriri) bilan oching va quyidagicha o'zgartiring:

```env
USE_SQLITE=False
DB_NAME=ishonchliusta_db
DB_USER=postgres
DB_PASSWORD=postgresql-ornatishda-qoygan-haqiqiy-parolingiz
DB_HOST=localhost
DB_PORT=5432
```

Saqlang, so'ng:
```bash
python manage.py migrate
python manage.py createsuperuser
```

> **Eslatma:** "password authentication failed" xatosi chiqsa — bu deyarli har doim `.env`dagi `DB_PASSWORD` PostgreSQL o'rnatishda haqiqatan qo'ygan parolingiz bilan mos kelmayotganini bildiradi. `.env` faylidagi parolni tekshirib, to'g'rilang.

## O'rnatish va ishga tushirish

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

# .env faylida DB sozlamalarini tekshiring (yuqoridagi bo'limga qarang)
python manage.py migrate      # PostgreSQL bazasida jadvallarni yaratadi
python manage.py createsuperuser   # agar PostgreSQL'da hali admin akkount bo'lmasa
python manage.py runserver
```

Brauzerda oching: **http://127.0.0.1:8000/**

> Ovozli xabar va lokatsiya funksiyalari brauzerdan mikrofon/joylashuvga ruxsat so'raydi — buning uchun sayt **HTTPS** yoki **localhost** orqali ochilishi kerak (production serverda albatta HTTPS bo'lishi shart, aks holda brauzerlar ruxsat so'ramaydi).

## Tayyor admin akkount

- **Login:** `admin`
- **Parol:** `admin12345`

> Bu akkount **SQLite** fayli (`db.sqlite3`) ichida tayyor holda mavjud (`USE_SQLITE=True` bilan ishlatilganda). Agar PostgreSQL'ga o'tsangiz, `python manage.py createsuperuser` orqali o'zingiz yangi admin yarating (chunki bo'sh PostgreSQL bazasida hali hech qanday foydalanuvchi yo'q).

Admin panelga standart Django admin orqali kiring: `/admin/`. U yerdan kasb kategoriyalarini boshqarish, foydalanuvchilarni ko'rish/tahrirlash, e'lonlar va baholarni moderatsiya qilish mumkin.

## 📱 REST API (mobil ilova uchun)

Sayt (HTML sahifalar) avvalgidek to'liq ishlaydi — bu API ularning **ustiga qo'shildi**, kelajakda Android/iOS mobil ilova yozish uchun. Autentifikatsiya — **JWT token** asosida (mobil ilovalar uchun standart yondashuv).

**Bazaviy manzil:** `/api/v1/`

### Autentifikatsiya oqimi

1. **Ro'yxatdan o'tish:** `POST /api/v1/auth/register/` — javobida `access` va `refresh` tokenlar qaytadi
2. **Kirish:** `POST /api/v1/auth/login/` — `{"username": "...", "password": "..."}` — javobida token va foydalanuvchi ma'lumoti
3. **Har bir keyingi so'rovda** sarlavhaga qo'shiladi: `Authorization: Bearer <access_token>`
4. `access` token 1 kunda eskiradi — `POST /api/v1/auth/refresh/` orqali `{"refresh": "..."}` yuborib, yangi `access` olinadi (30 kungacha amal qiladi)

### Asosiy endpointlar

| Metod | Manzil | Vazifasi |
|---|---|---|
| POST | `/api/v1/auth/register/` | Ro'yxatdan o'tish |
| POST | `/api/v1/auth/login/` | Kirish (JWT olish) |
| POST | `/api/v1/auth/refresh/` | Tokenni yangilash |
| GET/PATCH/DELETE | `/api/v1/accounts/me/` | O'z profili |
| GET | `/api/v1/accounts/<id>/` | Boshqa profil |
| POST | `/api/v1/accounts/location/` | Lokatsiyani yangilash |
| GET | `/api/v1/categories/` | Kasb kategoriyalari |
| GET | `/api/v1/workers/?q=&category=&radius=` | Ustalar (qidiruv/filtr) |
| GET/POST | `/api/v1/workers/posts/`, `/api/v1/workers/<id>/posts/` | Portfolio postlari |
| GET | `/api/v1/jobs/?q=&category=&radius=` | Ish e'lonlari |
| POST | `/api/v1/jobs/yarat/` | Yangi e'lon |
| GET | `/api/v1/jobs/mening-elonlarim/` | O'z e'lonlari |
| PATCH/DELETE | `/api/v1/jobs/<id>/holat/`, `/api/v1/jobs/<id>/` | E'lonni boshqarish |
| POST | `/api/v1/ratings/<worker_id>/` | Baholash |
| GET | `/api/v1/ratings/reyting/` | Reyting (leaderboard) |
| GET | `/api/v1/chat/conversations/` | Suhbatlar ro'yxati |
| POST | `/api/v1/chat/boshlash/<user_id>/` | Suhbat boshlash |
| GET/POST | `/api/v1/chat/conversations/<id>/messages/` | Xabarlar (`?after=<id>` — polling) |
| GET | `/api/v1/chat/conversations/<id>/jonli-lokatsiya/` | Jonli lokatsiya |

Barcha endpointlar **haqiqiy PostgreSQL bazasi va JWT autentifikatsiya bilan sinovdan o'tkazilgan** (ro'yxatdan o'tish, login, qidiruv, ish e'loni, baholash, chat, post — barchasi ishlaydi).

## 💰 "Tezkor xizmat" va Payme to'lovlari

Platformada haqiqiy pul ishlashi uchun birinchi daromad manbai qo'shildi: **"Tezkor xizmat"** — 26,000 so'm (~$2) evaziga 24 soatga ro'yxat boshiga chiqarish.

- **🛠️ Ishchi uchun — "⚡ Tezkor ish topish"**: profilini 24 soatga ustalar ro'yxatining eng yuqorisiga chiqaradi (bosh sahifada tugma)
- **🧑‍💼 Ish beruvchi uchun — "⚡ Tezkor buyurtma"**: bitta ish e'lonini 24 soatga ish e'lonlari ro'yxatining eng yuqorisiga chiqaradi ("Mening e'lonlarim" sahifasida har bir e'lon yonida tugma)
- Boost faol bo'lgan profil/e'lon ro'yxatlarda **⚡ sariq belgi va ramka** bilan alohida ajratiladi

### To'lov — Payme orqali (haqiqiy pul)

To'lov **Payme Merchant API** (rasmiy JSON-RPC protokoli) orqali to'liq amalga oshirilgan va **sinovdan o'tkazilgan** — ro'yxatdan o'tish, buyurtma yaratish, tranzaksiya yaratish/amalga oshirish/bekor qilish, idempotentlik va noto'g'ri autentifikatsiyani rad etish — barchasi Payme'ning rasmiy oqimiga muvofiq ishlaydi (`payments/payme_api.py`).

**Buni ishga tushirish uchun sizga kerak:**

1. **https://business.payme.uz** saytida biznes sifatida ro'yxatdan o'ting (YaTT yoki yuridik shaxs va bank hisobingiz bo'lishi kerak)
2. Ular sizga **Merchant ID** va **Kalit (Key)** beradi
3. `.env` faylida:
   ```env
   PAYME_MERCHANT_ID=sizning-merchant-id
   PAYME_MERCHANT_KEY=sizning-maxfiy-kalit
   PAYME_TEST_MODE=False
   ```
4. Payme'ning boshqaruv panelida **webhook manzilini** ko'rsating: `https://sizning-domeningiz.uz/payme/webhook/`

> ⚠️ **Muhim texnik talab:** Payme serveri sizning `/payme/webhook/` manzilingizga **ochiq internetdan, HTTPS orqali** murojaat qiladi. `localhost` yoki kompyuteringizda ishlab turgan sayt bilan bu **ishlamaydi** — saytingiz haqiqiy domenga ega bo'lgan serverga joylashtirilgan bo'lishi kerak (masalan VPS: Beget, TimeWeb, yoki DigitalOcean/AWS kabi xizmatlar + SSL sertifikat).

> ⚠️ **Narx haqida:** `PAYME_BOOST_PRICE_SOM` — bu so'mda ko'rsatiladi (Payme faqat O'zbekiston so'mida ishlaydi, to'g'ridan-to'g'ri dollarda emas). Hozir taxminan $2 ga teng summa (26,000 so'm) qo'yilgan — dollar kursi o'zgarganda `.env` faylida shu raqamni yangilab turing.

**Test qilingan holatlar:** buyurtma yaratish → CheckPerformTransaction → CreateTransaction → PerformTransaction (boost faollashishi, 24 soatlik muddat to'g'ri belgilanishi) → qayta so'rov (idempotentlik) → noto'g'ri autentifikatsiya rad etilishi → CancelTransaction — barchasi Payme test kalitlari bilan simulyatsiya qilinib, to'g'ri ishlashi tasdiqlangan.



```
ishonchliusta/
├── config/          -> asosiy sozlamalar (settings.py, urls.py)
├── core/            -> splash-animatsiya sahifasi
├── accounts/        -> User modeli, ro'yxatdan o'tish, profil, serializers.py/api_views.py
├── workers/         -> Kasb kategoriyalari, ustalar, portfolio postlari + API
├── jobs/            -> Ish e'lonlari + API
├── ratings/          -> Baholash va reyting + API
├── chat/             -> Suhbatlar, xabarlar, jonli lokatsiya + API
├── payments/          -> "Tezkor xizmat" (BoostOrder) va Payme Merchant API integratsiyasi
├── api/               -> Barcha API endpointlarini birlashtiruvchi urls.py (/api/v1/)
├── templates/          -> umumiy base.html (Bootstrap 5 + maxsus dizayn)
├── .env / .env.example  -> maxfiy sozlamalar (SECRET_KEY, DB ma'lumotlari)
└── db.sqlite3            -> zaxira baza (USE_SQLITE=True bo'lganda ishlatiladi)
```

## Muhim manzillar

| Sahifa | URL |
|---|---|
| Splash / bosh sahifa | `/` |
| Ro'yxatdan o'tish | `/royhat/` |
| Kirish | `/kirish/` |
| Foydalanuvchi profili | `/profil/<id>/` |
| Profilni tahrirlash | `/profil/tahrirlash/` |
| Lokatsiyani belgilash (xarita) | `/lokatsiya/belgilash/` |
| Hisobni o'chirish | `/profil/ochirish/` |
| Ustalar ro'yxati (ish beruvchi uchun) | `/ustalar/` |
| Ish e'lonlari (ishchi uchun) | `/ishlar/` |
| E'lon berish (ish beruvchi uchun) | `/ishlar/elon-berish/` |
| Mening e'lonlarim | `/ishlar/mening-elonlarim/` |
| Ustalar reytingi | `/reyting/` |
| Ustani baholash | `/baholash/<worker_id>/` |
| Chat ro'yxati | `/chat/` |
| Django admin | `/admin/` |

## Kengaytirish g'oyalari (kelajakda qo'shish mumkin)

- Haqiqiy GIF integratsiyasi (Tenor/Giphy API)
- Push-bildirishnomalar (yangi xabar/e'lon kelganda)
- Onlayn to'lov (ish haqi platforma orqali xavfsiz to'lanishi)
- Admin uchun moderatsiya paneli (soxta profillarni bloklash, shikoyatlarni ko'rish)
- WebSocket (Django Channels) orqali chatni to'liq real-vaqtli qilish (hozir 3 soniyalik polling ishlatilgan)

## Eslatma

`DEBUG = True` va `ALLOWED_HOSTS = ['*']` — faqat lokal/test muhiti uchun. Production'ga chiqarishdan oldin `config/settings.py`da `SECRET_KEY`ni yangilang, `DEBUG = False` qiling, `ALLOWED_HOSTS`ni aniq domenlar bilan cheklang va albatta HTTPS sertifikat o'rnating (mikrofon/lokatsiya ruxsatlari uchun ham majburiy).
