import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    key = {}
    len_corp_key = len(corpus.keys())
    corp_key = corpus.keys()
    eq = round((float(1 - damping_factor) / len_corp_key), 5)
    for x in corp_key:
        key[x] = eq
    page_link = corpus[page]
    totLinks = len(page_link)
    if totLinks == 0:
        for x in key.keys():
            key[x] = key[x] + (damping_factor / len_corp_key)
        return key
    for x in page_link:
        key[x] = key[x] + (float(damping_factor / totLinks))
    return key




def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    key = {}
    len_corp_key = len(corpus.keys())
    corp_key = corpus.keys()
    ran = random.randint(0, len_corp_key - 1)
    ctr = 0
    initial = list(corp_key)[ran]
    for x in corp_key:
        key[x] = 0
    while ctr < n:
        ctr = ctr + 1
        key[initial] = key[initial] + 1
        ran = random.random()
        probability = transition_model(corpus, initial, damping_factor)
        for x in probability.keys():
            if probability[x] < ran:
                ran = ran - probability[x]
            else:
                initial = x
                break
    norm = sum(key.values())
    for x in key.keys():
        key[x] = round(key[x] / norm, 5)
    return key



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = {}
    len_corp_key = len(corpus.keys())
    corp_key = corpus.keys()
    for x in corpus.keys():
        PageRank[x] = float(1 / len_corp_key)
    ctr2 = 0
    while not ctr2:
        copy_dict = {}
        ctr2 = 1
        for x in PageRank.keys():
            tmp = PageRank[x]
            copy_dict[x] = float((1 - damping_factor) / len_corp_key)
            for page,link in corpus.items():
                if x in link:
                    copy_dict[x] = copy_dict[x] + float(damping_factor * PageRank[page] / len(link))
            if abs(tmp - copy_dict[x]) > 0.001:
                ctr2 = 0
        for y in PageRank.keys():
            PageRank[y] = copy_dict[y]
    return PageRank

if __name__ == "__main__":
    main()
