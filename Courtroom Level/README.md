## Courtroom Level

This folder contains the code for your courtroom level. Copy the Courtroom folder into the folder where your renpy games are stored (the default is usually called renpy projects on Windows) to have your own modifiable copy.


### Instructions
You will need to do the following to complete your courtroom level:

TIP: To locate these TODOs in your files quickly, open the Renpy Launcher, press on your game, and then press Navigate Script (below Actions). Press the tab called TODOs and then click on the TODO you would like to be navigated to.

1. Update the courtroom.json file to match your case. We highly recommend only using at most two pieces of evidence per specialty. You can add as many specialties as you wish. For each evidence, you must include the name of the evidence, the image name of the evidence, the description of the evidence, and the truth bases associated with the evidence. The truth bases are points that the player should mention about the evidence during the interview portion. If the player mentions all the truth bases, then that piece of evidence will be considered fully discussed. Essentially, the truth bases help the game proceed/end.

NOTE: Make sure to add your evidence images inside the images/Inventory Items folder and ensure the dimensions are around 200 x 200 px. 

2. Make Steve (the character) explain the details of your case! Optionally, you can make a minigame where the player has to summarize the details of the case themselves (great learning opportunity, but given the August 8 time constraint, not necessary). You will need to do this around line 87 of script.rpy.
3. Provide the AI with the details of your case, similar to the above point, but more concisely since it will be used in the AI's instructions. You will need to do this around line 47 of a_script.rpy.
4. Update screen case_description and screen specialty_exploration_screen to match the titles of your case (lines 57 and 215 respectively).


### FAQ
After completing these steps, your level should be complete! If you run into any issues or if you have any questions, please reach out to either Janna or Navya on Teams!

1. I'm getting SyntaxError: unexpected EOF while parsing (none, line 2). What should I do?

This means that the Gemini API has reached its maximum quota. You'll either need to wait a little bit until it restores, or generate a new API key through [Google AI Studio](https://aistudio.google.com/prompts/new_chat?pli=1). If it's urgent and you've used all your API keys, please reach out to either Janna or Navya.
