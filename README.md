# Denge Atlası

Denge Atlası, React Native CLI mobil uygulaması ile FastAPI servisinden oluşan bir
monorepodur. Bu depo Sprint 03 sonundaki kaynak indeksleme ve yapılandırılmış
retrieval temelini içerir; üretken yanıt, analiz, günlük ve TTS özellikleri henüz
uygulanmamıştır.

## Gereksinimler

- Node.js 22.11 veya üzeri ve npm
- Python 3.9 veya üzeri
- iOS için Xcode ve CocoaPods
- Android için JDK 17 ve Android SDK
- İsteğe bağlı backend container doğrulaması için Docker

## Kurulum

```bash
npm install
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r services/api/requirements-dev.txt
```

Ortam dosyaları yalnızca güvenli yerel varsayılanlar içerir:

```bash
cp .env.example .env
cp services/api/.env.example services/api/.env
```

Gizli değerleri veya kullanıcı girdilerini bu dosyalara ya da loglara eklemeyin.

## Backend

```bash
source .venv/bin/activate
uvicorn services.api.app.main:app --reload --host 127.0.0.1 --port 8000
curl http://127.0.0.1:8000/health
```

Beklenen yanıt `status`, `service`, `version` ve ISO 8601 `timestamp` alanlarını
içerir. Yerel OpenAPI arayüzü `http://127.0.0.1:8000/docs` adresindedir.

## Mobil

Metro'yu başlatın:

```bash
npm run mobile:start
```

Başka bir terminalde platformu çalıştırın:

```bash
npm run mobile:android
npm run mobile:ios
```

iOS bağımlılıklarını ilk çalıştırmadan önce kurun:

```bash
cd apps/mobile
bundle install
cd ios
bundle exec pod install
```

## API sözleşmesi

FastAPI OpenAPI çıktısı tek sözleşme kaynağıdır. Sözleşmeyi ve TypeScript tiplerini
yeniden üretmek için:

```bash
source .venv/bin/activate
npm run openapi:generate
npm run api-client:generate
```

Üretilen dosyalar `packages/api-client/openapi.json` ve
`packages/api-client/src/generated/schema.ts` konumlarındadır. Mobil Zod sağlık
şeması, üretilen `HealthResponse` tipiyle derleme zamanında eşleştirilir.

## Kalite komutları

Sanal ortam etkinken:

```bash
npm run lint
npm run typecheck
npm run test
npm run contract:check
npm run docs:validate
npm run secrets:check
npm run security:check
npm run check
```

Backend container'ını depo kökünden oluşturun:

```bash
docker build -f services/api/Dockerfile -t denge-atlasi-api:local .
```

CI; lint, tip kontrolü, test, sözleşme üretimi, Android debug derlemesi ve backend
container derlemesini ayrı kalite kapıları olarak çalıştırır.

## Pre-commit

`pre-commit` kurulu bir geliştirme ortamında hook'ları etkinleştirin:

```bash
python -m pip install -r services/api/requirements.lock
pre-commit install
pre-commit run --all-files
```

Hook'lar Ruff, ESLint, mobil ve üretilen API TypeScript tip kontrolleri, MyPy,
Sprint 00 belge doğrulaması ve yerel secret taramasını çalıştırır.

Node bağımlılıkları `package-lock.json`, Python çalışma ortamı ise tam sürümlü
`services/api/requirements.lock` ile kilitlenmiştir.

## Depo yapısı

```text
apps/mobile          React Native CLI uygulaması
services/api         FastAPI servisi ve testleri
packages/api-client  OpenAPI çıktısı ve üretilen TypeScript tipleri
docs                 Blueprint ve ADR belgeleri
scripts              Paylaşılan scriptler için ayrılmış alan
tests                Depo-seviyesi testler için ayrılmış alan
```

`scripts/` ve `tests/` dizinleri, Sprint 01'de kanonik yapıyı görünür tutmak için
boş yer tutucu içerir; gelecek sprint özellikleri eklenmemiştir.

## Sprint Durumu

Sprint 00 yönetişim çıktıları ve Sprint 01 mühendislik temeli tamamlanmıştır. Belirli
Marifetname ve Ibn Sina baskılarının insan/telif incelemesi halen görünür bir içerik
operasyonu sınırlamasıdır; hiçbir baskı retrieval için onaylanmış değildir. Docker
daemon bulunmayan ortamlarda container doğrulaması atlanabilir ve ortam sınırlaması
olarak raporlanır.

## Sentetik Kaynak İndeksleme

Sprint 02 indeksleme akışı yalnızca kayıtlı ve `APPROVED` kaynakları kabul eder.
ADR-010 henüz öneri durumunda olduğundan üretim embedding modeli seçilmemiştir.
Aşağıdaki komut yalnızca açıkça sentetik test fixture'ları için deterministik test
embedding'i kullanır:

```bash
source .venv/bin/activate
npm run sources:index:test
```

Komut, yeniden üretilebilir ChromaDB indeksini `data/index/` altında; makine ve
insan tarafından okunabilen raporları `data/index-reports/` altında oluşturur.
Gerçek kaynak baskıları insan ve telif incelemesinden geçmeden bu komuta verilmemelidir.

## Retrieval API

`POST /api/v1/search`, sorguyu sunucuda sınıflandırır ve yalnızca onaylı kaynak
parçalarını yapılandırılmış gruplar halinde döndürür. Marifetname birincil,
Ibn Sina ise açıkça ek kaynak olarak yönlendirilir. İstemci koleksiyon ya da kaynak
önceliği seçemez ve endpoint üretken bir cevap oluşturmaz.

Üretim embedding modeli ADR-010 kapsamında onaylanana kadar endpoint bağımlılığı
bilinçli olarak yapılandırılmamıştır ve `503` döndürür. Sentetik fixture'larla
retrieval değerlendirmesini çalıştırmak için:

```bash
source .venv/bin/activate
npm run retrieval:eval
```

Komut sentetik değerlendirme kümesinde Recall@5 değerini ölçer.
