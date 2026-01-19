"""Query expansion service for improving search recall."""

# Common research/academic abbreviations and their expansions
ABBREVIATION_MAP = {
    # Machine Learning & AI
    "ML": "machine learning",
    "DL": "deep learning",
    "AI": "artificial intelligence",
    "RL": "reinforcement learning",
    "NLP": "natural language processing",
    "CV": "computer vision",
    "GAN": "generative adversarial network",
    "CNN": "convolutional neural network",
    "RNN": "recurrent neural network",
    "LLM": "large language model",
    "AGI": "artificial general intelligence",

    # Statistics & Math
    "PCA": "principal component analysis",
    "SVM": "support vector machine",
    "GMM": "gaussian mixture model",
    "HMM": "hidden markov model",
    "MCMC": "markov chain monte carlo",
    "MLE": "maximum likelihood estimation",
    "MAP": "maximum a posteriori",
    "ODE": "ordinary differential equation",
    "PDE": "partial differential equation",

    # Systems & Networks
    "HPC": "high performance computing",
    "IOT": "internet of things",
    "OS": "operating systems",
    "DB": "database",
    "API": "application programming interface",
    "P2P": "peer to peer",

    # Biology & Health
    "NMR": "nuclear magnetic resonance",
    "fMRI": "functional magnetic resonance imaging",
    "EEG": "electroencephalography",
    "DNA": "deoxyribonucleic acid",
    "RNA": "ribonucleic acid",
    "CRISPR": "clustered regularly interspaced short palindromic repeats",

    # Security & Crypto
    "PKI": "public key infrastructure",
    "MPC": "multi-party computation",
    "ZKP": "zero knowledge proof",
}

def expand_query(query: str) -> str:
    """
    Expand abbreviations in a query to improve search recall.

    Args:
        query: The original search query

    Returns:
        Expanded query with abbreviations replaced/augmented
    """
    expanded = query
    words = query.upper().split()

    additions = set()  # Use set to avoid duplicates
    for word in words:
        # Check exact match (case-insensitive)
        clean_word = word.strip('.,!?()[]{}')
        if clean_word in ABBREVIATION_MAP:
            additions.add(ABBREVIATION_MAP[clean_word])

    if additions:
        expanded = f"{query} {' '.join(sorted(additions))}"

    return expanded
