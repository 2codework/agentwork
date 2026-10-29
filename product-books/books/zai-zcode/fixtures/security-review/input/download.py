from pathlib import Path
def load(root,name):
    return (Path(root)/name).read_text()
