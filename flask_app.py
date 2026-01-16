from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import re
import sys
import random


app = Flask(__name__)
app.secret_key = 'my_secret_key45435rt43w543'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 10000



Session(app)

file_structure = {
    "/": ["terminal-jerry.txt", "Dimension_C-137"],
    "Dimension_C-137": ['terminal-beth.txt','Citadel_of_Ricks','Rick&#39;s_garage'],
    "Citadel_of_Ricks": ['terminal-birdperson.txt','legal_records.txt','Morty&#39;s_Mind_Blowers'],
    "Morty&#39;s_Mind_Blowers": ['Unknown_location','terminal-squanchy.txt'],
    "Rick&#39;s_garage": ['rickbot.txt', 'terminal-summer.txt'],
    "Unknown_location": []#,
    #"prison_cell_" : ['rick.txt']
}



file_structure_terminus = {
    "Home" : ["WelcomeLetter.txt","WesternForest","NorthernMeadow","MIT"],
    "MIT" : ["AdmissionLetter.txt","StataCenter","AthenaCluster"],
    "StataCenter" : ["WaryEyeOfGradStudent.txt","HelpfulTA.txt"],
    "AthenaCluster" : ["Workstation.txt"],
    "WesternForest" : ["Sign.txt","BackSign.txt","SpellCastingAcademy"],
    "SpellCastingAcademy" : ["HurryingStudent.txt","PracticeRoom","Lessons"],
    "PracticeRoom" : ["Box","PracticeDummy1","PracticeDummy2","PracticeDummy3","PracticeDummy4","PracticeDummy5"],
    "Box" : [],
    "Lessons": ["Professor.txt"],
    "NorthernMeadow" : ["Pony.txt","EasternMountains"],
    "EasternMountains" : ["OldMan.txt","OldManuscripts.txt","Cave"],
    "Cave" : ["DarkCorridor","Staircase"],
    "DarkCorridoe" : ["DankRoom"],
    "DankRoom": ["Boulder.txt","SmallHole","Tunnel"], #tunnel is hidden mv
    "SmallHole" : ["Boulder.txt"],
    "Tunnel" : ["Rat.txt","StoneChamber"],
    "StoneChamber" : ["Portal"],
    "Portal": ["TownSquare"],
    "TownSquare" : [ "RandomCitizen1.txt","RandomCitizen2.txt","DistraughtLady.txt","MarketPlace","Library","RockyPath","ArtisanShop","BrokenBridge"],
    "MarketPlace" : ["Vendor.txt","rmSpell.txt","mkdirSpell.txt"],
    "Library" : ["TotallyRadSpellBook.txt","PaperbackRomance.txt","HistoryOfTerminus.txt","NostalgiaForHome.txt","InconspicousLever.txt","BackRoom"], #lever shows backroom
    "BackRoom" : ["Grep.txt","Librarian.txt"],
    "RockyPath" : ["LargeBoulder.txt","Farm"], #farm is hidden rm
    "Farm" : ["EarOfCorn.txt","Farmer.txt"], #copy corn for reward
    "ArtisanShop" : ["StrangeTrinket.txt","ClockworkDragon.txt","Artisan.txt"],#touch to start conv. copy for reward
    "BrokenBridge" : ["Clearing"], #touch plank to fix bridge
    "Clearing" : ["CryingMan.txt","OminousLookingPath"], #mkdir a house - for password
    "OminousLookingPath" : ["ThornyBrambles.txt","Cave"], #rm brambles with password to enter cave
    "Cave" : ["UglyTroll.txt","UglierTroll.txt","HideousTroll.txt","Cage"], #rm ug trolls, #mv hideous troll
    "Cage" : ["KidnappedChild.txt"] #mv to escape

}

folder_images_terminus = {
    "Home" : "",
    "MIT" : "",
    "StataCenter" : "",
    "AthenaCluster" : "",
    "WesternForest" : "",
    "SpellCastingAcademy" : "",
    "PracticeRoom" : "",
    "Box" : "",
    "Lessons": "",
    "NorthernMeadow" : "",
    "EasternMountains" : "",
    "Cave" : "",
    "DarkCorridoe" : "",
    "DankRoom": "",
    "SmallHole" : "",
    "Tunnel" : "",
    "StoneChamber" : "",
    "Portal": "",
    "TownSquare" : "",
    "MarketPlace" : "",
    "Library" : "",
    "BackRoom" : "",
    "RockyPath" : "",
    "Farm" : "",
    "ArtisanShop" : "",
    "BrokenBridge" : "",
    "Clearing" :"",
    "OminousLookingPath" : "",
    "Cave" : "",
    "Cage" : ""
}

