from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F

class UrlVisitor(models.Model):
    ip_address  = models.CharField(
        max_length = 15,
        null = False,
        blank = False,
        unique = True
    )
    def __str__(self):
        return self.ip_address
    def visited_links(self):
        links = UrlVisit.objects.filter(
            visitor = self
        ).values(name = F('visited_url__name'))
        return links

    def visited_links_and_count(self):
        links = UrlVisit.objects.filter(
            visitor = self
        ).values(
            'visit_count', name = F('visited_url__name')
        )
        return links

class UrlShortener(models.Model):
    name    = models.CharField(
        max_length = 50,
        unique = True,
        blank = False,
        null = False
    )
    target  = models.URLField(
        blank = False, null = False
    )
    visitors= models.ManyToManyField(
        to = UrlVisitor, through = 'UrlVisit'
    )

    def __str__(self):
        return self.name

    def visitor_count(self):
        return self.visitors.count()

    def total_visits(self) -> int:
        count = UrlVisit.objects.filter(
            visited_url = self
        ).aggregate(Sum('visit_count'))
        return count['visit_count__sum']

    def visit(self, ip_address : str):
        try:
            visitor = UrlVisitor.objects.get(ip_address = ip_address)
            try:
                url_log = UrlVisit.objects.get(
                    visitor = visitor, visited_url = self
                )
                url_log.visit_count += 1
                url_log.save()
            except ObjectDoesNotExist:
                url_log = UrlVisit(
                    visitor = visitor, visited_url = self, visit_count = 1
                )
                url_log.save()
                return
        except ObjectDoesNotExist:
            visitor = UrlVisitor(ip_address = ip_address)
            visitor.save()
            url_log = UrlVisit(
                visitor = visitor, visited_url = self, visit_count = 1
            )
            url_log.save()



class UrlVisit(models.Model):
    visitor     = models.ForeignKey(
        to = UrlVisitor, on_delete = models.CASCADE
    )
    visited_url =models.ForeignKey(
        to = UrlShortener, on_delete = models.CASCADE
    )
    visit_count = models.BigIntegerField(default = 0)

    class Meta:
        unique_together = ('visitor', 'visited_url')

    def __str__(self):
        return '{visitor_name} {visited_url} {visit_count}'.format(
            visitor_name    = self.visitor.ip_address,
            visited_url     = self.visited_url.name,
            visit_count     = self.visit_count
        )
