# Roadmap publique

La V1 de FitRadarHR est complète (epics E1–E8 livrés). Cette page présente les
candidats à la **V2**, priorisés avec la méthode **RICE** — en toute transparence,
comme le reste du projet. Les items 1 à 8 sont déjà livrés ; seul l'item 9 reste
un candidat.

## Comment lire le score RICE

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach** — combien d'utilisateurs sont touchés par trimestre (échelle 1–10)
- **Impact** — effet sur la North Star (rapports consultés / semaine) : 0.5 = faible, 1 = moyen, 2 = fort, 3 = massif
- **Confidence** — confiance dans les estimations : 50 % / 80 % / 100 %
- **Effort** — charge en personne-semaines

## Priorisation V2

| # | Fonctionnalité | Reach | Impact | Conf. | Effort | Score RICE | Statut |
|---|---|---|---|---|---|---|---|
| 1 | Relances automatiques de questionnaire | 8 | 2 | 80 % | 1 | **12.8** | ✅ Livré |
| 2 | Invitation de managers dans l'org | 7 | 2 | 80 % | 2 | **5.6** | ✅ Livré |
| 3 | Comparaison de candidats sur un poste | 6 | 2 | 80 % | 2 | **4.8** | ✅ Livré |
| 4 | Import CSV des personnes | 6 | 1 | 100 % | 1.5 | **4.0** | ✅ Livré |
| 5 | Re-passation & suivi longitudinal | 5 | 2 | 50 % | 2 | **2.5** | ✅ Livré |
| 6 | Cohortes de rétention dans Analytics | 4 | 1 | 80 % | 1.5 | **2.1** | ✅ Livré |
| 7 | SSO Keycloak / OIDC | 3 | 1 | 80 % | 3 | **0.8** | ✅ Livré |
| 8 | Traductions ES / DE | 2 | 1 | 80 % | 2 | **0.8** | ✅ Livré |
| 9 | API publique (lecture seule) | 2 | 1 | 50 % | 3 | **0.3** | ✅ Livré |

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

**7. SSO / OIDC** — nécessaire pour les organisations plus grandes ; reach plus
faible sur la cible actuelle (PME/scale-ups) mais un IdP par organisation, additif
au mot de passe (jamais un remplacement), rend le coût de maintenance acceptable.
Livré, non encore validé avec un IdP réel en production.

**8. Traductions ES/DE** — parité complète, questionnaire IPIP inclus, pas
seulement l'interface. Le questionnaire allemand est intégralement sourcé sur la
traduction IPIP officielle (100/100 items) ; l'espagnol l'est pour la version
courte (50 items) mais la version longue introduit une zone traduite en interne,
faute de source officielle publiée — voir `docs/user/about/big-five.md`.

**9. API publique (lecture seule)** — valeur réelle mais pas différenciante
aujourd'hui. Livrée avec un périmètre volontairement restreint : postes/équipes,
personnes + statut questionnaire, résultats de fit — jamais les profils Big Five
bruts (minimisation RGPD). Authentification par clé API par organisation.

## Ce qui ne sera jamais fait

Voir les [anti-métriques](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
et les règles non négociables du projet : pas d'analyse de CV, pas de score de
décision automatique, pas de typologie non validée scientifiquement (MBTI…).

---

*Cette roadmap est indicative et réévaluée au fil des retours utilisateurs —
le [widget de feedback](../index.md) intégré à l'application alimente directement
cette priorisation.*
