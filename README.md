# Inaturalist_API_and_mobile_tests

Проект автоматизации тестирования **API** и **мобильного приложения (Android)** iNaturalist.

- Репозиторий: https://github.com/veliseeva/Inaturalist_API_and_mobile_tests
- Удалённый запуск: [GitHub Actions](https://github.com/veliseeva/Inaturalist_API_and_mobile_tests/actions)

## Содержание

- [Технологии](#технологии)
- [Что проверяют тесты](#что-проверяют-тесты)
- [Локальный запуск](#локальный-запуск)
- [Удалённый запуск](#удалённый-запуск-github-actions)
- [Структура проекта](#структура-проекта)

## Технологии

| Инструмент | Назначение |
|---|---|
| Python 3.11, pytest | запуск тестов |
| requests + jsonschema | API-тесты, валидация ответов по JSON-схемам |
| pydantic-settings + python-dotenv | конфигурация, чтение переменных из `.env` |
| Appium (UiAutomator2) + Appium-Python-Client | мобильные тесты |
| Selene | обёртка над WebDriver-сессией |
| Allure Report | отчёты о прогонах |
| GitHub Actions | удалённый запуск (CI) |

## Что проверяют тесты

**API** (`tests/API`): блокировка/разблокировка пользователя, запрос несуществующего пользователя (с проверкой по JSON-схеме), получение участников проекта, глобальный поиск таксонов, создание комментария к наблюдению.

**Mobile** (`tests/Mobile`): успешная авторизация, смена языка интерфейса, поиск вида и проверка его названия в результатах.

## Локальный запуск

### 1. Клонировать репозиторий и установить зависимости

```bash
git clone https://github.com/veliseeva/Inaturalist_API_and_mobile_tests.git
cd Inaturalist_API_and_mobile_tests

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Создать файл `.env` в корне проекта

`.env` в репозиторий не коммитится (он в `.gitignore`). Переменные (регистр не важен):

| Переменная | Обязательна | Значение по умолчанию | Назначение |
|---|---|---|---|
| `INAT_USERNAME` / `INAT_PASSWORD` | да | — | логин и пароль пользователя iNaturalist |
| `INAT_APP_ID` / `INAT_APP_SECRET` | да | — | OAuth-приложение (iNaturalist → Account settings → Applications) |
| `MY_EMULATOR_NAME` | нет | `emulator-5554` | имя эмулятора для `--context emulator` |
| `MY_LOCAL_UDID` | для `--context real` | — | udid устройства из `adb devices` |
| `LOCAL_URL` | нет | `http://127.0.0.1:4723` | адрес локального Appium-сервера |
| `TIMEOUT` | нет | `15` | неявное ожидание Selene, сек. |
| `BS_USER` / `BS_KEY` | для `--context bstack` | — | доступы BrowserStack |
| `BS_APP_ID` | для `--context bstack` | — | id загруженного APK (`bs://...`) |
| `BS_DEVICE_NAME` / `BS_PLATFORM_VERSION` | нет | `OnePlus 11R` / `13.0` | устройство и версия Android в BrowserStack |

Пример:

```dotenv
INAT_USERNAME=my_login
INAT_PASSWORD=my_password
INAT_APP_ID=my_app_id
INAT_APP_SECRET=my_app_secret
```

### 3. Запустить тесты

```bash
pytest tests/API                            # только API (нужны креды в .env)

pytest tests/Mobile --context emulator      # мобильные на эмуляторе
pytest tests/Mobile --context real          # мобильные на реальном устройстве
pytest tests/Mobile --context bstack        # мобильные в BrowserStack
```

> API- и Mobile-тесты запускаются отдельными командами: в каталогах есть одноимённые файлы `test_search.py`, поэтому общий запуск `pytest .` из корня завершается ошибкой `import file mismatch`.

Мобильным тестам нужен запущенный **Appium-сервер** и эмулятор/устройство:

```bash
# один раз: установить Appium и драйвер
npm install -g appium
appium driver install uiautomator2

# запустить Appium (порт по умолчанию 4723)
appium

# в другом терминале проверить, что устройство видно
adb devices
```

APK приложения (`iNaturalist-release.apk`) лежит в репозитории и устанавливается на эмулятор автоматически.

### 4. Allure-отчёт локально

```bash
pytest . --alluredir=allure-results
allure serve allure-results
```

Если Allure CLI не установлен — [инструкция по установке](https://allurereport.org/docs/install/). Каталоги `allure-results/` и `allure-report/` уже в `.gitignore`.

## Удалённый запуск (GitHub Actions)

> Ссылка на проект в GitHub Actions: https://github.com/veliseeva/Inaturalist_API_and_mobile_tests/actions

CI развёрнут в GitHub Actions: для публичных репозиториев это бесплатно и не требует собственного сервера (Jenkins на VPS больше не используется).

### Настройка (один раз)

В репозитории: **Settings → Secrets and variables → Actions → New repository secret**. Добавить:

- `INAT_USERNAME`, `INAT_PASSWORD`, `INAT_APP_ID`, `INAT_APP_SECRET` — для API-тестов;
- `BS_USER`, `BS_KEY`, `BS_APP_ID` — дополнительно, если мобильные тесты запускаются в BrowserStack.

### Запуск автотестов

1. **API-тесты** — workflow `API tests` (`.github/workflows/api-tests.yml`) запускается автоматически на `push` в `main` и на `pull_request`.
2. **Вручную** — вкладка **Actions** → выбрать workflow → кнопка **Run workflow**.
3. **Mobile-тесты** — workflow `Mobile tests`: **Actions → Mobile tests → Run workflow** → выбрать `context`:
   - `emulator` — Android-эмулятор поднимается прямо на раннере GitHub Actions (по умолчанию);
   - `bstack` — запуск на устройствах BrowserStack.

### Результаты запуска

В запуске сборки на вкладке **Actions**:

- **Artifacts → `allure-results`** — результаты для отчёта. Скачать и открыть локально:

  ```bash
  allure serve allure-results
  ```

- **Artifacts → `appium-log`** — лог Appium-сервера (для мобильных тестов).

## Структура проекта

```
.
├── .github/workflows/         # CI: api-tests.yml, mobile-tests.yml
├── inaturalist_project/
│   ├── pages/mobile/          # Page Object мобильного приложения
│   └── utils/                 # auth (OAuth → JWT), request_helper (API-клиент),
│                              # attach (скриншоты, XML, видео BrowserStack), gestures
├── schemas/                   # JSON-схемы ответов API
├── tests/
│   ├── API/                   # фикстуры и тесты API
│   └── Mobile/                # фикстуры и тесты мобильного приложения
├── config.py                  # настройки (pydantic-settings) и capabilities Appium
├── pytest.ini
└── requirements.txt
```