folder_text_terminus = {
     "Home" : ["""
Welcome! If you are new to the game, here are some tips:
Look at your surrounds with the command: ls (look at surroundings)
Move to a new location with: cd [location] (choose destination)
You can backtrack with the command: cd ..
Interact with things in world with: cat [item] (look at, examine, or speak to
something)
Go ahead. Explore. We hope you enjoy what you find.
"""],
    "MIT" : ["""
You have arrived by magic carpet to MIT!
"""],
    "StataCenter" : ["""
The center of computer science and artificial intelligence research at MIT.
Lots of magic happens here, including TAs, grad students, etc.
"""],
    "AthenaCluster" : ["""
None shall pass without the combination.
Youhave one chance to enter the combination.
Enter password:
"""],
    "WesternForest" : ["""
You enter and travel deep into the forest. Eventually, the path leads to a clearing with a
large impressive building. A sign on it reads: Spell Casting Academy: The Elite School of
Magic.
"""],
    "SpellCastingAcademy" : ["""
The halls are filled the hustle and bustle of academy students scurrying to and from
classes. The inside of the academy is as impressive as it is on the outside—with a high
ceiling and gothic arches, it seems even larger on the inside.
"""],
    "PracticeRoom" : ["""
The room is filled with practice dummies for students to practice their new spells on.
"""],
    "Box" : ["""
The box is too small for you to fit into. Trying “looking” into the box to see what’s inside (ls
Box).
"""],
    "Lessons": ["""
You enter the Lessons hall ready and eager. It’s much quieter here, as many of the
lessons have already started. You quickly ushered into the Introductory Lesson, which
already begun.
You enter the class on the "Move Spell."
"""],
    "NorthernMeadow" : ["""
This is a beautiful green meadow. A plump but majestic pony prances happily about.
"""],
    "EasternMountains" : ["""
You travel through a mountain path, which eventually leads you to the entrance of a cave.
Sitting right outside this cave is an old man.
"""],
    "Cave" : ["""
It’s your typical cave: dark and dank
"""],
    "DarkCorridoe" : ["""
You travel through the dark corridor and find a small dank room at the end.
"""],
    "DankRoom": ["""
It’s a musty dank room. A round boulder sits to the right side of the room.
"""], #tunnel is hidden mv
    "SmallHole" : ["""
It’s a hole, there’s nothing exciting to do here.
"""],
    "Tunnel" : ["""
It's quite moist in here.
You notice a small furry movement in the corner of your vision.
It's most likely a rat. A very large rat. Perhaps a mongoose.
At the end of the tunnel you find a stone chamber.
"""],
    "StoneChamber" : ["""
The whole rooms glows a dim blue light. The source of this light is a portal standing
in the middle of the room. This is obviously the portal of which the old man spoke.
"""],
    "Portal": ["""
You are in a sunny and spacious town square. There is a pedestal at the center of
the cobblestone turnabout, but no statue on it. The architecture is charming, but everyone
here seems nervous for some reason.
"""],
    "TownSquare" : [ """
You are in a sunny and spacious town square. There is a pedestal at the center of
the cobblestone turnabout, but no statue on it. The architecture is charming, but everyone
here seems nervous for some reason.
"""],
    "MarketPlace" : ["""
It seems like Terminus has fallen on hard times; there’s only one stall in the
marketplace. A sleazy-looking vendor lounges behind a table piled with strange wares.
"""],
    "Library" : ["""
The Library is dimly lit and smells like mildew. Still, it’s warm in here and the soft red
carpet makes it seem kind of cozy.
"""],
    "BackRoom" : ["""

"""],
    "RockyPath" : ["""
The weed-choked path leads off into the fields. There is an
enormous boulder blocking your way, however.
"""], #farm is hidden rm
    "Farm" : ["""
There was once a farm of some sort here, but now the fields are scorched and
brown.
"""], #copy corn for reward
    "ArtisanShop" : ["""
The walls of the shop are covered in clocks, all slightly out of sync. At the
workbench, a woman in an enormous pair of goggles is wielding a blowtorch with
frightening enthusiasm.
"""],#touch to start conv. copy for reward
    "BrokenBridge" : ["""
A creaky wooden bridges stretches across a chasm. But it’s missing a
plank, and the gap is too far to jump.
"""], #touch plank to fix bridge
    "Clearing" : ["""
There’s a small grassy clearing here, with a man sitting on a stone
and sobbing. Behind him is a pile of rubble.
"""], #mkdir a house - for password
    "OminousLookingPath" : ["""
The path leads toward a dark cave. It’s an ordinary cobblestone path, but for some
reason it fills you with a sense of dread.
"""], #rm brambles with password to enter cave
    "Cave" : ["""
: The cave is dark and smells like… feet? Oh, right, it’s probably the trolls. There’s a
scared-looking kid in a cage by the far wall.
"""], #rm ug trolls, #mv hideous troll
    "Cage" : ["""
"""] #mv to escape
}

folder_images = {
    "/": "home.jpg",
    "Dimension_C-137": "Dimension_C-137.jpg",
    "Citadel_of_Ricks": "Citadel_of_Ricks.jpg",
    "Morty&#39;s_Mind_Blowers": "Morty's_Mind_Blowers.jpg",
    "Rick&#39;s_garage": "Rick's_garage.jpg",
    "Unknown_location": "Unknown_location.jpg",
    "prison_cell": "prison.jpg",
    "escape_pod" : "escapepod.jpg"
}


