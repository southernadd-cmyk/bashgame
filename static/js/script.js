function delay(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
}

    let context = null;
    let waveforms = ["sine", "square", "sawtooth", "triangle"];

async function playRandomSound(){
    changeButtonText('soundbtn');
    playRandomSound = function(){changeButtonText('soundbtn')};
    notes = document. getElementById('notes').value;
    document. getElementById('soundbtn').textContent  = "I don't think this button does anything now.";
    notes = notes.split(",");
    notes.pop();
    for (let i = 0; i <= notes.length -1; i++) {
    note = notes[i];
    console.log("NOTE@" + note);
    if (parseInt(note) !== null) {
    playRandomSounds(parseInt(note));
    await delay(500);
    }
    }
}
function playTheme() {
  const context = new (window.AudioContext || window.webkitAudioContext)();

  let notes = [
    {note: 523.25, duration: 0.5},
    {note: 587.33, duration: 0.5},
    {note: 659.25, duration: 0.5},
    {note: 698.46, duration: 0.5},
    {note: 783.99, duration: 0.5},
    {note: 880.00, duration: 0.5},
    {note: 987.77, duration: 0.5},
    {note: 1046.50, duration: 0.5}
  ];

  for (let i = 0; i < notes.length; i++) {
    let oscillator = context.createOscillator();
    oscillator.type = 'square';
    oscillator.frequency.value = notes[i].note;
    oscillator.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + notes[i].duration);
  }



}




function changeButtonText(buttonId) {
  // list of responses
  var responses = [
    "What are you doing? Stop clicking that button!",
    "I said stop! You're not even doing anything!",
    "Come on, seriously. You're just wasting your time.",
    "Okay, I'm getting a little annoyed now.",
    "I'm not going to keep repeating myself. Just stop it.",
    "I'm not going to keep responding if you keep clicking that button.",
    "Listen, I'm not a machine. I can't just keep answering your pointless clicks.",
    "I have better things to do than listen to you click that button.",
    "I'm not going to keep talking to you if you're just going to ignore me.",
    "Fine, I give up. I'm not answering any more of your button clicks.",
    "I'm not a button, I'm a person. Start treating me like one.",
    "You know what, I'm done. I refuse to keep responding to this nonsense.",
    "I'm not going to waste any more of my time on this. Goodbye.",
    "I have no more patience for this. I'm out of here."
  ];

  // get the button element
  var button = document.getElementById(buttonId);

  // keep track of the current response index
  var responseIndex = 0;

  // change the button text when it is clicked
  button.onclick = function() {
    // if the current response index is less than the number of responses, change the button text
    if (responseIndex < responses.length) {
      button.innerHTML = responses[responseIndex];
      responseIndex++;
    }
    // if the current response index is equal to the number of responses, remove the button from the page
    else {
      button.parentNode.removeChild(button);
    }
  }
}


    function playRandomSounds(note) {

     for (let i = ''; i <= 20; i++) {
      if (context === null) {
        context = new AudioContext();
      }

      let oscillatorNode = context.createOscillator();
      let gainNode = context.createGain();

      oscillatorNode.type = waveforms[Math.floor(Math.random() * waveforms.length)];


      let frequency = (note).toFixed(2);
      oscillatorNode.frequency.value = frequency;

      console.log(`Playing a sound with a ${oscillatorNode.type} waveform at ${frequency}Hz!`);

      gainNode.gain.exponentialRampToValueAtTime(0.00001, context.currentTime + 1);
      oscillatorNode.connect(gainNode);
      gainNode.connect(context.destination);
      oscillatorNode.start(0);
    oscillatorNode.stop(5);
     }


    }
