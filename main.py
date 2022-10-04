from discord.ext import commands
import discord
client = commands.Bot(command_prefix="-",help_command=None, intents=discord.Intents().all())
import pickle
import random
from datetime import datetime, timedelta
import asyncio


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(str(len(getuserinfo())) + " Career Mode pilots"))
  print("ready")
#  while True:
#    print('meow')
#    await activitycheck()
#    await asyncio.sleep(1)

  
def getuserinfo():
  try:
    uidoc = open("userinfo.pkl","rb")
    ui = pickle.load(uidoc)
  except:
    ui = {}
  return ui


def edituservalue(key,userid,value):
  ui = getuserinfo()
  uilist = ui[userid]
  if key < 2:
    uilist[int(key)] = float(value)
  else:
    uilist[int(key)] = value
  ui.update({userid: uilist})
  pickle.dump(ui,open("userinfo.pkl","wb"))


async def getflightembed(picked):
  try:
    fleetnew = picked["fleetnew"]
  except:
    fleetnew = "N.A."
  if fleetnew == "": fleetnew = "N.A."
  try:
    time = picked["time"]
  except:
    time = "N.A."
  if picked["fleet"] == "":
    picked["fleet"] = "N.A."
  if "assignedtime" in picked:
    embed = discord.Embed(title="Assigned Flight Information",color=0x00FF00,timestamp=picked["assignedtime"])
  else:
    embed = discord.Embed(title="Assigned Flight Information",color=0x00FF00)
  embed.add_field(name="Departing Airport",value=picked["dep"].strip(),inline=True)
  embed.add_field(name="Arriving Airport",value=picked["arr"].strip(),inline=True)
  embed.add_field(name="Airline",value=picked["airline"].strip(),inline=True)
  embed.add_field(name="Flight Number",value=picked["num"].strip(),inline=True)
  embed.add_field(name="Aircraft",value=picked["fleet"].strip(),inline=True)
  embed.add_field(name="Aircraft (Updated)",value=fleetnew,inline=True)
  embed.add_field(name="Flight Time",value=time,inline=False)
  user = await client.fetch_user(picked["userid"])
  embed.set_footer(text="Remember to file your flight within 3 days! (Pilot User ID: {})".format(picked["userid"]))
  embed.set_author(name=user.name, icon_url=user.avatar.url)
  return embed


async def generateflight(ctx, userid):
  routes = pickle.load(open("routes.pkl","rb"))
  airport = getuserinfo()[userid][2]
  possible = []
  for x in routes:
    if x["dep"] == airport:
      possible.append(x)
  picked = random.choice(possible)
  userdict = {"userid": userid, "assignedtime": datetime.utcnow(), "alerted": False}
  picked.update(userdict)
  edituservalue(3, userid, picked)
  await ctx.send(embed= await getflightembed(picked))

  
