# 🎬 Movie Recommendation System

Yaptığım araştırmalar sonucunda, öneri sistemlerinin arama sonuçlarının kalitesini artırmak ve kullanıcılara daha alakalı içerikler sunmak için kullanılan bir tür bilgi filtreleme sistemi olduğunu gördüm. Bu sistemler, bir kullanıcının bir ürüne (veya içeriğe) vereceği puanı ya da ilgiyi tahmin etmek için yaygın olarak kullanılmaktadır. Günümüzde hemen hemen tüm büyük teknoloji şirketleri öneri sistemlerini çeşitli şekillerde uygulamaktadır:

* **Amazon** → müşterilere ürün önermek,
* **YouTube** → otomatik oynatma sırasında bir sonraki videoyu seçmek,
* **Facebook** → takip edilmesi önerilen sayfa ve kişileri sunmak,
* **Netflix ve Spotify** → kullanıcıya özel içerik önerileri sağlamak.

Ayrıca, öneri motorlarının genellikle üç ana yaklaşımla geliştirildiğini öğrendim:

1.  **Popülerliğe dayalı öneri motoru:** En basit yöntemdir; içerikler izlenme/popülerlik sırasına göre listelenir (YouTube ve Netflix’teki trend listeleri buna örnektir).
2.  **İçerik tabanlı öneri motoru:** Kullanıcının beğendiği bir içerik temel alınarak benzer hikâye, tür, oyuncu veya yönetmene sahip içerikler önerilir.
3.  **İşbirlikçi filtrelemeye dayalı öneri motoru:** Benzer tercihlere sahip kullanıcıların izleme alışkanlıkları karşılaştırılarak öneriler yapılır (Amazon’daki “Bu ürünü görüntüleyen müşteriler şunları da görüntüledi” listesi buna örnektir).

---

## Proje Hakkında

Staj süresince geliştirdiğim proje, kullanıcılara film öneri sistemi sunan **içerik tabanlı filtreleme** yöntemini kullanarak yapay zeka destekli film önerileri sunan bir sistem geliştirmeyi amaçlamıştır. Uygulamanın amacı, kullanıcıların girdiği film adlarına göre benzer filmleri hızlı, doğru ve görsel açıdan kullanıcı dostu bir şekilde önermekti. Proje, hem **backend** hem **frontend** tarafını kapsayan bir full-stack geliştirme deneyimi sağladı ve ölçeklenebilir bir yapı üzerine inşa edildi. Başlangıçta Kaggle’dan alınan 5.000 kayıtlı veri seti ile başlanan proje, ilerleyen aşamalarda veritabanı entegrasyonu ile genişletildi.

### Teknolojiler

* **Programlama Dili:** Python, JavaScript
* **Backend:** FastAPI, PostgreSQL, pgvector
* **Frontend:** React
* **Yapay Zeka & Veri İşleme:** Sentence-Transformers, pandas, tqdm
* **API Entegrasyonu:** OMDB API
* **Ortam Yönetimi:** Docker

### Proje Geliştirme Süreci

**Veri Toplama ve Ön İşleme:** Kaggle’dan temin edilen film veri setleri birleştirilip temizlendi. Önemli özellikler (`id`, `title`, `crew`, `cast`, `overview`, `keywords`) seçildi.

**Model Geliştirme ve Vektörleştirme:** Başlangıçta TF-IDF ve kosinüs benzerliği ile temel bir öneri sistemi kuruldu. Daha sonra Sentence-Transformers kullanılarak her film için 768 boyutlu embedding vektörleri oluşturuldu.

**Veritabanı Entegrasyonu:** PostgreSQL ile 5000 film verisi yönetildi ve `pgvector` eklentisi ile embedding benzerlikleri üzerinden sorgular gerçekleştirildi.

**Backend (API) Geliştirme:** FastAPI kullanılarak API oluşturuldu. Kullanıcının girdiği film adıyla en benzer filmler `pgvector` aracılığıyla sorgulandı ve OMDB API ile poster, özet ve IMDb puanı gibi bilgiler sağlandı.

**Frontend Geliştirme:** React ile kullanıcı arayüzü tasarlandı. Film kartları, yıldızlı puanlama, skeleton loading animasyonu, infinite scroll ve autocomplete özellikleri eklendi. Arayüz modernleştirildi ve hata yönetimi sağlandı.

---

### Ekran Görüntüleri

<img width="547" height="650" alt="Ekran görüntüsü 2025-08-10 231425" src="https://github.com/user-attachments/assets/7e31e34c-f8d4-42a7-96ed-6db5844db627" />
<img width="823" height="718" alt="Ekran görüntüsü 2025-08-24 222551" src="https://github.com/user-attachments/assets/bb7bb0c8-54bc-4246-a509-f68f2bf7fccc" />
