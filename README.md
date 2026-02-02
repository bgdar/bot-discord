<h1 align="center"> 
Rant Bot 
</h1>
> Bot untuk **mendeteksi kata kata** kasar dan memberikan himbauan

<p align="center">
  <img src="https://skillicons.dev/icons?i=python" width="50" alt="Python" />
  <img src="https://skillicons.dev/icons?i=discord" width="50" alt="Discord" />
</p>

### target

- bot bisa inetaksi ke user
- bot memberikan himbauan
- bisa interaksi lain atau chatings

### File

`cogs\cogChattings` : hanya chat berupa commadn biasa

`cogs\cogRant` : chat yang reletime listener detection dengan `on_message` untuk memantau kata kata

### Level Rant

- `ugnest` : paling parah
- `sedang` : di antara parah dan normal
- `normal` : mendekati kata kata sehari hari yang sedikit ambigu

### Bot

> setup bot di : https://discord.com/developers/

### Data

> `/data/` : jika tertarik mencoba bisa ubah data untuk menyesuikan bot nya , tapi **peringatan** untuk mengubah Key dari data tersebut , karena ya .... Error

- `dataRant.py` : data untuk kata kata kasar
