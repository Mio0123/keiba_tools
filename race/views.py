from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Race, Bet

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