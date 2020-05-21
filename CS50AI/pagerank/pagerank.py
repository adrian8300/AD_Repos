import os
import random
import re
import sys

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

    # get all links for given page
    links = corpus[page]

    # initiate len vars 
    N_pages = len(corpus)
    N_links = len(links)

    # if page has no links assume all pages equally likely
    if N_links == 0:
        rand_page_prob = 1 / N_pages
    else:
        rand_page_prob = (1 - damping_factor) / N_pages
        rand_link_prob = damping_factor / N_links

    # initiate probability distribution dictionary
    prob_dist = {}

    # calc prob of each page being visited
    for next_page in corpus:
        next_page_prob = rand_page_prob
        if next_page in links:
            next_page_prob += rand_link_prob
         
        prob_dist[next_page] = next_page_prob

    return prob_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # random page select
    page_select = random.choice(list(corpus))

    # initiate page rank dicts
    PageRank = {}
    for page in corpus:
        PageRank[page] = 0

    # iterate n random samples
    for _ in range(n):
        random_num = random.uniform(0, 1)
        trans_model = transition_model(corpus, page_select, damping_factor)
        cum_prob = 0
        for page in trans_model:
            cum_prob += trans_model[page]
            if random_num < cum_prob:
                page_select = page
                PageRank[page] += 1
                break

    for page in PageRank:
        PageRank[page] = PageRank[page] / n
    
    return PageRank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    PageRank = {}
    N_pages = len(corpus)

    # initiate list of pages that have sufficient rounding preciseness 
    rounded = []
    
    # initiate page ranks
    for page in corpus:
        PageRank[page] = 1/N_pages

    # do this until all pages are in the rounded list
    while len(rounded) < N_pages:
        for page in PageRank:

            x = 0
            for corp in corpus:
                if len(corpus[corp]) == 0:
                    x += PageRank[corp] / N_pages
                elif page in corpus[corp]:
                    x += PageRank[corp] / len(corpus[corp])

            new_PageRank = (1 - damping_factor)/N_pages + damping_factor * x
            
            if page not in rounded:
                if abs(new_PageRank - PageRank[page]) < 0.001:
                    rounded.append(page)
            
            PageRank[page] = new_PageRank
            
    return PageRank

if __name__ == "__main__":
    main()
