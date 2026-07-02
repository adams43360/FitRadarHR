"""
Insights contextuels pour les rapports Big Five / OCEAN.

Contenu :
  - DIMENSION_TOOLTIPS : texte court d'aide (infobulle) par dimension et par langue
  - get_position_exploration_points() : génère les "points à approfondir" pour le Fit Poste
  - get_team_exploration_points()     : génère les "points à approfondir" pour le Fit Équipe

Philosophie de framing :
  Ces contenus suggèrent des *questions à explorer en entretien*, jamais des verdicts.
  Conformément à la règle #2 du projet, le produit informe — il ne décide pas.
"""

# ─── Infobulles par dimension ─────────────────────────────────────────────────

DIMENSION_TOOLTIPS = {
    "openness": {
        "fr": (
            "Score élevé : curiosité intellectuelle, créativité, goût pour la nouveauté et les idées abstraites.\n"
            "Score faible : pragmatisme, préférence pour le concret et les méthodes éprouvées."
        ),
        "en": (
            "High score: intellectual curiosity, creativity, openness to new ideas and abstract thinking.\n"
            "Low score: pragmatism, preference for concrete approaches and proven methods."
        ),
    },
    "conscientiousness": {
        "fr": (
            "Score élevé : rigueur, organisation, sens du détail et de la planification.\n"
            "Score faible : flexibilité, spontanéité, préférence pour l'adaptabilité sur les process."
        ),
        "en": (
            "High score: rigor, organization, attention to detail and planning.\n"
            "Low score: flexibility, spontaneity, preference for adaptability over strict processes."
        ),
    },
    "extraversion": {
        "fr": (
            "Score élevé : aisance sociale, assertivité, énergie dans les interactions et le travail en groupe.\n"
            "Score faible : préférence pour l'autonomie, la réflexion avant d'agir et les environnements calmes."
        ),
        "en": (
            "High score: social ease, assertiveness, energy in interactions and group work.\n"
            "Low score: preference for autonomy, thinking before acting, and quieter environments."
        ),
    },
    "agreeableness": {
        "fr": (
            "Score élevé : coopération, empathie, bienveillance, orientation vers le collectif.\n"
            "Score faible : esprit critique affirmé, indépendance de jugement, franchise directe."
        ),
        "en": (
            "High score: cooperation, empathy, kindness, team-oriented.\n"
            "Low score: critical thinking, independence of judgment, directness in communication."
        ),
    },
    "neuroticism": {
        "fr": (
            "Score élevé : sensibilité accrue au stress, réactivité émotionnelle, tendance à l'anxiété ou au doute de soi.\n"
            "Score faible : stabilité émotionnelle, calme sous pression, résilience face aux difficultés."
        ),
        "en": (
            "High score: higher sensitivity to stress, emotional reactivity, tendency toward anxiety or self-doubt.\n"
            "Low score: emotional stability, calm under pressure, resilience when facing challenges."
        ),
    },
}


# ─── Points à approfondir — Fit Poste ────────────────────────────────────────

