"""
IPIP Big Five Markers — 100 items (Goldberg, 1992)
Source : International Personality Item Pool (ipip.ori.org) — domaine public
Traductions FR : adaptées pour le contexte professionnel

Deux versions de passation :
  - 50 items  : ITEMS[:50] — les échelles courtes (10 items/dimension)
  - 100 items : ITEMS complet — les échelles longues (20 items/dimension)
  L'ordre des 50 premiers items ne doit JAMAIS changer (compatibilité
  des questionnaires déjà envoyés et des profils déjà calculés).

Scoring :
  - key= 1 : score direct (1→1, 2→2, 3→3, 4→4, 5→5)
  - key=-1 : score inversé (1→5, 2→4, 3→3, 4→2, 5→1) = 6 - score
  - Normalisation 0-100 sur les items répondus : (somme - n) / (n × 4) × 100
"""

# Libellés de l'échelle de réponse
SCALE_FR = {
    1: "Pas du tout d'accord",
    2: "Plutôt pas d'accord",
    3: "Ni l'un ni l'autre",
    4: "Plutôt d'accord",
    5: "Tout à fait d'accord",
}

SCALE_EN = {
    1: "Strongly disagree",
    2: "Disagree",
    3: "Neither agree nor disagree",
    4: "Agree",
    5: "Strongly agree",
}

# Dimensions OCEAN
DIMENSIONS = ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]

