# Roadmap publique

La V1 de FitRadarHR est complète (epics E1–E8 livrés) et la **V2 est entièrement
livrée** (9/9 items). Cette page présente aussi les pistes candidates pour une
**V3**, priorisées avec la méthode **RICE** — en toute transparence, comme le
reste du projet.

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

## Priorisation V3

Les items #1 et #2 sont livrés ; les items 3 à 8 restent des candidats non tranchés.

| # | Fonctionnalité | Reach | Impact | Conf. | Effort | Score RICE | Statut |
|---|---|---|---|---|---|---|---|
| 1 | Fit inversé — meilleurs postes pour une personne | 5 | 2 | 90 % | 1.5 | **6.0** | ✅ Livré |
| 2 | Monétisation (essai gratuit → abonnement) | 8 | 3 | 80 % | 5 | **3.84** | ✅ Livré |
| 3 | Cartographie des manques d'une équipe | 5 | 2 | 60 % | 2 | **3.0** | Candidat |
| 4 | Portail candidat / collaborateur (accès à son profil) | 6 | 2 | 70 % | 3 | **2.8** | Candidat |
| 5 | Dossier de conformité AI Act exportable | 3 | 2 | 70 % | 2 | **2.1** | Candidat |
| 6 | Webhooks (complément de l'API publique) | 3 | 1 | 70 % | 2 | **1.05** | Candidat |
| 7 | Benchmarks anonymisés inter-organisations | 4 | 1 | 40 % | 4 | **0.4** | Candidat |
| 8 | Connecteurs natifs (Workday, BambooHR, Personio…) | 3 | 2 | 30 % | 5 | **0.36** | Candidat |

### Les arguments, item par item

**1. Fit inversé** — aujourd'hui on part d'un poste pour classer des personnes ;
l'inverse (partir d'une personne et voir les postes ouverts qui lui correspondent
le mieux) sert la mobilité interne, sans collecter la moindre donnée
supplémentaire : c'est une nouvelle vue sur le moteur de fit existant. Meilleur
ratio valeur/effort de la liste. Livré : aucun nouveau calcul, réutilise les
résultats de fit déjà produits par le moteur (E5).

**2. Monétisation** — c'est la raison même du passage à la licence Fair Source
(FSL-1.1-MIT) : Damien envisageait explicitement un essai gratuit puis un
abonnement. Reach élevé (touche potentiellement toutes les orgs à terme) et
impact fort (c'est le modèle économique), mais effort important : intégration
Stripe, quotas par plan, écrans de facturation, gestion des dépassements.
Livré : essai de 14 jours automatique, un seul plan payant (Stripe Checkout +
Customer Portal), quotas d'usage post-essai (postes/personnes/questionnaires).

**3. Cartographie des manques d'équipe** — étend la complémentarité déjà
calculée : à partir du profil agrégé d'une équipe, faire ressortir les
dimensions OCEAN sous-représentées. Reste dans le cadre du produit — présenté
comme des pistes à explorer pour un plan de recrutement, jamais comme une
recommandation tranchée (cohérent avec la règle "jamais de score de décision
automatique").

**4. Portail candidat/collaborateur** — aujourd'hui seuls RH/managers consultent
les rapports. Donner à la personne elle-même l'accès à son profil et son
rapport renforce le principe "human in the loop" et le droit d'accès RGPD déjà
implémenté (E8). Confiance moyenne : nécessite un nouveau modèle d'accès pour
des `Person` qui n'ont pas forcément de compte `User`.

**5. Dossier de conformité AI Act exportable** — un export (PDF/JSON) du
"dossier de traçabilité" — qui a consulté quoi, supervision humaine documentée —
pour les organisations qui doivent justifier leur conformité au titre du
classement "haut risque". Prolonge directement E8, cible surtout les organisations
plus réglementées (reach plus faible).

**6. Webhooks** — complément naturel de l'API publique (item #9 V2) : notifier
un système tiers quand un questionnaire est complété ou qu'un fit est recalculé,
plutôt que de faire du polling. Utile seulement pour les orgs qui utilisent déjà
l'API, donc reach restreint.

**7. Benchmarks anonymisés** — comparer la distribution OCEAN d'une organisation
à une moyenne agrégée inter-organisations, en opt-in et anonymisée. Valeur
analytique réelle mais confiance faible : soulève des questions de gouvernance
des données (agrégation cross-tenant, consentement) qui restent à cadrer avant
tout développement.

**8. Connecteurs natifs** — au-delà de l'API générique, des intégrations
préconstruites avec des SIRH/ATS spécifiques réduiraient la friction d'adoption.
Confiance la plus faible du lot : demande non encore validée par un cas d'usage
client réel, effort élevé (un connecteur = un projet à part entière). À réserver
si une organisation exprime un besoin concret.

## Ce qui ne sera jamais fait

Voir les [anti-métriques](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
et les règles non négociables du projet : pas d'analyse de CV, pas de score de
décision automatique, pas de typologie non validée scientifiquement (MBTI…).

---

*Cette roadmap est indicative et réévaluée au fil des retours utilisateurs —
le [widget de feedback](../index.md) intégré à l'application alimente directement
cette priorisation.*