_POSITION_MSGS = {
    "openness": {
        "fr": {
            "too_high": (
                "Le score d'Ouverture dépasse la fourchette cible. "
                "Si le poste exige rigueur procédurale ou exécution répétitive, "
                "il peut être utile d'explorer en entretien comment la personne s'épanouit dans un cadre structuré."
            ),
            "too_low": (
                "Le score d'Ouverture est en dessous de la fourchette cible. "
                "Si le poste implique créativité ou adaptation à des contextes changeants, "
                "il peut être utile d'explorer les expériences passées d'innovation ou d'adaptation de la personne."
            ),
        },
        "en": {
            "too_high": (
                "Openness score exceeds the target range. "
                "If the role requires procedural rigor or repetitive execution, "
                "it may be worth exploring how the person thrives within a structured framework."
            ),
            "too_low": (
                "Openness score is below the target range. "
                "If the role involves creativity or adaptation to changing contexts, "
                "it may be worth exploring the person's past experiences with innovation or change."
            ),
        },
    },
    "conscientiousness": {
        "fr": {
            "too_high": (
                "Le score de Conscienciosité dépasse la fourchette cible. "
                "Dans un environnement agile ou créatif, un excès de rigueur peut parfois freiner l'adaptabilité — "
                "un point utile à approfondir en entretien."
            ),
            "too_low": (
                "Le score de Conscienciosité est en dessous de la fourchette cible. "
                "Si le poste exige gestion des délais, organisation rigoureuse ou attention aux détails, "
                "il peut être utile d'explorer les méthodes d'organisation personnelle de la personne."
            ),
        },
        "en": {
            "too_high": (
                "Conscientiousness score exceeds the target range. "
                "In agile or creative environments, excessive rigor can sometimes hinder adaptability — "
                "worth exploring in an interview."
            ),
            "too_low": (
                "Conscientiousness score is below the target range. "
                "If the role demands deadline management, strong organization or attention to detail, "
                "it may be worth exploring the person's personal organizational methods."
            ),
        },
    },
    "extraversion": {
        "fr": {
            "too_high": (
                "Le score d'Extraversion dépasse la fourchette cible. "
                "Dans un poste nécessitant concentration soutenue ou travail en autonomie, "
                "il peut être utile d'explorer les préférences de la personne quant à son environnement de travail."
            ),
            "too_low": (
                "Le score d'Extraversion est en dessous de la fourchette cible. "
                "Si le poste implique présentations, management ou nombreuses interactions, "
                "il peut être utile d'explorer comment la personne gère les situations à forte dimension sociale."
            ),
        },
        "en": {
            "too_high": (
                "Extraversion score exceeds the target range. "
                "In a role requiring sustained focus or autonomous work, "
                "it may be worth exploring the person's preferences regarding their work environment."
            ),
            "too_low": (
                "Extraversion score is below the target range. "
                "If the role involves presentations, people management or frequent interactions, "
                "it may be worth exploring how the person handles high-social situations."
            ),
        },
    },
    "agreeableness": {
        "fr": {
            "too_high": (
                "Le score d'Agréabilité dépasse la fourchette cible. "
                "Dans des postes nécessitant de challenger des idées, de négocier ou de prendre des décisions difficiles, "
                "il peut être utile d'explorer comment la personne gère les situations de désaccord."
            ),
            "too_low": (
                "Le score d'Agréabilité est en dessous de la fourchette cible. "
                "Si le poste exige un fort travail collaboratif ou de la diplomatie, "
                "il peut être utile d'explorer les expériences de la personne en gestion de conflits et en coopération."
            ),
        },
        "en": {
            "too_high": (
                "Agreeableness score exceeds the target range. "
                "In roles that require challenging ideas, negotiating or making tough decisions, "
                "it may be worth exploring how the person handles disagreement."
            ),
            "too_low": (
                "Agreeableness score is below the target range. "
                "If the role requires strong collaboration or diplomacy, "
                "it may be worth exploring the person's experiences in conflict management and cooperation."
            ),
        },
    },
    "neuroticism": {
        "fr": {
            "too_high": (
                "Le score de Neuroticisme dépasse la fourchette cible. "
                "Dans des environnements à forte pression ou à imprévus fréquents, "
                "il peut être utile d'explorer en entretien comment la personne gère le stress et les situations exigeantes."
            ),
            "too_low": (
                "Le score de Neuroticisme est particulièrement bas, indiquant une très grande stabilité émotionnelle. "
                "Si le poste bénéficie d'une sensibilité aux enjeux humains (relation client sensible, médiation), "
                "ce point mérite d'être évoqué."
            ),
        },
        "en": {
            "too_high": (
                "Neuroticism score exceeds the target range. "
                "In high-pressure or frequently unpredictable environments, "
                "it may be worth exploring how the person manages stress and demanding situations."
            ),
            "too_low": (
                "Neuroticism score is particularly low, indicating very high emotional stability. "
                "If the role benefits from sensitivity to human concerns (sensitive client relations, mediation), "
                "this is worth discussing."
            ),
        },
    },
}


def get_position_exploration_points(dim_details, lang):
    """
    Retourne une liste de {"dimension": label, "message": text} pour les dimensions
    dont le score est hors de la fourchette cible du poste.

    dim_details doit contenir : dim_key, label, score, min, max.
    """
    lang = lang if lang in ("fr", "en") else "fr"
    points = []
    for d in dim_details:
        dim_key = d.get("dim_key")
        msgs = _POSITION_MSGS.get(dim_key, {}).get(lang, {})
        if d["score"] > d["max"]:
            msg = msgs.get("too_high")
        elif d["score"] < d["min"]:
            msg = msgs.get("too_low")
        else:
            msg = None
        if msg:
            points.append({"dimension": d["label"], "message": msg})
    return points


# ─── Points à approfondir — Fit Équipe ───────────────────────────────────────

