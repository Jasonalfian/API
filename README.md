# API
Membuat API dengan format output JSON

API ini berfungsi untuk mengscrape data dari https://coinmarketcap.com/all/views/all/
Data yang diambil berupa atribut dari cryptocurrency yang saat ini tercatat dan diperjualbelikan
Tipe data yang direturn adalah JSON dengan atribut :

•	Nama  : “String” (Nama dari cryptocurrency)
•	Simbol : “String” (Simbol dari Cryptocurrency)
•	Circulating_supply : “String” (Jumlah cryptocurrency yang ada di pasar)
•	Harga : “String” (Harga 1 buah cryptocurrency dalam USD)
•	Volume : “String” (Jumlah transaksi cryptocurrency satu hari sebelumnya)
•	Movement(24H) : ‘String” (Pergerakan harga cryptocurrency dalam 24 jam terakhir)

Untuk meng-run program, ketik python coinSpider.py di command line
Script akan mengscrape data dan membuat server lokal di port 1000

Untuk mengetes fungsionalitas dari API, dapat menggunakan POSTMAN
Parameter yang diinput adalah http://localhost:1000/coin dengan method GET

coin.json adalah contoh hasil scrapping dari https://coinmarketcap.com/all/views/all/
