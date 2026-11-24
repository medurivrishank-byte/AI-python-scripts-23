BOXES = {
    "Sports": "the team won the football match and the crowd cheered the goal "
              "she runs fast in the race and wins the gold medal for the team",
    "Food": "we cook pasta with tomato sauce and the soup is hot "
            "he bakes bread and the cake tastes sweet with cream",
    "Music": "the band plays a loud song and the singer sings with the guitar "
             "she learns the piano and sings a song in the choir",
}

TEST_NOTES = [
    ("the goal won the match", "Sports"),
    ("he bakes the cake and the bread", "Food"),
    ("the singer plays the guitar", "Music"),
    ("pasta with sweet cream", "Food"),
    ("the band wins the match", "Music"),
    ("", "unknown"),
]

THRESHOLD = 0.2

# ---------- PART 1: count the words ----------
def word_counts(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

PROFILES = {box: word_counts(text) for box, text in BOXES.items()}
print("PART 1: Word counts")
print(PROFILES["Food"].get("the", 0), PROFILES["Food"].get("goal", 0))

# ---------- PART 2: compare two word counts ----------
def cosine(a, b):
    dot = 0
    for word in a:
        dot += a[word] * b.get(word, 0)
    size_a = sum(count * count for count in a.values()) ** 0.5
    size_b = sum(count * count for count in b.values()) ** 0.5
    if size_a == 0 or size_b == 0:
        return 0.0
    return dot / (size_a * size_b)

print("\nPART 2: Cosine")
print(round(cosine(word_counts("the team"), PROFILES["Sports"]), 2))

# ---------- PART 3: find the best box ----------
def classify(note):
    counts = word_counts(note)
    best_box, best_score = "unknown", 0.0
    for box, profile in PROFILES.items():
        s = cosine(counts, profile)
        if s > best_score:
            best_box, best_score = box, s
    if best_score < THRESHOLD:
        return "unknown"
    return best_box

print("\nPART 3: Classify")
print(classify("the goal won the match"), "|", classify("zzz"))

# ---------- PART 4: check every test note ----------
print("\nPART 4: Test all notes")
mistakes = 0
for note, wanted in TEST_NOTES:
    answer = classify(note)
    if answer != wanted:
        mistakes += 1
    print(answer, "<-", note)
print(f"Mistakes: {mistakes} out of {len(TEST_NOTES)}")