class Confirm(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
  @discord.ui.button(label='Assign New Task (-50 coins)', style=discord.ButtonStyle.green)
  async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = True
    self.hub = False
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

  @discord.ui.button(label='Return to Hub & Assign New Task (-75 coins)', style=discord.ButtonStyle.blurple)
  async def hub(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = True
    self.hub = True
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

    # This one is similar to the confirmation button except sets the inner value to `False`
  @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
  async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = False
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)


class Exchange(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
  @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
  async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = True
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

    # This one is similar to the confirmation button except sets the inner value to `False`
  @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
  async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = False
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)


class Late(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
  @discord.ui.button(label='Late', style=discord.ButtonStyle.red)
  async def late(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = True
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

    # This one is similar to the confirmation button except sets the inner value to `False`
  @discord.ui.button(label='On Time', style=discord.ButtonStyle.green)
  async def ontime(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = False
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)


class Assign(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
  @discord.ui.button(label='Flight #1', style=discord.ButtonStyle.blurple)
  async def flight1(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = True
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

    # This one is similar to the confirmation button except sets the inner value to `False`
  @discord.ui.button(label='Flight #2', style=discord.ButtonStyle.blurple)
  async def flight2(self, interaction: discord.Interaction, button: discord.ui.Button):
    self.value = False
    self.stop()
    button.disabled = True
    await interaction.response.edit_message(view=self)

    
#unused because I am stupid
@client.event
async def activitycheck():
  userinfo = getuserinfo()
  for i in userinfo:
    x = userinfo[i]
    if "assignedtime" in x[3].keys() and "alerted" in x[3].keys():
      if datetime.utcnow() > x[3]["assignedtime"] and x[3]["alerted"] == False:
        print(x[3])
        await client.get_user(149371027510525954).send(embed=discord.Embed(title="Late Flight Warning", description="Our records show that your flight from {} to {} was assigned 2 days ago. Ignore this message if you have already filed your flight. However, if you do not file this flight in the next 24 hours, your flight will be late and you will lose some of your coins!".format(x[3]["dep"], x[3]["arr"])))
        x[3].update({"alerted": True})
        edituservalue(3, i, x[3])

        
#mod-only  
@client.command()
@commands.has_role('Staff')
async def edituser(ctx, key, userid, value):
  edituservalue(int(key),userid,value)
  text = ""
  if int(key) == 0: text = "Coin Balance"
  elif int(key) == 1: text = "Flight Time"
  elif int(key) == 2: text = "Current Airport"
  elif int(key) == 4: text = "Hub Airport"
  await ctx.send("Successfully set {} of <@!{}> to {}".format(text,userid,value))


@client.command()
async def setupuser(ctx, userid=None, hub=None):
  if userid and hub:
    ui = getuserinfo()
    ui.update({userid: [0,0,hub.upper(),{},hub.upper()]})
    pickle.dump(ui,open("userinfo.pkl","wb"))
    embed = discord.Embed(title="Successfully Registered",color=0x00FF00)
    user = await client.fetch_user(userid)
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    embed = discord.Embed(title="Welcome to CXVA Career Mode!",description="You have been registered with the hub airport of {}. Use the command -guide for an introduction to Career Mode! Feel free to ask a staff member for help.".format(hub),color=0x00FF00)
    try:
      await user.send(embed=embed)
    except:
      await ctx.send("Unable to send DM to the user.")
      await client.get_channel(978609206397653043).send("<@!{}>, you have been registered into CXVA Career Mode, but you do not allow DMs from me! Please allow direct messages from members in this server.".format(userid))
  else:
    await ctx.send("Please provide the user ID/hub airport (ICAO)")

    
#both
@client.command()
async def checkinfo(ctx, userid=None):
  if userid != None:
    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
    if role not in ctx.author.roles:
      userid = str(ctx.author.id)
  else:
    userid = str(ctx.author.id)
  ui = getuserinfo()
  if userid in ui:
    uilist = ui[userid]
    embed = discord.Embed(title="Pilot Info",color=0x5865F2)
    embed.add_field(name="Coin Balance",value=str(uilist[0]))
    embed.add_field(name="Flight Time",value=str(uilist[1]))
    embed.add_field(name="Current Airport",value=str(uilist[2]))
    embed.add_field(name="Hub Airport",value=str(uilist[4]))
    user = await client.fetch_user(userid)
    embed.set_footer(text="Pilot User ID: {}".format(userid))
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    picked = uilist[3]
    if uilist[3] != {}:
      print("yo wtf")
      await ctx.send(embed= await getflightembed(picked))
    else:
      await ctx.send("You currently do not have a task assigned. Type *-getflight* to be assigned one!")
  else:
    await ctx.send("It would appear you are not in career mode.")


@client.command()
async def getflight(ctx, userid=None):
  if userid != None:
    role = discord.utils.find(lambda r: r.name == 'Staff', ctx.message.guild.roles)
    if role not in ctx.author.roles:
      userid = str(ctx.author.id)
  else:
    userid = str(ctx.author.id)
  if getuserinfo()[userid][3] == {}:
    await generateflight(ctx, userid)
  else:
    view = Confirm()
    await ctx.send(embed=discord.Embed(title="Task Already Assigned", description="You already have an assigned task, would you like to spend 50 coins to be reassigned a new task, or spend 75 coins to return to hub?",color=0xFF0000), view=view)
    await view.wait()
    if view.value is None:
        await ctx.send("You have timed out. <@!" + str(ctx.author.id) + ">")
    elif view.value:
      if getuserinfo()[userid][0] >= 50:
        if view.hub:
          edituservalue(2, userid, getuserinfo()[userid][4])
        await ctx.send("Assigning new task for you...")
        if view.hub:
          edituservalue(0,userid,getuserinfo()[userid][0]-75)
        else:
          edituservalue(0,userid,getuserinfo()[userid][0]-50)
        await generateflight(ctx,userid)
      else:
        await ctx.send(embed=discord.Embed(title="Insufficient Funds", description="You have insufficient funds!",color=0xFF0000))
    else:
      await ctx.send("You have cancelled your request.")

      
#mod-only
@client.command()
@commands.has_role('Staff')
async def listflights(ctx):
  flights = []
  templist = list(getuserinfo().values())
  for x in templist:
    if x[3] != {}:
      flights.append(x[3])
  if flights != []:
    await ctx.send("Now listing active tasks for all pilots.")
    for n in flights:
      await ctx.send(embed= await getflightembed(n))
  else: await ctx.send("There are no active tasks.")

    
#mod-only
@client.command()
@commands.has_role('Staff')
async def approveflight(ctx, userid=None, ft=None):
  if not userid or not ft:
    await ctx.send("Please provide a valid user ID/flight time value (in hours)!")
  elif getuserinfo()[userid][3] != {}:
    if ":" in ft:
      (h, m) = ft.split(':')
      ft = round(int(h)+int(m)/60,1)
    else:
      ft = float(ft)
    assignedtime = getuserinfo()[userid][3]["assignedtime"]
    late = False
    limit = assignedtime + timedelta(days=3)
    print(limit)
    timenow = datetime.utcnow()
    if timenow > limit:
      view = Late()
      difference = timenow - assignedtime
      await ctx.send(embed=discord.Embed(title="Potentially late flight",description="The records show that this flight was assigned {} ago. If the PIREP was filed after {} (UTC), it is late. Was this flight late?".format(str(difference),str(limit))),view=view)
      await view.wait()
      if view.value is None:
        await ctx.send("You have timed out. <@!" + str(ctx.author.id) + ">")
        return
      elif view.value:
        late = True
    if late:  
      coins = round(float(ft)*12)
      coinstr = str(coins) + "({} coins were deducted because of a late flight)".format(round(float(ft)*8))
    if not late:
      coins = round(float(ft)*20)
      coinstr = str(coins)
    edituservalue(0,userid,getuserinfo()[userid][0]+coins)
    edituservalue(1,userid,getuserinfo()[userid][1]+ft)
    edituservalue(2,userid,getuserinfo()[userid][3]["arr"])
    edituservalue(3,userid,{})
    user = await client.fetch_user(userid)
    embed = discord.Embed(title="Flight Approved", description="{} flight hours has been added. They have earned {} coins.".format(ft,coinstr,color=0x00FF00))
    embed.set_author(name=user.name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    user = await client.fetch_user(userid)
    try:
      await user.send(embed=discord.Embed(title="Career Mode Flight Approved", description="Your latest Career Mode flight has been approved, you have earned {} flight hours and {} coins.".format(ft,str(round(float(ft)*20))),color=0x00FF00))
    except:
      await ctx.send("Unable to send DM to that user.")
      await client.get_channel(978609206397653043).send("<@!{}>, your latest Career Mode has been approved earning you {} flight hours and {} coins, but you do not allow DMs from me! Please allow direct messages from members in this server.".format(userid,ft,str(round(float(ft)*20))))
  else:
    await ctx.send("This user does not have an active task!")

    
#mod-only
@client.command()
@commands.has_role('Staff')
async def assignflight(ctx,userid=None, flightnum=None):
  if not userid or not flightnum:
    await ctx.send("Please provide a valid user ID/flight number!")
  else:
    routes = pickle.load(open("routes.pkl","rb"))
    found = False
    flights = []
    for x in routes:
      if x["num"].strip() == flightnum:
        flights.append(x)
        found = True
    if found:
      if len(flights) > 1 and len(flights) <= 2:
        message = "There are 2 flights with the flight number " + flightnum + "."
        for n in flights:
          message = message + "\nFlight #{}:```{} -> {}```".format(flights.index(n)+1,n["dep"],n["arr"])
        message = message + "\nPlease select the correct flight to assign."
        view = Assign()
        await ctx.send(message, view=view)
        await view.wait()
        if view.value is None:
          await ctx.send("You have timed out.")
        elif view.value:
          flight = flights[0]
        else:
          flight = flights[1]
      elif len(flights) > 2:
        await ctx.send("It shouldn't be possible for there two be more than 2 flights with the same flight number in the flight database. Please contact CXVA staff.")
      else:
        flight = flights[0]
      flight.update({"userid":userid, "assignedtime": datetime.utcnow(),"alerted": False})
      edituservalue(3, userid, flight)
      await ctx.send("Successfully assigned new flight for <@!" + userid + ">, new route is: " + flight["dep"] + "-" + flight["arr"])
      user = await client.fetch_user(userid)
      try:
        await user.send(embed=discord.Embed(title="New Flight Assignment", description="You have been assigned a new Career Mode flight:",color=0x00FF00))
        await user.send(embed= await getflightembed(flight))
      except:
        await ctx.send("Unable to send DM to that user.")
        await client.get_channel(978609206397653043).send("<@!{}>, you have been assigned a new Career Mode flight, but you do not allow DMs from me! Please allow direct messages from members in this server.".format(userid))
    else:
      await ctx.send("No such flight was found.")


@client.command()
async def exchange(ctx, coins):
  if coins.isdigit():
    if int(coins) <= getuserinfo()[str(ctx.author.id)][0]:
      view = Exchange()
      await ctx.send(embed=discord.Embed(title="Exchange Coins -> Flight Time",description="Confirm that you would like to exchange {} coins for {} hours of flight time?".format(coins,str(round(int(coins)/100,1))),color=0x5865F2),view=view)
      await view.wait()
      if view.value is None:
        await ctx.send("You have timed out. <@!" + str(ctx.author.id) + ">")
      elif view.value:
        edituservalue(0,str(ctx.author.id),getuserinfo()[str(ctx.author.id)][0]-int(coins))
        edituservalue(1,str(ctx.author.id),getuserinfo()[str(ctx.author.id)][1]+round(int(coins)/100,1))
        await ctx.send("Your exchange has been successfully processed. Please wait for a staff member to update your flight hours on the crew center website.")
        await client.get_channel(832606209868562502).send("<@!741555581864771624> | Pilot <@!{}> has requested to exchange {} coins for {} flight hours.".format(str(ctx.author.id),coins,str(round(int(coins)/100,1))))
      else:
        await ctx.send("You have cancelled your request.")
    else: await ctx.send("You do not have sufficient funds!")
  else: await ctx.send("Please input an integer number of coins that you would like to exchange.")


@client.command()
async def guide(ctx):
  await ctx.send('''**Career Mode User Guide**\n\nWelcome to Career Mode! After you have been registered into Career Mode by our staff, you may now fly Career Mode flights. You will begin at your selected hub airport, and you will be assigned flights that originate from your current airport.\n\nOur staff will manually assign flights that you will fly. The bot will notify you when this occurs, thus you must allow DMs from the bot. Once you have finished the flight, file a PIREP in the crew center as usual. The staff team will review and approve it. You will again receive a notification from the bot once it is approved, and you will automatically earn 20 coins for each flight hour. You will then be able to embark on your next flight!\n\nYou can interact with the bot in #bot-commands. The commands available to you are:\n\n`-getflight` | If you were assigned a flight and are unwilling/unable to fly it, run this command to pay 50 coins to be automatically assigned a new flight, or pay 75 coins to return to your hub airport and be assigned a new flight from your hub airport.\n\n`-checkinfo` | Check your coin balance, flight hours, current airport, hub airport and flight information.\n\n`-exchange [number of coins]` | Run this command to exchange coins for flight hours, which will help you be promoted faster. You can exchange 100 coins for 1 flight hour.''')


@client.command()
@commands.has_role('Staff')
async def removeuser(ctx,userid=None):
  if userid != None and userid in getuserinfo():
    userlist = getuserinfo()
    userlist.pop(userid)
    pickle.dump(userlist,open("userinfo.pkl","wb"))
    await ctx.send("<@!{}> has been removed from Career Mode.".format(userid))
  await ctx.send("Please provide a valid user ID!")


@client.command()
@commands.has_role('Staff')
async def listusers(ctx):
  text = "Now listing all users."
  for user in getuserinfo():
    text += "\n- <@!{}> (User ID: {})".format(user,user)
  await ctx.send(text)


@client.command()
@commands.has_role('Staff')
async def debug(ctx):
  await ctx.send(getuserinfo())
      
    

client.run("OTc4MzIzNjI2MzM4MTc3MDQ1.GU4EGQ.MsZelP_yuQeJvVMPVN30dqDwQ4sjsMprSlZysM")
