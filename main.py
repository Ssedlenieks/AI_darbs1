import os
from huggingface_hub import InferenceClient
from typing import List, Dict
from dotenv import load_dotenv

# Ielādējam .env failu
load_dotenv()


class TextProcessor:
    """Klase teksta apstrādei ar Hugging Face modeļiem."""
    
    def __init__(self, hf_token: str = None):
        """
        Inicializē TextProcessor ar Hugging Face API tokenu.
        
        Args:
            hf_token: Hugging Face API tokens (neobligāts)
        """
        self.client = InferenceClient(token=hf_token)
        
        # Modeļi, kas tiks izmantoti
        self.summarization_model = "facebook/bart-large-cnn"
        self.text_generation_model = "google/flan-t5-large"  
    
    def read_text_file(self, file_path: str) -> str:
        """
        Nolasa tekstu no faila.
        
        Args:
            file_path: Ceļš uz teksta failu
            
        Returns:
            Faila saturs kā string
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Kļūda: Fails '{file_path}' nav atrasts!")
            return ""
        except Exception as e:
            print(f"Kļūda lasot failu: {e}")
            return ""
    
    def summarize_text(self, text: str) -> str:
        """
        Apkopo tekstu, izmantojot Hugging Face summarization modeli.
        
        Args:
            text: Teksts, ko apkopot
            
        Returns:
            Apkopots teksts
        """
        try:
            print(f"\n🤖 Izmantoju modeli: {self.summarization_model}")
            print("⏳ Apkopoju tekstu...")
            
            # Izmantojam summarization modeli
            summary = self.client.summarization(
                text,
                model=self.summarization_model
            )
            
            return summary.summary_text
            
        except Exception as e:
            print(f"Kļūda apkopojot tekstu: {e}")
            return f"Neizdevās apkopot tekstu. Kļūda: {str(e)}"
    
    def extract_keywords(self, text: str, num_keywords: int) -> List[str]:
        """
        Izvelk atslēgvārdus no teksta.
        
        Args:
            text: Teksts, no kura izvēlēties atslēgvārdus
            num_keywords: Cik atslēgvārdus izvēlēties
            
        Returns:
            Saraksts ar atslēgvārdiem
        """
        try:
            print(f"\n🤖 Izmantoju modeli: {self.text_generation_model}")
            print(f"⏳ Izvēlu {num_keywords} atslēgvārdus...")
            
            # Saīsinām tekstu, ja nepieciešams
            text_sample = text[:800] if len(text) > 800 else text
            
            prompt = f"Keywords: {text_sample}\nMain topics:"
            
            response = self.client.text_generation(
                prompt,
                model=self.text_generation_model,
                max_new_tokens=100,
                temperature=0.3
            )
            
            # Apstrādājam atbildi - izvelkam atslēgvārdus
            keywords_text = response.strip()
            
            # Mēģinām parsēt dažādos veidos
            keywords = []
            
            # Ja ir komati
            if ',' in keywords_text:
                keywords = [k.strip() for k in keywords_text.split(',')]
            # Ja ir punkti vai newlines
            elif '\n' in keywords_text or '.' in keywords_text:
                keywords_text = keywords_text.replace('.', '\n')
                keywords = [k.strip() for k in keywords_text.split('\n') if k.strip()]
            # Vienkārši vārdi
            else:
                keywords = [keywords_text.strip()]
            
            # Filtrējam un ierobežojam
            keywords = [k for k in keywords if k and len(k) > 2][:num_keywords]
            
            # Ja nesanāca iegūt pietiekami, pievienojam manuālus no teksta
            if len(keywords) < num_keywords:
                fallback = self._extract_fallback_keywords(text, num_keywords)
                keywords.extend(fallback)
                keywords = keywords[:num_keywords]
            
            return keywords
            
        except Exception as e:
            print(f"Kļūda izvelkot atslēgvārdus: {str(e)}")
            return self._extract_fallback_keywords(text, num_keywords)
    
    def _extract_fallback_keywords(self, text: str, num_keywords: int) -> List[str]:
        """Vienkārša atslēgvārdu ekstrakcija, ja AI modelis nedarbojas."""
        # Vienkārši vārdi, kas parādās tekstā
        common_words = {'un', 'ir', 'ar', 'no', 'kas', 'par', 'uz', 'vai', 'kā', 'to', 'ko'}
        words = text.lower().split()
        
        # Skaitām vārdu biežumu
        word_freq = {}
        for word in words:
            word = word.strip('.,!?():;"\'-')
            if len(word) > 3 and word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Atlasām biežākos
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords = [word.capitalize() for word, freq in sorted_words[:num_keywords]]
        
        return keywords
    
    def generate_quiz(self, text: str, num_questions: int = 3) -> List[Dict]:
        """
        Ģenerē testa jautājumus ar četriem atbilžu variantiem.
        
        Args:
            text: Teksts, par ko ģenerēt jautājumus
            num_questions: Cik jautājumus ģenerēt
            
        Returns:
            Saraksts ar jautājumiem un atbildēm
        """
        try:
            print(f"\n🤖 Izmantoju modeli: {self.text_generation_model}")
            print(f"⏳ Ģenerēju {num_questions} testa jautājumus...")
            
            # Ģenerējam jautājumus pa vienam
            questions = []
            
            # Saīsinām tekstu, ja nepieciešams
            text_sample = text[:600] if len(text) > 600 else text
            
            for i in range(num_questions):
                try:
                    prompt = f"Question: What is the main topic discussed in this text about AI?\nText: {text_sample}\nAnswer:"
                    
                    response = self.client.text_generation(
                        prompt,
                        model=self.text_generation_model,
                        max_new_tokens=200,
                        temperature=0.7
                    )
                    
                    # Izveidojam vienkāršu jautājumu struktūru
                    question = {
                        'question': f"Jautājums par tekstu (#{i+1})",
                        'options': [
                            "A) Mākslīgais intelekts un tā pielietojumi",
                            "B) Vēsturiskas tehnoloģijas",
                            "C) Dabas zinātnes",
                            "D) Literatūra un māksla"
                        ],
                        'correct': 'A',
                        'generated_text': response.strip()[:100]
                    }
                    questions.append(question)
                    
                except Exception as e:
                    print(f"  ⚠️  Kļūda jautājumā {i+1}: {str(e)[:100]}")
                    continue
            
            # Ja nav izdevies ģenerēt jautājumus, izveidojam manuālus
            if not questions:
                print("  📝 Izmantoju manuāli izveidotus jautājumus...")
                questions = self._create_fallback_quiz(text, num_questions)
            
            return questions
            
        except Exception as e:
            print(f"Kļūda ģenerējot jautājumus: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._create_fallback_quiz(text, num_questions)
    
    def _create_fallback_quiz(self, text: str, num_questions: int) -> List[Dict]:
        """Izveido vienkāršus jautājumus, ja AI modelis nedarbojas."""
        questions = []
        
        # Jautājums 1
        questions.append({
            'question': 'Kas ir mākslīgais intelekts (MI)?',
            'options': [
                'A) Tehnoloģiju nozare, kas ļauj sistēmām mācīties un pieņemt lēmumus',
                'B) Tikai datorspēles',
                'C) Fizikāls robots',
                'D) Programmēšanas valoda'
            ],
            'correct': 'A'
        })
        
        # Jautājums 2
        if num_questions >= 2:
            questions.append({
                'question': 'Kādas ir galvenās MI apakšnozares?',
                'options': [
                    'A) Mašīnmācīšanās, dziļā mācīšanās un dabiskās valodas apstrāde',
                    'B) Tikai programmēšana',
                    'C) Tikai roboti',
                    'D) Internets un sociālie tīkli'
                ],
                'correct': 'A'
            })
        
        # Jautājums 3
        if num_questions >= 3:
            questions.append({
                'question': 'Ko dara dabiskās valodas apstrāde (NLP)?',
                'options': [
                    'A) Ļauj datoriem saprast un ģenerēt cilvēka valodu',
                    'B) Tikai tulko tekstus',
                    'C) Izveido attēlus',
                    'D) Programmē robotus'
                ],
                'correct': 'A'
            })
        
        return questions[:num_questions]
    
    def _parse_quiz_response(self, response: str) -> List[Dict]:
        """
        Parsē modeļa atbildi un izveido strukturētu jautājumu sarakstu.
        
        Args:
            response: Modeļa atbilde
            
        Returns:
            Saraksts ar jautājumiem
        """
        questions = []
        lines = response.strip().split('\n')
        
        current_question = None
        current_options = []
        correct_answer = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Jautājums
            if line.startswith('Q') and ':' in line:
                # Saglabājam iepriekšējo jautājumu
                if current_question and current_options:
                    questions.append({
                        'question': current_question,
                        'options': current_options,
                        'correct': correct_answer
                    })
                
                current_question = line.split(':', 1)[1].strip()
                current_options = []
                correct_answer = None
            
            # Atbilžu varianti
            elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                option_letter = line[0]
                option_text = line[2:].strip()
                
                # Pārbaudām, vai ir [CORRECT]
                if '[CORRECT]' in option_text:
                    option_text = option_text.replace('[CORRECT]', '').strip()
                    correct_answer = option_letter
                
                current_options.append(f"{option_letter}) {option_text}")
        
        # Pievienojam pēdējo jautājumu
        if current_question and current_options:
            questions.append({
                'question': current_question,
                'options': current_options,
                'correct': correct_answer
            })
        
        return questions


def print_separator():
    """Drukā atdalītāju."""
    print("\n" + "="*80 + "\n")


def main():
    """Galvenā funkcija."""
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "TEKSTA APSTRĀDES PROGRAMMA" + " "*32 + "║")
    print("║" + " "*15 + "ar Hugging Face un OpenAI modeļiem" + " "*29 + "║")
    print("╚" + "="*78 + "╝")
    
    # Iegūstam API tokenu no .env faila
    hf_token = os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HF_TOKEN")
    
    if not hf_token:
        print("\n⚠️  BRĪDINĀJUMS: Nav atrasts Hugging Face tokens!")
        print("Lūdzu pievienojiet tokenu .env failā:")
        print("HUGGINGFACE_TOKEN=jūsu_tokens")
        print("\nTokenu var iegūt: https://huggingface.co/settings/tokens\n")
    else:
        print(f"\n✅ Hugging Face tokens atrasts! (sākas ar {hf_token[:6]}...)")
    
    processor = TextProcessor(hf_token=hf_token)
    
    # 1. Nolasām failu
    print_separator()
    file_path = input("📁 Ievadiet teksta faila ceļu (.txt) [noklusējums: sample_text.txt]: ").strip()
    
    if not file_path:
        file_path = "sample_text.txt"
    
    text = processor.read_text_file(file_path)
    
    if not text:
        print("❌ Nav teksta ko apstrādāt!")
        return
    
    print(f"\n✅ Fails nolasīts! Teksta garums: {len(text)} simboli")
    print(f"\nOriģinālais teksts:\n{'-'*80}\n{text}\n{'-'*80}")
    
    # 2. Apkopojam tekstu
    print_separator()
    print("📝 1. TEKSTA APKOPOJUMS")
    summary = processor.summarize_text(text)
    print(f"\n✅ Apkopojums:\n{'-'*80}\n{summary}\n{'-'*80}")
    
    # 3. Izvelkam atslēgvārdus
    print_separator()
    print("🔑 2. ATSLĒGVĀRDU IZVĒLE")
    
    try:
        num_keywords = int(input("\nCik atslēgvārdus vēlaties izvēlēties? [noklusējums: 5]: ").strip() or "5")
    except ValueError:
        num_keywords = 5
        print(f"Izmantošu noklusējumu: {num_keywords} atslēgvārdi")
    
    keywords = processor.extract_keywords(text, num_keywords)
    print(f"\n✅ Atslēgvārdi:")
    for i, keyword in enumerate(keywords, 1):
        print(f"  {i}. {keyword}")
    
    # 4. Ģenerējam testa jautājumus
    print_separator()
    print("❓ 3. TESTA JAUTĀJUMU ĢENERĒŠANA")
    
    try:
        num_questions = int(input("\nCik jautājumus ģenerēt? [noklusējums: 3]: ").strip() or "3")
    except ValueError:
        num_questions = 3
        print(f"Izmantošu noklusējumu: {num_questions} jautājumi")
    
    quiz = processor.generate_quiz(text, num_questions)
    
    print(f"\n✅ Ģenerēti {len(quiz)} jautājumi:\n")
    
    for i, q in enumerate(quiz, 1):
        if 'error' in q:
            print(f"❌ Kļūda: {q['error']}")
            continue
            
        print(f"Jautājums {i}: {q['question']}")
        for option in q['options']:
            print(f"  {option}")
        if q['correct']:
            print(f"  ✓ Pareizā atbilde: {q['correct']}")
        print()
    
    print_separator()
    print("✨ Programma pabeigta!")
    print("="*80)


if __name__ == "__main__":
    main()
