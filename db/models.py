from django.db import models

import json


class Race(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bonus = models.CharField(max_length=255)
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="skills"
    )


class Guild(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class Player(models.Model):
    nickname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    bio = models.CharField(max_length=255)
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="players"
    )
    guild = models.ForeignKey(
        Guild,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members"
    )
    created_at = models.DateTimeField(auto_now_add=True)


def main() -> None:

    with open("player.json", "r") as file:
        data = json.load(file)

    for nickname, details in data.items():

        race_data = details.get("race", {})
        race, _ = Race.objects.get_or_create(
            name=race_data.get("name"),
            defaults={"description": race_data.get("description")}
        )

        for skill in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill["name"],
                defaults={"bonus": skill["bonus"], "race": race}
            )

        guild = None
        guild_data = details.get("guild")
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data.get("name"),
                defaults={"description": guild_data.get("description")}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": details["email"],
                "bio": details["bio"],
                "race": race,
                "guild": guild
            }
        )
