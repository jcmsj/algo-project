from pyscript import document
from kmp import kmp_search
from split import split_string, highlight, timer
from rk import rabin_karp
from boyer import boyer_moore
import time
import sys
textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
selectElement = document.querySelector("#Algorithms")
modeElement = document.querySelector("#modes")
matchElement = document.querySelector("#n")
matchesElement = document.querySelector("#matches")

def showMatches(result:list[str]):
    matchesElement.innerHTML += f"<div>{len(result)}</div>"
def run(algo, text:str, pattern:str, n:int, *args):
    start = time.perf_counter()
    result = algo(text, pattern, n, *args)
    stop = time.perf_counter()
    duration = stop - start
    timer(duration)
    parts = split_string(text, pattern, result)
    print(parts)
    highlight(parts)
    showMatches(result)
    
def run_dna(algo, text:str, pattern:str, n:int, *args):
    # normal
    run(algo, text, pattern, n, *args)
    # reversed
    inverted = pattern[::-1]
    run(algo, text, inverted, n, *args)
    # replaced
    spliced = []
    for char in patternElement.value:
        if char == "A":
            spliced.append("T")
        elif char == "C":
            spliced.append("G")
        elif char == "T":
            spliced.append("A")
        elif char == "G":
            spliced.append("C")
        else:
            spliced.append(char)
    replaced = "".join(spliced)
    replaced_inverted = replaced[::-1]
    run(algo, text, replaced, n, *args)
    run(algo, text, replaced_inverted, n, *args)
def start_search(event):
    outputElement = document.querySelector(".output")
    outputElement.innerHTML = ''
    matchesElement.innerHTML = ''
    timerElement = document.querySelector(".timer")
    timerElement.innerHTML = 'Time: '
    
    if not matchElement.value.isdigit():
        matchElement.value = sys.maxsize
    elif matchElement.value == '0':
        matchElement.value = sys.maxsize
    matches = int(matchElement.value)   

    if (selectElement.value == "Knuth-Morris-Pratt"):
        if modeElement.value == "Standard":
            run(kmp_search, textElement.value, patternElement.value, matches)
        elif (modeElement.value == "DNA"):
            run_dna(kmp_search, textElement.value, patternElement.value, matches)
    elif (selectElement.value == "Boyer-Moore"):
        if modeElement.value == "Standard":
            run(boyer_moore, textElement.value, patternElement.value, matches)
        elif modeElement.value == "DNA":
            alphabet = 'ACTG'
            run_dna(boyer_moore, textElement.value, patternElement.value, matches, alphabet)
    elif (selectElement.value == "Rabin-Karp"):
        if modeElement.value == "Standard":
            run(rabin_karp, textElement.value, patternElement.value, matches)
        elif (modeElement.value == "DNA"):
            run_dna(rabin_karp, textElement.value, patternElement.value, matches)
