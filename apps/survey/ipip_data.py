"""
IPIP Big Five Markers — 100 items (Goldberg, 1992)
Source : International Personality Item Pool (ipip.ori.org) — domaine public

Traductions :
  - FR : adaptées pour le contexte professionnel
  - EN : source originale IPIP (Goldberg, 1992)
  - DE : traduction officielle IPIP 100 items (Streib & Wiedmaier, 2001,
    Universität Bielefeld) — couverture 100/100, validée par rétro-traduction.
    https://ipip.ori.org/German100-ItemBig-FiveFactorMarkers.htm
  - ES : traduction officielle IPIP 50 items (de Oliveira, Cherubini & Oliver,
    2013, ACM TOCHI) pour les 50 premiers items — les 50 items d'extension
    (identifiants se terminant par 11 à 20 dans chaque dimension, ex. E11-E20)
    n'ont pas de traduction espagnole officiellement publiée : ils sont
    traduits par nos soins, dans un registre professionnel cohérent avec le
    reste du questionnaire. Voir le disclaimer complet dans
    `docs/product/translations-ipip.md`.
    https://ipip.ori.org/SpanishBig-FiveFactorMarkers.htm
  - Quelques items FR (ex. C5, C10, O4, O5) sont des paraphrases qui ne
    correspondent à aucun item officiel des 100 marqueurs de Goldberg : leurs
    versions DE/ES sont donc elles aussi des adaptations maison, pas des
    traductions officielles. Détail dans `docs/product/translations-ipip.md`.

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

SCALE_DE = {
    1: "Stimme überhaupt nicht zu",
    2: "Stimme eher nicht zu",
    3: "Weder noch",
    4: "Stimme eher zu",
    5: "Stimme voll und ganz zu",
}

SCALE_ES = {
    1: "Totalmente en desacuerdo",
    2: "Más bien en desacuerdo",
    3: "Ni de acuerdo ni en desacuerdo",
    4: "Más bien de acuerdo",
    5: "Totalmente de acuerdo",
}

# Toutes les échelles de réponse, indexées par code langue
SCALES = {
    "fr": SCALE_FR,
    "en": SCALE_EN,
    "de": SCALE_DE,
    "es": SCALE_ES,
}

# Dimensions OCEAN
DIMENSIONS = ["extraversion", "agreeableness", "conscientiousness", "neuroticism", "openness"]

ITEMS = [
    # ── Extraversion ──────────────────────────────────────────────────────────
    {"id": "E1",  "dim": "extraversion", "key":  1, "de": "Ich bringe Leben in eine Party.", "es": "Soy el alma de la fiesta.", "fr": "Je suis le centre de l'attention.",                    "en": "I am the life of the party."},
    {"id": "E2",  "dim": "extraversion", "key": -1, "de": "Ich rede nicht viel.", "es": "No hablo mucho.", "fr": "Je ne parle pas beaucoup.",                           "en": "I don't talk a lot."},
    {"id": "E3",  "dim": "extraversion", "key":  1, "de": "Unter Menschen zu sein, ist mir angenehm.", "es": "Me siento cómodo con la gente.", "fr": "Je me sens à l'aise avec les gens.",                  "en": "I feel comfortable around people."},
    {"id": "E4",  "dim": "extraversion", "key":  1, "de": "Ich beginne Unterhaltungen.", "es": "Comienzo las conversaciones.", "fr": "Je prends facilement l'initiative dans les échanges.", "en": "I start conversations."},
    {"id": "E5",  "dim": "extraversion", "key": -1, "de": "Ich habe wenig zu sagen.", "es": "No tengo mucho que decir.", "fr": "J'ai peu de choses à dire.",                          "en": "I have little to say."},
    {"id": "E6",  "dim": "extraversion", "key":  1, "de": "Auf Parties unterhalte ich mich mit vielen verschiedenen Leuten.", "es": "En las fiestas hablo con muchas personas diferentes.", "fr": "Je parle facilement à de nombreuses personnes.",      "en": "I talk to a lot of different people at parties."},
    {"id": "E7",  "dim": "extraversion", "key": -1, "de": "Ich ziehe nicht gern Aufmerksamkeit auf mich.", "es": "No me gusta llamar la atención.", "fr": "Je n'aime pas me mettre en avant.",                   "en": "I don't like to draw attention to myself."},
    {"id": "E8",  "dim": "extraversion", "key":  1, "de": "Es stört mich nicht im Mittelpunkt der Aufmerksamkeit zu stehen.", "es": "No me importa ser el centro de atención.", "fr": "Être au centre de l'attention ne me dérange pas.",    "en": "I don't mind being the center of attention."},
    {"id": "E9",  "dim": "extraversion", "key": -1, "de": "Ich bin still unter Fremden.", "es": "Cuando estoy entre desconocidos me mantengo callado.", "fr": "Je suis réservé(e) face aux inconnus.",               "en": "I am quiet around strangers."},
    {"id": "E10", "dim": "extraversion", "key": -1, "de": "Ich halte mich im Hintergrund.", "es": "Prefiero mantenerme al margen.", "fr": "Je préfère rester en retrait.",                       "en": "I keep in the background."},

    # ── Agréabilité ───────────────────────────────────────────────────────────
    {"id": "A1",  "dim": "agreeableness", "key": -1, "de": "Andere Menschen kümmern mich wenig.", "es": "Me preocupo poco por los demás.", "fr": "Je me soucie peu des autres.",                       "en": "I feel little concern for others."},
    {"id": "A2",  "dim": "agreeableness", "key":  1, "de": "Ich interessiere mich für Leute.", "es": "Me intereso por la gente.", "fr": "Je m'intéresse sincèrement aux gens.",               "en": "I am interested in people."},
    {"id": "A3",  "dim": "agreeableness", "key": -1, "de": "Ich beleidige Leute.", "es": "Ofendo a la gente.", "fr": "Il m'arrive d'être blessant(e) envers les autres.",  "en": "I insult people."},
    {"id": "A4",  "dim": "agreeableness", "key":  1, "de": "Ich kann die Gefühle anderer nachempfinden.", "es": "Soy sensible hacia las emociones de otros.", "fr": "Je compatis facilement aux émotions des autres.",    "en": "I sympathize with others' feelings."},
    {"id": "A5",  "dim": "agreeableness", "key": -1, "de": "Ich interessiere mich nicht für die Probleme anderer Leute.", "es": "No me interesan los problemas de otras personas.", "fr": "Les problèmes des autres me laissent indifférent(e).","en": "I am not interested in other people's problems."},
    {"id": "A6",  "dim": "agreeableness", "key":  1, "de": "Ich habe ein weiches Herz.", "es": "Tengo un corazón sensible.", "fr": "J'ai bon cœur.",                                     "en": "I have a soft heart."},
    {"id": "A7",  "dim": "agreeableness", "key": -1, "de": "Ich interessiere mich nicht wirklich für andere.", "es": "En realidad no me intereso por los demás.", "fr": "Je ne m'intéresse pas vraiment aux autres.",         "en": "I am not really interested in others."},
    {"id": "A8",  "dim": "agreeableness", "key":  1, "de": "Ich nehme mir Zeit für andere.", "es": "Dedico tiempo a los demás.", "fr": "Je prends du temps pour les autres.",                "en": "I take time out for others."},
    {"id": "A9",  "dim": "agreeableness", "key":  1, "de": "Ich kann die Gefühle anderer nachfühlen.", "es": "Siento las emociones de los otros.", "fr": "Je ressens les émotions des autres.",                "en": "I feel others' emotions."},
    {"id": "A10", "dim": "agreeableness", "key":  1, "de": "Ich mache andere Leute ungezwungen.", "es": "Hago sentir cómoda a la gente.", "fr": "Je mets les gens à l'aise.",                         "en": "I make people feel at ease."},

    # ── Conscience / Rigueur ──────────────────────────────────────────────────
    {"id": "C1",  "dim": "conscientiousness", "key":  1, "de": "Ich bin immer vorbereitet.", "es": "Siempre estoy preparado.", "fr": "Je suis toujours bien préparé(e).",              "en": "I am always prepared."},
    {"id": "C2",  "dim": "conscientiousness", "key": -1, "de": "Ich lasse meine Sachen herumliegen.", "es": "Dejo mis pertenencias en cualquier lado.", "fr": "Je laisse traîner mes affaires.",                "en": "I leave my belongings around."},
    {"id": "C3",  "dim": "conscientiousness", "key":  1, "de": "Ich lege Wert auf Details.", "es": "Pongo atención en los detalles.", "fr": "Je fais attention aux détails.",                 "en": "I pay attention to details."},
    {"id": "C4",  "dim": "conscientiousness", "key":  1, "de": "Ich folge einem Plan.", "es": "Hago un programa y lo sigo.", "fr": "Je respecte un planning.",                       "en": "I follow a schedule."},
    {"id": "C5",  "dim": "conscientiousness", "key": -1, "de": "Ich achte nicht auf Details.", "es": "No presto atención a los detalles.", "fr": "Je néglige souvent les détails.",                "en": "I don't pay attention to details."},
    {"id": "C6",  "dim": "conscientiousness", "key":  1, "de": "Ich erledige Hausarbeit sofort.", "es": "Realizo mis tareas inmediatamente.", "fr": "J'effectue les tâches sans tarder.",             "en": "I get chores done right away."},
    {"id": "C7",  "dim": "conscientiousness", "key": -1, "de": "Ich vergesse oft, Dinge wieder an den richtigen Platz zurück zu bringen.", "es": "A menudo olvido poner las cosas en su lugar.", "fr": "J'oublie souvent de ranger les choses.",         "en": "I often forget to put things back in their proper place."},
    {"id": "C8",  "dim": "conscientiousness", "key":  1, "de": "Ich mag Ordnung.", "es": "Me gusta el orden.", "fr": "J'aime l'ordre et la méthode.",                  "en": "I like order."},
    {"id": "C9",  "dim": "conscientiousness", "key": -1, "de": "Ich verpfusche die Dinge.", "es": "Soy desordenado.", "fr": "Je génère parfois du désordre autour de moi.",   "en": "I make a mess of things."},
    {"id": "C10", "dim": "conscientiousness", "key":  1, "de": "Ich führe meine Vorhaben zu Ende.", "es": "Llevo a cabo mis proyectos hasta el final.", "fr": "Je mène mes projets à leur terme.",              "en": "I follow through with my plans."},

    # ── Névrotisme (stabilité émotionnelle inversée) ──────────────────────────
    {"id": "N1",  "dim": "neuroticism", "key":  1, "de": "Ich bin schnell stressgeplagt.", "es": "Me estreso con facilidad.", "fr": "Je stresse facilement.",                               "en": "I get stressed out easily."},
    {"id": "N2",  "dim": "neuroticism", "key": -1, "de": "Ich bin die meiste Zeit entspannt.", "es": "Estoy relajado la mayor parte del tiempo.", "fr": "Je suis détendu(e) la plupart du temps.",              "en": "I am relaxed most of the time."},
    {"id": "N3",  "dim": "neuroticism", "key":  1, "de": "Ich mache mir Sorgen über Dinge.", "es": "Me preocupo por todo.", "fr": "Je m'inquiète souvent.",                               "en": "I worry about things."},
    {"id": "N4",  "dim": "neuroticism", "key": -1, "de": "Ich fühle mich selten traurig.", "es": "Rara vez me siento triste.", "fr": "Je me sens rarement déprimé(e).",                      "en": "I seldom feel blue."},
    {"id": "N5",  "dim": "neuroticism", "key":  1, "de": "Ich lasse mich leicht stören.", "es": "Me molesto fácilmente.", "fr": "Je me laisse facilement perturber.",                   "en": "I am easily disturbed."},
    {"id": "N6",  "dim": "neuroticism", "key":  1, "de": "Ich gerate leicht aus der Fassung.", "es": "Me disgusto con facilidad.", "fr": "Je suis facilement contrarié(e).",                    "en": "I get upset easily."},
    {"id": "N7",  "dim": "neuroticism", "key":  1, "de": "Meine Laune ändert sich häufig.", "es": "Cambio mucho de humor.", "fr": "Mon humeur change fréquemment.",                       "en": "I change my mood a lot."},
    {"id": "N8",  "dim": "neuroticism", "key":  1, "de": "Ich habe häufige Stimmungsschwankungen.", "es": "Tengo cambios frecuentes de estado de ánimo.", "fr": "J'ai souvent des sautes d'humeur.",                   "en": "I have frequent mood swings."},
    {"id": "N9",  "dim": "neuroticism", "key":  1, "de": "Ich lasse mich leicht irritieren.", "es": "Me irrito fácilmente.", "fr": "Je m'énerve facilement.",                             "en": "I get irritated easily."},
    {"id": "N10", "dim": "neuroticism", "key":  1, "de": "Ich fühle mich oft traurig.", "es": "Me siento triste frecuentemente.", "fr": "Je me sens souvent déprimé(e).",                      "en": "I often feel blue."},

    # ── Ouverture à l'expérience ──────────────────────────────────────────────
    {"id": "O1",  "dim": "openness", "key":  1, "de": "Ich habe einen reichen Wortschatz.", "es": "Tengo un vocabulario amplio.", "fr": "J'ai un vocabulaire riche et varié.",                     "en": "I have a rich vocabulary."},
    {"id": "O2",  "dim": "openness", "key": -1, "de": "Ich habe Schwierigkeiten abstrakte Ideen zu verstehen.", "es": "Me cuesta entender ideas abstractas.", "fr": "J'ai du mal à comprendre les idées abstraites.",          "en": "I have difficulty understanding abstract ideas."},
    {"id": "O3",  "dim": "openness", "key":  1, "de": "Ich habe eine lebhafte Vorstellungskraft.", "es": "Tengo mucha imaginación.", "fr": "J'ai une imagination fertile.",                           "en": "I have a vivid imagination."},
    {"id": "O4",  "dim": "openness", "key":  1, "de": "Ich interessiere mich für abstrakte Ideen.", "es": "Me interesan las ideas abstractas.", "fr": "Les idées abstraites m'intéressent.",                     "en": "I am interested in abstract ideas."},
    {"id": "O5",  "dim": "openness", "key": -1, "de": "Ich denke nicht gerne viel nach.", "es": "No me gusta pensar demasiado.", "fr": "Je n'aime pas les sujets qui demandent trop de réflexion.","en": "I do not like to think a lot."},
    {"id": "O6",  "dim": "openness", "key":  1, "de": "Ich habe hervorragende Ideen.", "es": "Tengo excelentes ideas.", "fr": "J'ai souvent de bonnes idées originales.",               "en": "I have excellent ideas."},
    {"id": "O7",  "dim": "openness", "key": -1, "de": "Ich habe keine gute Vorstellungskraft.", "es": "No tengo una buena imaginación.", "fr": "Je n'ai pas beaucoup d'imagination.",                    "en": "I do not have a good imagination."},
    {"id": "O8",  "dim": "openness", "key":  1, "de": "Ich bin schnell im Verstehen von Dingen.", "es": "Soy rápido para entender las cosas.", "fr": "Je comprends les choses rapidement.",                    "en": "I am quick to understand things."},
    {"id": "O9",  "dim": "openness", "key":  1, "de": "Ich benutze schwierige Worte.", "es": "Utilizo palabras difíciles.", "fr": "J'utilise des mots recherchés ou peu courants.",         "en": "I use difficult words."},
    {"id": "O10", "dim": "openness", "key":  1, "de": "Ich verbringe Zeit damit, Dinge zu reflektieren.", "es": "Dedico tiempo a reflexionar.", "fr": "Je prends le temps de réfléchir en profondeur aux choses.","en": "I spend time reflecting on things."},

    # ══════════════════════════════════════════════════════════════════════════
    # Items 51–100 — extension IPIP-100 (échelles 20 items/dimension)
    # Ne jamais insérer d'item avant cette ligne : ITEMS[:50] = version courte.
    # ══════════════════════════════════════════════════════════════════════════

    # ── Extraversion (suite) ──────────────────────────────────────────────────
    {"id": "E11", "dim": "extraversion", "key":  1, "de": "Ich finde leicht Freunde.", "es": "Hago amigos con facilidad.", "fr": "Je me fais facilement des amis.",                     "en": "I make friends easily."},
    {"id": "E12", "dim": "extraversion", "key":  1, "de": "Ich übernehme Verantwortung.", "es": "Tomo el mando con naturalidad.", "fr": "Je prends naturellement les choses en main.",         "en": "I take charge."},
    {"id": "E13", "dim": "extraversion", "key":  1, "de": "Ich weiß, wie man Leute fesseln kann.", "es": "Sé cómo cautivar a la gente.", "fr": "Je sais capter l'attention des gens.",                "en": "I know how to captivate people."},
    {"id": "E14", "dim": "extraversion", "key":  1, "de": "Ich fühle mich ungezwungen unter Leuten.", "es": "Me siento cómodo en las interacciones sociales.", "fr": "Je suis détendu(e) dans les interactions sociales.",  "en": "I feel at ease with people."},
    {"id": "E15", "dim": "extraversion", "key":  1, "de": "Ich bin geschickt darin, mit sozialen Situationen umzugehen.", "es": "Tengo habilidad para manejar situaciones sociales.", "fr": "Je suis habile dans les situations sociales.",        "en": "I am skilled in handling social situations."},
    {"id": "E16", "dim": "extraversion", "key": -1, "de": "Ich finde es schwierig andere zu erreichen.", "es": "Me cuesta acercarme a los demás.", "fr": "J'ai du mal à aborder les autres.",                   "en": "I find it difficult to approach others."},
    {"id": "E17", "dim": "extraversion", "key": -1, "de": "Ich fühle mich oft unbehaglich in der Gegenwart anderer.", "es": "A menudo me siento incómodo en grupo.", "fr": "Je me sens souvent mal à l'aise en groupe.",          "en": "I often feel uncomfortable around others."},
    {"id": "E18", "dim": "extraversion", "key": -1, "de": "Ich verschließe meine Gefühle.", "es": "Guardo mis emociones para mí.", "fr": "Je garde mes émotions pour moi.",                     "en": "I bottle up my feelings."},
    {"id": "E19", "dim": "extraversion", "key": -1, "de": "Ich bin eine sehr private Person.", "es": "Soy una persona muy reservada.", "fr": "Je suis quelqu'un de très réservé.",                  "en": "I am a very private person."},
    {"id": "E20", "dim": "extraversion", "key": -1, "de": "Ich überlasse es anderen, den Weg zu zeigen.", "es": "Espero a que los demás tomen la iniciativa.", "fr": "J'attends que les autres prennent l'initiative.",     "en": "I wait for others to lead the way."},

    # ── Agréabilité (suite) ───────────────────────────────────────────────────
    {"id": "A11", "dim": "agreeableness", "key":  1, "de": "Ich erkundige mich nach dem Wohlbefinden anderer.", "es": "Me intereso por el bienestar de los demás.", "fr": "Je prends des nouvelles des autres.",                "en": "I inquire about others' well-being."},
    {"id": "A12", "dim": "agreeableness", "key":  1, "de": "Ich weiß wie ich andere trösten kann.", "es": "Sé cómo reconfortar a los demás.", "fr": "Je sais réconforter les autres.",                    "en": "I know how to comfort others."},
    {"id": "A13", "dim": "agreeableness", "key":  1, "de": "Ich liebe Kinder.", "es": "Me encantan los niños.", "fr": "J'aime les enfants.",                                "en": "I love children."},
    {"id": "A14", "dim": "agreeableness", "key":  1, "de": "Ich komme mit fast jedem gut aus.", "es": "Me llevo bien con casi todo el mundo.", "fr": "Je m'entends bien avec presque tout le monde.",      "en": "I am on good terms with nearly everyone."},
    {"id": "A15", "dim": "agreeableness", "key":  1, "de": "Ich habe ein gutes Wort für jeden.", "es": "Siempre tengo una palabra amable para cada persona.", "fr": "J'ai un mot aimable pour chacun.",                   "en": "I have a good word for everyone."},
    {"id": "A16", "dim": "agreeableness", "key":  1, "de": "Ich zeige meine Dankbarkeit.", "es": "Expreso mi gratitud.", "fr": "J'exprime ma gratitude.",                            "en": "I show my gratitude."},
    {"id": "A17", "dim": "agreeableness", "key":  1, "de": "Ich denke zuerst an andere.", "es": "Pienso primero en los demás.", "fr": "Je pense d'abord aux autres.",                       "en": "I think of others first."},
    {"id": "A18", "dim": "agreeableness", "key":  1, "de": "Ich liebe es anderen zu helfen.", "es": "Me encanta ayudar a los demás.", "fr": "J'aime aider les autres.",                           "en": "I love to help others."},
    {"id": "A19", "dim": "agreeableness", "key": -1, "de": "Mich kennenzulernen ist schwer.", "es": "Soy difícil de conocer.", "fr": "Je suis difficile à cerner.",                        "en": "I am hard to get to know."},
    {"id": "A20", "dim": "agreeableness", "key": -1, "de": "Ich bin den Gefühlen anderer gegenüber gleichgültig.", "es": "Los sentimientos de los demás me son indiferentes.", "fr": "Les sentiments des autres me laissent indifférent(e).","en": "I am indifferent to the feelings of others."},

    # ── Conscience / Rigueur (suite) ──────────────────────────────────────────
    {"id": "C11", "dim": "conscientiousness", "key":  1, "de": "An der Arbeit bin ich genau.", "es": "Soy perfeccionista en mi trabajo.", "fr": "Je suis exigeant(e) dans mon travail.",          "en": "I am exacting in my work."},
    {"id": "C12", "dim": "conscientiousness", "key":  1, "de": "Ich tue Dinge einem Plan entsprechend.", "es": "Hago las cosas siguiendo un plan establecido.", "fr": "Je fais les choses selon un plan établi.",       "en": "I do things according to a plan."},
    {"id": "C13", "dim": "conscientiousness", "key":  1, "de": "Ich mache so lang weiter, bis alles perfekt ist.", "es": "Persisto hasta que todo quede perfecto.", "fr": "Je persévère jusqu'à ce que tout soit parfait.", "en": "I continue until everything is perfect."},
    {"id": "C14", "dim": "conscientiousness", "key":  1, "de": "Ich mache Pläne und halte an ihnen fest.", "es": "Hago planes y los cumplo.", "fr": "Je fais des plans et je m'y tiens.",             "en": "I make plans and stick to them."},
    {"id": "C15", "dim": "conscientiousness", "key":  1, "de": "Ich liebe Ordnung und Regelmäßigkeit.", "es": "Aprecio el orden y la regularidad.", "fr": "J'apprécie la régularité et la constance.",      "en": "I love order and regularity."},
    {"id": "C16", "dim": "conscientiousness", "key":  1, "de": "Ich mag es aufzuräumen.", "es": "Me gusta ordenar y organizar mi espacio de trabajo.", "fr": "J'aime ranger et organiser mon espace de travail.","en": "I like to tidy up."},
    {"id": "C17", "dim": "conscientiousness", "key": -1, "de": "Ich vernachlässige meine Pflichten.", "es": "Descuido mis obligaciones.", "fr": "Je néglige mes obligations.",                    "en": "I neglect my duties."},
    {"id": "C18", "dim": "conscientiousness", "key": -1, "de": "Ich verschwende meine Zeit.", "es": "Pierdo el tiempo.", "fr": "Je perds mon temps.",                            "en": "I waste my time."},
    {"id": "C19", "dim": "conscientiousness", "key": -1, "de": "Ich erledige Dinge halbherzig.", "es": "Hago las cosas a medias.", "fr": "Je fais les choses à moitié.",                   "en": "I do things in a half-way manner."},
    {"id": "C20", "dim": "conscientiousness", "key": -1, "de": "Ich finde es schwierig Arbeit in Angriff zu nehmen.", "es": "Me cuesta ponerme a trabajar.", "fr": "J'ai du mal à me mettre au travail.",            "en": "I find it difficult to get down to work."},

    # ── Névrotisme (suite) ────────────────────────────────────────────────────
    {"id": "N11", "dim": "neuroticism", "key": -1, "de": "Ich rege mich nicht leicht über Dinge auf.", "es": "Pocas cosas me perturban.", "fr": "Peu de choses me perturbent.",                         "en": "I am not easily bothered by things."},
    {"id": "N12", "dim": "neuroticism", "key": -1, "de": "Ich bin selten irritiert.", "es": "Rara vez me irrito.", "fr": "Je m'irrite rarement.",                                "en": "I rarely get irritated."},
    {"id": "N13", "dim": "neuroticism", "key": -1, "de": "Ich werde selten sauer.", "es": "Rara vez me enojo.", "fr": "Je me mets rarement en colère.",                       "en": "I seldom get mad."},
    {"id": "N14", "dim": "neuroticism", "key":  1, "de": "Ich werde leicht ärgerlich.", "es": "Me enfado con facilidad.", "fr": "Je me fâche facilement.",                              "en": "I get angry easily."},
    {"id": "N15", "dim": "neuroticism", "key":  1, "de": "Ich gerate leicht in Panik.", "es": "Entro en pánico con facilidad.", "fr": "Je panique facilement.",                               "en": "I panic easily."},
    {"id": "N16", "dim": "neuroticism", "key":  1, "de": "Ich fühle mich leicht bedroht.", "es": "Me siento amenazado con facilidad.", "fr": "Je me sens facilement menacé(e).",                     "en": "I feel threatened easily."},
    {"id": "N17", "dim": "neuroticism", "key":  1, "de": "Ich werde von Gefühlen überwältigt.", "es": "Me dejo desbordar por mis emociones.", "fr": "Je me laisse déborder par mes émotions.",              "en": "I get overwhelmed by emotions."},
    {"id": "N18", "dim": "neuroticism", "key":  1, "de": "Ich fühle mich leicht angegriffen.", "es": "Me ofendo con facilidad.", "fr": "Je me vexe facilement.",                               "en": "I take offense easily."},
    {"id": "N19", "dim": "neuroticism", "key":  1, "de": "Ich verstricke mich in meinen Problemen.", "es": "Le doy vueltas a mis problemas.", "fr": "Je rumine mes problèmes.",                             "en": "I get caught up in my problems."},
    {"id": "N20", "dim": "neuroticism", "key":  1, "de": "Ich nörgle über Dinge.", "es": "Tiendo a quejarme de las cosas.", "fr": "J'ai tendance à me plaindre.",                         "en": "I grumble about things."},

    # ── Ouverture à l'expérience (suite) ──────────────────────────────────────
    {"id": "O11", "dim": "openness", "key":  1, "de": "Ich bin voller Ideen.", "es": "Estoy lleno de ideas.", "fr": "Je déborde d'idées.",                                     "en": "I am full of ideas."},
    {"id": "O12", "dim": "openness", "key":  1, "de": "Ich bringe die Unterhaltung auf ein höheres Niveau.", "es": "Elevo el nivel de la conversación.", "fr": "J'élève le niveau de la conversation.",                   "en": "I carry the conversation to a higher level."},
    {"id": "O13", "dim": "openness", "key":  1, "de": "Ich kapiere Dinge schnell.", "es": "Capto rápidamente las situaciones nuevas.", "fr": "Je saisis rapidement les situations nouvelles.",          "en": "I catch on to things quickly."},
    {"id": "O14", "dim": "openness", "key":  1, "de": "Ich kann mit eine Menge von Information umgehen.", "es": "Puedo procesar mucha información a la vez.", "fr": "Je peux traiter beaucoup d'informations à la fois.",      "en": "I can handle a lot of information."},
    {"id": "O15", "dim": "openness", "key":  1, "de": "Ich liebe es, mir neue Wege, Dinge zu tun, auszudenken.", "es": "Me encanta inventar nuevas formas de hacer las cosas.", "fr": "J'aime inventer de nouvelles façons de faire.",           "en": "I love to think up new ways of doing things."},
    {"id": "O16", "dim": "openness", "key":  1, "de": "Ich liebe es, Dinge zu lesen, die mich herausfordern.", "es": "Me encanta leer contenidos exigentes.", "fr": "J'aime lire des contenus exigeants.",                     "en": "I love to read challenging material."},
    {"id": "O17", "dim": "openness", "key":  1, "de": "Ich bin in vielen Sachen gut.", "es": "Se me dan bien muchas cosas.", "fr": "Je suis doué(e) dans plusieurs domaines.",                "en": "I am good at many things."},
    {"id": "O18", "dim": "openness", "key": -1, "de": "Ich versuche komplizierte Menschen zu meiden.", "es": "Evito a las personas demasiado complicadas.", "fr": "J'évite les personnes trop compliquées.",                 "en": "I try to avoid complex people."},
    {"id": "O19", "dim": "openness", "key": -1, "de": "Ich habe Schwierigkeiten mir Dinge vorzustellen.", "es": "Me cuesta imaginar las cosas.", "fr": "J'ai du mal à me projeter dans l'imaginaire.",            "en": "I have difficulty imagining things."},
    {"id": "O20", "dim": "openness", "key": -1, "de": "Ich werde nie eine Sache gründlich untersuchen.", "es": "No profundizo de buena gana en un tema.", "fr": "Je n'approfondis pas volontiers un sujet.",               "en": "I will not probe deeply into a subject."},
]

# Index rapide par id
ITEMS_BY_ID = {item["id"]: item for item in ITEMS}

# Items par dimension (ordre fixe)
ITEMS_BY_DIM = {dim: [i for i in ITEMS if i["dim"] == dim] for dim in DIMENSIONS}
