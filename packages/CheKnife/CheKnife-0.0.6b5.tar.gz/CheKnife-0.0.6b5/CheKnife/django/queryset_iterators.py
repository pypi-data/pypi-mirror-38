# from django.core.paginator import Paginator


# def chunked_iterator(queryset, chunk_size=10000):
#     paginator = Paginator(queryset, chunk_size)
#     for page in range(1, paginator.num_pages + 1):
#         for obj in paginator.page(page).object_list:
#             yield obj


def batch_qs(qs, batch_size=10000):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:
        # Make sure to order your querset
        article_qs = Article.objects.order_by('id')
        for start, end, total, qs in batch_qs(article_qs):
            print "Now processing %s - %s of %s" % (start + 1, end, total)
            for article in qs:
                print article.body
    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])
