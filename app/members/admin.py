from django.contrib import admin

from members.models import (
    Member, MemberInfo, MemberImage, MemberRibbon, Star, Pick, Tag, TagTypeSelection, Story
)

admin.site.register(Member)
admin.site.register(MemberInfo)
admin.site.register(MemberImage)
admin.site.register(MemberRibbon)
admin.site.register(Star)
admin.site.register(Pick)
admin.site.register(Tag)
admin.site.register(TagTypeSelection)
admin.site.register(Story)
