"""Query expansion service for improving search recall."""

ABBREVIATION_MAP = {
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

    "PCA": "principal component analysis",
    "SVM": "support vector machine",
    "GMM": "gaussian mixture model",
    "HMM": "hidden markov model",
    "MCMC": "markov chain monte carlo",
    "MLE": "maximum likelihood estimation",
    "MAP": "maximum a posteriori",
    "ODE": "ordinary differential equation",
    "PDE": "partial differential equation",

    "HPC": "high performance computing",
    "IOT": "internet of things",
    "OS": "operating systems",
    "DB": "database",
    "API": "application programming interface",
    "P2P": "peer to peer",

    "NMR": "nuclear magnetic resonance",
    "fMRI": "functional magnetic resonance imaging",
    "EEG": "electroencephalography",
    "DNA": "deoxyribonucleic acid",
    "RNA": "ribonucleic acid",
    "CRISPR": "clustered regularly interspaced short palindromic repeats",

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

    additions = set()
    for word in words:
        clean_word = word.strip('.,!?()[]{}')
        if clean_word in ABBREVIATION_MAP:
            additions.add(ABBREVIATION_MAP[clean_word])

    if additions:
        expanded = f"{query} {' '.join(sorted(additions))}"

    return expanded
