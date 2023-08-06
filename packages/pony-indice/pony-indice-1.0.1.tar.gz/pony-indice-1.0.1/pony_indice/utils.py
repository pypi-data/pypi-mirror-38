from django.template.defaultfilters import capfirst
from pony_indice import models
from pony_indice import settings


def create_or_update_link(instance, model_class, options):
    # Skip
    skip = options['skip']
    if callable(skip):
        skip = skip(instance)
    if skip:
        return
    # URL
    url = options['url']
    if callable(url):
        url = url(instance)
    elif url and hasattr(instance, url):
        url = getattr(instance, url)
        if callable(url):
            url = url(instance)
    elif not url and hasattr(instance, 'get_absolute_url'):
        url = instance.get_absolute_url()
    else:
        msg = "No method found for find the link's URL."
        raise Exception(msg)
    # Display
    display = options['display']
    if callable(display):
        display = display(instance)
    elif display and hasattr(instance, display):
        display = getattr(instance, display)
        if callable(display):
            display = display(instance)
    else:
        display = '%s : %s' % (
            capfirst(model_class._meta.verbose_name),
            str(instance))
    # Description
    description = options['description']
    if callable(description):
        description = description(instance)
    elif description and hasattr(instance, description):
        description = getattr(instance, description)
        if callable(description):
            description = description(instance)
    elif isinstance(description, str):
        description = description
    else:
        description = ''
    # Tags
    tags = options['tags']
    if callable(tags):
        tags = tags(instance)
    elif tags and hasattr(instance, tags):
        tags = getattr(instance, tags)
        if callable(tags):
            tags = tags(instance)
    elif isinstance(tags, str):
        tags = tags
    else:
        tags = '%s %s' % (instance._meta.verbose_name, str(instance))
    # Default rank
    rank = options['rank']
    if isinstance(rank, int):
        rank = rank
    elif callable(rank):
        rank = rank(instance)
    elif rank and hasattr(instance, rank):
        rank = getattr(instance, rank)
        if callable(rank):
            rank = rank(instance)
    # Create or Update
    link = models.Link.objects.filter(url=url).first()
    if link is None:
        create_kwargs = {}
        if rank is not None:
            create_kwargs = {'rank': rank}
        link = models.Link.objects.create(
            url=url, display=display, description=description,
            tags=tags, **create_kwargs)
    elif settings.AUTO_UPDATE_TAGS:
        link.tags = " ".join(set((tags + ' ' + link.tags).split()))
    link.display = display
    link.url = url
    link.save()
