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
        "de": (
            "Hoher Wert: intellektuelle Neugier, Kreativität, Offenheit für neue Ideen und abstraktes Denken.\n"
            "Niedriger Wert: Pragmatismus, Vorliebe für konkrete Ansätze und bewährte Methoden."
        ),
        "es": (
            "Puntuación alta: curiosidad intelectual, creatividad, gusto por la novedad y las ideas abstractas.\n"
            "Puntuación baja: pragmatismo, preferencia por lo concreto y los métodos probados."
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
        "de": (
            "Hoher Wert: Sorgfalt, Organisation, Liebe zum Detail und zur Planung.\n"
            "Niedriger Wert: Flexibilität, Spontaneität, Vorliebe für Anpassungsfähigkeit gegenüber starren Prozessen."
        ),
        "es": (
            "Puntuación alta: rigor, organización, atención al detalle y a la planificación.\n"
            "Puntuación baja: flexibilidad, espontaneidad, preferencia por la adaptabilidad frente a los procesos estrictos."
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
        "de": (
            "Hoher Wert: soziale Leichtigkeit, Durchsetzungsvermögen, Energie in Interaktionen und Teamarbeit.\n"
            "Niedriger Wert: Vorliebe für Autonomie, Nachdenken vor dem Handeln und ruhigere Umgebungen."
        ),
        "es": (
            "Puntuación alta: soltura social, asertividad, energía en las interacciones y el trabajo en grupo.\n"
            "Puntuación baja: preferencia por la autonomía, la reflexión antes de actuar y los entornos tranquilos."
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
        "de": (
            "Hoher Wert: Kooperationsbereitschaft, Empathie, Freundlichkeit, Ausrichtung auf das Kollektiv.\n"
            "Niedriger Wert: ausgeprägter kritischer Geist, Urteilsunabhängigkeit, direkte Offenheit."
        ),
        "es": (
            "Puntuación alta: cooperación, empatía, amabilidad, orientación hacia el colectivo.\n"
            "Puntuación baja: espíritu crítico marcado, independencia de juicio, franqueza directa."
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
        "de": (
            "Hoher Wert: erhöhte Stressempfindlichkeit, emotionale Reaktivität, Neigung zu Angst oder Selbstzweifel.\n"
            "Niedriger Wert: emotionale Stabilität, Ruhe unter Druck, Widerstandsfähigkeit gegenüber Schwierigkeiten."
        ),
        "es": (
            "Puntuación alta: mayor sensibilidad al estrés, reactividad emocional, tendencia a la ansiedad o la duda personal.\n"
            "Puntuación baja: estabilidad emocional, calma bajo presión, resiliencia frente a las dificultades."
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
        "de": {
            "too_high": "Der Offenheitswert liegt über der Zielspanne. Wenn die Stelle prozedurale Genauigkeit oder repetitive Ausführung erfordert, kann es hilfreich sein, im Gespräch zu erkunden, wie die Person in einem strukturierten Rahmen aufblüht.",
            "too_low": "Der Offenheitswert liegt unter der Zielspanne. Wenn die Stelle Kreativität oder Anpassung an sich verändernde Kontexte erfordert, kann es hilfreich sein, die bisherigen Erfahrungen der Person mit Innovation oder Veränderung zu erkunden.",
        },
        "es": {
            "too_high": "La puntuación de Apertura supera el rango objetivo. Si el puesto exige rigor procedimental o ejecución repetitiva, puede ser útil explorar en la entrevista cómo la persona se desenvuelve en un marco estructurado.",
            "too_low": "La puntuación de Apertura está por debajo del rango objetivo. Si el puesto implica creatividad o adaptación a contextos cambiantes, puede ser útil explorar las experiencias pasadas de la persona en innovación o adaptación.",
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
        "de": {
            "too_high": "Der Gewissenhaftigkeitswert liegt über der Zielspanne. In einem agilen oder kreativen Umfeld kann zu viel Genauigkeit manchmal die Anpassungsfähigkeit bremsen — ein Punkt, der sich für ein vertiefendes Gespräch eignet.",
            "too_low": "Der Gewissenhaftigkeitswert liegt unter der Zielspanne. Wenn die Stelle Terminmanagement, strenge Organisation oder Liebe zum Detail erfordert, kann es hilfreich sein, die persönlichen Organisationsmethoden der Person zu erkunden.",
        },
        "es": {
            "too_high": "La puntuación de Responsabilidad supera el rango objetivo. En un entorno ágil o creativo, un exceso de rigor puede a veces frenar la adaptabilidad — un punto útil para profundizar en la entrevista.",
            "too_low": "La puntuación de Responsabilidad está por debajo del rango objetivo. Si el puesto exige gestión de plazos, organización rigurosa o atención al detalle, puede ser útil explorar los métodos de organización personal de la persona.",
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
        "de": {
            "too_high": "Der Extraversionswert liegt über der Zielspanne. Bei einer Stelle, die anhaltende Konzentration oder autonomes Arbeiten erfordert, kann es hilfreich sein, die Präferenzen der Person hinsichtlich ihres Arbeitsumfelds zu erkunden.",
            "too_low": "Der Extraversionswert liegt unter der Zielspanne. Wenn die Stelle Präsentationen, Führung oder zahlreiche Interaktionen umfasst, kann es hilfreich sein, zu erkunden, wie die Person mit stark sozialen Situationen umgeht.",
        },
        "es": {
            "too_high": "La puntuación de Extraversión supera el rango objetivo. En un puesto que requiere concentración sostenida o trabajo autónomo, puede ser útil explorar las preferencias de la persona respecto a su entorno de trabajo.",
            "too_low": "La puntuación de Extraversión está por debajo del rango objetivo. Si el puesto implica presentaciones, gestión de personas o numerosas interacciones, puede ser útil explorar cómo la persona maneja las situaciones de alta exigencia social.",
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
        "de": {
            "too_high": "Der Verträglichkeitswert liegt über der Zielspanne. Bei Stellen, die das Hinterfragen von Ideen, Verhandlungen oder schwierige Entscheidungen erfordern, kann es hilfreich sein zu erkunden, wie die Person mit Meinungsverschiedenheiten umgeht.",
            "too_low": "Der Verträglichkeitswert liegt unter der Zielspanne. Wenn die Stelle starke Zusammenarbeit oder Diplomatie erfordert, kann es hilfreich sein, die Erfahrungen der Person im Konfliktmanagement und in der Kooperation zu erkunden.",
        },
        "es": {
            "too_high": "La puntuación de Amabilidad supera el rango objetivo. En puestos que requieren cuestionar ideas, negociar o tomar decisiones difíciles, puede ser útil explorar cómo la persona gestiona las situaciones de desacuerdo.",
            "too_low": "La puntuación de Amabilidad está por debajo del rango objetivo. Si el puesto exige una fuerte colaboración o diplomacia, puede ser útil explorar las experiencias de la persona en gestión de conflictos y cooperación.",
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
        "de": {
            "too_high": "Der Neurotizismuswert liegt über der Zielspanne. In Umgebungen mit hohem Druck oder häufigen Unwägbarkeiten kann es hilfreich sein, im Gespräch zu erkunden, wie die Person mit Stress und anspruchsvollen Situationen umgeht.",
            "too_low": "Der Neurotizismuswert ist besonders niedrig, was auf eine sehr hohe emotionale Stabilität hinweist. Wenn die Stelle von Sensibilität für menschliche Anliegen profitiert (sensible Kundenbeziehungen, Mediation), verdient dieser Punkt Beachtung.",
        },
        "es": {
            "too_high": "La puntuación de Neuroticismo supera el rango objetivo. En entornos de alta presión o con imprevistos frecuentes, puede ser útil explorar en la entrevista cómo la persona gestiona el estrés y las situaciones exigentes.",
            "too_low": "La puntuación de Neuroticismo es particularmente baja, lo que indica una muy alta estabilidad emocional. Si el puesto se beneficia de sensibilidad hacia aspectos humanos (relación con clientes sensibles, mediación), este punto merece ser mencionado.",
        },
    },
}


def get_position_exploration_points(dim_details, lang):
    """
    Retourne une liste de {"dimension": label, "message": text} pour les dimensions
    dont le score est hors de la fourchette cible du poste.

    dim_details doit contenir : dim_key, label, score, min, max.
    """
    lang = lang if lang in ("fr", "en", "de", "es") else "fr"
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
        "de": {
            "different": "Die Person unterscheidet sich von der Gruppe in Bezug auf Offenheit. Das kann zu Divergenzen bei den Arbeitsmethoden führen — ein Thema, das sich für die Einarbeitung eignet.",
            "complementary": "Die Person bringt eine andere Perspektive zur Offenheit ein, wo das Team homogen ist. Je nach Richtung der Abweichung kann dies die Kreativität oder die operative Verankerung der Gruppe bereichern.",
        },
        "es": {
            "different": "La persona se distingue del equipo en Apertura. Esto puede generar divergencias en los métodos de trabajo — un tema útil de abordar durante la incorporación.",
            "complementary": "La persona aporta una perspectiva diferente sobre la Apertura donde el equipo es homogéneo. Según el sentido de la diferencia, esto puede enriquecer la creatividad o el anclaje operativo del grupo.",
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
        "de": {
            "different": "Die Person unterscheidet sich von der Gruppe in Bezug auf Gewissenhaftigkeit. Eine deutliche Abweichung bei diesem Merkmal kann die kollektive Dynamik in Bezug auf Organisation beeinflussen — ein Punkt, der bei der Einarbeitung zu antizipieren ist.",
            "complementary": "Die Person bringt ein anderes Profil zur Gewissenhaftigkeit in ein homogenes Team ein. Je nach Richtung der Abweichung kann dies Struktur oder Flexibilität für die Gruppe bedeuten.",
        },
        "es": {
            "different": "La persona se distingue del equipo en Responsabilidad. Una diferencia marcada en este rasgo puede afectar la dinámica colectiva en materia de organización — un punto a anticipar durante la incorporación.",
            "complementary": "La persona aporta un perfil diferente en Responsabilidad dentro de un equipo homogéneo. Según el sentido de la diferencia, esto puede aportar estructura o flexibilidad al grupo.",
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
        "de": {
            "different": "Die Person unterscheidet sich von der Gruppe in Bezug auf Extraversion. Dieser Unterschied kann die interne Kommunikation und die Dynamik von Besprechungen beeinflussen — ein Punkt, der zu antizipieren ist.",
            "complementary": "Die Abweichung bei der Extraversion gegenüber einem homogenen Team kann komplementär sein: je nach Richtung der Abweichung bringt sie soziale Energie oder reflektierten Abstand.",
        },
        "es": {
            "different": "La persona se distingue del equipo en Extraversión. Esta diferencia puede influir en la comunicación interna y en la dinámica de las reuniones — un punto a anticipar.",
            "complementary": "La diferencia de Extraversión respecto a un equipo homogéneo puede ser complementaria: aporta energía social o distancia reflexiva según el sentido de la diferencia.",
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
        "de": {
            "different": "Die Person unterscheidet sich von der Gruppe in Bezug auf Verträglichkeit. Eine deutliche Abweichung kann die Zusammenarbeit und das Teamklima beeinflussen — nützlich, dies im Gespräch zu erkunden.",
            "complementary": "Die Person bringt ein anderes Profil zur Verträglichkeit in ein homogenes Team ein. Je nach Richtung der Abweichung kann dies den kritischen Geist oder den Zusammenhalt der Gruppe bereichern.",
        },
        "es": {
            "different": "La persona se distingue del equipo en Amabilidad. Una diferencia notable puede influir en la cooperación y el clima del equipo — útil de explorar en la entrevista.",
            "complementary": "La persona aporta un perfil diferente en Amabilidad dentro de un equipo homogéneo. Esto puede enriquecer el espíritu crítico o la cohesión del grupo según el sentido de la diferencia.",
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
        "de": {
            "different": "Die Person unterscheidet sich von der Gruppe in Bezug auf Neurotizismus. Eine deutliche Abweichung bei diesem Merkmal kann die kollektive Dynamik in Drucksituationen beeinflussen — ein Punkt, der bei der Einarbeitung zu antizipieren ist.",
            "complementary": "Die Person bringt ein anderes Neurotizismus-Profil in ein homogenes Team ein. Je nach Richtung der Abweichung kann dies Resilienz oder Sensibilität für menschliche Anliegen bedeuten.",
        },
        "es": {
            "different": "La persona se distingue del equipo en Neuroticismo. Una diferencia notable en este rasgo puede afectar la dinámica colectiva en situaciones de presión — un punto a anticipar durante la incorporación.",
            "complementary": "La persona aporta un perfil de Neuroticismo diferente dentro de un equipo homogéneo. Según el sentido de la diferencia, esto puede aportar resiliencia o sensibilidad hacia aspectos humanos.",
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
    lang = lang if lang in ("fr", "en", "de", "es") else "fr"
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
