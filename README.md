### Test case liberator.

### Beskrivning:

Test Case Liberator är ett Pythonbaserat konsolprogram för att registrera och visa testfall. Programmet gör det möjligt för användaren att skapa testfall med tillhörande information och därefter visa en sammanställning eller öppna enskilda testfall för att granska deras innehåll.

Registrerade testfall lagras i programmets minne under den aktuella körningen. Informationen sparas inte permanent, vilket innebär att registrerade testfall försvinner när programmet avslutas.

### Centrala delar:

Programmet är uppbyggt med en uppdelning mellan användargränssnitt, servicelager, datamodeller och datalagring.

**TestCaseDialog**: Hanterar programmets menyer, användarinmatning och presentation av information.

**ConsoleHelper**: Innehåller hjälpfunktioner för konsolhantering, exempelvis rensning av skärmen, paus och kontroll av obligatorisk inmatning.

**TestCaseService**: Hanterar programmets affärslogik och validerar information innan ett nytt testfall skapas.

**TestCaseRepository**: Ansvarar för att lagra och hämta registrerade testfall från en intern lista.

**TestCase**: Representerar ett registrerat testfall och dess tillhörande information.

**CreateTestCaseDto**: Används för att överföra information från användargränssnittet till servicelagret.

**CreateTestCaseResult** / **GetTestCaseResult**: Resultatklasser som används för att returnera information från servicelagret.

### Design reflektion:

I början av utvecklingen gjordes valet att dela upp funktionaliteten i olika filer och mappar för att skapa en tydlig struktur som är i enighet med single responsible principle. Var sak har sitt ansvarsområde, som i sin tur påverkar systemets läsbarhet, underhållbarhet och testbarhet positivt.

**Diagrams** innehåller klass, aktivitets- och sekvensdiagram som tillhör systemet.

**Dialogs** innehåller systemets användargränssnitt.

**Models** innehåller systemets modeller.

**Repository** innehåller systemets lagring.

**Services** innehåller systemets logik, normalisering och validering.

**Tests** innehåller de enhetstester som tillhör systemet.

**Utils** innehåller funktionalitet som hjälper konsolhanteringen.

**Main** innehåller programmets startpunkt.

### Mappstruktur:

```
Test Case Liberator/
|
|── main.py
|
├── diagrams/
│   ├── activity_diagram_register_test_case_detailed.puml
│   ├── activity_diagram_register_test_case_simple.puml
│   ├── class_diagram_test_case_liberator_new.puml
│   ├── class_diagram_test_case_liberator_old.puml
│   └── sequence_diagram_register_test_case.puml
│
├── dialogs/
│   └── tc_dialog.py
│
├── models/
│   ├── tc_create_test_case_dto.py
│   ├── tc_create_test_case_result.py
│   ├── tc_get_test_case_result.py
│   ├── tc_precondition.py
│   ├── tc_step.py
│   ├── tc_test_case.py
│   └── tc_test_data.py
│
├── repository/
│   └── tc_repository.py
│
├── services/
│   └── tc_service.py
│
├── tests/
│   ├── conftest.py
│   ├── test_tc_dialog_and_tc_console_helper.py
│   ├── test_tc_repository.py
│   ├── test_tc_service.py
│   └── test_tc_test_case_and_dto.py
│
├── utils/
│   └── tc_console_helper.py
```

### Funktionalitet:

Programmet erbjuder följande funktioner:

Registrera nya testfall.

Validera att obligatoriska uppgifter har fyllts i.

Visa en sammanställning av registrerade testfall.

Öppna och granska enskilda testfall.

### Starta programmet:

Ladda ner eller klona projektet till din dator.

Öppna projektmappen i exempelvis Visual Studio Code.

Öppna terminalen i projektets rotmapp.

Starta programmet genom att köra:

python main.py

### Begränsningar:

Programmet är en grundläggande implementation och har för närvarande stöd för att skapa och läsa testfall (Create och Read). Det finns ännu ingen funktionalitet för att uppdatera eller ta bort registrerade testfall. All data lagras endast under programmets aktuella körning.

### Testning:

Samtliga klasser som började med ordet Test har fått en ändring.
Jag trodde att problemet med att döpa om filerna till exempelvis tc_test_case skulle lösa problemet inför testning.
Det jag inte tänkte på var att pytest läser in klasserna i .py filerna, så TestCase utlöste en varning om att den hade en egen __init__ konstruktor. Eftersom den läste av dem som Test-klasser.
Lösningen till detta var att lägga till __test__ = False på de klasser som påverkades.

### Sammanfattning av Testning

**TestCaseRepository** - Lagring, hämtning och kopiering av listan.

**TestCaseService** - Registrering, validering, hämtning och indexbaserad sökning.

**TestCaseDialog** - Visning av testfall, navigering, detaljvy och registrering.

**ConsoleHelper** - Inmatnning, trimmning av blanksteg och hantering av tomma värden.

**TestCase** - Skapandet av testfall och överföring av data från DTO.

**CreateTestCaseDto** - testas indirekt genom tester av dialogens och servicens hantering av DTO-objektet.

**CreateTestCaseResult** - Testas indirekt genom servicetester som verifierar resultatet av registrering av testfall.

**GetTestCaseResult** - Testas indirekt genom seerrvicetester som verifierar resultatet av hämtning av testfall.
