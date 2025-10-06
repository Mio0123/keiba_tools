from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Race, Bet
from django.db.models import Sum

# デバッグ用のヘルスチェック（これはそのまま残します）
def health_check(request):
    return HttpResponse("Hello, Vercel! Health check from race.views is OK.")

# ▼▼▼ 以下2つの関数を新しく追加（または上書き）▼▼▼

# 受付中のレース一覧を表示するビュー
def race_list(request):
    # ステータスが「受付中」のレースを、開催日が新しい順に取得
    open_races = Race.objects.filter(status='OPEN').order_by('-held_date')
    context = {
        'races': open_races,
    }
    return render(request, 'race/race_list.html', context)

# 個別のレースの投票フォームを表示・処理するビュー
def betting_form(request, race_id):
    race = get_object_or_404(Race, pk=race_id)

    # フォームが送信された場合（POSTリクエスト）の処理
    if request.method == 'POST':
        for horse in race.horses.all():
            # HTMLのinputタグのname属性（'units_馬のID'）から口数を取得
            units_str = request.POST.get(f'units_{horse.id}')
            # 口数が入力されていて、0より大きい場合のみ
            if units_str and int(units_str) > 0:
                # 単勝（WIN）の投票(Bet)オブジェクトを作成してデータベースに保存
                Bet.objects.create(
                    race=race,
                    bet_type=Bet.BetType.WIN,
                    horse1=horse,
                    units=int(units_str)
                )
        # 処理が終わったら、レース一覧ページにリダイレクト
        return redirect('race_list')

    # 通常のページ表示（GETリクエスト）の場合の処理
    context = {
        'race': race,
    }
    return render(request, 'race/betting_form.html', context)

# レースのオッズ表示ビュー
def odds_display(request, race_id):
    race = get_object_or_404(Race, pk=race_id)

    # 1. レースの総売上と総口数を計算
    total_bet_units_agg = Bet.objects.filter(race=race).aggregate(total_units=Sum('units'))
    total_bet_units = total_bet_units_agg['total_units'] or 0
    total_sales = total_bet_units * race.stake_per_unit

    # 2. 払戻原資を計算 (控除率25%と仮定)
    payout_pool = total_sales * 0.75

    # 3. 各出走馬の単勝オッズと投票状況を計算
    horse_data = []
    for horse in race.horses.all().order_by('name'):
        # この馬の単勝への総投票口数を取得
        win_units_agg = Bet.objects.filter(
            race=race, horse1=horse, bet_type=Bet.BetType.WIN
        ).aggregate(total=Sum('units'))
        win_units_on_horse = win_units_agg['total'] or 0
        win_sales_on_horse = win_units_on_horse * race.stake_per_unit

        # オッズを計算
        odds = 0  # 投票がない場合のデフォルト値
        if win_sales_on_horse > 0:
            odds = payout_pool / win_sales_on_horse
            # 1.5倍を下回らないように補正
            if odds < 1.5:
                odds = 1.5
        
        horse_data.append({
            'horse': horse,
            'win_units': win_units_on_horse,
            'win_sales': win_sales_on_horse,
            'odds': round(odds, 1) if odds > 0 else '---' # 投票がなければ '---' と表示
        })

    context = {
        'race': race,
        'total_sales': total_sales,
        'total_bet_units': total_bet_units,
        'horse_data': horse_data,
    }
    return render(request, 'race/odds_display.html', context)