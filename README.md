# scripts
helpful scripts; file handling / pdf gen / other


## Features

- **Image Manipulation**: Convert, edit, and process various image formats.
- **Document Handling**: Create and modify Word, Excel, and PowerPoint files.
- **AI Interaction**: Easily interact with ChatGPT and Claude AI for natural language processing.
- **PDF Manipulation**: Generate, read, and manipulate PDF files.


## Project Setup

This project is managed using **Poetry**. To get started, you'll need to install Poetry and set up the environment.

### 1. Install Poetry

If you don't have Poetry installed, you can install it by running:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install dependancies

```bash
poetry install
```

This will set up a virtual environment and install all the required libraries specified in the pyproject.toml.

### 3. Activate the Virtual Environment
```bash
poetry shell
```

### Libraries included

#### Image Manipulation

1. Pillow

Pillow is a powerful Python Imaging Library (PIL) fork used for opening, manipulating, and saving many different image formats.

```python
from PIL import Image

# Open an image
img = Image.open("image.jpg")
img = img.resize((200, 200))  # Resize the image
img.save("resized_image.jpg")
```

2. opencv-python
import cv2

```python
# Read an image
img = cv2.imread("image.jpg")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
cv2.imwrite("gray_image.jpg", gray_img)
```

3. scikit-image

```python
from skimage import io, filters

# Load an image
img = io.imread("image.jpg")
edges = filters.sobel(img)  # Apply an edge detection filter
io.imsave("edges_image.jpg", edges)
```

4. imageio
a simple library to read and write a wide range of image formats, including animated images (GIFs).

```python
import imageio

# Read an image
img = imageio.imread("image.jpg")
imageio.imwrite("new_image.jpg", img)  # Save it to a new file
```

#### Document handling (Word/Excel/PowerPoint)

1. python-docx
A library for creating, reading and modifying Word docs
```python
from docx import Document

# Create a new Word document
doc = Document()
doc.add_heading("Title", 0)
doc.add_paragraph("This is a paragraph.")
doc.save("document.docx")
```

2. openpyxl
a lib for read / write excel 
```python
from openpyxl import Workbook

# Create a new Excel workbook and add a sheet
wb = Workbook()
ws = wb.active
ws['A1'] = "Hello, Excel!"
wb.save("spreadsheet.xlsx")
```

3. python-pptx
a library for creating and manipulating pptx
```python
from pptx import Presentation

# Create a new PowerPoint presentation
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Presentation Title"
prs.save("presentation.pptx")
```

#### AI Interaction

1. openai
chatgpt
```python
from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("API_KEY_OPENAI")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="What is the capital of France?",
  max_tokens=50
)

print(response.choices[0].text.strip())
```

2. anthropic
claude.ai
```python
from dotenv import load_dotenv
import os
import anthropic

anthropic_api_key = os.getenv("API_KEY_ANTHROPIC")
client = anthropic.Client(api_key=anthropic_api_key)

response = client.completion(
    prompt="What is the capital of France?",
    model="claude-1",
    max_tokens=50
)

print(response['completion'])
```

3. transformers
a popular library from hugging face that supports transformer-based models, including GPT, BERT and other state of the art NLP models
```python
from transformers import pipeline

# Load a pre-trained model for text generation
generator = pipeline('text-generation', model='gpt2')
result = generator("What is the capital of France?", max_length=50)

print(result[0]['generated_text'])
```

#### PDF Manipulation
1. PyPDF2
A python library for manipulating PDF files, such as merging, splitting, and rotating pages
```python
from PyPDF2 import PdfReader, PdfWriter

# Read a PDF file
reader = PdfReader("document.pdf")
writer = PdfWriter()

# Add all pages to the writer
for page in reader.pages:
    writer.add_page(page)

# Write the PDF to a new file
with open("merged_document.pdf", "wb") as output:
    writer.write(output)
```

2. reportlab
a library for generating pdf docs porgrammatically. Allows create complex layouts, charts, and vector graphics
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a PDF document
c = canvas.Canvas("document.pdf", pagesize=letter)
c.drawString(100, 750, "Hello, ReportLab!")
c.save()

3. pdfminer.six
A library for extracting text, images and metadata from PDF files.

```python
from pdfminer.high_level import extract_text

# Extract text from a PDF
text = extract_text("document.pdf")
print(text)
```

