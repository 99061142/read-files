from time import sleep

readme_text = open("README.md", "r").read() # Readme text
sentences = readme_text.splitlines() # List with all the sentences of the readme file

# Show every sentence
for sentence in sentences:
    print(sentence)
    sleep(1)