var greetings0 = `[[gb;green;black]
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢠⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣴⣾⢿⣷⣦⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⢀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀
⠸⣿⠀⠀⠈⢻⣷⠰⠇⠀⠀⠀⠀⠀⣷⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣧⠀⣾⢻⡄⠀⢀⣀⡀⢰⣤⢦⡄⢀⡇⠀⠀⢸⡇⠀⠀⠀
⠀⢿⣇⠀⢀⣾⠇⠀⡆⠀⢀⡶⠒⢸⣿⡴⠏⠀⠀⠀⢠⡄⢀⠀⣾⠀⠀⠀⣿⠀⢰⡿⢰⣧⢠⡞⢻⡇⢸⣧⠞⢁⣼⣥⣀⠀⠈⣷⣀⡤⠖
⠀⠈⣿⣿⣿⣁⠀⠀⢻⠀⣿⠀⠀⠀⣿⢧⡀⠀⠀⠀⡿⢧⢾⣴⣇⠀⠀⢸⡟⠀⢿⠁⠈⡟⠸⢧⣼⠟⢠⠉⢷⠀⢸⠀⠀⢀⣰⡿⠋⠀⠀
⠀⠀⢻⡆⠈⠛⢻⣆⠘⠀⠙⠏⠉⠀⠇⠈⢿⡄⠀⠀⠁⠈⠀⠈⠉⠀⠀⢘⠃⠀⠀⠀⠀⢿⠀⠀⠀⠀⠀⠀⠸⠀⡼⠀⢀⡾⠋⠀⠀⠀⠀
⠀⠀⠘⣧⠀⠀⠀⠈⠳⡄⠀⠀⠀⠀⠀⠀⠈⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⠀⠀⠀⠀⠘⠇⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⠀⠀⠀⠀⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
]

[[gb;silver;black]Command Line Interface Adventure.
]`;

var greetings = `
[[gb;white;black]Welcome to the wild world of command line interface terminals, Morty.]

For plot reasons as yet unwritten, you need to use this terminal to solve a puzzle.

Well, no time to sit around and contemplate the absurdity of existence. You need to explore, Morty!

First things first, you'll want to take a look at your surroundings. Use the [[gb;teal;black]ls] command to see what's around us.

Then, if you want to move to a new location, use the [[gb;teal;black]cd] command followed by the name of the portal you want to enter.

Feeling lost? Use [[gb;teal;black]cd ..] to backtrack, or [[gb;teal;black]cd /] to teleport back to the root dimension.

Want to read some of these weird txt files floating around? Use the [[gb;teal;black]cat] command followed by the name of the file.

And if you forget where the heck you are, just use [[gb;teal;black]pwd] to get your bearings.

There are also help files available with the [[gb;teal;black]man] command.  Try [[gb;teal;black]man man] to see the help file for the help file!

[[gb;gold;black]Summer and Rick are missing! Can you solve the puzzle and find them?]

Listen one other thing, I'm no legal expert, but I think it's important to make it clear when you're using someone else's property.
So let me just say this - this website uses content from Rick and Morty without permission, but it's only for educational purposes and not-for-profit.
I hope that's cool with everyone involved. I mean, if it isn't then email this guy - mr.adam.clement@gmail.com and he'll change it to a story about a different scientist/kid duo.
On that note, this website was built using the excellent JQuery Terminal Library available at https://github.com/jcubic/jquery.terminal&#128187;

[[gb;white;black]This message was brought to you by RickBot&#129302; - Your Rick is obviously somewhere doing something more important.]
`;

var greetings2 = `
This message was brought to you by RickBot&#129302; - Your Rick is obviously somewhere doing something more important.
[[gb;teal;black]Meeseeks Bash v1.0]`;