file_contents = {
    'rick.txt': """
Great, just great Morty. My vacation's officially ruined. Thanks a lot, guys. Real nice job. I mean, I did save Summer a while back, but still. Everyone, just head on home.
<br/> But before we do that, Morty, we gotta delete this entire world. I know it sounds counterintuitive, but that's the way the story goes.
<br/> First things first, go to the root directory and create a new folder called 'escape_pod' using <span style='color:#22ff22'>mkdir</span>. It's simple Morty, just type <span style='color:#22ff22'>mkdir escape_pod</span> when you're in the root directory.
<br/> Once that's done, create a file called 'morty.txt' inside that folder. Got it? Then, and only then, delete everything else using 'rm'. Just type <span style='color:#22ff22'>rm name_of_file_or_folder</span> and get rid of it all! Except for the escape pod, obviously.
<br/> Oh, and make sure to move me into the pod as well using <span style='color:#22ff22'>mv</span>. And make sure the pod and text files are there BEFORE you delete everything else.
<br/> The guy who coded this is a lazy piece of slurm Morty, so 'rm' only works with absolute paths. Ask around to find out what that means.
<br/> Good luck Morty, you're gonna need it.
""",
    'rickbot.txt': """
It's a puzzle based loosely around a text-based adventure game Morty - they were big in the 80s. Rick programmed me to help you with it.
<br/><br/>Puzzle clue one: Proceed to the Citadel and search through the legal records, locate a kidnapper from season one or two, Morty!
<br/><br/>Puzzle clue two: Learn how to create new text files, then use that knowledge to create a text file of the kidnapper. Once the file has been created, read it, Morty!
<br/><br/>Puzzle clue three: The commands 'mv', 'rm' and 'mkdir' are required for puzzle number 3, Morty. Use caution as these commands do not have an undo function. For more information on how these commands function, utilize the 'man' command, Morty. <br/><br/>One final clue before you depart, if you wish to extract information from a criminal, try the Citadel of Ricks. My judgement is questionable, therefore, any criminal will likely cooperate to leave the Citadel, Morty.
<br/><br/> Warning: This message is generated by a robotic version of Rick Sanchez, any deviation from the original Rick Sanchez's behavior is an artifact of the programming.
""",
    'terminal-beth.txt': """
Hello Morty,
<br//>
I hope you're doing well in your adventure. I'm sure you're using all the BASH commands to your advantage and finding all kinds of interesting things.
<br//>
I wanted to remind you about the grep command. It's a really useful tool for searching through text files and finding specific information.
<br//>
<br//>
To use it, you just need to type grep followed by the search term and the name of the text file. For example, if you wanted to find all the instances of the word "grep" in this text file, you could use the command:
<br//>
<span  style='color:#22ff22'>grep clue terminal-beth.txt</span>
This will search through the terminal-beth.txt file and return any lines that contain the word clue.
<br//>
<br//>
Grep is case sensitive, so make sure you type the search term exactly as it appears in the text file. It's also a good idea to put the search term in single quotes \' if it's more than one word.
<br//>
Remember, Morty, it's important to always pay attention to the details when you're using BASH commands.
<br//>
A small mistake can have big consequences, so make sure you double check your work.
<br//>
O.K. Morty, I'm not sure how this will help, but trust me it will - now go find your sister!""",
    'terminal-jerry.txt': """
Can you believe it? Someone has gone and kidnapped Summer. Not our Summer, yours, but still.
<br//>Also, your Rick is missing. There is a Rickbot somewhere though who seems to know more than me about this whole mess.
<br//>The Rickbot taught me about autocomplete.
<br//>
<br//>I know I'm not exactly the adventurer type, Morty, but we've got to do something.
<br//>You can use the <span style='color:#22ff22'>cd</span> command to move through the different portals. Use it like:
<br//><span style='color:#22ff22'>cd Dimension_C-137</span> to go through that one there.
<br//>
<br//>That autocomplete I mentioned, well if you don't want to type out the file or folder name, just type the first letter then hit the <span style='color:#ff2222'>TAB</span> key and the rest is put there by some sort of magic, or science, or something. Anyway, it saves you typing.
<br//>
<br//>And don't forget to use the <span style='color:#22ff22'>ls</span> command to look around and get a sense of your surroundings. It'll help you find any clues that might lead us to Summer.
<br//>I'll stay here in the root dimension and see if I can find any clues to help you on your quest.
<br//>We can't let her down, Morty. You've got to bring her home safe.""",
    'terminal-summer.txt': """
Hey dweeb. So I'm like, the terminal universe version of Summer or something, and I'm supposed to help you save the other me, or something? Anyway, I'm here to teach you about the `touch` command.
<br//>So, let's say you want to create a new text file called `Dreamy_Dude`. Here's how you do it:
<br//><br//>
<br//><span style='color:#22ff22'>touch Dreamy_Dude.txt</span>
<br//><br//>
<br//>See? Super easy. Now you have a brand new, empty text file with no contents. But why don't we use spaces in the file name, you ask? Well, it's because the terminal gets confused when you use spaces. It's just easier to use an underscore or something like that to separate words.
<br//>And here's the really cool part - creating this `Dreamy_Dude.txt` file will actually bring Dreamy Dude into the terminal universe! I know, right, the science is questionable, but roll with it - it'll come in handy. So...cool.
<br//>Okay, that's all for now. Happy terminal-ing!
<br//><span style='color:pink'>xoxo</span>,
<br//>Summer
<br//>

""",
    'terminal-squanchy.txt': """
Squanchy, let me explain to you about relative and absolute paths. So, in computing, a path is like a squanchin' map that tells you how to get from one place to another. And there are two types of paths: relative and absolute.
<br//><br//>A relative path is like a squanchin' shortcut that tells you how to get to a destination based on your current location.
<br//>For example, if you're in the kitchen and you want to get to the living room, you could use a relative path like "go down the hallway and turn left".
<br//>This path is relative to your current location, so it's not the same for everyone.
<br//><br//>
On the other hand, an absolute path is like a squanchin' GPS system that gives you a specific set of squanchin' coordinates to follow.
<br//>It doesn't matter where you are, the absolute path will always take you to the same destination.
<br//>For example, if you want to get to the living room, an absolute path might be "go to the second floor and turn right at the end of the hallway".
<br//><br//>
So, in summary, relative paths are based on your current location and absolute paths are specific squanchin' directions that always take you to the same place. Squanch it!
""",
    'legal_records.txt': """
Council in session - minutes being recorded.
<br//>
Yes, that means everything I say is written down
<br//>
No, I won't say that.
<br//>
Blip blop, I can't believe you actually went and let the meeseeks out of the box again! Do you have any idea how much trouble they can cause? Now we have to deal with all sorts of crazy mishaps and problems, all because you couldn't resist the temptation to pull that lever. I hope you're happy, because I certainly am not.
<br//>
Zorp, I can't believe you just smeckled all over the floob again! You know how much I hate having to clean up your mess. And now we're all out of gloop and I have to go to the store to buy more. I swear, sometimes I think you do these things just to annoy me. I hope you're happy, because now I have to go to the interdimensional market and try to find some more of that rare, imported schleem. It's going to be a long, grueling day, and all because you couldn't control yourself. I hope you're happy, Zorp. I really do.
<br//>
Rick C-137 is suggesting we create a mind control device to force all other versions of ourselves to follow our every command. And don't even get me started on Rick G-19's idea to create a portal gun that can transport us to different dimensions at will. I fear for the future of the multiverse if any of these plans are put into action. I just hope I can keep up with all the chaos and madness that seems to follow the council of ricks wherever they go.
<br//>
Fellow members of the council of Ricks, I bring to your attention a list of associates of the Smith family from dimension C-137 and so called 'adventures' they have been on. These individuals have been connected to a series of illegal activities and must be apprehended and brought to justice. The list includes:
<br//> Rick Sanchez - Creating a toxic environment - "The Wedding Squanchers".
<br//> Morty Smith - Stealing a car - "Mortynight Run".
<br//> Summer Smith - Vandalism - "Total Rickall".
<br//> Beth Smith - Aiding and abetting in various crimes - "The Wedding Squanchers".
<br//> Jerry Smith - None (yet) - .
<br//> Mr. Poopybutthole - Unknown - .
<br//> Birdperson - Collaborating with the enemy - "The Wedding Squanchers".
<br//> Squanchy - Unknown - .
<br//> Krombopulos Michael - Illegal arms dealing - "The Wedding Squanchers".
<br//> Gazorpazorpfield - Breaking and entering - "Raising Gazorpazorp".
<br//> Gleeb - Grand theft auto - "Total Rickall".
<br//> Snuffles - None (yet) - .
<br//> Dr. Xenon Bloom - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop's son - None (yet) - .
<br//> Scary Terry - Burglary - "Lawnmower Dog".
<br//> Rick Sanchez - Blowing up a planet - "A Rickle in Time".
<br//> Morty Smith - Stealing a miniverse - "Close Rick-counters of the Rick Kind".
<br//> Summer Smith - Breaking into the Pentagon - "The Wedding Squanchers".
<br//> Beth Smith - Aiding and abetting in various crimes - "The Wedding Squanchers".
<br//> Jerry Smith - None (yet) - .
<br//> Mr. Poopybutthole - Unknown - .
<br//> Birdperson - Collaborating with the enemy - "The Wedding Squanchers".
<br//> Squanchy - Unknown - .
<br//> Krombopulos Michael - Illegal arms dealing - "The Wedding Squanchers".
<br//> Gazorpazorpfield - Breaking and entering - "Raising Gazorpazorp".
<br//> Gleeb - Grand theft auto - "Total Rickall".
<br//> Snuffles - None (yet) - .
<br//> Dr. Xenon Bloom - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop's son - None (yet) - .
<br//> Scary Terry - Kidnapping Summer (probably kidnap, still investigating) - "Lawnmower Dog".
<br//> Rick Sanchez - Blowing up a planet - "A Rickle in Time".
<br//> Morty Smith - Stealing a miniverse - "Close Rick-counters of the Rick Kind".
<br//> Summer Smith - Breaking into the Pentagon - "The Wedding Squanchers".
<br//> Beth Smith - Aiding and abetting in various crimes - "The Wedding Squanchers".
<br//> Jerry Smith - Embezzlement - "The Wedding Squanchers".
<br//> Mr. Poopybutthole - Fraud - "Total Rickall".
<br//> Birdperson - Collaborating with the enemy - "The Wedding Squanchers".
<br//> Squanchy - Arson - "The Wedding Squanchers".
<br//> Krombopulos Michael - Illegal arms dealing - "The Wedding Squanchers".
<br//> Gazorpazorpfield - Breaking and entering - "Raising Gazorpazorp".
<br//> Gleeb - Grand theft auto - "Total Rickall".
<br//> Snuffles - Identity theft - "The Ricks Must Be Crazy".
<br//> Dr. Xenon Bloom - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop - Stealing research - "The Ricks Must Be Crazy".
<br//> Dr. Glip Glop's son - Extortion - "Total Rickall".
In closing, the Council of Ricks would like to thank all members for their participation in this meeting. The discussions and updates provided were valuable and will be taken into consideration in future decision making. The council would also like to remind all members to maintain the highest level of secrecy and caution in order to avoid detection by law enforcement or rival councils. The meeting is now officially adjourned. Thank you.
""",
    'terminal-birdperson.txt': """
Birdperson, rise.
<br//>As a birdperson, I often find myself using basic mv and rm commands to organize my files and documents.
<br//>To move a file using a relative path, you can simply type <span style='color:#22ff22'>mv file.txt whereIam/OtherDirectory/file.txt</span>.
<br//>This will move the file "file.txt" to the "new/directory" folder.
<br//>
<br//>Alternatively, you can use an absolute path by specifying the full file path, such as <br//><span style='color:#22ff22'>mv /Dimension_C-137/Citadel_of_Ricks/terminal-birdperson.txt /Dimension_C-137</span>.
<br//>I use <span style='color:#22ff22'>mv rick.txt /</span> to move Rick back to the root directory if things get really tricky.
<br//>If I'm in the same place as him I can use that without knowing any paths!
<br//>Now, the programmer who made this world is lazy, so this mv command doesn't have full functionality.  In proper command line interfaces you can use this command to rename files as well as move them.
<br//><br//>
<br//>Lots of the commands here are weaker versions of the true commands.  Another one the programmer of this world attempted to implement is the remove command.
<br//>To remove a file using an absolute path, you can use the rm command followed by the file path,
<br//>such as <span style='color:#22ff22'>rm /home/birdperson/documents/file.txt</span>.
<br//><br//>
<br//>This non-complete version of rm can not use relative pathways, again, the programmer of this world is lazy.
<br//>It's important to be careful when using rm, as it will permanently delete the specified file and it cannot be undone.
<br//>In fact, Rick once accidentally deleted all of his memories using the rm command, so be sure to double check the file path before using rm to avoid any mishaps.
""",
    'summer.txt':"",
    'Summer.txt':""
}



