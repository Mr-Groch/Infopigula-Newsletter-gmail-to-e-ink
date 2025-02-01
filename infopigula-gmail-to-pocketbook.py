# coding=utf-8

# Adres e-mail urządzenia (Send-to-Pocketbook lub Send-to-Kindle)
E_INK_DEVICE_EMAIL = "mr_groch-era-color@pbsync.com"

# Nazwa etykiety, po której należy szukać nieprzeczytanych newsletterów Infopiguły do wysyłki
GMAIL_INFOPIGULA_LABEL = "Infopiguła"
# Nazwa nadawcy maila
GMAIL_SENDER = "grocholski@gmail.com"

# Czy generować epub za pomocą ebooklib czy pypub3?
USE_EBOOKLIB = False

from simplegmail import Gmail
from unidecode import unidecode
import os
import re
if (USE_EBOOKLIB):
  import uuid
  from ebooklib import epub
  from ebooklib.plugins import standard
else:
  import pypub
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from bs4 import BeautifulSoup
import copy

# Szukanie nieprzeczytanych maili z ustaloną etykietą newslettera
gmail = Gmail(noauth_local_webserver=True)
labels = gmail.list_labels()
infopigula_label = list(filter(lambda x: x.name == GMAIL_INFOPIGULA_LABEL, labels))[0]
messages = gmail.get_unread_inbox(labels=[infopigula_label])

for message in messages:
  # Nazwa pliku i tytuł z tematu newslettera
  subject = message.subject
  matches = re.search(r"] (.+)", subject, re.I)
  if matches:
    subject = matches.group(1)
  filename = f"Infopigula - {unidecode(subject)}.epub"
  
  # Nałożenie tytułu na okładkę
  img = Image.open("cover-template.png")
  draw = ImageDraw.Draw(img)
  fnt = ImageFont.truetype("NotoSans-Bold.ttf", 28)
  W, H = (632, 40)
  _, _, w, h = draw.textbbox((0, 0), subject, font=fnt)
  draw.text(((W-w)/2, (H-h)/2), subject, font=fnt, fill=(0, 0, 0))
  draw.text(((W-w)/2, 800-(H-h)/2), subject, font=fnt, fill=(0, 0, 0))
  img.save("cover.png")
  
  # Wydzielenie rozdziałów z treści newslettera do osobnych html'i
  chapters = []
  soup = BeautifulSoup(message.html, "html.parser")
  sections = soup.find_all("h2", class_="newsletter-header-label")
  if not sections:
    # Jak nie znaleziono rozdziałów to zostawiamy wszystko w jednym pliku
    chapters.append((soup.prettify(), "Infopiguła - Newsletter", "newsletter.xhtml"))
  else:
    # Wszystko przed pierwszym rozdziałem jest "wstępem"
    intro_soup = BeautifulSoup("", "html.parser")
    for element in sections[0].previous_siblings:
      intro_soup.insert(0, copy.copy(element))
    chapters.append((intro_soup.prettify(), "Wstęp", "intro.xhtml"))
    # Kolejne rozdziały
    for i, header in enumerate(sections):
      section_soup = BeautifulSoup("", "html.parser")
      # pypub3 dodaje nazwę rozdziału automatycznie, więc nie trzeba kopiować nagłówka z nazwą
      if (USE_EBOOKLIB):
        section_soup.append(copy.copy(header))
      for element in header.next_siblings:
        if element in sections:
          break
        section_soup.append(copy.copy(element))
      chapters.append((section_soup.prettify(), header.get_text(strip=True).capitalize(), f"{i}_{unidecode(header.get_text(strip=True).lower()).replace(' ', '-')}.xhtml"))
  
  # Generowanie pliku epub przez ebooklib
  if (USE_EBOOKLIB):
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(subject)
    book.set_language("pl")
    book.add_author("Infopiguła")
    book.set_cover("cover.png", open("cover.png", "rb").read())
    toc = ()
    spine = []
    for chapter in chapters:
      c = epub.EpubHtml(title=chapter[1], file_name=chapter[2], lang="pl")
      c.set_content(chapter[0])
      book.add_item(c)
      toc += (c, )
      spine.append(c)
    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["cover", "nav"] + spine
    epub.write_epub(filename, book, {'plugins': [standard.SyntaxPlugin()]})
  # Generowanie pliku epub przez pypub3
  else:
    epub = pypub.Epub(subject, "Infopiguła", "pl", cover="cover.png")
    for chapter in chapters:
      c = pypub.create_chapter_from_html(chapter[0].encode(), chapter[1])
      epub.add_chapter(c)
    epub.create(filename)
  
  # Wysyłka maila na czytnik
  params = {
    "to": E_INK_DEVICE_EMAIL,
    "sender": GMAIL_SENDER,
    "subject": subject,
    "attachments": [filename]
  }
  gmail.send_message(**params).trash()
  # Czyszczenie i usuwanie newslettera z gmaila
  os.remove(filename)
  message.mark_as_read()
  message.trash()
