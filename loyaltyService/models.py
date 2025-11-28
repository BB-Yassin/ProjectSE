from django.db import models
class loyaltyTier(models.TextChoices):  
    BRONZE = 'BRONZE', 'Bronze'
    SILVER = 'SILVER', 'Silver'
    GOLD = 'GOLD', 'Gold'
    PLATINUM = 'PLATINUM', 'Platinum'   
# Create your models here.
class LoyaltyProgram(models.Model):
    user=models.OneToOneField('client.User', on_delete=models.CASCADE)
    points=models.PositiveIntegerField(default=0)
    enrolled_at=models.DateTimeField(auto_now_add=True) 
    tier = models.CharField(
        max_length=10,
        choices=loyaltyTier.choices,
        default=loyaltyTier.BRONZE,
    )
    totalEarnedPoints=models.PositiveIntegerField(default=0)
    totalRedeemedPoints=models.PositiveIntegerField(default=0)
    pointsExpiryDate=models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"LoyaltyProgram for {self.user.get_full_name()} - Tier: {self.tier}"