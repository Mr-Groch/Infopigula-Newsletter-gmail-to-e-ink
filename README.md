# Infopigula-Newsletter-gmail-to-e-ink
Generowanie pliku ePub z newslettera Infopiguły i wysyłka go na czytnik (Pocketbook lub Kindle)

Wykorzystuje:
- [Python 3](https://www.python.org/)
- [simplegmail](https://github.com/jeremyephron/simplegmail) - **Koniecznie musisz zapoznać się z instrukcją jak podpiąć się pod swojego gmaila! Zmień także stan publikacji OAuth z testowanie na produkcja, by uniknąć reautoryzacji co 7 dni**
- [ebooklib](https://github.com/aerkalov/ebooklib) lub [pypub3](https://github.com/imgurbot12/pypub) - do wyboru, można sobie porównać generowany ePub i wybrać bardziej nam odpowiadający
- [Pillow](https://python-pillow.github.io/) - do generowania okładki
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - do podziału na rozdziały

Z instalacją i konfiguracją poradzić musisz sobie sam - jak napisałeś kiedyś jakiś skrypt w Pythonie to dasz sobie radę ;) Najważniejsze jest zapoznanie się z dokuemntacją modułu simplegmaila, by podpiąć się ze swoim gmailem. Zalecane odpalanie w jakimś harmonogramie (np crontab), by zautomatyzować sobie wysyłkę newslettera na czytnik ;) 

![IMG_20250201_140324 jpg_compressed](https://github.com/user-attachments/assets/1cef1179-7fa4-4c2b-9993-e127ccefc87d)
![IMG_20250201_140354 jpg_compressed](https://github.com/user-attachments/assets/58bd8f7a-4e03-4939-9337-e4ff9c858b3f)
![IMG_20250201_140436 jpg_compressed](https://github.com/user-attachments/assets/dd4711f3-61c5-460f-a88a-de3cb4d9c86c)
