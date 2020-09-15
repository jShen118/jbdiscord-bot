import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import random
import asyncio
import dnd

client = commands.Bot(command_prefix=">")

# EVENTS
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("beep boop"))
    print("Bot is ready")


@client.event
async def on_disconnect():
    await client.change_presence(status=discord.Status.offline)


@client.event
async def on_member_join(member):
    await member.channel.send(f"{member} has joined the server")


@client.event
async def on_member_remove(member):
    await member.channel.send(f"{member} has left a server")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("Bad argument. Please type again")
    elif isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("This command is not within your permissions")
    elif isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("This command does not exist")


# @client.event
# async def on_message(message):
#    if message.author != client.user and "bruh" in message.content.lower():
#        await message.channel.send(file=discord.File("bruh.jpeg"))
#    await client.process_commands(message)


# @client.event
# async def on_message_delete


# COMMANDS
@client.command(help="<int> Clears messages")
@has_permissions(administrator=True)
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)


@client.command(help="<mention> Kicks a member off the server")
@has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


@client.command(help="Shows ping of the bot")
async def ping(ctx):
    await ctx.send(f"{round(client.latency * 1000)}ms")


@client.command(aliases=["8ball", "testalias"], help="<question> Predicts the future")
async def _8ball(ctx, *, question):
    responses = [
        "It is certain",
        "It is decidedly so",
        "Without a doubt",
        "Yes, definitely",
        "You may rely on it",
        "As I see it, yes",
        "Most likely",
        "Outlook good",
        "Yes",
        "Signs point to yes",
        "Reply hazy, try again",
        "Ask again later",
        "Better not tell you now",
        "Cannot predict right now",
        "Concentrate and ask again",
        "Don't count on it",
        "No",
        "My sources say no",
        "Outlook not so good",
        "Very doubtful",
    ]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command(help = "Flips a coin")
async def coinflip(ctx):
    await ctx.send("Heads" if random.randint(1,2) == 1 else "Tails")


@client.command(help = "<math expression> Does arithmetic")
async def calc(ctx, *, expression):
    if set(expression).issubset(set("0123456789+-*/.()")):
        await ctx.send(eval(expression))
    else: await ctx.send("Bad argument. Please type again")


@client.command(help = "<delay(HH:MM)> <message>")
async def remindme(ctx, *, arg):
    argList = arg.split()
    # print(argList)
    time = argList[0]
    if not (len(time) == 5 and time[0:2].isnumeric() and time[2] == ":" and time[3:5].isnumeric()):
        await ctx.send("Please enter a valid delay time")
        return
    delay = 3600*int(time[0:2]) + 60*int(time[3:5])

    if len(argList) == 1:
        await asyncio.sleep(delay)
        await ctx.message.author.send("Reminder: " + ctx.message.jump_url)
    elif len(argList) >= 2:
        await asyncio.sleep(delay)
        await ctx.message.author.send("Reminder: " + " ".join(argList[1:]))

@client.command(help = "<num die>d<dice sides>")
async def roll(ctx, *, arg):
    argList = arg.split("d")
    print(argList)
    message = "["
    sum = 0
    print("b1")
    for _ in range(int(argList[0])):
        print("b2")
        n = random.randint(1,int(argList[1]))
        print("b3")
        message += f"{n}, "
        sum += int(n)
    message = message[:-2]
    message += f"] Sum: {sum}"
    await ctx.send(message)

@client.command(help = "generates a quest for DnD")
async def quest(ctx):
    rewardMultiplier = 1
    aRoll = random.randint(1,20)
    while aRoll == 19 or aRoll == 20:
        if aRoll == 19: rewardMultiplier = 2
        aRoll = random.randint(1,20)
    # past this point aRoll is between 1 and 18
    action = dnd.actions[aRoll - 1]
    sRoll = random.randint(1,10)
    difficulty = random.randint(1,100) + dnd.actionDictionary[action][sRoll - 1][1]
    rIndex = 0
    # determining where to index in the rewards array based on difficulty
    if -41 <= difficulty <= -20: rIndex =1
    elif -19 <= difficulty <= 0: rIndex = 2
    elif 1 <= difficulty <= 30: rIndex = 3
    elif 31 <= difficulty <= 40: rIndex = 4
    elif 41 <= difficulty <= 50: rIndex = 5
    elif 51 <= difficulty <= 60: rIndex = 6
    elif 61 <= difficulty <= 70: rIndex = 7
    elif 71 <= difficulty <= 80: rIndex = 8
    elif 81 <= difficulty <= 85: rIndex = 9
    elif 86 <= difficulty <= 90: rIndex = 10
    elif 91 <= difficulty <= 95: rIndex = 11
    elif 96 <= difficulty <= 100: rIndex = 12
    elif 101 <= difficulty <= 110: rIndex = 13
    elif 111 <= difficulty <= 115: rIndex = 14
    elif 116 <= difficulty <= 120: rIndex = 15
    elif 121 <= difficulty <= 125: rIndex = 16
    elif 126 <= difficulty <= 130: rIndex = 17
    elif 131 <= difficulty <= 139: rIndex = 18
    elif 140 <= difficulty <= 145: rIndex = 19
    elif 146 <= difficulty <= 150: rIndex = 20
    elif 151 <= difficulty <= 155: rIndex = 21
    elif 156 <= difficulty <= 160: rIndex = 22
    else: rIndex = -1

    rewards = "2 x [" if rewardMultiplier == 2 else "["
    special = True if random.randint(1,2) == 1 else False
    if special:
        numPrevious = random.randint(1,4)
        for r in dnd.specialRewardArray[(rIndex-numPrevious):(rIndex+1)]:
            rewards += f"{r}, "
        rewards = rewards[:-2]
    else:
        rewards += f"{dnd.rewardArray[rIndex][1]} {dnd.rewardArray[rIndex][0]}"
    rewards += "]"
    await ctx.send(f"Action: {action}\nSpecifics: {dnd.actionDictionary[action][sRoll - 1][0]}")
    await ctx.send(f"Difficulty: {difficulty}\nRewards: {rewards}")


@client.command(help = "generates a DnD feat")
async def feat(ctx):
    await ctx.send(dnd.feats[random.randint(1, 42) - 1])

@client.command(help = "generates a DnD boon")
async def boon(ctx):
    await ctx.send(dnd.boons[random.randint(1, 26) - 1])

"""
import pint
@client.command(help = "<quantity> <from unit> <to unit> Converts units")
async def uc(ctx, quant, bu, au):
    if not quant.isnumeric():
        await ctx.send("Bad argument. Please type again")
        return"""


client.run("private token")
