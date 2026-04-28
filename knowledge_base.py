"""
Pet care knowledge base for PawPal+ RAG advisor.
Each fact has a text field and a list of keyword tags used for retrieval.
"""

FACTS = [
    # ── Dogs: exercise ──────────────────────────────────────────────────────
    {
        "text": "Adult dogs need 30–120 minutes of exercise per day; high-energy breeds (Huskies, Border Collies) need more than low-energy breeds (Bulldogs, Basset Hounds).",
        "tags": ["dog", "exercise", "walk", "activity", "energy", "breed", "daily"],
    },
    {
        "text": "Golden Retrievers are prone to hip dysplasia; keep walks moderate and avoid high-impact jumping, especially as they age past 7.",
        "tags": ["dog", "golden", "retriever", "hip", "walk", "breed", "joint", "age"],
    },
    # ── Dogs: feeding ───────────────────────────────────────────────────────
    {
        "text": "Dogs should be fed measured portions 2 times per day; avoid feeding within an hour of vigorous exercise to reduce bloat risk.",
        "tags": ["dog", "feed", "food", "meal", "portion", "bloat", "schedule"],
    },
    {
        "text": "Puppies under 6 months need 3–4 small meals per day; transition to twice-daily feeding after 6 months.",
        "tags": ["dog", "puppy", "feed", "food", "meal", "young", "schedule"],
    },
    # ── Dogs: grooming & health ─────────────────────────────────────────────
    {
        "text": "Most dogs need a bath every 4–6 weeks; over-bathing strips natural oils from the coat and causes skin dryness.",
        "tags": ["dog", "bath", "groom", "coat", "hygiene", "skin"],
    },
    {
        "text": "Dog teeth should be brushed 2–3 times per week to prevent dental disease; dental chews can supplement but not replace brushing.",
        "tags": ["dog", "teeth", "dental", "brush", "groom", "health", "hygiene"],
    },
    {
        "text": "Dogs need annual vaccinations (rabies, DHPP) and monthly heartworm and flea-prevention medication year-round.",
        "tags": ["dog", "vaccine", "vaccination", "medication", "vet", "flea", "heartworm", "prevention", "annual"],
    },
    # ── Cats: feeding ───────────────────────────────────────────────────────
    {
        "text": "Adult cats should be fed measured portions 2 times per day; free-feeding dry food often leads to obesity.",
        "tags": ["cat", "feed", "food", "meal", "portion", "obesity", "schedule"],
    },
    {
        "text": "Kittens under 6 months need 3–4 small meals per day of high-protein kitten food; do not feed adult cat food to kittens.",
        "tags": ["cat", "kitten", "feed", "food", "meal", "young", "protein", "schedule"],
    },
    # ── Cats: grooming ──────────────────────────────────────────────────────
    {
        "text": "Long-haired cats such as Ragdolls and Persians need brushing 3–4 times per week to prevent matting and reduce hairballs.",
        "tags": ["cat", "ragdoll", "persian", "brush", "groom", "fur", "mat", "long-haired", "hairball"],
    },
    {
        "text": "Short-haired cats are mostly self-grooming but benefit from weekly brushing to reduce shedding and hairballs.",
        "tags": ["cat", "brush", "groom", "fur", "short-haired", "shed", "hairball"],
    },
    {
        "text": "Cat nails should be trimmed every 2–4 weeks to prevent overgrowth and curling; provide scratching posts to naturally wear them down.",
        "tags": ["cat", "nails", "trim", "claws", "groom", "scratch", "post"],
    },
    # ── Cats: enrichment & behaviour ────────────────────────────────────────
    {
        "text": "Ragdoll cats are social and prone to loneliness; 10–15 minutes of daily interactive play prevents boredom and anxiety.",
        "tags": ["cat", "ragdoll", "play", "activity", "social", "breed", "boredom", "enrichment"],
    },
    {
        "text": "Indoor cats need environmental enrichment (climbing trees, puzzle feeders, window perches) to stay mentally stimulated.",
        "tags": ["cat", "indoor", "enrichment", "play", "stimulation", "mental", "activity"],
    },
    # ── Cats: litter & hygiene ──────────────────────────────────────────────
    {
        "text": "Cats need their litter box scooped daily and fully replaced with fresh litter once per week; keep one box per cat plus one extra.",
        "tags": ["cat", "litter", "box", "hygiene", "clean", "scoop", "daily"],
    },
    # ── Cats: vet ───────────────────────────────────────────────────────────
    {
        "text": "Cats need annual wellness exams and core vaccines (FVRCP, rabies); indoor cats still need yearly vet visits to catch hidden illness early.",
        "tags": ["cat", "vet", "vaccine", "vaccination", "health", "annual", "check-up", "exam"],
    },
    # ── General: water ──────────────────────────────────────────────────────
    {
        "text": "Fresh water must always be available for dogs and cats; change it daily and clean the bowl weekly to prevent bacterial growth.",
        "tags": ["dog", "cat", "water", "hydration", "daily", "hygiene", "bowl"],
    },
    # ── General: toxic substances ───────────────────────────────────────────
    {
        "text": "Never give pets ibuprofen, acetaminophen (Tylenol), aspirin, or xylitol — these are toxic and can be fatal to dogs and cats.",
        "tags": ["dog", "cat", "medication", "toxic", "ibuprofen", "tylenol", "acetaminophen", "xylitol", "aspirin", "danger", "poison"],
    },
    {
        "text": "Grapes, raisins, onions, garlic, macadamia nuts, and chocolate are toxic to dogs and cats and should never be fed to them.",
        "tags": ["dog", "cat", "food", "toxic", "grapes", "chocolate", "onion", "garlic", "macadamia", "danger"],
    },
    # ── General: senior pets ────────────────────────────────────────────────
    {
        "text": "Senior pets (dogs 7+, cats 10+) benefit from twice-yearly vet check-ups and may need joint supplements or senior-formula food.",
        "tags": ["dog", "cat", "senior", "old", "age", "vet", "check-up", "health", "joint", "supplement"],
    },
    # ── General: stress & behaviour ─────────────────────────────────────────
    {
        "text": "Signs of stress in pets include hiding, aggression, loss of appetite, and excessive grooming; consult a vet if these persist for more than a few days.",
        "tags": ["dog", "cat", "stress", "anxiety", "behavior", "health", "hiding", "aggression", "appetite"],
    },
]
