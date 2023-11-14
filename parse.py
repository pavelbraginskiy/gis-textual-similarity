import re

prelude = re.compile(r'^.*?\*{3}.*?\*{3}', re.DOTALL)
postlude = re.compile(r'\*{3}.*?\*{3}.*?$', re.DOTALL)
paragraph_break = re.compile(r'\n\s*\n')

def paragraphs(file: str) -> [str]:
    with open(file, 'r', encoding='UTF-8') as r:
        data = r.read()
    data = prelude.sub('', data)
    data = postlude.sub('', data)
    chunks = paragraph_break.split(data)
    chunks = [i.strip().lower() for i in chunks]
    return chunks