file_images = {
'terminal-jerry.txt':"terminal-jerry.txt.png",
'rick.txt':"1.jpg",
  "rickbot.txt":"rickbot.txt.png",
  'terminal-summer.txt':"terminal-summer.txt.png" ,
  'terminal-beth.txt':"terminal-beth.txt.png" ,

 'terminal-squanchy.txt':"terminal-squanchy.txt.png" ,

'legal_records.txt':"legal_records.txt.jpg",

  'terminal-birdperson.txt':"terminal-birdperson.txt.png",
  'morty.txt' : "scary.png",

   '':"root.jpg"

}


def add_to_dict(dictionary, key, value):
    values = dictionary[key]
    values.append(value)
    dictionary.update({key: values})
    return dictionary

def find_parent(file_structure, path):
  if path == "/":
    return "/"
  for key in file_structure:
    for file in file_structure[key]:
      if file == path:
        return key


def fake_grep(searchword,file,file_contents):
  sentances = re.split(r'(?<=[.?!])(?:[\s]|[\s]*<br\/\/>[\s]*|\r\n)(?=[A-Z])|(?<=<br\/\/>)', file_contents[file])
  match = ""
  #print(sentances)
  for sentan in sentances:
    if searchword in sentan:
      match = match + sentan
  return match



def path_exists(file_structure, path):
  name=""
  if path == "/":
      return "/"
  # Split the path into a list of individual directory and file names
  path_list = path.split("/")

  # Remove the first element, which will be an empty string if the path is absolute
  if path_list[0] == "":
    path_list = path_list[1:]

  # Set the current directory to the root
  current_dir = "/"

  # Iterate over the list of directory and file names
  for name in path_list:
    # Check if the current directory contains the name as a key (for a subdirectory) or a value (for a file)
    if name in file_structure[current_dir]:
      # If the name is a key, update the current directory to the subdirectory
      if name in file_structure:
        current_dir = name
      # If the name is a value, the path exists
      else:
        return name
    # If the name is not found in the current directory, the path does not exist
    else:
      return False
  # If the loop completes, the path exists
  return name

def build_file_path(file_structure, value, path = ""):
  # Base case: value was found
  if value in file_structure:
    return path

  # Recursive case: value was not found, search subdirectories
  for subdir in file_structure:
    # Add the current subdirectory to the path
    new_path = subdir if path == "" else f"{path}/{subdir}"

    if subdir == value:
      return new_path

    # Recursively search the subdirectory
    subdir_structure = file_structure[subdir]
    if isinstance(subdir_structure, list):
      # subdir_structure is a list of files, search for the value
      if value in subdir_structure:
        return new_path
    else:
      # subdir_structure is a dictionary, search recursively
      subdir_path = build_file_path(subdir_structure, value, new_path)
      if subdir_path is not None:
        return subdir_path

  # Value was not found in any subdirectory
  return None

def build_folder_path(file_structure, value, path = ""):
  if value.strip() == "":
   return "/"
  if value == "/":
   return value
  value = value.replace("'","&#39;")
  value = value.split("/")[-1]
  # Base case: value was found
  if value in file_structure.values():
    return path

  # Recursive case: value was not found, search subdirectories
  for subdir in file_structure:
    # Add the current subdirectory to the path
    new_path = subdir if path == "" else f"{path}/{subdir}"

    if subdir == value:
      return new_path

    # Recursively search the subdirectory
    subdir_structure = file_structure[subdir]
    if isinstance(subdir_structure, list):
      # subdir_structure is a list of files, search for the value
      if value in subdir_structure:
        return new_path
    else:
      # subdir_structure is a dictionary, search recursively
      subdir_path = build_folder_path(subdir_structure, value, new_path)
      if subdir_path is not None:
        return subdir_path

  # Value was not found in any subdirectory
  return None



