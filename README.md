# KYC Name Screening Tool (Sanctions and PEP check)

A Python app that checks customer names against a **sanctions list** and a **PEP list** (Politically Exposed Persons) using **fuzzy matching**.

## Why fuzzy matching?
Names are written in many ways. "Mohamad Al Hasan" and "Mohammad Al Hassan" are the same person, but a normal exact search will not find the match. Fuzzy matching gives a **similarity score** from 0 to 100, so the tool can find similar names too.

## How it works
1. **Normalise** the name: lowercase, remove accents and punctuation.
2. **Compare** it with every name in the watchlist (RapidFuzz: `token_sort_ratio` and `token_set_ratio`). This works even if the word order is different or a middle name is missing.
3. **Classify** the best score:

| Score | Status | Meaning |
|---|---|---|
| 85 or more | HIT | Very similar. A human must check. |
| 70 to 84 | POSSIBLE | Maybe. Check by hand. |
| under 70 | CLEAR | No match. |

## Tools
Python 3, pandas, RapidFuzz, Streamlit

## How to run
```bash
pip install -r requirements.txt

python screening.py        # screens customers.csv, makes screening_report.csv
streamlit run app.py       # opens the web page
python test_screening.py   # runs the tests
```

## The web page
- **Tab 1:** type one name and see the top 5 matches
- **Tab 2:** check a whole customer CSV, see HIT / POSSIBLE / CLEAR counts, download the report
- Sidebar: upload your own watchlist

## Use a real list (optional)
The file `sanctions_sample.csv` has **made-up names** for the demo. To test with real public data, download a free list from [OpenSanctions](https://www.opensanctions.org/datasets/) as CSV, keep the columns `name` and `list_type`, and upload it in the sidebar. Check their license terms first.

## Files
| File | What it does |
|---|---|
| `screening.py` | Core logic (normalise, score, classify) |
| `app.py` | Streamlit web page |
| `test_screening.py` | Tests |
| `sanctions_sample.csv` | Fake watchlist |
| `customers.csv` | Fake customers |

## Limits (good to say in an interview)
- Only compares names. Real systems also use date of birth, country and ID numbers to reduce false alarms.
- Fuzzy matching creates **false positives**. That is why a HIT goes to a human, and the tool does not block anyone alone.
- Thresholds (85 and 70) are examples and should be tuned with real data.

## Important
All data is **fake**. Names in the sample lists are made up.
