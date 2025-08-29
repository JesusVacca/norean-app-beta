import pandas as pd
from urllib.parse import urlencode

from apps.common.utils.choices import MemberRoleChoices
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ( CreateView, ListView, UpdateView, View )
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group


from apps.members.models import Member
from apps.members.forms import MemberForm, MultipleMembersByCSVForm
from apps.common.utils.decorators import requires_permission
from apps.common.utils.notify import Notify

notify = Notify()


@method_decorator(requires_permission('members.add_member'), name='dispatch')
class CreateMemberView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:members:list')

    def form_valid(self, form):
        form.save(created_by=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Crear usuario'
        context['subtitle'] = 'Para crear un usuario, por favor llenar todos los campo requeridos'
        return context


@method_decorator(requires_permission('members.view_member'), name='dispatch')
class ListMembersView(ListView):
    model = Member
    template_name = 'members/list.html'
    context_object_name = 'members'
    paginate_by = 10
    def get_queryset(self):
        search = self.request.GET.get('search', "")
        selected_role = self.request.GET.get('selected_role', "")
        queryset = Member.objects.all().exclude(document_number=self.request.user.document_number)
        if not self.request.user.is_superuser:
            queryset = queryset.filter(groups__name__in=[MemberRoleChoices.STUDENT, MemberRoleChoices.STUDENT])
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(document_number__contains=search)
            )
        if selected_role:
            queryset = queryset.filter(groups__name=selected_role)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search']  = self.request.GET.get('search', "")
        context['selected_role']  = self.request.GET.get('selected_role', "")
        context['groups_user'] = Group.objects.all()
        return context

@method_decorator(requires_permission('members.change_member'), name='dispatch')
class UpdateMemberView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'recycle/create.html'
    success_url = reverse_lazy('management:members:list')
    slug_field = 'email'
    slug_url_kwarg = 'email'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text_button'] = 'Actualizar usuario'
        return context

@method_decorator(requires_permission('members.change_member'), name='dispatch')
@method_decorator(require_POST, name='dispatch')
class ToggleMemberStatusView(View):
    def post(self, request, *args, **kwargs):
        search = self.request.GET.get('search', "")
        selected_role = self.request.GET.get('selected_role', "")
        base_url = reverse('management:members:list')
        params = {}
        if search:
            params['search'] = search
        if selected_role:
            params['selected_role'] = selected_role
        try:
            member = Member.objects.get(email=kwargs['email'])
            member.is_active = not member.is_active
            member.save()
        except Member.DoesNotExist:
            pass
        return HttpResponseRedirect(f'{base_url}?{urlencode(params)}')


@method_decorator(requires_permission('members.change_member'), name='dispatch')
class CreateMultipleMembersByCSVView(View):
    form_class = MultipleMembersByCSVForm
    def get(self, request, *args, **kwargs):
        return render(
            request,
            'members/upload_members.html',{
                'form': self.form_class(),
            }
        )
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        try:
            if 'preview' in request.POST:
                if form.is_valid():
                        file = request.FILES['file_csv']
                        df = pd.read_csv(file)
                        session_data = df.to_dict(orient='records')
                        request.session['session_data'] = session_data
                        return render(
                            request,
                            'members/preview_members.html',{
                                'form': form,
                                'session_data': session_data,
                            }
                        )
            elif 'confirm' in request.POST:
                self.__confirm_creation(request)
                return redirect('management:members:list')
        except Group.DoesNotExist:
            pass
        except Exception as e:
            message = (
                "correo electrónico" if "email" in str(e)
                else "número de documento" if "document_number" in str(e)
                else "error desconocido"
            )
            notify.notify(request, f'Puede que algunos usuarios cargados, cuenten con {message} repetidos', 'error')
        return redirect('management:members:create-multiple-members')

    def __confirm_creation(self, request):
        student_group = Group.objects.get(name=MemberRoleChoices.STUDENT)
        cache_members = request.session['session_data']
        distinct_members = []
        clean_members = []
        build_members = []

        seen_emails = set()
        seen_document_numbers = set()
        total_members_load = 0

        # ---- First filter ----
        for member in cache_members:
            email = member['email']
            document_number = member['document_number']
            total_members_load += 1
            if (
                    Member.objects.filter(email=email).exists()
                    or Member.objects.filter(document_number=document_number).exists()
            ):
                continue
            distinct_members.append(member)

        # ----- Second filter -----
        for member in distinct_members:
            email = member['email']
            document_number = member['document_number']
            if email not in seen_emails and document_number not in seen_document_numbers:
                seen_emails.add(email)
                seen_document_numbers.add(document_number)
                member_instance = Member(
                    email=email,
                    document_number=document_number,
                    phone_number=member['phone_number'],
                    created_by=request.user,
                    document_type=member['document_type'],
                    first_name=member['first_name'],
                    last_name=member['last_name'],
                )
                member_instance.set_password(str(document_number))
                build_members.append(member_instance)

        # Inserción masiva
        created_members = Member.objects.bulk_create(build_members, batch_size=500)

        # Relación M2M masiva
        MemberGroup = Member.groups.through
        group_links = [
            MemberGroup(member_id=m.id, group_id=student_group.id)
            for m in created_members
        ]
        MemberGroup.objects.bulk_create(group_links, batch_size=500)

        # Limpieza de sesión
        del request.session['session_data']

        # Notificación
        total_members_saved = len(created_members)
        if total_members_load > 0:
            notify.notify(
                request=request,
                message=f'Usuarios creados {total_members_saved} de {total_members_load} cargados'
            )
            if total_members_saved > 0:
                notify.notify(
                    request=request,
                    message=f'La contraseña de cada usuario es su número de documento',
                    level='info'
                )










