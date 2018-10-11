from .forms import MakeMessageForm
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Profile
from django.contrib.auth import get_user_model
from message_group.forms import MakeMessageGroupForm
from message_group.models import GroupMessage
from notify.signals import notify
from django.contrib.auth.decorators import login_required
User = get_user_model()


@login_required
def make_a_message(request, pk):
    recipient = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = MakeMessageForm(data=request.POST, files=request.FILES)
        form2 = MakeMessageGroupForm(request.POST)
        form3 = MakeMessageGroupForm(request.POST)

        if form.is_valid() and form2.is_valid() and form3.is_valid():
            notify.send(sender=request.user, actor=request.user, recipient=recipient.user, verb='new message', nf_type='followed_by_one_user')

            my_message = form.save(commit=False)
            my_message.recipient = recipient
            my_message.author = request.user
            my_message.save()

            request_user_message_group_form2 = form2.save(commit=False)
            foreign_user_message_group_form3 = form3.save(commit=False)

            request_user_message_group_form2.member = recipient
            foreign_user_message_group_form3.member = request.user.profiles

            request_user_message_group_form2.user = request.user
            foreign_user_message_group_form3.user = recipient.user

            if_obj_form2_exists = GroupMessage.objects.filter(member=recipient, user__exact=request.user).exists()
            if_obj_form3_exists = GroupMessage.objects.filter(member=request.user.profiles, user=recipient.user).exists()

            if if_obj_form2_exists and if_obj_form3_exists:
                return redirect('accounts:detail_messages', pk=recipient.pk)

            elif if_obj_form2_exists == True and if_obj_form3_exists == False:
                foreign_user_message_group_form3.save()
                return redirect('accounts:detail_messages', pk=recipient.pk)

            elif if_obj_form2_exists == False and if_obj_form3_exists == True:
                request_user_message_group_form2.save()
                return redirect('accounts:detail_messages', pk=recipient.pk)

            else:
                request_user_message_group_form2.save()
                foreign_user_message_group_form3.save()
                return redirect('accounts:detail_messages', pk=recipient.pk)
    else:
        form = MakeMessageForm()
        form2 = MakeMessageGroupForm
        form3 = MakeMessageGroupForm

    return render(request, 'mymessage/mymessage_form.html', {'form': form, 'form2': form2, 'form3': form3})


