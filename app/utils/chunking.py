import re
from typing import List, Dict
from app.utils.timestamp import parse_timestamp_to_secs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

TS_RE = re.compile(r"\[(\d{2}:\d{2}:\d{2})\]")

def extract_blocks(raw_text: str) -> List[Dict]:
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    blocks = []
    for line in lines:
        m = TS_RE.match(line)
        if m:
            ts = m.group(1)
            text = TS_RE.sub("", line, count=1).strip()
            blocks.append({"start": parse_timestamp_to_secs(ts), "text": text})
        else:
            if blocks:
                blocks[-1]["text"] += " " + line
            else:
                blocks.append({"start": 0, "text": line})
    # assign end times (next start or +30s)
    for i in range(len(blocks)):
        start = blocks[i]["start"]
        end = blocks[i+1]["start"] if i+1 < len(blocks) else start + 30
        blocks[i]["end"] = end
    return blocks

def blocks_to_documents(blocks: List[Dict], chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    stitched = []
    for b in blocks:
        stitched.append(f"[[TS:{b['start']}]] {b['text']}")
    big = "\n".join(stitched)
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    parts = splitter.split_text(big)
    docs: List[Document] = []
    for p in parts:
        ts = re.findall(r"\[\[TS:(\d+)\]\]", p)
        if ts:
            start = int(ts[0])
            end = int(ts[-1])
        else:
            start = 0
            end = 0
        clean = re.sub(r"\[\[TS:\d+\]\]", "", p).strip()
        docs.append(Document(page_content=clean, metadata={"start": start, "end": end}))
    return docs
