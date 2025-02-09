from bs4 import BeautifulSoup
import re

def normalize_spacing(text):
  """Ensure space after periods when missing before lowercase letters"""
  text = re.sub(r'\.([a-zA-Z])', r'. \1', text)
  return re.sub(r'\n{3,}', '\n\n', text)

def insert_missing_paragraph_breaks(text):
  """
  It is safe to assume after a full stop, if whitespace is not present in the text, a new paragraph begins. 
  """
  # Look for a period directly followed by a non-whitespace character.
  return re.sub(r'\.(?=\S)', '.\n\n', text)

def clean_extracted_text(text):
  """
  Cleans the extracted text by removing lines that are weird i.e. chapter headers or navigation text. 
  """
  text = normalize_spacing(text)

  paragraphs = []
  current_para = []

  for line in text.splitlines():
    stripped = line.strip()
    if not stripped:
      if current_para:
        paragraphs.append(" ".join(current_para))
        current_para = []
      continue

    if any(re.match(p, stripped, re.I) for p in [
      r'^(Ch\.?\s*\d+)$',
      r'^(Chapter\s+\d+:?)$'
    ]):
      continue

    sentences = re.split(r'\. (?=[A-Z])', stripped)
    current_para.extend(sentences)
  
  if current_para:
    paragraphs.append(" ".join(current_para))
  
  cleaned_text = "\n\n".join(
    p.replace('. ', '.\n')
     .replace('  ', ' ')
     .strip()
    for p in paragraphs if p.strip()
  )
  return cleaned_text

def is_potential_navigation(div):
  """
  If the number of words is low in comparison to the number of links the div is likely
  to part of a navigation or footer element. 
  """
  text = div.get_text(separator=" ", strip=True)
  words = text.split()
  num_words = len(words)
  num_links = len(div.find_all("a"))
  if num_links and (num_words / num_links) < 3:
    return True
  return False

def extract_main_content(html):
  """
  Given HTML content, attempt to extract the main article body.
  First, it checks for candidate IDs or class names that are common
  for article content (e.g. "maincontent", "article-body", etc.).
  If none are found, it falls back to scanning all <div> elements and
  selecting the one with the largest block of text that does not appear
  to be navigational.
  """
  soup = BeautifulSoup(html, 'html.parser')

  # Remove generally rubbish tags
  for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

  # List of common identifiers used for the content of an article
  candidate_identifiers = [
    "maincontent", "article-body", "text-block", "main-content", "entry-content", "post-content"
  ]

  main_elem = None
  # Try finding by ID
  for candidate in candidate_identifiers:
    main_elem = soup.find(id=lambda x: x and candidate in x.lower())
    if main_elem:
      break

  # If not found try by class
  if not main_elem:
    for candidate in candidate_identifiers:
      main_elem = soup.find(class_=lambda c: c and candidate in c.lower())
      if main_elem:
        break

  # FALLBACK
  # Perhaps we should be keeping links within the text?
  if not main_elem:
    divs = soup.find_all("div")
    best_div = None
    max_text_length = 0
    for div in divs:
      for tag in div.find_all(["script", "style", "header", "footer", "iframe", "video"]):
        tag.decompose()
      text = div.get_text(separator="\n", strip=True)
      # Skip very short candidates
      if len(text) < 200:
        continue
      links = div.find_all("a")
      if links:
        words = text.split()
        if len(words) / len(links) < 3:
          continue
      if len(text) > max_text_length:
        max_text_length = len(text)
        best_div = div
    main_elem = best_div

  # LAST RESORT :(
  if not main_elem:
    main_elem = soup.find("body")
  
  for tag in main_elem.find_all(["script", "style", "nav", "header", "footer", "iframe", "video"]):
    tag.decompose()

  paragraphs = main_elem.find_all("p")
  if paragraphs:
    extracted_text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
  else:
    extracted_text = main_elem.get_text(separator="\n", strip=True)
  
  cleaned_text = clean_extracted_text(extracted_text)
  return cleaned_text