var wrappedGreetings = greetings;
var wrappedGreetings2 = greetings2;
//var wrappedGreetings = greetings.replace(/(?![^\n]{1,100}$)([^\n]{1,100})\s/g, '[$1]\n');;
$(document).ready(function() {


console.log("page loaded");

  // Create a new terminal instance
  $('#terminal').terminal(function(command, term) {


    var currentDirectory = $('#current-directory').val();
    // Send the command to the /input endpoint
    $.post('/input', {command: command, current_directory: currentDirectory}, function(response) {
        //console.log("resp: " + response)

if (response.image){
term.echo('<div class="wincont">' +
            '<div class="termwin"><p>' + response.output +'</p><p>' + response.contents +  '</p></div>' +
            '<div class="picwin"><img style="width:100%" src="/static/img/' + response.image + '"/></div>' +
          '</div>', { raw: true, keepWords:true });
}
else{
term.echo('<div class="wincont">' +
            '<div class="termwin"><p>' + response.output +'</p><p>' + response.contents +  '</p></div>' +
          '</div>', { raw: true, keepWords:true });

}
// Update the current directory
     term.set_prompt('[[gb;green;black]@bashLearner ~' + response.current_directory +'[[gb;green;black]$]');
      $('#current-directory').val(response.current_directory);
    });
  }, {
    // Set the prompt to the current directory
    prompt: '[[gb;green;black]@bashLearner ~]/[[gb;green;black]$]',
    clear: false,
    doubleTab: false,
    //greetings: wrappedGreetings,
    greetings: false,
   onInit: function(term) {


        term.echo(greetings0, { keepWords: true });
term.set_prompt('>');
        // TODAY -- term.typing('echo', 75,  'clear_logo_&because;&copy; | cat game-intro.txt\n' ,{keepWords:true}, function() {  });
term.enter("clear_logo_&because;&copy; | cat game-intro.txt\n", { typing: true,keepWords:true, delay: 75 });

         //term.echo(,{keepWords:true});
         //term.typing('echo', 100, greetings2,{keepWords:true}, function() {  });

              setTimeout(function(){
console.log("pause code");
term.pause();


}, 2400);

              setTimeout(function(){

console.log("clear code");
term.clear();

}, 3200);


        setTimeout(function(){
console.log("button code");
/*
term.echo('<div class="wincont">' +
            '<div class="termwin">' , { raw: true, keepWords:true });

term.echo(wrappedGreetings , { raw: false, keepWords:true });

term.echo( '</div>' +
            '<div class="picwin"><img style="width:100%" src="/static/img/rickbot.txt.png"/></div>' +
          '</div>' , { raw: true, keepWords:true });
*/


//term.echo('<img style="float:left" src="/static/img/rickbot.txt.png"/>', {raw: true});



term.echo(`

<button
  class="btn"
  type="button"
  onclick="displayPreferenceModal()"
>
    Click Here To Manage Cookie Preferences
</button>
<button
  id="soundbtn"
  class="btn"
  type="button"
   onclick="playRandomSound()"
>
    Click Here For Sound Check
</button>

`, {raw: true});



console.log("greetings code");
         term.echo(wrappedGreetings, { keepWords: true });

         // TODAY  - term.typing('echo', 100,  'open meeseeksBash.bin\n' ,{keepWords:true}, function() {  });

          term.enter("open meeseeksBash.bin\n", { typing: true,keepWords:true, delay: 100 });

         term.resume();


}, 3200);


        setTimeout(function(){
    term.echo('[[gb;teal;black]Meeseeks Bash v1.0]',{keepWords:true},null);
    term.set_prompt('[[gb;green;black]@bashLearner ~[[gb;green;black]$]');
}, 5800);
   },
    keepWords:true,
    wrap:true,
    completion: function(command, callback) {

    let cd =  $('#current-directory').val();
    cd = cd.replace("&#39;","'")

    if (cd=="/" || cd =="" || cd == null ){
        cd = "root";
    }

    $.ajax({

        url: "/session/" + cd,
        success: callback,
        error: function(xhr, status, error) {
          if(status==="timeout") {
            console.log("Request timed out");
            callback(['big', 'hairy', 'gorilla'])
          } else {
            console.log("Error: " + error);
            callback(['big', 'hairy', 'gorilla'])
          }
        },

        timeout: 2000 //2 sec
    });
    console.log("ajax code");
}
  });




});