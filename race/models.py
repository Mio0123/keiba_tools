from django.db import models
from django.db.models import Sum

class Horse(models.Model):
    """競走馬モデル"""
    name = models.CharField("馬名", max_length=100, unique=True)
    created_at = models.DateTimeField("登録日", auto_now_add=True)

    def __str__(self):
        return self.name

class Bettor(models.Model):
    """投票者モデル"""
    name = models.CharField("投票者名", max_length=100, unique=True)

    def __str__(self):
        return self.name

class Race(models.Model):
    """レースモデル"""
    class Status(models.TextChoices):
        PREPARING = 'PREP', '準備中'
        OPEN = 'OPEN', '受付中'
        CLOSED = 'CLOSED', '受付終了'
        FINISHED = 'FIN', 'レース終了'

    name = models.CharField("レース名", max_length=200)
    held_date = models.DateField("開催日")
    horses = models.ManyToManyField(Horse, verbose_name="出走馬")
    stake_per_unit = models.PositiveIntegerField("一口当たりの掛け金", default=100)
    status = models.CharField("ステータス", max_length=10, choices=Status.choices, default=Status.PREPARING)
    
    # 控除率 (例: 25%の場合、払戻率は75%)
    DEDUCTION_RATE = 0.75

    def __str__(self):
        return self.name

    def get_total_sales(self):
        """このレースの総売上を計算する"""
        total_units = self.bet_set.aggregate(total=Sum('units'))['total'] or 0
        return total_units * self.stake_per_unit

class Bet(models.Model):
    """投票モデル"""
    class BetType(models.TextChoices):
        WIN = 'WIN', '単勝'
        TRIFECTA = 'TRI', '3連単'
        TRIO = 'TRO', '3連複'
        
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="レース")
    bettor = models.ForeignKey(Bettor, on_delete=models.CASCADE, verbose_name="投票者")
    bet_type = models.CharField("賭け式", max_length=3, choices=BetType.choices)
    units = models.PositiveIntegerField("口数")
    
    # 賭ける馬 (単勝ならhorse1のみ、3連系なら3頭)
    horse1 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='bet_horse1')
    horse2 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='bet_horse2', null=True, blank=True)
    horse3 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='bet_horse3', null=True, blank=True)

    def __str__(self):
        return f"{self.race.name} - {self.get_bet_type_display()}"


class InitialOdds(models.Model):
    """初期オッズモデル"""
    race = models.ForeignKey(Race, on_delete=models.CASCADE, verbose_name="レース")
    bet_type = models.CharField("賭け式", max_length=3, choices=Bet.BetType.choices)
    odds = models.FloatField("オッズ")
    
    # オッズの対象となる馬
    horse1 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='odds_horse1')
    horse2 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='odds_horse2', null=True, blank=True)
    horse3 = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name='odds_horse3', null=True, blank=True)

    def __str__(self):
        return f"{self.race.name} {self.get_bet_type_display()} オッズ"