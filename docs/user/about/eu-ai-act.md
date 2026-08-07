# L'EU AI Act et le recrutement

!!! danger "Ceci n'est pas un conseil juridique"
    Cette page a un but informatif. Le calendrier et le contenu de l'EU AI Act ont
    évolué plusieurs fois depuis son adoption et peuvent encore évoluer. Pour toute
    décision de conformité engageant votre organisation, consultez un juriste ou
    votre DPO — FitRadarHR ne se substitue pas à ce conseil.

## Pourquoi le recrutement est concerné

L'**EU AI Act** (règlement (UE) 2024/1689) classe les systèmes d'IA utilisés pour
le recrutement et la gestion des ressources humaines — sélection de candidats,
promotion, répartition des tâches, rupture de contrat, évaluation de
performance — dans la catégorie **« haut risque »** (Annexe III). C'est cette
classification, pas le fait d'utiliser tel ou tel outil précis, qui déclenche les
obligations les plus lourdes du règlement.

FitRadarHR a été conçu en anticipant ce classement dès le départ — voir la règle
« jamais de score de décision automatique » dans les [principes du
produit](../index.md) — plutôt qu'en réaction à une échéance réglementaire.

## Où en est le calendrier (à jour au 7 août 2026)

Le calendrier a changé récemment. À l'origine, les obligations « haut risque »
devaient s'appliquer à partir du **2 août 2026**. Un paquet de simplification (le
*Digital Omnibus AI*) a modifié ce calendrier :

- Accord politique provisoire entre le Parlement européen et le Conseil : **7 mai
  2026**
- Adoption formelle par le Parlement européen : **16 juin 2026**
- Approbation finale par le Conseil de l'UE : **29 juin 2026**, puis publication
  au Journal officiel de l'UE

Résultat : les obligations « haut risque » pour les systèmes autonomes (dont les
outils RH/recrutement) sont **reportées au 2 décembre 2027**. Pour les systèmes
d'IA à haut risque intégrés dans un produit plus large, l'échéance est le **2 août
2028**.

!!! info "Ce report ne change rien aux règles déjà en vigueur"
    Le report concerne spécifiquement les obligations liées au classement « haut
    risque » (Annexe III). Il ne suspend ni le RGPD, ni le droit du travail
    français, ni les interdictions de pratiques d'IA déjà en vigueur depuis
    février 2025 (par exemple la reconnaissance d'émotions sur le lieu de
    travail, interdite dès l'entrée en application du règlement).

## Ce qui s'applique déjà, indépendamment de l'AI Act

Deux cadres juridiques encadrent le recrutement assisté par un outil aujourd'hui,
sans attendre décembre 2027 :

**RGPD, article 22** — toute personne a le droit de ne pas faire l'objet d'une
décision fondée exclusivement sur un traitement automatisé produisant des effets
juridiques ou l'affectant de manière significative, dès lors qu'aucune
intervention humaine n'a lieu. C'est la raison structurelle pour laquelle
FitRadarHR n'affiche jamais de score de décision (« recommandé » /
« non recommandé ») : voir [confidentialité et RGPD](privacy.md).

**Code du travail, articles L.1221-8 et L.1221-9** — un candidat doit être
informé, préalablement à leur mise en œuvre, des techniques et méthodes utilisées
pour son évaluation et son recrutement, y compris lorsqu'un traitement automatisé
y contribue. Les résultats obtenus doivent rester confidentiels et le candidat
peut demander communication des informations le concernant.

## Ce que la classification « haut risque » exigera à partir de 2027

Une fois les obligations applicables, un système d'IA à haut risque utilisé pour
le recrutement devra notamment disposer de :

- un système de gestion des risques documenté sur tout le cycle de vie de l'outil,
- une **supervision humaine** effective — la personne qui utilise l'outil doit
  pouvoir comprendre ses limites et ne pas s'y fier aveuglément,
- une **traçabilité** (journalisation) des utilisations,
- une documentation technique et une évaluation de conformité avant mise sur le
  marché,
- une information claire des personnes concernées.

## Comment FitRadarHR s'inscrit dans ce cadre

Ces principes ne sont pas nouveaux dans le produit — ils recoupent des choix de
conception déjà faits :

| Obligation à venir (Annexe III) | Ce que fait déjà FitRadarHR |
|---|---|
| Supervision humaine documentée | Aucun score de décision automatique — le produit informe, il ne décide jamais |
| Traçabilité des usages | Journal d'audit immuable sur les consultations, exports et envois de lien |
| Minimisation / consentement | Consentement explicite horodaté avant le questionnaire, droit à l'effacement |
| Instrument scientifiquement validé | Questionnaire Big Five (IPIP), jamais d'analyse de CV ni de typologie non validée — voir [Big Five vs MBTI](big-five-vs-mbti.md) |

Cela ne dispense pas votre organisation de sa propre analyse de conformité : la
classification « haut risque » porte sur l'usage que *vous* faites de l'outil dans
votre processus de recrutement, pas uniquement sur l'outil lui-même.

## Sources

- [Digital Omnibus AI — report des obligations haut risque à décembre 2027 (Gibson
  Dunn)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/){ target="_blank" }
- [EU Nears Approval of Agreement to Delay Rules for AI Use in Employment
  Decisions (Ogletree
  Deakins)](https://ogletree.com/insights-resources/blog-posts/eu-nears-approval-of-agreement-to-delay-rules-for-ai-use-in-employment-decisions/){ target="_blank" }
- [HR Tools and Artificial Intelligence: Europe Delays High-Risk Obligations to
  December 2027 (actuIA)](https://www.actuia.com/en/news/hr-tools-and-artificial-intelligence-europe-delays-high-risk-obligations-to-december-2027/){ target="_blank" }
- Règlement (UE) 2024/1689 (EU AI Act), Annexe III
- Code du travail, articles L.1221-8 et L.1221-9
- Règlement (UE) 2016/679 (RGPD), article 22