ITEMS = [
    # ── Extraversion ──────────────────────────────────────────────────────────
    {"id": "E1",  "dim": "extraversion", "key":  1, "fr": "Je suis le centre de l'attention.",                    "en": "I am the life of the party."},
    {"id": "E2",  "dim": "extraversion", "key": -1, "fr": "Je ne parle pas beaucoup.",                           "en": "I don't talk a lot."},
    {"id": "E3",  "dim": "extraversion", "key":  1, "fr": "Je me sens à l'aise avec les gens.",                  "en": "I feel comfortable around people."},
    {"id": "E4",  "dim": "extraversion", "key":  1, "fr": "Je prends facilement l'initiative dans les échanges.", "en": "I start conversations."},
    {"id": "E5",  "dim": "extraversion", "key": -1, "fr": "J'ai peu de choses à dire.",                          "en": "I have little to say."},
    {"id": "E6",  "dim": "extraversion", "key":  1, "fr": "Je parle facilement à de nombreuses personnes.",      "en": "I talk to a lot of different people at parties."},
    {"id": "E7",  "dim": "extraversion", "key": -1, "fr": "Je n'aime pas me mettre en avant.",                   "en": "I don't like to draw attention to myself."},
    {"id": "E8",  "dim": "extraversion", "key":  1, "fr": "Être au centre de l'attention ne me dérange pas.",    "en": "I don't mind being the center of attention."},
    {"id": "E9",  "dim": "extraversion", "key": -1, "fr": "Je suis réservé(e) face aux inconnus.",               "en": "I am quiet around strangers."},
    {"id": "E10", "dim": "extraversion", "key": -1, "fr": "Je préfère rester en retrait.",                       "en": "I keep in the background."},

    # ── Agréabilité ───────────────────────────────────────────────────────────
    {"id": "A1",  "dim": "agreeableness", "key": -1, "fr": "Je me soucie peu des autres.",                       "en": "I feel little concern for others."},
    {"id": "A2",  "dim": "agreeableness", "key":  1, "fr": "Je m'intéresse sincèrement aux gens.",               "en": "I am interested in people."},
    {"id": "A3",  "dim": "agreeableness", "key": -1, "fr": "Il m'arrive d'être blessant(e) envers les autres.",  "en": "I insult people."},
    {"id": "A4",  "dim": "agreeableness", "key":  1, "fr": "Je compatis facilement aux émotions des autres.",    "en": "I sympathize with others' feelings."},
    {"id": "A5",  "dim": "agreeableness", "key": -1, "fr": "Les problèmes des autres me laissent indifférent(e).","en": "I am not interested in other people's problems."},
    {"id": "A6",  "dim": "agreeableness", "key":  1, "fr": "J'ai bon cœur.",                                     "en": "I have a soft heart."},
    {"id": "A7",  "dim": "agreeableness", "key": -1, "fr": "Je ne m'intéresse pas vraiment aux autres.",         "en": "I am not really interested in others."},
    {"id": "A8",  "dim": "agreeableness", "key":  1, "fr": "Je prends du temps pour les autres.",                "en": "I take time out for others."},
    {"id": "A9",  "dim": "agreeableness", "key":  1, "fr": "Je ressens les émotions des autres.",                "en": "I feel others' emotions."},
    {"id": "A10", "dim": "agreeableness", "key":  1, "fr": "Je mets les gens à l'aise.",                         "en": "I make people feel at ease."},

    # ── Conscience / Rigueur ──────────────────────────────────────────────────
    {"id": "C1",  "dim": "conscientiousness", "key":  1, "fr": "Je suis toujours bien préparé(e).",              "en": "I am always prepared."},
    {"id": "C2",  "dim": "conscientiousness", "key": -1, "fr": "Je laisse traîner mes affaires.",                "en": "I leave my belongings around."},
    {"id": "C3",  "dim": "conscientiousness", "key":  1, "fr": "Je fais attention aux détails.",                 "en": "I pay attention to details."},
    {"id": "C4",  "dim": "conscientiousness", "key":  1, "fr": "Je respecte un planning.",                       "en": "I follow a schedule."},
    {"id": "C5",  "dim": "conscientiousness", "key": -1, "fr": "Je néglige souvent les détails.",                "en": "I don't pay attention to details."},
    {"id": "C6",  "dim": "conscientiousness", "key":  1, "fr": "J'effectue les tâches sans tarder.",             "en": "I get chores done right away."},
    {"id": "C7",  "dim": "conscientiousness", "key": -1, "fr": "J'oublie souvent de ranger les choses.",         "en": "I often forget to put things back in their proper place."},
    {"id": "C8",  "dim": "conscientiousness", "key":  1, "fr": "J'aime l'ordre et la méthode.",                  "en": "I like order."},
    {"id": "C9",  "dim": "conscientiousness", "key": -1, "fr": "Je génère parfois du désordre autour de moi.",   "en": "I make a mess of things."},
    {"id": "C10", "dim": "conscientiousness", "key":  1, "fr": "Je mène mes projets à leur terme.",              "en": "I follow through with my plans."},

    # ── Névrotisme (stabilité émotionnelle inversée) ──────────────────────────
    {"id": "N1",  "dim": "neuroticism", "key":  1, "fr": "Je stresse facilement.",                               "en": "I get stressed out easily."},
    {"id": "N2",  "dim": "neuroticism", "key": -1, "fr": "Je suis détendu(e) la plupart du temps.",              "en": "I am relaxed most of the time."},
    {"id": "N3",  "dim": "neuroticism", "key":  1, "fr": "Je m'inquiète souvent.",                               "en": "I worry about things."},
    {"id": "N4",  "dim": "neuroticism", "key": -1, "fr": "Je me sens rarement déprimé(e).",                      "en": "I seldom feel blue."},
    {"id": "N5",  "dim": "neuroticism", "key":  1, "fr": "Je me laisse facilement perturber.",                   "en": "I am easily disturbed."},
    {"id": "N6",  "dim": "neuroticism", "key":  1, "fr": "Je suis facilement contrarié(e).",                    "en": "I get upset easily."},
    {"id": "N7",  "dim": "neuroticism", "key":  1, "fr": "Mon humeur change fréquemment.",                       "en": "I change my mood a lot."},
    {"id": "N8",  "dim": "neuroticism", "key":  1, "fr": "J'ai souvent des sautes d'humeur.",                   "en": "I have frequent mood swings."},
    {"id": "N9",  "dim": "neuroticism", "key":  1, "fr": "Je m'énerve facilement.",                             "en": "I get irritated easily."},
    {"id": "N10", "dim": "neuroticism", "key":  1, "fr": "Je me sens souvent déprimé(e).",                      "en": "I often feel blue."},

    # ── Ouverture à l'expérience ──────────────────────────────────────────────
    {"id": "O1",  "dim": "openness", "key":  1, "fr": "J'ai un vocabulaire riche et varié.",                     "en": "I have a rich vocabulary."},
    {"id": "O2",  "dim": "openness", "key": -1, "fr": "J'ai du mal à comprendre les idées abstraites.",          "en": "I have difficulty understanding abstract ideas."},
    {"id": "O3",  "dim": "openness", "key":  1, "fr": "J'ai une imagination fertile.",                           "en": "I have a vivid imagination."},
    {"id": "O4",  "dim": "openness", "key":  1, "fr": "Les idées abstraites m'intéressent.",                     "en": "I am interested in abstract ideas."},
    {"id": "O5",  "dim": "openness", "key": -1, "fr": "Je n'aime pas les sujets qui demandent trop de réflexion.","en": "I do not like to think a lot."},
    {"id": "O6",  "dim": "openness", "key":  1, "fr": "J'ai souvent de bonnes idées originales.",               "en": "I have excellent ideas."},
    {"id": "O7",  "dim": "openness", "key": -1, "fr": "Je n'ai pas beaucoup d'imagination.",                    "en": "I do not have a good imagination."},
    {"id": "O8",  "dim": "openness", "key":  1, "fr": "Je comprends les choses rapidement.",                    "en": "I am quick to understand things."},
    {"id": "O9",  "dim": "openness", "key":  1, "fr": "J'utilise des mots recherchés ou peu courants.",         "en": "I use difficult words."},
    {"id": "O10", "dim": "openness", "key":  1, "fr": "Je prends le temps de réfléchir en profondeur aux choses.","en": "I spend time reflecting on things."},

    # ══════════════════════════════════════════════════════════════════════════
    # Items 51–100 — extension IPIP-100 (échelles 20 items/dimension)
    # Ne jamais insérer d'item avant cette ligne : ITEMS[:50] = version courte.
    # ══════════════════════════════════════════════════════════════════════════

    # ── Extraversion (suite) ──────────────────────────────────────────────────
    {"id": "E11", "dim": "extraversion", "key":  1, "fr": "Je me fais facilement des amis.",                     "en": "I make friends easily."},
    {"id": "E12", "dim": "extraversion", "key":  1, "fr": "Je prends naturellement les choses en main.",         "en": "I take charge."},
    {"id": "E13", "dim": "extraversion", "key":  1, "fr": "Je sais capter l'attention des gens.",                "en": "I know how to captivate people."},
    {"id": "E14", "dim": "extraversion", "key":  1, "fr": "Je suis détendu(e) dans les interactions sociales.",  "en": "I feel at ease with people."},
    {"id": "E15", "dim": "extraversion", "key":  1, "fr": "Je suis habile dans les situations sociales.",        "en": "I am skilled in handling social situations."},
    {"id": "E16", "dim": "extraversion", "key": -1, "fr": "J'ai du mal à aborder les autres.",                   "en": "I find it difficult to approach others."},
    {"id": "E17", "dim": "extraversion", "key": -1, "fr": "Je me sens souvent mal à l'aise en groupe.",          "en": "I often feel uncomfortable around others."},
    {"id": "E18", "dim": "extraversion", "key": -1, "fr": "Je garde mes émotions pour moi.",                     "en": "I bottle up my feelings."},
    {"id": "E19", "dim": "extraversion", "key": -1, "fr": "Je suis quelqu'un de très réservé.",                  "en": "I am a very private person."},
    {"id": "E20", "dim": "extraversion", "key": -1, "fr": "J'attends que les autres prennent l'initiative.",     "en": "I wait for others to lead the way."},

    # ── Agréabilité (suite) ───────────────────────────────────────────────────
    {"id": "A11", "dim": "agreeableness", "key":  1, "fr": "Je prends des nouvelles des autres.",                "en": "I inquire about others' well-being."},
    {"id": "A12", "dim": "agreeableness", "key":  1, "fr": "Je sais réconforter les autres.",                    "en": "I know how to comfort others."},
    {"id": "A13", "dim": "agreeableness", "key":  1, "fr": "J'aime les enfants.",                                "en": "I love children."},
    {"id": "A14", "dim": "agreeableness", "key":  1, "fr": "Je m'entends bien avec presque tout le monde.",      "en": "I am on good terms with nearly everyone."},
    {"id": "A15", "dim": "agreeableness", "key":  1, "fr": "J'ai un mot aimable pour chacun.",                   "en": "I have a good word for everyone."},
    {"id": "A16", "dim": "agreeableness", "key":  1, "fr": "J'exprime ma gratitude.",                            "en": "I show my gratitude."},
    {"id": "A17", "dim": "agreeableness", "key":  1, "fr": "Je pense d'abord aux autres.",                       "en": "I think of others first."},
    {"id": "A18", "dim": "agreeableness", "key":  1, "fr": "J'aime aider les autres.",                           "en": "I love to help others."},
    {"id": "A19", "dim": "agreeableness", "key": -1, "fr": "Je suis difficile à cerner.",                        "en": "I am hard to get to know."},
    {"id": "A20", "dim": "agreeableness", "key": -1, "fr": "Les sentiments des autres me laissent indifférent(e).","en": "I am indifferent to the feelings of others."},

    # ── Conscience / Rigueur (suite) ──────────────────────────────────────────
    {"id": "C11", "dim": "conscientiousness", "key":  1, "fr": "Je suis exigeant(e) dans mon travail.",          "en": "I am exacting in my work."},
    {"id": "C12", "dim": "conscientiousness", "key":  1, "fr": "Je fais les choses selon un plan établi.",       "en": "I do things according to a plan."},
    {"id": "C13", "dim": "conscientiousness", "key":  1, "fr": "Je persévère jusqu'à ce que tout soit parfait.", "en": "I continue until everything is perfect."},
    {"id": "C14", "dim": "conscientiousness", "key":  1, "fr": "Je fais des plans et je m'y tiens.",             "en": "I make plans and stick to them."},
    {"id": "C15", "dim": "conscientiousness", "key":  1, "fr": "J'apprécie la régularité et la constance.",      "en": "I love order and regularity."},
    {"id": "C16", "dim": "conscientiousness", "key":  1, "fr": "J'aime ranger et organiser mon espace de travail.","en": "I like to tidy up."},
    {"id": "C17", "dim": "conscientiousness", "key": -1, "fr": "Je néglige mes obligations.",                    "en": "I neglect my duties."},
    {"id": "C18", "dim": "conscientiousness", "key": -1, "fr": "Je perds mon temps.",                            "en": "I waste my time."},
    {"id": "C19", "dim": "conscientiousness", "key": -1, "fr": "Je fais les choses à moitié.",                   "en": "I do things in a half-way manner."},
    {"id": "C20", "dim": "conscientiousness", "key": -1, "fr": "J'ai du mal à me mettre au travail.",            "en": "I find it difficult to get down to work."},

    # ── Névrotisme (suite) ────────────────────────────────────────────────────
    {"id": "N11", "dim": "neuroticism", "key": -1, "fr": "Peu de choses me perturbent.",                         "en": "I am not easily bothered by things."},
    {"id": "N12", "dim": "neuroticism", "key": -1, "fr": "Je m'irrite rarement.",                                "en": "I rarely get irritated."},
    {"id": "N13", "dim": "neuroticism", "key": -1, "fr": "Je me mets rarement en colère.",                       "en": "I seldom get mad."},
    {"id": "N14", "dim": "neuroticism", "key":  1, "fr": "Je me fâche facilement.",                              "en": "I get angry easily."},
    {"id": "N15", "dim": "neuroticism", "key":  1, "fr": "Je panique facilement.",                               "en": "I panic easily."},
    {"id": "N16", "dim": "neuroticism", "key":  1, "fr": "Je me sens facilement menacé(e).",                     "en": "I feel threatened easily."},
    {"id": "N17", "dim": "neuroticism", "key":  1, "fr": "Je me laisse déborder par mes émotions.",              "en": "I get overwhelmed by emotions."},
    {"id": "N18", "dim": "neuroticism", "key":  1, "fr": "Je me vexe facilement.",                               "en": "I take offense easily."},
    {"id": "N19", "dim": "neuroticism", "key":  1, "fr": "Je rumine mes problèmes.",                             "en": "I get caught up in my problems."},
    {"id": "N20", "dim": "neuroticism", "key":  1, "fr": "J'ai tendance à me plaindre.",                         "en": "I grumble about things."},

    # ── Ouverture à l'expérience (suite) ──────────────────────────────────────
    {"id": "O11", "dim": "openness", "key":  1, "fr": "Je déborde d'idées.",                                     "en": "I am full of ideas."},
    {"id": "O12", "dim": "openness", "key":  1, "fr": "J'élève le niveau de la conversation.",                   "en": "I carry the conversation to a higher level."},
    {"id": "O13", "dim": "openness", "key":  1, "fr": "Je saisis rapidement les situations nouvelles.",          "en": "I catch on to things quickly."},
    {"id": "O14", "dim": "openness", "key":  1, "fr": "Je peux traiter beaucoup d'informations à la fois.",      "en": "I can handle a lot of information."},
    {"id": "O15", "dim": "openness", "key":  1, "fr": "J'aime inventer de nouvelles façons de faire.",           "en": "I love to think up new ways of doing things."},
    {"id": "O16", "dim": "openness", "key":  1, "fr": "J'aime lire des contenus exigeants.",                     "en": "I love to read challenging material."},
    {"id": "O17", "dim": "openness", "key":  1, "fr": "Je suis doué(e) dans plusieurs domaines.",                "en": "I am good at many things."},
    {"id": "O18", "dim": "openness", "key": -1, "fr": "J'évite les personnes trop compliquées.",                 "en": "I try to avoid complex people."},
    {"id": "O19", "dim": "openness", "key": -1, "fr": "J'ai du mal à me projeter dans l'imaginaire.",            "en": "I have difficulty imagining things."},
    {"id": "O20", "dim": "openness", "key": -1, "fr": "Je n'approfondis pas volontiers un sujet.",               "en": "I will not probe deeply into a subject."},
]

# Index rapide par id
ITEMS_BY_ID = {item["id"]: item for item in ITEMS}

# Items par dimension (ordre fixe)
ITEMS_BY_DIM = {dim: [i for i in ITEMS if i["dim"] == dim] for dim in DIMENSIONS}
