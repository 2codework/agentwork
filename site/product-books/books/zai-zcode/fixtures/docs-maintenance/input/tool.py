import argparse
p=argparse.ArgumentParser()
p.add_argument("--name",required=True)
a=p.parse_args()
print("Hello, "+a.name+"!")
