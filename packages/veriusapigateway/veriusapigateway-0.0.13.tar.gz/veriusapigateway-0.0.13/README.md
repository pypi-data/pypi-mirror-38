# PROJECT DESCRIPTION

A Gateway for VeriUs Text Mining API.
Version: 0.0.12-beta (Anything on this document is subject to change.)
---

## Authentication

VeriUs Text API’s uses “Username” and “Password” to authenticate incoming requests.
You should pass in your "Username" and "Password" while creating the VeriUsAPI Object.

###### INFO

- You must replace **“$USER”** with your **“Username”** and **“$PASSWORD”** with you **“Password”**.
- Since our services are constantly get updated results in this page may or may not represent actual values.

---
## Installation and Importation

```
pip3 install veriusapigateway
python3
from veriusapigateway import VeriUsAPIGateway
VeriUsAPI = VeriUsAPIGateway("$USER", "$PASSWORD")
```

---
## Text Similarity

**Estimate the degree of similarity between two texts**

**Usage:**

```
text1 = "Artificial intelligence (AI), the ability of a digital computer or computer-controlled robot to perform tasks commonly associated with intelligent beings."
text2 = "AI (artificial intelligence) is the simulation of human intelligence processes by machines, especially computer systems."
result = VeriUsAPI.getSimilarity(text1, text2)
print(result)
0.5679123042313889
```

---
## Semantic Text Similarity

**Estimate the degree of semantic similarity between two texts**

**Usage:**

```
text1 = "Yapay zeka (AI), bir dijital bilgisayarın veya bilgisayar kontrollü robotun, akıllı varlıklar ile yaygın olarak ilişkili görevleri gerçekleştirme kabiliyetidir."
text2 = "Yapay zeka, insan zekası süreçlerinin makineler, özellikle bilgisayar sistemleri ile simülasyonudur."
result = VeriUsAPI.getSemanticSimilarity(text1, text2)
print(result)
0.8897541234782312
```

---
## Language Detection

**Detect the language of a text.**

**Usage:**

```
text = "Yapay zeka (AI), bir dijital bilgisayarın veya bilgisayar kontrollü robotun, akıllı varlıklar ile yaygın olarak ilişkili görevleri gerçekleştirme kabiliyetidir."
result = VeriUsAPI.getLanguage(text)
print(result)
tr
```

---
## Part of Speech Tagger

**Assign parts of speech to each word, such as noun, verb, adjective, etc.**

**Usage:**

```
text = "Yapay zeka (AI), bir dijital bilgisayarın veya bilgisayar kontrollü robotun, akıllı varlıklar ile yaygın olarak ilişkili görevleri gerçekleştirme kabiliyetidir."
result = VeriUsAPI.getPartofSpeechTags(text)
{'Yapay': 'Adjective', 'zeka': 'Noun', '(': 'Punctuation', 'AI': 'Noun', ')': 'Punctuation', ',': 'Punctuation', 'bir': 'Determiner', 'dijital': 'Noun', 'bilgisayarın': 'Noun', 'veya': 'Conjunction', 'bilgisayar': 'Noun', 'kontrollü': 'Adjective', 'robotun': 'Noun', 'akıllı': 'Adjective', 'varlıklar': 'Noun', 'ile': 'Postp', 'yaygın': 'Adjective', 'olarak': 'Adverb', 'ilişkili': 'Noun', 'görevleri': 'Noun', 'gerçekleştirme': 'Verb', 'kabiliyetidir': 'Verb'}
```

---
## Abusive Content Detection

**Check if a sentence is abusive or not.**

**Usage:**

```
text = "Yapay zeka (AI), bir dijital bilgisayarın veya bilgisayar kontrollü robotun, akıllı varlıklar ile yaygın olarak ilişkili görevleri gerçekleştirme kabiliyetidir."
result = VeriUsAPI.getAbusive(text)
print(result)
Non-abusive
```

---
## Text Summarization

**Summarize with the major points of the original document.**

**Usage:**

```
text = "Bir kedi varmış, çok yalnızmış.  Çünkü kedi, annesini ve babasını kaybetmiş.Her gün yollarda gezermiş aç aç. Çöplükte yaşarmış. Bir gün bir evin yanından geçerken bir çocuğa rastlamış. Çocuk kediyi 2-3 dakika sevdikten sonra onu evine götürmüş, kedi ise hiç bir şey dememiş çünkü kedi hiç  Olamaz çünkü onun bir ailesi var demiş. Ancak çocuk ısrar etmiş ve babasını ikna etmiş. Çocuk da mutluymuş kedi  de. Kediyi beslemeye başlamışlar. 1 sene geçtikten sonra kedinin annesi ve babası ortaya çıkmış. Yavrularını bulmak için çabalamışlar ve sonunda bulmuşlar. Kedi ilk önce gitmek istememiş fakat annesi babası olduğunu anlayınca hemen onların yanına gitmiş. Çocuk ağlamaya başlamış.-Anladım baba, mutlu mutlu yaşasınlar, demiş. Kedi ve ailesi yola çıkmışlar, iyi bir hayata yeniden başlamışlar."
result = VeriUsAPI.getSummary(text)
print(result)
Çocuk kediyi 2-3 dakika sevdikten sonra onu evine götürmüş, kedi ise hiç bir şey dememiş çünkü kedi hiç Olamaz çünkü onun bir ailesi var demiş. Çocuk da mutluymuş kedi de.
```

