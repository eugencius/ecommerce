import math


def insert_new_pagination(context, request, qty_pages=10):
    paginator = context["paginator"]
    page_range = paginator.page_range
    current_page = int(request.GET.get("page", 1))

    paginator = make_pagination(
        page_range=page_range, qty_pages=qty_pages, current_page=current_page
    )

    context["paginator"] = paginator


def make_pagination(page_range, qty_pages, current_page):
    total_pages = len(page_range)

    middle_page = math.ceil(qty_pages / 2)
    start_index = current_page - middle_page
    stop_index = current_page + middle_page

    if start_index < 0:
        stop_index += abs(start_index)
        start_index = 0

    if stop_index > total_pages:
        start_index -= abs(stop_index - total_pages)

    pagination = page_range[start_index:stop_index]

    return {
        "pagination": pagination,
        "is_paginated": len(page_range) > 1,
        "page_range": page_range,
        "qty_pages": qty_pages,
        "current_page": current_page,
        "has_next": current_page < total_pages,
        "has_previous": current_page > 1,
        "next_page": current_page + 1,
        "previous_page": current_page - 1,
    }
