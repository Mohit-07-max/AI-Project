"""Creates data/movies_sample.csv: SYNTHETIC movie plots, only so the project runs out of the box.

The text is generated from templates, so accuracy on it is NOT meaningful.
Replace it with a real dataset (see train.py --help) for real results.
"""

import csv
import random
from pathlib import Path

random.seed(42)
PER_GENRE = 140

GENRES = {
    "Action": dict(
        starts=["A retired soldier", "An undercover agent", "A former cop", "An elite pilot", "A rogue mercenary"],
        plots=["must stop {v} before the city is destroyed", "fights through an army of gunmen to rescue {x}",
               "races against time to defuse a bomb planted by {v}", "leads a dangerous mission to steal back {x} from {v}",
               "is hunted by assassins after a chase across three countries"],
        extra=["{v} and a team of fighters", "a fast car chase ends in a huge explosion", "a final brutal fight on a moving train"],
        v=["a ruthless terrorist", "a criminal mastermind", "a corrupt general", "a deadly cartel boss"],
        x=["a kidnapped scientist", "a stolen weapon", "his captured partner", "the president's daughter"],
        keywords=["explosion", "gun", "chase", "fight", "mission", "spy", "terrorist", "hero", "revenge", "bomb"]),
    "Comedy": dict(
        starts=["Two clumsy roommates", "A nervous groom", "An unlucky office worker", "A group of silly friends", "A failed comedian"],
        plots=["accidentally ruin {x} and chaos follows", "pretend to be {y} to impress their boss and everything goes wrong",
               "get into a hilarious mix-up at {x}", "try to hide a ridiculous secret during {x}",
               "enter a goofy competition and make a mess of it"],
        extra=["a prank spirals out of control", "awkward jokes and silly misunderstandings pile up", "the whole town laughs at their disaster"],
        x=["a wedding", "a birthday party", "a family dinner", "a job interview"],
        y=["a famous chef", "a rich businessman", "a married couple", "a secret agent"],
        keywords=["funny", "prank", "party", "silly", "misunderstanding", "friends", "joke", "awkward", "road trip", "mix-up"]),
    "Horror": dict(
        starts=["A group of teenagers", "A young family", "A lonely night nurse", "A team of paranormal investigators", "A curious student"],
        plots=["discover {x} in {p} and soon realize something evil is watching", "are stalked by {x} after a cursed ritual",
               "move into {p} haunted by {x}", "wake {x} and fight to survive the night",
               "vanish one by one in {p} as a terrifying presence grows"],
        extra=["blood on the walls and screams in the dark", "the lights flicker as a shadow moves closer", "nobody who enters leaves unharmed"],
        x=["a demonic spirit", "a masked killer", "an ancient curse", "a zombie outbreak"],
        p=["an abandoned asylum", "a remote cabin", "a haunted mansion", "a dark forest"],
        keywords=["ghost", "haunted", "killer", "blood", "demon", "scream", "curse", "monster", "dark", "terror"]),
    "Romance": dict(
        starts=["Two strangers", "A shy bookshop owner", "A busy architect", "Childhood friends", "A traveling musician"],
        plots=["meet in {p} and slowly fall in love despite {o}", "rekindle an old romance after {o}",
               "share an unexpected kiss in {p} that changes their hearts forever", "must choose between love and {o}",
               "write love letters to each other while {o}"],
        extra=["a tender dance under the stars", "a heartfelt confession of love", "a first date that feels like destiny"],
        p=["Paris", "a small seaside town", "a snowy village", "a crowded train station"],
        o=["their different worlds", "years apart", "a family disapproval", "a painful breakup"],
        keywords=["love", "kiss", "wedding", "heart", "relationship", "couple", "romantic", "dating", "passion", "soulmate"]),
    "Drama": dict(
        starts=["A struggling single mother", "An aging father", "A talented but troubled teacher", "A young immigrant", "A grieving widow"],
        plots=["struggles with {c} while holding the family together", "confronts {c} after a painful loss",
               "fights to rebuild a broken life after {c}", "must face {c} and forgive the past",
               "faces a difficult moral choice caused by {c}"],
        extra=["a quiet portrait of hardship and hope", "old family wounds finally come to the surface", "a difficult journey of self-discovery"],
        c=["poverty", "addiction", "illness", "an unfair trial", "a family secret"],
        keywords=["family", "loss", "struggle", "hope", "society", "grief", "sacrifice", "justice", "emotional", "real life"]),
}
# A few words that can show up in any genre, so the classes overlap a little (like real data)
SHARED = ["set in a small town", "over one unforgettable summer", "in the middle of a changing world", "with the help of an old friend"]


def build_row(genre: str, spec: dict, number: int) -> dict:
    # (titles are just numbers, so they never reveal the genre)
    fill = {k: random.choice(v) for k, v in spec.items() if k not in ("starts", "plots", "extra", "keywords")}
    parts = [f"{random.choice(spec['starts'])} {random.choice(spec['plots'])}.", f"{random.choice(spec['extra'])}."]
    if random.random() < 0.6:
        parts.append(random.choice(SHARED) + ".")
    keywords = random.sample(spec["keywords"], 3)
    if random.random() < 0.15:  # sometimes borrow a keyword from another genre
        keywords.append(random.choice(random.choice([s for g, s in GENRES.items() if g != genre])["keywords"]))
    return {"title": f"Sample Film {number:04d}", "plot": " ".join(parts).format(**fill), "keywords": ", ".join(keywords), "genre": genre}


if __name__ == "__main__":
    rows = [build_row(g, s, 0) for g, s in GENRES.items() for _ in range(PER_GENRE)]
    random.shuffle(rows)
    for number, row in enumerate(rows, 1):
        row["title"] = f"Sample Film {number:04d}"
    out = Path(__file__).parent / "data" / "movies_sample.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "plot", "keywords", "genre"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic rows to {out}")
