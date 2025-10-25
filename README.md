# 📊 Otomobil Satış İstatistikleri Dashboard'u

Bu proje, Python, Plotly ve Dash kullanılarak oluşturulmuş interaktif bir web dashboard'udur. Kullanıcıların, durgunluk dönemlerine (recession) ve yıllara göre geçmiş otomobil satış verilerini analiz etmelerini sağlar.

Bu uygulama, **IBM Data Visualization with Python** (IBM Data Science Professional Certificate programının bir parçası) kursunda becerilerimi geliştirmek amacıyla tamamladığım bir lab projesidir.

---

## 🚀 Proje Görünümü

Dashboard'un "Yearly Statistics" (Yıllık İstatistikler) seçiliyken nasıl göründüğüne dair bir örnek:


---

## ✨ Temel Özellikler

* **İnteraktif Kontroller:** Rapor türünü ("Yearly Statistics" veya "Recession Period Statistics") seçmek için bir açılır menü.
* **Dinamik Filtreleme:** Yıla göre filtreleme yapmak için ikinci bir açılır menü. Bu menü, sadece "Yearly Statistics" raporu seçildiğinde aktif hale gelir.
* **Dörtlü Grafik Düzeni:** Seçilen filtrelere göre 4 farklı analizi (çizgi, çubuk ve pasta grafikler) aynı anda gösteren 2x2'lik bir ızgara düzeni.
* **Durgunluk Analizi:** Durgunluk dönemlerindeki satış trendlerini, araç tipi başına düşen ortalama satışları ve reklam harcamalarının payını gösterir.
* **Yıllık Analiz:** Hem tüm zamanlardaki yıllık/aylık trendleri hem de seçilen spesifik bir yıla ait araç tipi ve reklam harcaması dökümünü gösterir.

---

## 🛠️ Kullanılan Teknolojiler

* **Python**: Ana programlama dili.
* **Dash**: Web uygulamasının iskeletini oluşturmak ve interaktiviteyi (callback'ler) sağlamak için kullanıldı.
* **Plotly Express**: İnteraktif ve estetik veri görselleştirmeleri (grafikler) oluşturmak için kullanıldı.
* **Pandas**: Veriyi yüklemek, işlemek ve analiz için gruplamak amacıyla kullanıldı.
* **Requests**: Veri setini web'den çekmek için kullanıldı.

---

## 📦 Veri Seti

Bu projede kullanılan veri seti, IBM tarafından bu kursun amaçları için yapay olarak oluşturulmuştur. Gerçek verileri temsil etmemektedir.

* **Veri Kaynağı:** `https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv`

### Veri Sözlüğü (Değişkenler)

* **Date**: Gözlem tarihi.
* **Recession**: Durgunluk dönemini belirten ikili değişken (1 = Durgunluk, 0 = Normal).
* **Automobile_Sales**: Dönem içinde satılan araç sayısı.
* **GDP**: Kişi başına düşen GSYİH değeri (USD).
* **Unemployment_Rate**: Aylık işsizlik oranı.
* **Consumer_Confidence**: Tüketici güvenini temsil eden sentetik bir endeks.
* **Seasonality_Weight**: Dönem boyunca otomobil satışları üzerindeki mevsimsellik etkisini temsil eden ağırlık.
* **Price**: Dönem içindeki ortalama araç fiyatı.
* **Advertising_Expenditure**: Şirketin reklam harcamaları.
* **Vehicle_Type**: Satılan araç türü (Supperminicar, Smallfamiliycar, Mediumfamilycar, Executivecar, Sports).
* **Competition**: Pazara giren rakip sayısı veya büyük üreticilerin pazar payı.
* **Month**: `Date`'ten çıkarılan ay bilgisi.
* **Year**: `Date`'ten çıkarılan yıl bilgisi.

---

## 🏃‍♀️ Projeyi Bilgisayarında Çalıştırma

Bu projeyi kendi bilgisayarında denemek istersen aşağıdaki adımları izleyebilirsin.

**1. Proje Dosyalarını İndir:**
Bu GitHub sayfasındayken, yeşil renkli `<> Code` butonuna tıkla ve ardından `Download ZIP` seçeneğine bas. Bu, tüm proje dosyalarını bir ZIP dosyası olarak bilgisayarına indirecektir. İndirdikten sonra ZIP dosyasını bir klasöre çıkar.

**2. Gerekli Kütüphaneleri Yükle:**
Projeyi indirdiğin klasörün içine `requirements.txt` adında bir metin dosyası oluştur ve içine aşağıdakileri yapıştır:
