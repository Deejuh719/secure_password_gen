## Secure Password Generator
This project started as a side creation that I had done with basic python and terminal interfacing.
I had wanted to make a GUI for it, and ended up taking a class in school that taught me Django, which ended up being the better option.
So, here we have a Django project that utilizes skills I've learned over the 16 week course as well as some attempts that I was teaching myself.
The project itself is <strong>not complete</strong> and certain features are only partially working. There are a lot of things I actually want to fix and incorporate within the project itself when given the time.

### What it includes so far:
1. Password generation and storage using secret. Comes with a scale to select length, labelling of the app/site it is for as well as the use of that site, and the option to use special characters, numbers, and similar characters
2. Storage of the password that hides the password unless a button is clicked to reveal it
3. Sorting and search (both require minimal updates to functionality)
4. Recreating/self-implimented updating with timestamp
5. Access only via log-in to only your information

### What is missing/needs updating:
1. TFA: The two-factor auth was a frustrating addition that was only partially added and did not work. Since the project was on a time limit, I did not get to impliment it properly
2. Complete encryption: had wanted to include, but time limit didn't allow
3. Saving to JSON or CSV for personal keeping
4. Allowing log-in using another method: i.e. Apple or Google

As I go along, I'll figure out more I want to add. If you play with this yourself, do feel free to add your own branch with updates. As I will be adding updates as well when I get around to it.

#### Play with it, have fun with it. Will probably delete the requirements.txt and reupdate that as there are several things in it that were required for things that didn't work

## 08/23/2025 Update:
1. Since I am including this as a part of my portfolio, I created an active website for it so that it can be tested and used online as a functional tool.
  Site: [Gimme Passwords Please!](https://secure-password-gen.onrender.com)
2. Also did a minor tweak to the code to make it more mobile friendly (considering I've decided to play with it on my phone for the first time today and learned that I had forgotten to do that)
