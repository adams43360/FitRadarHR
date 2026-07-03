# Roadmap publique

La V1 de FitRadarHR est complète (epics E1–E8 livrés). Cette page présente les
candidats à la **V2**, priorisés avec la méthode **RICE** — en toute transparence,
comme le reste du projet.

## Comment lire le score RICE

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach** — combien d'utilisateurs sont touchés par trimestre (échelle 1–10)
- **Impact** — effet sur la North Star (rapports consultés / semaine) : 0.5 = faible, 1 = moyen, 2 = fort, 3 = massif
- **Confidence** — confiance dans les estimations : 50 % / 80 % / 100 %
- **Effort** — charge en personne-semaines

## Priorisation V2

| # | Fonctionnalité | Reach | Impact | Conf. | Effort | Score RICE |
|---|---|---|---|---|---|---|
| 1 | Relances automatiques de questionnaire | 8 | 2 | 80 % | 1 | **12.8** |
| 2 | Invitation de managers dans l'org | 7 | 2 | 80 % | 2 | **5.6** |
| 3 | Comparaison de candidats sur un poste | 6 | 2 | 80 % | 2 | **4.8** |
| 4 | Import CSV des personnes | 6 | 1 | 100 % | 1.5 | **4.0** |
| 5 | Re-passation & suivi longitudinal | 5 | 2 | 50 % | 2 | **2.5** |
| 6 | Cohortes de rétention dans Analytics | 4 | 1 | 80 % | 1.5 | **2.1** |
| 7 | SSO Keycloak / OIDC | 3 | 1 | 80 % | 3 | **0.8** |
| 8 | Traductions ES / DE | 2 | 1 | 80 % | 2 | **0.8** |
| 9 | API publique (lecture seule) | 2 | 1 | 50 % | 3 | **0.3** |

## Les arguments, item par item

**1. Relances automatiques** — le funnel Analytics montre que l'essentiel de la
déperdition se joue entre l'envoi du lien et le démarrage. Une relance à J+3
attaque directement le taux de complétion, pour un effort minime. Meilleur ratio
valeur/effort de la liste.

**2. Invitation de managers** — aujourd'hui une org vit avec un seul compte RH la
plupart du temps. Chaque manager invité est un consommateur de rapports
supplémentaire : c'est le levier "referral" du funnel AARRR.

**3. Comparaison de candidats** — le classement de fit existe sur la fiche poste ;
la vue côte à côte (radars superposés, complémentarités) est la suite naturelle
demandée par le cas d'usage recrutement. Fort impact sur la consultation de rapports.

**4. Import CSV** — friction d'onboarding : saisir 50 collaborateurs à la main
décourage. Impact indirect sur la North Star mais confiance maximale (besoin évident).

**5. Re-passation** — les profils Big Five évoluent lentement mais évoluent ;
utile pour la mobilité interne. Confiance à 50 % : le besoin réel reste à valider
en discovery.

**6. Cohortes de rétention** — approfondit la page Analytics pour les orgs matures.
Réservé aux orgs déjà activées, donc reach plus faible.

**7. SSO / OIDC** — nécessaire pour les organisations plus grandes, mais reach
faible sur la cible actuelle (PME/scale-ups) et effort élevé. Décision assumée
depuis le cadrage : reporté tant que la demande n'est pas avérée.

**8–9. Traductions & API** — valeur réelle mais pas différenciante aujourd'hui.
L'API attendra des cas d'usage concrets d'intégration (ATS/SIRH).

## Ce qui ne sera jamais fait

Voir les [anti-métriques](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
et les règles non négociables du projet : pas d'analyse de CV, pas de score de
décision automatique, pas de typologie non validée scientifiquement (MBTI…).

---

*Cette roadmap est indicative et réévaluée au fil des retours utilisateurs —
le [widget de feedback](../index.md) intégré à l'application alimente directement
cette priorisation.*