def is_file_or_folder(path):
    if path == "":
        path = "/"
    # Check if the path ends in a filename (e.g. "file.txt")
    if len(path.split("."))>1:
        return 'file'
    # Check if the path ends in a folder (e.g. "folder/")
    elif re.search(r'[/]*$', path):
        return 'folder'
    else:
        return 'neither'

def extract_path(path_and_filename):
    # Use a regular expression to match the path and filename
    match = re.search(r'(.*)/([^/]+)$', path_and_filename)
    # Return the path if a match was found, or an empty string if no match was found
    return match.group(1) if match else '/'


def fake_mv(file_structure, target, destination, pwd):
    print(f"file structure before fake_mv:{file_structure}")


    if is_file_or_folder(destination)=="file":
        filename = destination.split("/")[-1]
        new_dest = extract_path(destination)
        if new_dest == "":
            new_dest = "/"
        destination = new_dest
        copy = True
        print(copy,filename,destination)
    else:
        copy = False




    if build_folder_path(file_structure,target)== None or  build_folder_path(file_structure,destination)== None:
        return ([file_structure, f"Error *: {target} not found in {file_structure}"])
    if destination[0:2]=="./":
        destination = destination[2:]
    print ("a debugginng  message eee:" + destination + ":" + target )
    if destination == "/":
        pass
    elif destination[-1] == "/":
        destination = destination[:-1]
    currentpath = build_folder_path(file_structure,pwd)
    target = target.replace("'","&#39;")
    og_target = target
    targetpath = og_target
    destination = destination.replace("'","&#39;")
    og_dest = destination
    if target[0] != "/":

            #targetpath = build_file_path(file_structure,target)
            currentpath = og_target
            targetpath = ""
            if currentpath != "/":
                while currentpath != "/":
                    currentpath = build_folder_path(file_structure,currentpath)
                    targetpath = currentpath   + "/" + targetpath
                targetpath = targetpath[2:-1]

            if targetpath == None:
                return ([file_structure, f"Error *: {target} not found in {file_structure}"])
            if targetpath == "/":
                target = targetpath + target
            else:
                if currentpath == "/":
                    target = currentpath  + targetpath + "/" + target
                else:
                    target = currentpath + "/" + targetpath + "/" + target
            if og_target in file_structure[pwd]:
                pass
            elif currentpath + '/' + pwd + '/' + og_target != target:
                return ([file_structure, f"Error *: {target} not found in {file_structure}"])
    destpath = ""

    if destination[0] != "/":

            currentpath = og_dest

            while currentpath != "/":
                currentpath = build_folder_path(file_structure,currentpath)
                destpath = currentpath   + "/" + destpath
            destpath = destpath[2:-1]
            if destpath == None:
                return ([file_structure, f"Error **: {destination} not found in {file_structure}"])
            if destpath == "/":
                destination = destpath + destination.split("/")[-1]
            else:
                destination = "/" + destpath + "/" + destination.split("/")[-1]
            if pwd == currentpath:
                root = True
            if og_dest in file_structure[pwd]:
                pass
            elif root == True:
                if currentpath + og_dest != destination:
                    return ([file_structure, f"Error *: {destination} didn't match {currentpath  + og_dest}"])
            elif currentpath + pwd + og_dest != destination:
                    return ([file_structure, f"Error ***: {destination} didn't match {currentpath  + pwd  + og_dest}"])

    print(path_exists(file_structure,target))
    print(path_exists(file_structure,targetpath))
    print(target)
    print(targetpath)
    if (path_exists(file_structure,target) == False and (path_exists(file_structure,targetpath) == False)):
        return ([file_structure, f"Error ^^^: {target} not found in {file_structure}"])
    if (path_exists(file_structure,destination) == False) and (path_exists(file_structure,destpath) == False):
        return ([file_structure, f"Error ^*: {destination} not found in {file_structure}"])
    try:
        targetdir = target.split("/")[-2]
    except:
        targetdir="/"
    destinationdir = destination.split("/")[-1]
    if destinationdir == "":
        destinationdir = "/"
    if targetdir == "":
        targetdir = "/"

    if copy == True:
        print("COPIER",target,filename)
        target = target.split("/")[-1]
        current_dir = file_structure[destinationdir]
        current_dir.append(filename)
        session['file_contents'][filename] = session['file_contents'][target]
        session['file_images'][filename] = session['file_images'][target]
        print(filename,target)
    else:
        try:
            current_dir = file_structure[targetdir]
            current_dir.remove(target.split("/")[-1])
            current_dir = file_structure[destinationdir]
            current_dir.append(target.split("/")[-1])
        except:
            return ([file_structure,False])
    print(f"file structure after fake_mv:{file_structure}")
    return ([file_structure,True])

def rm(file_structure, path):
  # Split the path into a list of folder names and the file name
    try:
        folders, file_name = path.rsplit("/", 1)
    except:
        return "Error: you must use absolute paths - apologies"
    folders = folders.split("/")
    # Get the root folder
    root = file_structure["/"]
    # Iterate through the list of folders, starting at the second one (since the first one is the root)
    for folder in folders[1:]:
      # Find the subfolder in the current folder
      subfolder = next((f for f in root if f == folder), None)
      # If the subfolder does not exist, return an error message
      if subfolder is None:
        return f"Error: folder {folder} does not exist in path {path}"
      # If the subfolder exists, set it as the current folder and continue iterating
      else:
        root = file_structure[subfolder]

    # When we reach the end of the list of folders, check if the file_name is in the current folder
    if file_name in root:
      # If the file exists, remove it from the list of files in the current folder
      root.remove(file_name)
      if file_name in file_structure:
          for val in file_structure[file_name]:
              print (val)
              if val in file_structure:
                  for val2 in file_structure[val]:
                      if val2 in file_structure:
                          for val3 in file_structure[val2]:
                              if val3 in file_structure:
                                  for val4 in file_structure[val3]:
                                    if val4 in file_structure:
                                        del file_structure[val4]
                                  del file_structure[val3]
                          del file_structure[val2]
                  del file_structure[val]
      if file_name in file_structure:
        del file_structure[file_name]

      # Return a success message
      print (file_structure)

      if session['file_structure'] == {'/': ['escape_pod'], 'escape_pod': ['', 'morty.txt','rick.txt']}:
        return '<h2>WELL DONE MORTY! WE WIN! NOW WE CAN USE YOUR BASH SKILLS IN THE REAL WORLD!</h2><video autoplay onended="document.location.href=\'/winner\'"><source src=\'static/video/video.mp4\'/></video>'
      else:
        print(f"DEBUG END GAME FAIL{session['file_structure']}")
        return f"Successfully deleted file {path}"

    else:
      # If the file does not exist, return an error message
      return f"Error: file {path} does not exist"

