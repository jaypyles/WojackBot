def gather_prompt_text(filename):
    """Read from a textfile"""
    prompt = ""
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        prompt += line.strip()
    file.close()
    return prompt
