# Lords of Polywarphisim

Lords of Polywarphisim, strateji tabanlı bir savaş oyunu simülasyonudur. Oyuncular, farklı türde savaşçılar kullanarak haritada savaşır ve rakiplerini yenmeye çalışır.

## 🎮 Oyun Özellikleri

- **1-4 Oyuncu** desteği
- **Özelleştirilebilir harita boyutları** (16x16, 24x24, 32x32 veya özel boyut)
- **5 farklı savaşçı türü**: Muhafız, Okçu, Atlı, Topçu, Sağlıkçı
- **Renkli terminal arayüzü** (Rich kütüphanesi ile)
- **Stratejik savaş mekaniği** ve kaynak yönetimi

## 📋 Gereksinimler

- Python 3.6 veya üzeri
- `rich` kütüphanesi

## 🚀 Kurulum

### 1. Projeyi İndirin

```bash
cd /Users/selencalik/Desktop/Lords-Of-Polywarphisim-main
```

### 2. Virtual Environment Oluşturun (Önerilen)

```bash
python3 -m venv venv
```

### 3. Virtual Environment'ı Aktifleştirin

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

veya doğrudan:

```bash
pip install rich
```

## 🎯 Oyunu Çalıştırma

Virtual environment aktifken:

```bash
python main.py
```

veya virtual environment olmadan:

```bash
venv/bin/python main.py
```

## 🎲 Oyun Kuralları

### Başlangıç

1. **Harita Boyutu Seçimi**: Oyun başında harita boyutunu seçin (16x16, 24x24, 32x32 veya özel boyut)
2. **Oyuncu Sayısı**: 1-4 arası oyuncu sayısı seçin
3. **Oyuncu İsimleri**: Her oyuncu için isim girin
4. Her oyuncu başlangıçta haritanın köşelerinden birinde bir **Muhafız** ile başlar

### Kaynaklar

- Her oyuncu **200 kaynak** ile başlar
- Savaşçı eklemek için kaynak harcarsınız
- Düşman savaşçıyı yendiğinizde, o savaşçının kaynağının %80'ini geri kazanırsınız

### Savaşçı Türleri

| Savaşçı      | Kaynak | Can | Hasar | Menzil  | Özellikler                                                                     |
| ------------ | ------ | --- | ----- | ------- | ------------------------------------------------------------------------------ |
| **Muhafız**  | 10     | 80  | 20    | (1,1,1) | Gerçek hasar verir, yakın mesafe                                               |
| **Okçu**     | 20     | 30  | 60%   | (2,2,2) | Yüzde hasar, en yüksek canlı 3 düşmana saldırır                                |
| **Atlı**     | 30     | 40  | 30    | (0,0,3) | Gerçek hasar, sadece çapraz saldırı, en yüksek kaynaklı 2 düşmana saldırır     |
| **Topçu**    | 50     | 30  | 100%  | (2,2,0) | Yüzde hasar, çapraz saldırı yok, en yüksek canlı 1 düşmana saldırır            |
| **Sağlıkçı** | 10     | 100 | 50%   | (2,2,2) | Düşmanlara değil, dostlara can verir, en düşük canlı 3 dosta iyileştirme yapar |

### Oyun Akışı

1. **Sıra Sistemi**: Oyuncular sırayla hamle yapar
2. **Hamle Seçenekleri**:
   - **'E'**: Savaşçı ekle
   - **'P'**: Pas geç
3. **Savaşçı Yerleştirme**: Savaşçılarınızı sadece mevcut savaşçılarınızın komşu karelerine yerleştirebilirsiniz
4. **Otomatik Saldırı**: Her tur sonunda tüm savaşçılar menzillerindeki düşmanlara otomatik olarak saldırır

### Kazanma Koşulları

Oyun aşağıdaki durumlardan biri gerçekleştiğinde biter:

- Bir oyuncunun tüm savaşçıları yok edilirse → O oyuncu kaybeder
- Bir oyuncu 3 tur üst üste pas geçerse → O oyuncu kaybeder
- Bir oyuncu haritanın %60'ını kontrol ederse → O oyuncu kazanır

## 🎨 Arayüz

Oyun, `rich` kütüphanesi kullanılarak renkli ve görsel bir terminal arayüzüne sahiptir:

- **Harita**: Savaşçılar haritada renkli harflerle gösterilir
- **Komşu Kareler**: Yerleştirilebilir kareler özel sembollerle işaretlenir
- **Oyuncu Bilgileri**: Her oyuncunun kaynakları ve savaşçılarının can durumu tabloda gösterilir

## 📝 Örnek Oyun Akışı

```
1= 16x16
2= 24x24
3= 32x32
4= Kendi boyutumu seçmek istiyorum.
Lütfen dünya boyutunu seçiniz: 1

1= 1 Oyuncu
2= 2 Oyuncu
3= 3 Oyuncu
4= 4 Oyuncu
Oyuncu sayısını seçiniz: 2

1. oyuncunun adını girin: Oyuncu1
2. oyuncunun adını girin: Oyuncu2

Sıra Oyuncu1 oyuncusunda.
Oyuncu1, elinizde 200 kaynak var.
Savaşçı eklemek için 'E', pas geçmek için 'P' girin: E
...
```

## 🛠️ Sorun Giderme

### "ModuleNotFoundError: No module named 'rich'" Hatası

Virtual environment'ı aktifleştirdiğinizden emin olun:

```bash
source venv/bin/activate
pip install rich
```

### "externally-managed-environment" Hatası

Virtual environment kullanın veya `--break-system-packages` flag'ini kullanın (önerilmez):

```bash
python3 -m venv venv
source venv/bin/activate
pip install rich
```

## 📄 Lisans

Bu proje eğitim amaçlıdır.

## 👥 Katkıda Bulunma

Projeye katkıda bulunmak için:

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📧 İletişim

Sorularınız veya önerileriniz için issue açabilirsiniz.

---

**İyi Oyunlar! 🎮**
