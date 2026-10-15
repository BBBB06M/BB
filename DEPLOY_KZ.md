# GraphMind AI: нөлден жариялауға дейін (қазақша нұсқаулық)

## Саған не керек?

- **OpenAI API** аккаунты мен жарамды API key (ChatGPT Plus-тен бөлек есептелуі мүмкін).
- **GitHub** аккаунты (кодты сақтау үшін).
- **Streamlit Community Cloud** аккаунты (сайтты жариялау үшін, GitHub-пен кіруге болады).
- Компьютерде тексеретін болсаң, **Python 3.11+**.

## 1. Дайын файлды ашу

1. `GraphMind_AI.zip` архивін компьютерге жүктеп, ішін аш.
2. Ішінде `app.py`, `ai_engine.py`, `math_engine.py`, `requirements.txt`, `.streamlit/`, `tests/`, `README.md` бар екенін тексер.
3. Бұл файлдар — сайттың толық бастапқы коды; қолмен Python жазу міндетті емес.

## 2. OpenAI API key алу

1. <https://platform.openai.com/> сайтын ашып, аккаунтқа кір.
2. <https://platform.openai.com/api-keys> бөлімінен **Create new secret key** таңда.
3. Кілтті көшіріп ал да, тек өзіңде сақта. **Ешкімге жіберме және GitHub-қа салма.**
4. Billing/credits параметрлерін тексер. ChatGPT жазылымы API қолдануды автоматты түрде тегін етпейді; API сұраныстарына төлем алынуы мүмкін.
5. Шығынды бақылау үшін есептік жазбада аз бюджет/ескерту шегін қой.

## 3. Компьютеріңде тексеру (міндетті емес, бірақ ұсынылады)

Windows-та:

1. <https://www.python.org/downloads/> арқылы Python орнат.
2. Архивтен шыққан `GraphMind_AI` бумасын аш. Windows Explorer мекенжай жолына `cmd` жазып, Enter бас (терминал сол буманың ішінде ашылады).
3. Мынаны енгіз:

   ```bat
   py -m pip install -r requirements.txt
   ```

4. `.streamlit` бумасында `secrets.example.toml` атты файл бар. Оның көшірмесін `secrets.toml` деп ата.
5. `secrets.toml` файлын Notepad-та ашып, `paste-your-own-secret-key-here` орнына **өзіңнің** API key-іңді қой. Тырнақшалар қалсын.
6. Терминалда іске қос:

   ```bat
   py -m streamlit run app.py
   ```

7. Браузерде `http://localhost:8501` ашылуы тиіс. **Foundation → Generate new AI problem** басып көр. Сол сияқты Standard және Advanced тексер.

Егер компьютерге Python орнатқың келмесе, 4-5-қадамдармен бірден GitHub/Streamlit Cloud-қа жүктеуге болады.

## 4. GitHub-қа кодты салу

1. <https://github.com/> сайтында аккаунтыңа кір.
2. `+` → **New repository**. Атауы: `graphmind-ai`. **Public** таңда, сосын **Create repository** бас.
3. **uploading an existing file** немесе **Add file → Upload files** арқылы архивтен шығарған файлдарды жүкте. `app.py`, `ai_engine.py`, `math_engine.py`, `requirements.txt`, `README.md`, `DEPLOY_KZ.md`, `REPORT.md`, `.gitignore`, `.streamlit/config.toml`, `.streamlit/secrets.example.toml` және `tests/` түгел болуы қажет.
4. **НАЗАР АУДАР:** `.streamlit/secrets.toml` деген нағыз кілт сақталатын файлды ешқашан жүктеме. Ол `.gitignore` арқылы жабылған.
5. **Commit changes** бас. GitHub-та `app.py` файлы түбірлік бетте тұрғанын тексер.
6. Репозиторий сілтемесін сақта. Мысалы: `https://github.com/YOUR_USERNAME/graphmind-ai`.

*Егер GitHub веб-интерфейсі бумаларды жүктеуге ыңғайсыз болса, GitHub Desktop арқылы репозиторий жариялау оңайырақ: <https://desktop.github.com/>.*

## 5. Сайтты Streamlit Cloud арқылы интернетке шығару

1. <https://share.streamlit.io/> аш.
2. GitHub арқылы кіріп, репозиторийге рұқсат бер.
3. **Create app** → **Yup, I have an app** таңда.
4. Repository: `YOUR_USERNAME/graphmind-ai`.
5. Branch: `main`.
6. Main file path / Entrypoint: `app.py`.
7. **Advanced settings → Secrets** аш.
8. Төмендегі мәтінді **сол жерге ғана** қой. `sk-...` орнына өз кілтіңді жаз:

   ```toml
   OPENAI_API_KEY = "sk-YOUR_REAL_SECRET_KEY"
   OPENAI_MODEL = "gpt-5-mini"
   ```

9. **Save**, кейін **Deploy** бас.
10. Сәтті ашылғаннан кейін сайт сілтемесін көшір. Ол `https://....streamlit.app` түрінде болады.

Егер **'OpenAI key not configured'** шықса: Streamlit app settings → Secrets ішіндегі атауы `OPENAI_API_KEY` екеніне көз жеткіз. Егер API 401/429 қате болса: key/model access, billing және quota-ны тексер.

## 6. Нақты тексеретін нәрселер

- Foundation-та жеңіл `±x²+c` функциясы шықты ма?
- Standard-та `b` нөлге тең емес, ал төбе формуласымен табылады ма?
- Advanced-та доп биіктігі туралы есеп шығып, парабола төмен қараған ба?
- Hint 1 және Hint 2 көрсетіле ме?
- Жауап енгізгенде **3 түрлі жауап** тексеріле ме?
- Show solution басқанда тексерілген қадамдар және графиктегі төбе көріне ме?
- Generate қайта басқанда жаңа коэффициенттер шыға ма?

## 7. Мұғалімге жіберетін 3 нәрсе

1. **Live Website URL** — Streamlit жарияланған адресі.
2. **Public GitHub Repo** — кодың + README.
3. **Brief Report (1 Page)** — дайын `REPORT.pdf` файлын оқып, аты-жөніңді және нақты тексеру нәтижесін қосып бейімде.

**Маңызды:** тапсырмада «өз түпнұсқа жұмысың» деген талап бар. Сондықтан дайын кодты түсініп, өз идеяларыңмен жетілдіріп, есептердің дұрыстығын өзің тексеріп, қорғауда қалай жұмыс істейтінін айтып беру керек.
