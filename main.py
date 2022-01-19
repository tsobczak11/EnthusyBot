import discord
import os
import requests
import json
import random
from replit import db
from hosting import hosting

client = discord.Client()

# SERVER DOWN FOR JOKE API #
#function to get a random joke from the api and display the joke in discord messages
# def get_joke():
#   response = requests.get("https://official-joke-api.appspot.com/random_joke")
#   json_data = json.loads(response.text)
#   joke = json_data['setup']
#   answer = json_data['punchline']
#   result = joke + "\n" + answer
#   return(result)

# def get_meme():
#   response = requests.get("http://alpha-meme-maker.herokuapp.com/")
#   json_data = json.loads(response.text)
#   return (json_data)

#function to get a random joke from the api and display the joke in discord messages
#filter jokes
def get_joke():
  response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist,explicit")
  #response = requests.get("https://v2.jokeapi.dev/joke/Any?")
  json_data = json.loads(response.text)
  joke = json_data['setup']
  answer = json_data['delivery']
  result = joke + "\n" + answer
  return(result)
  

#function to add a joke to the database
def update_joke(joke_msg):
  if "joke" in db.keys():
    joke = db["joke"]
    joke.append(joke_msg)
    db["joke"] = joke
  else:
    db["joke"] = [joke_msg]

#function to delete a joke from the database given an index from the list of jokes
def delete_joke(index):
  joke = db["joke"]
  if len(joke) > index:
    del joke[index]
    db["joke"] = joke

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('!help'):
        embedVar = discord.Embed(title="Hello and welcome to the EnthusyBot help menu", description="Below you will find all available commands to use with EnthusyBot!", color=0x87CEEB)
        embedVar.add_field(name="!joke", value="This command will generate a random joke.", inline=False)
        embedVar.add_field(name="!new", value="This command followed by a space and a text input will allow you to add your own personal jokes to be used by everyone.", inline=False)
        embedVar.add_field(name="!list", value="This command allows you to view the list of jokes added by users.", inline=False)
        embedVar.add_field(name="!delete", value="This command followed by a space and a number allows you to delete a joke at that number index in the list of jokes.", inline=False)
        await message.channel.send(embed=embedVar)

  #display random joke with !joke command
  if message.content.startswith('!joke'):
    joke = get_joke()
    await message.channel.send(joke)

  # if message.content.startswith('!meme'):
  #   meme = get_meme()
  #   await message.channel.send(meme)


  #pass the message from user to the function to append in database list
  if message.content.startswith('!new'):
    joke_message = message.content.split('!new ',1)[1]
    update_joke(joke_message)
    await message.channel.send("Congrats! You added a new joke!")

  #delete the joke at the index in the list
  if message.content.startswith('!delete'):
    joke = []
    if "joke" in db.keys():
      index = int(message.content.split("!delete",1)[1])
      delete_joke(index)
      joke = db["joke"]
    await message.channel.send(joke)

  #display list of jokes
  if message.content.startswith('!list'):
    joke = []
    if "joke" in db.keys():
      joke = list(db["joke"])
    main_message = "The list of jokes are as follows..."
    await message.channel.send(main_message)
    for x in range(len(joke)):
      await message.channel.send(joke[x])

  # display random personally created joke with !pjoke command
  if message.content.startswith('!pjoke'):
    joke = []
    if "joke" in db.keys():
      joke = db["joke"]
      joke_message = random.choice(joke)
      personal_joke = joke_message.split('?',1)
      first = personal_joke[0] + '?'
      second = personal_joke[1]
      result = first + "\n" + second
    await message.channel.send(result)


hosting()
client.run(os.getenv('TOKEN'))