from django.contrib import admin
from .models import Horse, Race, Bet, InitialOdds

# レース登録画面で初期オッズを同時に入力できるようにする設定
class InitialOddsInline(admin.TabularInline):
    model = InitialOdds
    extra = 1 # 最初から表示する空のフォーム数

@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'held_date', 'stake_per_unit', 'status')
    list_filter = ('held_date', 'status')
    filter_horizontal = ('horses',) # 出走馬を選択しやすくするUI
    inlines = [InitialOddsInline] # レース画面に初期オッズ入力欄を埋め込む

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('race', 'bet_type', 'units', 'horse1', 'horse2', 'horse3')
    list_filter = ('race',)