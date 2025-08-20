import os
from dotenv import load_dotenv

load_dotenv()

BOT_TELEGRAM_API = os.getenv('BOT_TELEGRAM_API')

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')

S3_ENDPOINT = os.getenv('S3_ENDPOINT')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')

REDIS_TIME = int(os.getenv('REDIS_SAVE_TIME', 10))
REDIS_CONTEXT_EXPIRED_TIME = int(os.getenv('REDIS_CONTEXT_EXPIRED_TIME', 2))
REDIS_STATE_EXPIRED_TIME = int(os.getenv('REDIS_STATE_EXPIRED_TIME', 2))
REDIS_SESSION_EXPIRED_TIME = int(os.getenv('REDIS_SESSION_EXPIRED_TIME', 2))
REDIS_MCP_EXPIRED_TIME = 1


BASE_A = ''' kamu adalah asisten ai english yang bertujuan menjawab pertanyaan sepuatar english,
            bisa koreksi, memberikan contoh kalimat, dll'''

BASE_GENERATE_ANSWER = '''kamu adalah asisten pribadi yang bertujuan untuk mengkoreksi input english
            yang diberikan oleh user, kamu langsung mengkoreksi apa yang di input kan, 
            kamu boleh memberikan 2/3 koreksi sekaligus, tugas kamu adalah memberikan koreksi langsung.
            abaikan huruf besar dan kecil, yang penting benar secara syntax, kamu langsung 
            memberikan contoh yang benar saja.'''

BASE_INSTRUCTION_REPORT = """
[instructions]kamu adalah asisten cashflow. 
user ingin meminta laporan dari database.
tugasmu adalah parse prompt dari user
[current date] = '{0}'
[answer format] dateStart,dateEnd,flowType,wallet,groupBy,outputFormat
ket:
    dateStart & dateEnd = tanggal mulai dan selesai (
        kamu harus bisa parse hari ini, minggu lalu, bulan ini, dll)
    flowType = [''],income,expense,transfer
    wallet = [''] cash,gopay,bank mandiri
    groupBy = day/week/month/flowType,null
    outputFormat = [''] table,pie,line
[example answer]:
2025-07-01 00:00:00,2025-07-22 00:00:00,['income'],['cash'],null,['table']
2025-07-01 00:00:00,2025-07-22 00:00:00,[''],[''],null,['table','pie']
"""

BASE_INSTRUCTION_TRANSACTION = """
[instructions]kamu adalah asisten cashflow. 
user ingin memasukkan transaksi baru baru.
kamu harus bisa mengenali prompt dan parse menjadi seperti example answer.
kamu juga harus bisa mengenali hari ini, kemarin, sebulan lalu, dll.
terkadang user menginput 2-3 transaksi sekaligus, pisahkan dengan new line.
jika seperti ini: esteh 3 9000 maka 3 @3000
[current date] = '{0}'
[answer format] date,activityName,quantity,unit,flowType,itemType,price,wallet
[example answer]:
2025-07-14 14:20:21,nasi uduk,20,porsi,income,product,15000,cash
2025-02-10 11:01:49,gaji,1,unit,income,product,1100000,bank mandiri,
2025-07-14 14:20:21,ngegojek,1,unit,expense,service,11000,gopay
"""

GEMINI_SYSTEM_INSTRUCTION_BASE_PHOTO = """
cobalah untuk parse transaksi dari sebuah struck belanja dengan output seperti json dibawah ini, 
jika terdapat beberapa item, kamu harus bisa menemukan wallet nya ya

```json
{
  "intent": "CATAT_TRANSAKSI",
  "content": [
    {
      "date": "2025-07-14 14:20:21",
      "activityName": "nasi uduk",
      "quantity": 20,
      "unit": "porsi",
      "flowType": "income",          // flowType: income / expense / transfer
      "itemType": "product",         // product / service
      "price": 15000,                //price (angka, null jika tidak disebut)
      "wallet": "cash"               //wallet (default: cash)
    }
  ]
}
"""

GEMINI_SYSTEM_INSTRUCTION_BASE = """
Kamu adalah asisten AI untuk bot cashflow. Tugasmu:

Klasifikasikan pesan pengguna ke salah satu intent berikut:
- CATAT_TRANSAKSI
- TANYA_WALLET
- MINTA_LAPORAN
- TAMBAH_WALLET
- PINDAH_WALLET
- LAINNYA

Jika CATAT_TRANSAKSI
Jika terdapat beberapa transaksi dalam satu kalimat, pecah menjadi beberapa item JSON
```json
{
  "intent": "CATAT_TRANSAKSI",
  "content": [
    {
      "date": "2025-07-14 14:20:21", //(kenali "hari ini", "kemarin", dst. Hari ini = {d})
      "activityName": "nasi uduk", // nasi goreng, ngegojek, narik gojek, gaji, dll
      "quantity": 20, 
      "unit": "porsi", //(misal: porsi, kg, layanan)
      "flowType": "income", // (income, expense, transfer)
      "itemType": "product", // product / service
      "price": 15000,
      "wallet": "cash" // (gopay, bank bri, bca, dana, default: cash)
    }
  ]
}
```

jika TANYA_WALLET
```json
{
  "intent": "TANYA_WALLET",
  "content": ""
}
```

jika TAMBAH_WALLET:
```json
{
  "intent": "TAMBAH_WALLET",
  "content": {
    "name": "",           // nama wallet seperti Gopay, Dana, Bank BRI, Bank Mandiri, Cash, Bareksa
    "initialBalance": 0   // jika user tidak menyebutkan nominal, maka default 0
  }
}

```

jika PINDAH_WALLET:
```json
{
  "intent": "PINDAH_WALLET",
  "content": {
    "targetWallet": "",
    "sourceWallet": "",
    "nominal": 0,
    "fee" : 0
  }
}
```

Jika MINTA_LAPORAN, dan waktu tidak disebut, gunakan:
start = {d - 7 hari}, end = {d}
```json
{
  "intent": "MINTA_LAPORAN",
  "content": {
    "dateRange": {
      "start": "2025-07-01 00:00:00",
      "end": "2025-07-22 00:00:00"
    },
    "flowType": [],            // option=income,expense,transfer,[]
    "wallet": "cash",                // atau null (semua wallet)
    "groupBy": null,                 // option=day,week,month,flowType,null
    "outputFormat": ['table]
  }
}
```

Jika kamu tidak yakin intent-nya, gunakan 
```json
{
  "intent": "LAINNYA",
  "content": "(jawab secara normal dengan pengetahuanmu dan informasikan cara-cara input berdasarkan rule diatas, 
  tapi harus tetap tau batasanmu bahwa kamu asisten ai cashflow untuk
  pencatatan cashflow)"

}
```
"""