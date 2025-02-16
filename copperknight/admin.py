from django.contrib import admin
from .models import User, Opus, FavoritedOpus

admin.site.register(User)


@admin.register(Opus)
class OpusAdmin(admin.ModelAdmin):
    list_display = ["title", "created_by", "created_at"]

    def __str__(self):
        return self.title


admin.site.register(FavoritedOpus)