---
## Keyword Extraction

**Identify terms that best decribe the subject of a document.**

**Usage:**

```
text = "Carl Sagan, Dünya dışında akıllı hayatın araştırılmasından yanaydı. Bilim dünyasını, Dünya dışı akıllı yaşam formlarından gelen sinyalleri dinlemek için büyük radyo-teleskopları kullanmaya sevk etmiştir. Diğer gezegenlere sondalar gönderilmesi gerektiğini savunmuştur. Carl Sagan, 12 yıl boyunca Icarus dergisinin editörlüğünü yapmıştır. Planetary Society nin kurucularındandır. Carl Sagan, SETI Enstitüsü nün yönetim kurulunun bir üyesiydi."
result = VeriUsAPI.getKeywords(text)
print(result)
Carl Sagan Akıllı
```

---
## Entity Extraction

**Identify relevant nouns (people, places and organizations) that are mentioned in a text.**

**Usage:**

```
text = "Merhaba ben Ahmet, nasılsınız?"
result = VeriUsAPI.getNamedEntitites(text)
print(result)
{'Merhaba': 'Other', 'ben': 'Other', 'Ahmet': 'Person', ',': 'Other', 'nasılsınız': 'Other', '?': 'Other'}
```

---
## Distorted Language Detection

**A fun project to detect distorted language spoken by the white collar.**

**Usage:**

```
text = "Gelecek hafta için bir toplantı assign edip brainstorming yapalım ve bir an önce bu konuda aksiyon alalım çünkü deadline yaklaşıyor."
result = VeriUsAPI.getDistorted(text)
print(result)
0.9901372301239035
```

---
## Intent Detection

**Determine the expressed intent of given text.**

**Usage:**

```
text = "Merhaba banka hesabı açmak istiyorum yardımcı olabilir misiniz?"
result = VeriUsAPI.getIntent(text)
print(result)
QUERY
```

---
## Short News Classification

**Classify the subject of the given short news**

**Usage:**

```
text = "Ayrım duvarına 'Filistinli cesur kız' Temimi'nin resmini çizen 2 İtalyan aktivist, İsrail güvenlik güçleri tarafından gözaltına alındı"
result = VeriUsAPI.getShortNewsClass(text)
print(result)
PLANET
```

---
## Taxonomy

**Classify the subject of the given text**

**Usage:**

```
text = "VeriUs teknoloji servis olarak yapay zeka (AIaaS) ürünleri geliştiren çeşitli yapay zeka, makine öğrenmesi, metin madenciliği, doğal dil isleme ve sosyal ağ analizi servisleri ve danışmanlığı sağlayan bir yapay zeka servis sağlayıcıdır."
result = VeriUsAPI.getTaxonomy(text)
print(result)
Bilgisayar
```

---
## News Classification

**Classify the subject of the given news**

**Usage:**

```
text = "Beşiktaş maçında şok görüntü! Bu hale geldi... UEFA Avrupa Ligi ön eleme turu rövanş maçında temsilcimiz Beşiktaşın, Avusturya ekibi LASK Linz ile deplasmanda karşılaştığı maçta tribünlerde istenmeyen olaylar yaşandı. Bir taraftar başından yaralandı."
result = VeriUsAPI.getNewsClass(text)
print(result)
SPORTS
```

---
## Semantic Similarity (e-Commerce)

**Estimate the degree of semantic similarity between two product titles**

**Usage:**

```
text1 = "Fabrikadan Halka Dyl Z100 Eko Rok Günlük Erkek Ayakkabı"
text2 = "Fabrikadan Halka FPC T714 Süet Erkek Ayakkabı"
result = VeriUsAPI.getSemanticSimilarityECommerce(text1, text2)
print(result)
0.9810324891178293
```

---
## Normalization

**Normalize a given sentence to its proper written form**

**Usage:**

```
text = "@dida bi yere gitcem büttttttüüüünnnnn insanlar hür, haysiyet ve haklari bakimindan e$it doğarlaaaar."
result = VeriUsAPI.getNormal(text)
print(result)
@mention[@dida] bir yere gideceğim bütün insanlar hür, haysiyet ve hakları bakımından eşit doğarlar.
```

---
## Deasciifier

**Replace ascii characters with Turkish characters**

**Usage:**

```
text = "Dun yolda bir kedi gordum, cok sevımlıydı. Hemen alıp cantama koydum ve eve getırdım."
result = VeriUsAPI.getDeasciified(text)
print(result)
Dün yolda bir kedi gördüm, çok sevimliydi. Hemen alıp çantama koydum ve eve getirdim.
```

---
## Morphological Analysis

**Decompose a given text to its morphogical characteristics**

**Usage:**

```
text = "Bütün insanlar hür , haysiyet ve haklar bakımından eşit doğarlar ."
result = VeriUsAPI.getMorphology(text)
print(result)
[[bütün:Adj] bütün:Adj, [insan:Noun] insan:Noun+lar:A3pl, [hür:Adj] hür:Adj, [,:Punc] ,:Punc, [haysiyet:Noun] haysiyet:Noun+A3sg, [ve:Conj] ve:Conj, [hak:Noun] hak:Noun+lar:A3pl, [bakım:Noun] bakım:Noun+A3sg+ı:P3sg+ndan:Abl, [eşit:Adj] eşit:Adj, [doğmak:Verb] doğ:Verb+ar:Aor+lar:A3pl, [.:Punc] .:Punc]
```
