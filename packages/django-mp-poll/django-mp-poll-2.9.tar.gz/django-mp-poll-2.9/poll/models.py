
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from ordered_model.models import OrderedModelBase


class Poll(models.Model):

    question = models.CharField(_('Question'), max_length=255)

    created = models.DateTimeField(_('Created'), auto_now_add=True)

    votes = models.IntegerField(_('Votes'), default=0, editable=False)

    def is_voted(self, user, user_ip, session_key):
        check_query = Q(ip=user_ip) | Q(session=session_key)

        if user.is_authenticated:
            check_query = check_query | Q(user=user)

        return self.vote_set.filter(check_query).exists()

    def __str__(self):
        return self.question

    class Meta:
        get_latest_by = 'id'
        ordering = ['-id']
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')


class PollChoice(OrderedModelBase):

    poll = models.ForeignKey(
        Poll, verbose_name=_('Poll'), related_name='choices',
        on_delete=models.CASCADE)

    value = models.CharField(_('Value'), max_length=255)

    votes = models.IntegerField(_('Votes'), default=0, editable=False)

    order = models.PositiveIntegerField(_('Ordering'), default=0)

    order_field_name = 'order'
    order_with_respect_to = 'poll'

    @cached_property
    def percent(self):
        if self.votes:
            return int(float(self.votes) / float(self.poll.votes) * 100)
        return 0

    def __str__(self):
        return self.value

    class Meta:
        ordering = ('order', 'id', )
        unique_together = ['poll', 'value']
        verbose_name = _('Poll choice')
        verbose_name_plural = _('Poll choices')


class Vote(models.Model):

    user = models.ForeignKey(
        get_user_model(), verbose_name=_('User'), null=True, editable=False,
        on_delete=models.SET_NULL)

    poll = models.ForeignKey(
        Poll, verbose_name=_('Poll'), on_delete=models.CASCADE)

    choice = models.ForeignKey(
        PollChoice, verbose_name=_('Choice'), on_delete=models.CASCADE)

    created = models.DateTimeField(
        _('Created'), editable=False, auto_now_add=True, db_index=True)

    ip = models.CharField(_('IP'), max_length=40, editable=False, db_index=True)

    session = models.CharField(
        _('Session'), max_length=40, editable=False, db_index=True)

    user_agent = models.CharField(
        _('User agent'), max_length=255, editable=False)

    def __str__(self):
        return self.choice.value

    class Meta:
        ordering = ['-created']
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
