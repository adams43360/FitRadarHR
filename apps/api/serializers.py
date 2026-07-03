"""
Sérialisation JSON de l'API publique — lecture seule.

Principe non négociable : **jamais les scores Big Five bruts** (`BigFiveProfile`
O/C/E/A/N) dans une réponse d'API. Seuls des résultats dérivés (fit, statut du
questionnaire) sont exposés — voir la décision produit (roadmap V2 #9).
"""

DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 100


def paginate(request, queryset, serialize):
    from django.core.paginator import Paginator

    try:
        page_number = int(request.GET.get("page", 1))
    except (TypeError, ValueError):
        page_number = 1
    try:
        page_size = int(request.GET.get("page_size", DEFAULT_PAGE_SIZE))
    except (TypeError, ValueError):
        page_size = DEFAULT_PAGE_SIZE
    page_size = max(1, min(page_size, MAX_PAGE_SIZE))

    paginator = Paginator(queryset, page_size)
    page = paginator.get_page(page_number)
    return {
        "count": paginator.count,
        "page": page.number,
        "num_pages": paginator.num_pages,
        "page_size": page_size,
        "results": [serialize(obj) for obj in page.object_list],
    }


def serialize_position(position):
    return {
        "id": str(position.id),
        "title_fr": position.title_fr,
        "title_en": position.title_en or None,
        "status": position.status,
        "department": position.department.name_fr if position.department_id else None,
        "team_id": str(position.team_id) if position.team_id else None,
        "has_target_profile": position.has_profile,
        "created_at": position.created_at.isoformat(),
    }


def serialize_team(team):
    member_count = team.memberships.filter(left_at__isnull=True).count()
    return {
        "id": str(team.id),
        "name": team.name,
        "department": team.department.name_fr if team.department_id else None,
        "manager_email": team.manager.email if team.manager_id else None,
        "member_count": member_count,
        "created_at": team.created_at.isoformat(),
    }


def _latest_questionnaire_status(person):
    link = person.questionnaire_links.order_by("-sent_at").first()
    return link.status if link else None


def serialize_person(person):
    return {
        "id": str(person.id),
        "first_name": person.first_name,
        "last_name": person.last_name,
        "email": person.email,
        "person_type": person.person_type,
        "questionnaire_status": _latest_questionnaire_status(person),
        "has_big_five_profile": hasattr(person, "big_five_profile"),
        "created_at": person.created_at.isoformat(),
    }


def serialize_position_fit(fit):
    return {
        "id": str(fit.id),
        "person_id": str(fit.person_id),
        "position_id": str(fit.position_id),
        "openness_fit": float(fit.openness_fit),
        "conscientiousness_fit": float(fit.conscientiousness_fit),
        "extraversion_fit": float(fit.extraversion_fit),
        "agreeableness_fit": float(fit.agreeableness_fit),
        "neuroticism_fit": float(fit.neuroticism_fit),
        "overall_fit": float(fit.overall_fit),
        "computed_at": fit.computed_at.isoformat(),
    }


def serialize_team_fit(fit):
    return {
        "id": str(fit.id),
        "person_id": str(fit.person_id),
        "team_id": str(fit.team_id),
        "openness_fit": float(fit.openness_fit),
        "conscientiousness_fit": float(fit.conscientiousness_fit),
        "extraversion_fit": float(fit.extraversion_fit),
        "agreeableness_fit": float(fit.agreeableness_fit),
        "neuroticism_fit": float(fit.neuroticism_fit),
        "overall_fit": float(fit.overall_fit),
        "complementarity": fit.complementarity,
        "computed_at": fit.computed_at.isoformat(),
    }
