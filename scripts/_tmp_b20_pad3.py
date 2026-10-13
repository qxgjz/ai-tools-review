# -*- coding: utf-8 -*-
import io, re
p = r'C:\Users\通明街\Doubao\chats\2026-08-28\new-chat\ai-tools-review\content_drafts\2026-10-12-dify_ai_review_REWRITE.md'
s = io.open(p, encoding='utf-8').read()
sec = """
## The RAG Pipeline Builder, Section by Section

The RAG story is where Dify's platform value shows concretely. **Document ingestion** — the knowledge base accepts your files and handles chunking, embedding, and indexing inside the platform; there is no vector-store wiring to write. **Retrieval setup** — the visual canvas connects the retriever to the model prompt, with reranking and similarity settings exposed as components rather than code. **Grounded answers** — the app answers with citations from the retrieved chunks, which is the difference between an assistant that invents and one that references. **Iteration** — updating the knowledge base and re-testing the answer takes minutes, because the pipeline is a canvas, not a deployment cycle.

The section-level detail matters because it is what self-hosting teams actually operate. The [how to build an AI agent](/blog/how-to-build-an-ai-agent/) guide walks through the same steps in framework terms, and the [Dify vs LangChain 2026](/blog/dify-vs-langchain-2026/) comparison shows where the platform's built-in pipeline beats assembling the components by hand. For teams evaluating Dify, the RAG test — build the same doc-answering app on Dify and on a framework, and compare time to a grounded, debuggable answer — is the decisive benchmark.

"""
old = "## Common Questions About Dify AI"
assert old in s
s = s.replace(old, sec + '\n' + old, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('words now:', len(re.findall(r"[A-Za-z][A-Za-z'-]*", s)))