_TEAM_MSGS = {
    "openness": {
        "fr": {
            "different": (
                "La personne se distingue de l'équipe sur l'Ouverture. "
                "Cela peut créer des divergences sur les méthodes de travail — "
                "un sujet utile à aborder lors de l'intégration."
            ),
            "complementary": (
                "La personne apporte une perspective différente sur l'Ouverture là où l'équipe est homogène. "
                "Selon le sens de l'écart, cela peut enrichir la créativité ou l'ancrage opérationnel du groupe."
            ),
        },
        "en": {
            "different": (
                "The person stands out from the team on Openness. "
                "This may lead to divergences on work methods — "
                "a useful topic to address during onboarding."
            ),
            "complementary": (
                "The person brings a different perspective on Openness where the team is homogeneous. "
                "Depending on the direction of the gap, this can enrich creativity or operational grounding."
            ),
        },
    },
    "conscientiousness": {
        "fr": {
            "different": (
                "La personne se distingue de l'équipe sur la Conscienciosité. "
                "Un écart marqué sur ce trait peut affecter la dynamique collective en matière d'organisation — "
                "un point à anticiper lors de l'intégration."
            ),
            "complementary": (
                "La personne apporte un profil différent sur la Conscienciosité dans une équipe homogène. "
                "Selon le sens de l'écart, cela peut apporter structure ou flexibilité au groupe."
            ),
        },
        "en": {
            "different": (
                "The person stands out from the team on Conscientiousness. "
                "A notable gap on this trait may affect team dynamics around organization and rigor — "
                "worth anticipating during onboarding."
            ),
            "complementary": (
                "The person brings a different profile on Conscientiousness in a homogeneous team. "
                "Depending on the direction, this may bring structure or flexibility to the group."
            ),
        },
    },
    "extraversion": {
        "fr": {
            "different": (
                "La personne se distingue de l'équipe sur l'Extraversion. "
                "Cette différence peut influencer la communication interne et la dynamique des réunions — "
                "un point à anticiper."
            ),
            "complementary": (
                "L'écart d'Extraversion par rapport à une équipe homogène peut être complémentaire : "
                "apporter de l'énergie sociale ou du recul réflexif selon le sens de l'écart."
            ),
        },
        "en": {
            "different": (
                "The person stands out from the team on Extraversion. "
                "This difference may influence internal communication and meeting dynamics — "
                "worth anticipating."
            ),
            "complementary": (
                "The person's Extraversion gap within a homogeneous team can be complementary: "
                "bringing social energy or reflective perspective depending on the direction."
            ),
        },
    },
    "agreeableness": {
        "fr": {
            "different": (
                "La personne se distingue de l'équipe sur l'Agréabilité. "
                "Un écart notable peut influencer la coopération et le climat d'équipe — "
                "utile à explorer en entretien."
            ),
            "complementary": (
                "La personne apporte un profil différent sur l'Agréabilité dans une équipe homogène. "
                "Cela peut enrichir l'esprit critique ou la cohésion du groupe selon le sens de l'écart."
            ),
        },
        "en": {
            "different": (
                "The person stands out from the team on Agreeableness. "
                "A notable gap may influence cooperation and team climate — worth exploring."
            ),
            "complementary": (
                "The person brings a different profile on Agreeableness in a homogeneous team. "
                "This can enrich critical thinking or group cohesion depending on the direction of the gap."
            ),
        },
    },
    "neuroticism": {
        "fr": {
            "different": (
                "La personne se distingue de l'équipe sur le Neuroticisme. "
                "Un écart notable sur ce trait peut affecter la dynamique collective lors des situations de pression — "
                "un point à anticiper lors de l'intégration."
            ),
            "complementary": (
                "La personne apporte un profil de Neuroticisme différent dans une équipe homogène. "
                "Selon le sens de l'écart, cela peut apporter résilience ou sensibilité aux enjeux humains."
            ),
        },
        "en": {
            "different": (
                "The person stands out from the team on Neuroticism. "
                "A notable gap may affect collective dynamics during stressful situations — "
                "worth anticipating during onboarding."
            ),
            "complementary": (
                "The person brings a different Neuroticism profile in a homogeneous team. "
                "Depending on the direction, this may bring resilience or sensitivity to human concerns."
            ),
        },
    },
}


def get_team_exploration_points(dim_details, lang):
    """
    Retourne une liste de {"dimension": label, "signal": signal, "message": text}
    pour les dimensions avec signal "different" ou "complementary" dans le Fit Équipe.
    Les dimensions "similar" n'ont pas de point à approfondir.

    dim_details doit contenir : dim_key, label, signal.
    """
    lang = lang if lang in ("fr", "en") else "fr"
    points = []
    for d in dim_details:
        dim_key = d.get("dim_key")
        signal = d.get("signal", "similar")
        if signal not in ("different", "complementary"):
            continue
        msgs = _TEAM_MSGS.get(dim_key, {}).get(lang, {})
        msg = msgs.get(signal)
        if msg:
            points.append({
                "dimension": d["label"],
                "signal": signal,
                "message": msg,
            })
    return points
