from todo.models import *
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def mark_done(request, pk):
    item = Item.objects.get(pk=pk)
    item.done = True
    item.onhold = True
    item.save()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

def __unicode__(self):
    return unicode(self.datetime.strftime("%b %d, %Y, %I:%M %p"))