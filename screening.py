"""Name screening with fuzzy matching.
Compares a customer name with a sanctions / PEP list.
Fuzzy matching finds names that are SIMILAR, not only exactly the same.
Example: "Mohamad Al Hasan" can match "Mohammad Al Hassan".
"""
import re
import unicodedata
import pandas as pd
from rapidfuzz import fuzz

HIT_THRESHOLD = 85      # score >= 85  -> HIT (send to a human)
REVIEW_THRESHOLD = 70   # score 70-84  -> POSSIBLE (check by hand)


def normalize(name: str) -> str:
    """Lowercase, remove accents, remove punctuation, fix extra spaces."""
    name = unicodedata.normalize("NFKD", str(name))
    name = "".join(ch for ch in name if not unicodedata.combining(ch))
    name = re.sub(r"[^a-zA-Z\s]", " ", name.lower())
    return " ".join(name.split())


def match_score(a: str, b: str) -> float:
    """Best of 2 methods: token_sort (order of words does not matter)
    and token_set (works when one name has extra middle names)."""
    a, b = normalize(a), normalize(b)
    return max(fuzz.token_sort_ratio(a, b), fuzz.token_set_ratio(a, b))


def classify(score: float) -> str:
    if score >= HIT_THRESHOLD:
        return "HIT"
    if score >= REVIEW_THRESHOLD:
        return "POSSIBLE"
    return "CLEAR"


def screen_name(name: str, watchlist: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    """Returns the best matches in the watchlist for one name."""
    scores = watchlist["name"].apply(lambda w: match_score(name, w))
    result = watchlist.assign(match_score=scores.round(1))
    result = result.sort_values("match_score", ascending=False).head(top_n)
    result["status"] = result["match_score"].apply(classify)
    return result.reset_index(drop=True)


def screen_customers(customers: pd.DataFrame, watchlist: pd.DataFrame) -> pd.DataFrame:
    """Screens every customer, keeps the best match for each."""
    rows = []
    for _, c in customers.iterrows():
        best = screen_name(c["full_name"], watchlist, top_n=1).iloc[0]
        rows.append({
            "customer_id": c["customer_id"],
            "customer_name": c["full_name"],
            "best_match": best["name"],
            "list_type": best["list_type"],
            "match_score": best["match_score"],
            "status": best["status"],
        })
    return pd.DataFrame(rows).sort_values("match_score", ascending=False)


if __name__ == "__main__":
    watchlist = pd.read_csv("sanctions_sample.csv")
    customers = pd.read_csv("customers.csv")
    report = screen_customers(customers, watchlist)
    report.to_csv("screening_report.csv", index=False)
    print(report.to_string(index=False))
    print("\nSaved in screening_report.csv")
