from file_tools import DocsCollection

"""
Docs available:
docs-lisa
news-group
npl
"""

def init():
    dc = DocsCollection("docs-lisa")
    print(dc[:10])

init()