def rick_and_morty_word(seed):

    # create a list of syllables
    syllables_1 = ["fr", "gl", "sk", "bl", "st", "fl", "du", "ti", "pl", "tr",
                   "gr", "dr", "fl", "sp", "dr", "th", "bl", "wa", "dw",
                   "re", "pl", "tr", "fr", "sk", "wi", "spl", "dr", "tw", "fl",
                   "gl", "th", "sh", "st", "bl", "st", "spl", "dr", "sp",
                   "sc", "wr", "th", "sc", "spl", "dw", "sk", "sw", "sk",
                   "fr", "sk", "th", "sw", "sc", "sc", "sp", "shr", "dw",
                   "st", "spr", "dw", "skr", "skr", "spr", "skr", "skr",
                   "skr", "skr"]
    syllables_2 = ["a", "e", "i", "o", "u", "ee", "oo", "ai", "ou", "ie", "ei", "ooi", "aie", "eie", "iou", "aou", "eei", "ooa", "ooe", "oou"]

    # set the length of the word based on the length of the seed
    length = int(len(str(seed))/2)

    # set the random seed
    random.seed(seed)

    # randomly select full syllables to form the word
    word = ""
    for i in range(length):
        if i ==3 and length>3:
             word += "-"
        word += random.choice(syllables_1) + random.choice(syllables_2)

    return word




@app.route('/bantest')
def bantester():
    return render_template("ban.html")




@app.route('/session/<cd>')
def get_session_variables(cd):
# Retrieve the session variables
  cd = cd.replace("'","&#39;")
  if cd not in session['file_structure'] and cd !="root":
      print(f"------------------------bodgey prison error fix on {cd}")
      print(session['file_structure'])
      return jsonify("/")
  print("checking session for " + cd)
  print(session['file_structure'])
  if cd == "" or cd == "root":
      cd = "/"


  try:
    list = session['file_structure'][cd]
  except:
     print("error:" + cd + ":")
     list = ["/"]
     return jsonify(list)
  currentpath = cd
  targetpath = cd
  if currentpath != "/" and currentpath.strip() != "" and currentpath != None and currentpath in session['file_structure']:
                #while currentpath != "/" and currentpath.strip() != "" and currentpath != None:
                while currentpath not in ["/", "", None]:
                    currentpath = build_folder_path(session['file_structure'],currentpath)
                    targetpath = currentpath   + "/" + targetpath
                targetpath = targetpath[1:]
  currentpath = targetpath
  paths = []
  if currentpath == "/":
      currentpath = ""
  for val in list:
      #val = val.replace("&#39;","'")
      paths.append (currentpath + "/" +val)
  print (list)
  # Return the session variables as part of the response
  return jsonify(list+paths)

@app.route('/')
@app.route('/🖥')

def index2():
    for key in list(session.keys()):
        del session[key]

    cell_number = random.randint(0,99999)
    prison_word = rick_and_morty_word(cell_number)
    session['file_structure'] = file_structure
    session['file_contents'] = file_contents
    session['file_images'] = file_images
    session['folder_images'] = folder_images
    session['file_structure']['Unknown_location'] = []
    #session['prison'] = "prison_cell_" + str(cell_number)
    session['prison'] = "prison_cell_in_" + prison_word
    session['file_structure']['Unknown_location'].append(session['prison'])
   # session['file_structure'][session['prison']] = ["rick.txt"]

    session['folder_images'][session['prison']] = session['folder_images']['prison_cell']
    session['commands'] = []
    print(session['file_structure'])
    notes = ""
    for digit in str(cell_number):
        notes = notes + (str((int(digit) + 32) * 128) + ",")
    print (session['prison'])

    for key in session['file_structure']['Unknown_location']:
        print (f"KEY TEST:{key}")
    old_keys = []
    for key in session['file_structure']:
        if key != session['file_structure']['Unknown_location'] and "prison_cell_in" in key:
            old_keys.append(key)

    #print (session['file_structure']['Unknown_location'])
    for key in old_keys:
        del session['file_structure'][key]


    session['file_structure']['prison_cell_in_' + prison_word] = ["rick.txt"]
    print(f"final dictionary on load {session['file_structure']}")
    return render_template("index2.html",notes=notes)

@app.route('/terminus')
def indexT():
    for key in list(session.keys()):
        del session[key]

    session['file_structure'] = file_structure_terminus
    session['folder_text'] = folder_text_terminus
    session['folder_images'] = folder_images_terminus
    session['commands'] = []
    return render_template("index3.html")

@app.route('/winner')
def winnings():
    winnings = 8000 * (8 - len(session['file_structure']))
    return render_template("winner.html",winnings = winnings, commands = session['commands'])

