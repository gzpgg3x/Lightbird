from django.db import models
from django.contrib import admin

from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.contrib.auth.models import User

# class Item(models.Model):
#     name = models.CharField(max_length=60)
#     created = models.DateTimeField(auto_now_add=True)
#     priority = models.IntegerField(default=0)
#     difficulty = models.IntegerField(default=0)
#     done = models.BooleanField(default=False)

# class ItemAdmin(admin.ModelAdmin):
#     list_display = ["name", "priority", "difficulty", "created", "done"]
#     search_fields = ["name"]

# admin.site.register(Item, ItemAdmin)

class DateTime(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        # return unicode(self.datetime)
        return unicode(self.datetime.strftime("%b %d, %Y, %I:%M %p"))

class Item(models.Model):
    # user = models.ForeignKey(User, blank=True, null=True)	
    name = models.CharField(max_length=60)
    created = models.ForeignKey(DateTime)
    priority = models.IntegerField(default=0)
    difficulty = models.IntegerField(default=0)
    done = models.BooleanField(default=False)
    def mark_done(self):
        return "<a href='%s'>Done</a>" % reverse("todo.views.mark_done", args=[self.pk])
    mark_done.allow_tags = True
    onhold = models.BooleanField(default=False)
    def mark_onhold(self):
        return "<a href='%s'>Onhold</a>" % reverse("todo.views.mark_onhold", args=[self.pk])
    mark_onhold.allow_tags = True

    progress = models.IntegerField(default=0)

    def progress_(self):
        return "<div style='width: 100px; border: 1px solid #ccc;'>" + \
          "<div style='height: 4px; width: %dpx; background: #555; '></div></div>" % self.progress
    progress_.allow_tags = True

class ItemAdmin(admin.ModelAdmin):
    list_display = ["name", "priority", "difficulty", "created", "done"]
    search_fields = ["name"]

class ItemInline(admin.TabularInline):
    model = Item

# class DateAdmin(admin.ModelAdmin):
#     list_display = ["datetime"]
#     inlines = [ItemInline]

# class User(admin.ModelAdmin):
#     user = models.ForeignKey(User, blank=True, null=True)

class DateAdmin(admin.ModelAdmin):
    list_display = ["datetime"]
    inlines = [ItemInline]

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """ Determines the HttpResponse for the add_view stage.  """
        opts = obj._meta
        pk_value = obj._get_pk_val()
        user = models.ForeignKey(User, blank=True, null=True)
        msg = "Item(s) were added successfully."
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.
        if request.POST.has_key("_continue"):
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if request.POST.has_key("_popup"):
                post_url_continue += "?_popup=1"
            return HttpResponseRedirect(post_url_continue % pk_value)

        if request.POST.has_key("_popup"):
            return HttpResponse(
              '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");'
              '</script>' % (escape(pk_value), escape(obj)))
        elif request.POST.has_key("_addanother"):
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") %
                                                    force_unicode(opts.verbose_name)))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            for item in Item.objects.filter(created=obj):
                if not item.user:
                    item.user = request.user
                    item.save()
            return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

        # user = models.ForeignKey(User, blank=True, null=True)
        # for item in Item.objects.filter(created=obj):
        #     if not item.user:
        #         item.user = request.user
        #         item.save()
        #     return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)