"""
Automatizēts tests programmas pamatfunkcionalitātei.
"""

from main import TextProcessor


def test_basic_functionality():
    """Testē pamata funkcionalitāti."""
    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "AUTOMATIZĒTS TESTS" + " "*35 + "║")
    print("╚" + "="*78 + "╝\n")
    
    # Inicializējam procesoru
    processor = TextProcessor()
    
    # Testējam faila lasīšanu
    print("1️⃣  Testēju faila lasīšanu...")
    text = processor.read_text_file("sample_text.txt")
    
    if text:
        print(f"✅ Fails nolasīts! Garums: {len(text)} simboli\n")
        print(f"Pirmie 100 simboli: {text[:100]}...\n")
    else:
        print("❌ Neizdevās nolasīt failu!\n")
        return
    
    # Testējam apkopojumu
    print("2️⃣  Testēju teksta apkopošanu...")
    print("   (Tas var aizņemt dažas sekundes...)\n")
    try:
        summary = processor.summarize_text(text)
        print(f"✅ Apkopojums iegūts!")
        print(f"   Apkopojuma garums: {len(summary)} simboli\n")
    except Exception as e:
        print(f"❌ Kļūda apkopojumā: {e}\n")
    
    # Testējam atslēgvārdus
    print("3️⃣  Testēju atslēgvārdu izvēli...")
    print("   (Tas var aizņemt dažas sekundes...)\n")
    try:
        keywords = processor.extract_keywords(text, 5)
        print(f"✅ Atslēgvārdi iegūti: {len(keywords)}")
        for i, kw in enumerate(keywords, 1):
            print(f"   {i}. {kw}")
        print()
    except Exception as e:
        print(f"❌ Kļūda atslēgvārdos: {e}\n")
    
    # Testējam jautājumu ģenerēšanu
    print("4️⃣  Testēju testa jautājumu ģenerēšanu...")
    print("   (Tas var aizņemt ilgāku laiku...)\n")
    try:
        quiz = processor.generate_quiz(text, 2)
        print(f"✅ Jautājumi ģenerēti: {len(quiz)}\n")
        
        for i, q in enumerate(quiz, 1):
            if 'error' in q:
                print(f"❌ Kļūda jautājumā {i}: {q['error']}")
                continue
            
            print(f"Jautājums {i}:")
            print(f"   {q.get('question', 'Nav jautājuma')}")
            if 'options' in q:
                for opt in q['options']:
                    print(f"      {opt}")
            print()
    except Exception as e:
        print(f"❌ Kļūda jautājumos: {e}\n")
    
    print("="*80)
    print("✨ Tests pabeigts!")
    print("="*80)


if __name__ == "__main__":
    test_basic_functionality()
