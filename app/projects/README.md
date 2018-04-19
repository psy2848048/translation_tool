# docx 활용하기

## docx 문서 만들기

[마이캣툴 API](https://docs.google.com/document/d/1TsqcnW4W-_cK1vxvjQGAw5ib5F0qjAyrwJ4HTAYb_JI/edit?usp=sharing) `번역내용 파일로 다운로드` 만들어 두었습니다.
예: https://localhost:5001/api/v1/toolkit/workbench/docs/236/output?type=docx

현재는 원문의 글씨체 적용 전혀 없이 텍스트로만 출력됩니다..

- 참조할 함수
  - app/workbench/controllers.py
    - output_doc_to_file
  - app/workbench/models.py
    - export_doc
    - write_file_in_requested_format






## docx 문서 읽기

[마이캣툴 API](https://docs.google.com/document/d/1TsqcnW4W-_cK1vxvjQGAw5ib5F0qjAyrwJ4HTAYb_JI/edit?usp=sharing) `문서 추가` 만들어 두었습니다. 

Paragraph(일반 텍스트)만 인식되는 기본 적인 형태이며, 표나 하이퍼링크 이런건 안되는 상태입니다.

```python
from flask import request
from io import BytesIO
from docx import Document
import nltk


file = request.files.get('file', None)

file_bin = file.read()
source_stream = BytesIO(file_bin)
document = Document(source_stream)
source_stream.close()

sentences = []
# 파일에서 문장 꺼내기
for para in document.paragraphs:
    if len(para.text) > 0:
        sentences.extend(nltk.data.load('tokenizers/punkt/english.pickle').tokenize(para.text))
```



```python
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell
from docx.table import Table as _Table
from docx.text.paragraph import Paragraph


def iter_block_items(parent):
    """
    Generate a reference to each paragraph and table child within *parent*,
    in document order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
        # print(parent_elm.xml)
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def table_print(block):
    t = block
    for row in t.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                print(paragraph.text, '  ', end='')
                # y.write(paragraph.text)
                # y.write('  ')
        print("\n")

for block in iter_block_items(document):
    if isinstance(block, Paragraph):
        print(block.text)
    elif isinstance(block, _Table):
        table_print(block)
```





> 참조
>
> - https://python-docx.readthedocs.io/en/latest/

