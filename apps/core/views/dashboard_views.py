from datetime import timedelta

from django.utils import timezone
from django.contrib.auth.models import Group
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.views import View


from apps.members.models import Member
from apps.inventory.models import Furniture
from apps.common.utils.choices import MemberRoleChoices






class DashboardView(View):
    def get(self, request):


        today = timezone.now()
        last_day = today - timedelta(days=10)

        recent_members = Member.objects.filter(
            created_at__range=[last_day, today]
        )[:10]
        total_members = Member.objects.all().count()
        roles = list(
            Group.objects.all()
            .annotate(count=Count('user'))
            .values('name', 'count')
        )
        furnitures = list(
            Furniture.objects.all()
            .values('status')
            .annotate(count=Count('status'))
        )
        return render(
            request,
            'core/dashboard.html',{
                'total_members': total_members,
                'roles': roles,
                'recent_members': recent_members,
                'furnitures': furnitures,

            }
        )