@app.route('/input', methods=["GET","POST"])
def input():
  try:
    command = request.form['command']
    current_directory = request.form['current_directory']
    session['commands'].append(command)
  except:
    command = ""
    response = {'output': 'Command does not exist, or requires a parameter','current_directory':current_directory,'image': "",'contents': ""}
    return jsonify(response)

  if command == 'pwd':
      currentpath = current_directory
      targetpath = current_directory
      if currentpath != "/":
                while currentpath != "/":
                    currentpath = build_folder_path(file_structure,currentpath)
                    targetpath = currentpath   + "/" + targetpath
                targetpath = targetpath[1:]
      currentpath = targetpath
      response = {'output': f'You are in {currentpath}','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)

  elif command == 'cd..':
      current_directory = find_parent(session['file_structure'], current_directory)
      response = {'output': f'You are now in {current_directory}','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)
  elif command == 'cd/':
        current_directory = "/"
        response = {'output': f'You are now in {current_directory}','current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)



  elif command.split(" ")[0] == 'cat':
    try:
        filename = command.split(" ")[1]
        filename = filename.replace("'","&#39;")
    except:
        response = {'output': 'cat function requires a file to open.','current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    if filename in session['file_structure'][current_directory]:
        if (filename == "legal_records.txt"):
            response = {'output': f'File {filename} is too large to open with cat.','current_directory':current_directory,'contents': "", 'image': session['file_images'][filename]}
            return jsonify(response)

        print(session['file_contents'][filename], file=sys.stderr)
        response = {'output': f'Opened {filename}.','current_directory':current_directory,'contents': session['file_contents'][filename], 'image': session['file_images'][filename]}
        return jsonify(response)

    else:
        response = {'output': f'File {filename} does not exist in this folder.','current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)





  elif command.split(" ")[0] == 'grep':
    try:
      search_string = " ".join(command.split(' ')[1:-1])
      if search_string[0] =="'" and search_string[-1] =="'":
          search_string = search_string[1:-2]
      file = command.split(" ")[-1]
      file = file.replace("'","&#39;")

    except:
      response = {'output': 'File name, or search string not found.','current_directory':current_directory,'contents': "", 'image': ""}
      return jsonify(response)
    if file in session['file_structure'][current_directory]:
      result = fake_grep(search_string,file,session['file_contents'])
      #print(result)
      response = {'output': f'Opened {file} and used grep to search contents.','current_directory':current_directory,'contents': result, 'image': session['file_images'][file]}
      return jsonify(response)
    else:
      response = {'output': f'File named {file} not found.','current_directory':current_directory,'contents': "", 'image': ""}
      return jsonify(response)





  elif command.split(" ")[0] == 'cd':
    # change directory code here
    try:
      destination = command.split(" ")[1]
      destination = destination.replace("'","&#39;")
      #thispath = command.split(" ")[1:]
      #firstchar = thispath[0]
      #print("path:" + thispath)
      #print("fchar:" + firstchar)
     #if firstchar=="/" and path_exists(file_structure, thispath):
        #current_directory = thispath
        #response = {'output': f'You are now in {destination}','current_directory':current_directory,'image': "",'contents': "",'clear':True}
    except:
      response = {'output': 'cd command requires a parameter.','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)

    if destination.strip() == "Unknown_location":
        response = {'output': f"Directory {destination} can not be navigated to due to plot reasons. We'll say it's encrypted.",'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    if destination.strip() == "..":
      current_directory = find_parent(session['file_structure'], current_directory)
      response = {'output': f'You are now in {current_directory}','current_directory':current_directory,'image': "",'contents': "",'clear':True}
      return jsonify(response)
    elif destination.strip() == "/":
        current_directory = "/"
        response = {'output': f'You are now in {destination}','current_directory':current_directory,'image': "",'contents': "",'clear':True}
        return jsonify(response)
    elif destination in session['file_structure'][current_directory] and destination in session['file_structure']:
        current_directory = destination
        response = {'output': f'You are now in {destination}','current_directory':current_directory,'image': "",'contents': "",'clear':True}
        return jsonify(response)
    else:
        response = {'output': f'Directory {destination} does not exist','current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)


  elif command == 'ls' or command.split(" ")[0] == 'ls':
    # list directory code here
    try:
        folder = command.split(" ")[1]
        files = session['file_structure'][folder]
        files.sort()
    except:
        files = session['file_structure'][current_directory]

    portals = []
    texts = []
    for file in files:
        if file in session['file_structure']:
            portals.append(file)
        else:
            texts.append(file)

    portals.sort()
    texts.sort()
    lsstring = ""
    if len(portals)>0:
        lsstring = lsstring + "<span style='color:#229922;'>Portals to:</span>"
        for portal in portals:
            lsstring = lsstring +"<br//>" + portal
    if lsstring != "":
        lsstring = lsstring + "<br//>"
    if len(texts)>0:
        lsstring = lsstring + "<span style='color:#229922;'>Text messages called:</span>"
        for text in texts:
            lsstring = lsstring +"<br//>" + text
    if (''.join(files)==''):
        response = {'output': 'There\'s nothing here!','current_directory':current_directory,'image': "",'contents': ""}
    else:
        response = {'output': 'You look around and see:' + '<br//><br//>' + lsstring,'current_directory':current_directory,'image': session['folder_images'][current_directory],'contents': ""}

    return jsonify(response)


  elif command.split(" ")[0] == 'touch':
    try:
      filename = command.split(" ")[1]
      filename = filename.replace("'","&#39;")
    except:
      response = {'output': 'touch command requires a parameter.','current_directory':current_directory,'image': "",'contents': ""}
    try:
      ext = filename.split(".")[1]
    except:
      response = {'output': 'file name requires a file extension in this version.','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)
    if filename in session['file_structure'][current_directory]:
      response = {'output': 'file name exists in this folder.','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)
    if filename in ['summer.txt','Summer.txt','SUMMER.txt','SUMMER.TXT','rick.txt']:
      response = {'output': 'For reasons of plot, rather than logic, this does nothing - Apologies.','current_directory':current_directory,'image': "",'contents': ""}
      return jsonify(response)

    session['file_structure'] = add_to_dict(session['file_structure'], current_directory, filename)
    session['file_contents'][filename] = "You made this!"

    if filename in session['file_images']:
        pass
    else:
        session['file_images'][filename] = ['root.jpg']

    if (filename in ["scary_terry.txt","Scary_Terry.txt"]):
        session['file_images'][filename] = "terry.png"
        if current_directory == "Citadel_of_Ricks":
            session['file_contents'][filename] = "O.K. I know where Summer is. She is in a prison cell. The path to the cell is '/Dimension_C-137/Citadel_of_Ricks/Morty's_Mind_Blowers/Unknown_location/" + session['prison'] +"'. If only there was some way to move the cell here..."
        else:
            session['file_contents'][filename] = "Nope. Not here. You'll need to move me somewhere else to make me co=operate."



    print(session['file_contents'][filename], file=sys.stderr)
    files = session['file_structure'][current_directory]
    files.sort()
    response = {'output': filename + ' created.<br//><br//>','current_directory':current_directory,'image': "",'contents': ""}
    if session['file_structure'] == {'/': ['escape_pod'], 'escape_pod': ['', 'morty.txt','rick.txt']}:
        return '<h2>WELL DONE MORTY! WE WIN! NOW WE CAN USE YOUR BASH SKILLS IN THE REAL WORLD!</h2><video autoplay onended="document.location.href=\'/winner\'"><source src=\'static/video/video.mp4\'/></video>'

    return jsonify(response)



  elif command.split(" ")[0] == 'mkdir':
    try:
      foldername = command.split(" ")[1]
      foldername = foldername.replace("'","&#39;")
    except:
      response = {'output': 'mkdir command requires a parameter.','current_directory':current_directory,'image': "",'contents': ""}

    add_to_dict(session['file_structure'], current_directory, foldername)
    session['file_structure'][foldername] = ['']

    if foldername in session['folder_images']:
        pass
    else:
        session['folder_images'][foldername] = ['aaa.jpg']

    files = session['file_structure'][current_directory]
    files.sort()
    response = {'output': foldername + ' created.<br//><br//>','current_directory':current_directory,'image': "",'contents': ""}
    return jsonify(response)

  elif command.split(" ")[0] == 'mv':
    try:
      targetname = command.split(" ")[1]
      destname = command.split(" ")[2]
      foldername = foldername.replace("'","&#39;")
      destname = destname.replace("'","&#39;")
      print("DEBUG" + destname + ":" + foldername)
    except:
      response = {'output': 'mv command requires two parameters.','current_directory':current_directory,'image': "",'contents': ""}

    fakemvcall = fake_mv(session['file_structure'], targetname, destname,current_directory)
    #fakemvcall = fake_mv(session['file_structure'], targetname, 'test/test',current_directory)

    #bodge fix for odd session clearing bug
    backup_session = session['file_structure']

    session['file_structure'] =  fakemvcall[0]

    #bodge fix for odd session clearing bug
    if session.get('file_structure') is None:
        session['file_structure'] =  backup_session

    if fakemvcall[1]==True:

        if targetname.split("/")[-1] in ["scary_terry.txt","Scary_Terry.txt"]:
            if destname.split("/")[-1] == "Citadel_of_Ricks":
                session['file_contents'][targetname] = "O.K. I know where Summer is. She is in a prison cell. The path to the cell is '/Dimension_C-137/Citadel_of_Ricks/Morty's_Mind_Blowers/Unknown_Location/'" + session['prison'] +". If only there was some way to move the cell here..."

        response = {'output': targetname + ' moved to ' + destname +'.<br//>','current_directory':current_directory,'image': "",'contents': ""}
    else:
        response = {'output': targetname + ' not moved to ' + destname +'. Unknown target or destination.<br//>','current_directory':current_directory,'image': "",'contents': ""}
    return jsonify(response)
  elif command.split(" ")[0] == 'rm':
    try:
      targetname = command.split(" ")[1]
    except:
      response = {'output': 'rm command requires a file or folder.','current_directory':current_directory,'image': "",'contents': ""}
    result = rm(session['file_structure'], targetname)
    print(result)
    response = {'output': result,'current_directory':current_directory,'image': "",'contents': ""}
  elif command.split(" ")[0] == 'man':
    try:
        command_name = command.split(" ")[1]
    except:
        response = {'output': 'man command requires a command name parameter.','current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)

    if command_name == 'man':
        text = """
The `man` command followed by a command name displays information about how to use the command.
Example: `man pwd` will show information about how to use the `pwd` command.
Usage: man [command]
<br//>
<br//>Limited support for:
<br//>pwd
<br//>cd
<br//>ls
<br//>cat
<br//>touch
<br//>grep
<br//>mkdir
<br//>mv
<br//>rm
<br//>
<br//>please report any bugs to mr.adam.clement@gmail.com
"""
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'pwd':
        text = """
The `pwd` command stands for "print working directory." It displays the current directory that the user is in.
Example: `pwd` will display the current directory, e.g. `/Dimension_C-137/Citadel_of_Ricks/`.
Usage: pwd
"""
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name in ['cd', 'cd..', 'cd/']:
        text = """
The `cd` command stands for "change directory." It allows the user to navigate to a different directory.
To navigate to the parent directory, use `cd..`. To navigate to the root directory, use `cd/`.
To navigate to a specific directory, use `cd [directory name]`.
Example: `cd Citadel_of_Ricks` will navigate to the `Citadel_of_Ricks` directory.
Usage: cd [directory name]
"""
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'ls':
        text = """
The `ls` command stands for "list." It lists the files and directories within the current directory.
To list the files and directories within a specific directory, use `ls [directory name]`.
Example: `ls` will list the files and directories within the current directory. `ls Citadel_of_Ricks` will list the files and directories within the `Citadel_of_Ricks` directory.
Usage: ls [directory name]
    """
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'touch':
        text = """
The `touch` command creates a new file with the specified name and extension.
The file name must include an extension, e.g. `.txt` or `.jpg`.
Example: `touch new_file.txt` will create a new file called `new_file.txt`.
Usage: touch [file name].[file extension]
    """
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'mkdir':
        text = """
The `mkdir` command stands for "make directory." It creates a new directory with the specified name.
Example: `mkdir new_directory` will create a new directory called `new_directory`.
Usage: mkdir [directory name]
    """
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'mv':
        text = """
Yo, the <span style='color:#22ff22'>mv</span> command is like a teleportation device for your files and directories. It stands for "move," and it lets you move a file or directory to a new destination. Just type <span style='color:#22ff22'>mv</span> followed by the name of the file or directory you want to move, and then the destination you want it to go to.
For example, if you want to move a file called <span style='color:#22ff22'>terminal-jerry.txt</span> from the root dimension to the <span style='color:#22ff22'>Citadel_of_Ricks</span> directory, just type <span style='color:#22ff22'>mv /terminal-jerry.txt /Dimension_C-137/Citadel_of_Ricks</span>. It's like in that episode where we had to move that giant thing to the Vindicators' headquarters. Remember, Morty? We just used the <span style='color:#22ff22'>mv</span> command and boom, it was there in no time.
So just remember, when you wanna move a file or directory, use <span style='color:#22ff22'>mv [target] [destination]</span>. Easy peasy, Morty.
    """
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'rm':
        text = """
Yo, the <span style='color:#22ff22'>rm</span> command is how you get rid of a file or folder on your computer. Just type rm followed by the file or folder name, and boom, it's gone.
For example, if you want to get rid of a file called rick.txt in the root directory, just type rm /rick.txt. And if you want to get rid of a folder called Dimension_C-137 and all the stuff inside it, just type rm /Dimension_C-137.
Just be careful, because once you use this command, there's no going back. You can't undo it. It's like in that episode where we had to get rid of that giant robot's factory on that alien planet. Remember, Morty? We just typed rm factory and boom, the whole thing was gone. So use with caution, Morty.
"""
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    elif command_name == 'cat':
        text = """
The <span style='color:#22ff22'>cat</span> command followed by a file name displays the contents of the file.
Example: <span style='color:#22ff22'>cat rick.txt</span> will show the contents of the file `rick.txt` in the current directory.
Note: Some files may be too large to display in the terminal.
"""
        response = {'output': text,'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)
    else:
        response = {'output': f"No information available for command '{command_name}'. The programmer who made this will add more soon, probably.",'current_directory':current_directory,'image': "",'contents': ""}
        return jsonify(response)

  elif command == "":
        return
        #response = {'output': None,'current_directory':current_directory,'image': "",'contents': ""}

  else:
    # handle invalid command
    response = {'output': 'Command not found. Limited command support - Use man man to see list of supported commands and man command-name to see help on each command.','current_directory':current_directory,'image': "",'contents': ""}

  return jsonify(response)

