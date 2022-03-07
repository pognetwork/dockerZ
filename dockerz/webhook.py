from discord_webhook import DiscordWebhook, DiscordEmbed

colors = {"Green": 260128, "Red": 16253699}

 
def run(testResults, url, commitHash):
    shortHash = commitHash[0:7]
    webhook = DiscordWebhook(url=url)
    color = colors["Green"]
    commitURL = f"https://github.com/pognetwork/champ/commit/{shortHash}"
    embed = DiscordEmbed(
        title="End-to-End Tests",
        description=f"[`{shortHash}`]({commitURL})",
        color=color,
    )

    for key, value in testResults.items():
        if not value.passed:
            color = colors["Red"]
        testResult = f"{'Pass' if value.passed else 'Failed - '}{'' if value.passed else value.context}"
        embed.add_embed_field(name=f"{key}:", value=testResult)

    embed.set_timestamp()
    embed.color = color
    webhook.add_embed(embed)

    response = webhook.execute()
