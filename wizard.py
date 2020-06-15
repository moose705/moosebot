import random
import shared_functions

def stat_wizard(message, wizard_data):
  try:
    stat = int(message.content)
  except ValueError:
    return "That doesn't seem like a number buddy."
  if stat < 0:
    return "Negative stats aren't allowed at character creation; please submit a zero or positive number"
  wizard_data[wizard_data["Phase"]] = stat
  if wizard_data["Phase"] == "Strongness":
    wizard_data["Phase"] = "Smartness"
  elif wizard_data["Phase"] == "Smartness":
    wizard_data["Phase"] = "Coolness"
  elif wizard_data["Phase"] == "Coolness":
    return ""
  return ("What is your character's " + wizard_data["Phase"] + "?")

def trait_wizard(message, wizard_data):
  response = ""
  if wizard_data["Phase"] == "Coolness": 
    filename = "traits.json"
    num_samples = 3
    option_string = "Trait Options"
    wizard_data["Phase"] = "Traits"
  else:
    option_string = wizard_data["Phase"] + " Options"
    if option_string == "Traits Options":
      option_string = "Trait Options"
    if message.content not in wizard_data[option_string]:
      return "Choice not recognized as one of the options. Make sure you sent it exactly as shown, I am just a stupid robot..."
    if wizard_data["Phase"] == "Traits":
      filename = "blessings.json"
      num_samples = 5
      option_string = "Blessing Options"
      wizard_data["Phase"] = "Blessing"
      options_dict = shared_functions.get_dict_from_json("traits.json")
      wizard_data["Traits"].append("** " + message.content + "**: " + options_dict[message.content]) 
    else:
      options_dict = shared_functions.get_dict_from_json("blessings.json")
      wizard_data["Blessing"] = "**Blessing of " + message.content + "**: " + options_dict[message.content]
      return None
  options_dict = shared_functions.get_dict_from_json(filename)
  options = random.sample(options_dict.keys(), num_samples)
  wizard_data[option_string] = options
  response += "Choose **one** of the below random options:\n"
  for i in range(0,num_samples):
    response += "** " + options[i] + "**: " + options_dict[options[i]] + "\n"
  return response
