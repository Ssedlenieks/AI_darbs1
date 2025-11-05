# AI_darbs1 - Teksta Apstrādes Programma

Python programma teksta apstrādei, izmantojot Hugging Face modeļus. Programma veic trīs galvenās funkcijas:

1. **Teksta apkopošana** - Apkopo informāciju no teksta faila .txt formātā
2. **Atslēgvārdu izvēle** - Atlasa aprakstošus atslēgvārdus no teksta
3. **Testa jautājumu ģenerēšana** - Izveido jautājumus ar četriem atbilžu variantiem

## Izmantotās tehnoloģijas

- **Hugging Face Hub** - Piekļuve AI modeļiem
- **OpenAI bibliotēka** - Teksta ģenerēšanai
- Teksta apkopošanai: `facebook/bart-large-cnn`
- Teksta ģenerēšanai: `mistralai/Mistral-7B-Instruct-v0.2`

## Instalācija

### 1. Klonējiet repozitoriju

```bash
git clone https://github.com/Ssedlenieks/AI_darbs1.git
cd AI_darbs1
```

### 2. Izveidojiet virtuālo vidi (ieteicams)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalējiet atkarības

```powershell
pip install -r requirements.txt
```

### 4. Konfigurācija (neobligāti)

Ja vēlaties izmantot Hugging Face API ar autentifikāciju:

1. Izveidojiet `.env` failu:
   ```powershell
   copy .env.example .env
   ```

2. Pievienojiet savu Hugging Face tokenu `.env` failā:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   ```

Tokenu var iegūt: https://huggingface.co/settings/tokens

## Lietošana

### Palaidiet programmu:

```powershell
python main.py
```

### Programmas gaita:

1. **Faila ievade**: Programma jautās teksta faila ceļu (noklusējums: `sample_text.txt`)
2. **Apkopojums**: Automātiski apkopos tekstu
3. **Atslēgvārdi**: Jūs varēsiet izvēlēties, cik atslēgvārdus vēlaties (noklusējums: 5)
4. **Testa jautājumi**: Jūs varēsiet izvēlēties, cik jautājumus ģenerēt (noklusējums: 3)

### Piemērs:

```powershell
python main.py
```

Ievade:
```
📁 Ievadiet teksta faila ceļu (.txt) [noklusējums: sample_text.txt]: 
Cik atslēgvārdus vēlaties izvēlēties? [noklusējums: 5]: 5
Cik jautājumus ģenerēt? [noklusējums: 3]: 3
```

Izvade:
- Teksta apkopojums
- 5 atslēgvārdi
- 3 jautājumi ar 4 atbilžu variantiem katram

## Failu struktūra

```
AI_darbs1/
├── main.py              # Galvenā programma
├── requirements.txt     # Python atkarības
├── sample_text.txt      # Parauga teksta fails
├── .env.example         # Konfigurācijas piemērs
└── README.md           # Dokumentācija
```

## Funkcionalitāte

### 1. TextProcessor klase

Galvenā klase, kas nodrošina visu funkcionalitāti:

- `read_text_file(file_path)` - Nolasa tekstu no faila
- `summarize_text(text)` - Apkopo tekstu
- `extract_keywords(text, num_keywords)` - Izvelk atslēgvārdus
- `generate_quiz(text, num_questions)` - Ģenerē testa jautājumus

### 2. Izmantotie Hugging Face modeļi

- **facebook/bart-large-cnn** - BART modelis teksta apkopošanai
- **mistralai/Mistral-7B-Instruct-v0.2** - Mistral modelis teksta ģenerēšanai

## Prasības

- Python 3.7+
- Interneta savienojums (API izsaukumiem)
- (Neobligāti) Hugging Face konts un API tokens

## Autors

Projekts izveidots kā mācību darbs AI tehnoloģiju apguvei.

## Licence

Šis projekts ir izveidots izglītības nolūkos.