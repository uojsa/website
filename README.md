### Outline

- [Outline](#outline)
- [To-Do](#to-do)
- [Build and Run Locally](#build-and-run-locally)
- [Development references](#development-references)

### To-Do

This is a list compiled for the current things that need fixing / doing. They're sorted by difficulty level for clarity. 


**Easy**
- [x] Fix UI inconsistencies accross pages
  - [x] Nav bar
  - [x] Footer
- [x] Make mentioned links point to correct pages
- [ ] Remove occurences of made-up template things (e.g. sushi workshop, building location)
- [ ] Fix contact information accross website (e.g., email, instagram)
- [ ] Fix colours to match uOJSA Branding (see Google Drive > Communication > Branding)
- [ ] Review wording is inline with uOJSA brand and vocabulary
  - [ ] JSA -> uOJSA
  - [ ] Add more items... (there are some not so great sentences in some places)

**Medium**
- [ ] Replace logo with actual logo (See Google Drive above)
  - [ ] Header / Navbar
  - [ ] Footer
- [ ] Fix Mobile Usability
  - [ ] Top right corner hamburger currently not opening navbar
  - [ ] Check if any other issues

**Hard / Undecided**
- [ ] Create copies of website in EN/FR/JP


Feel free to add more things to the site (e.g., improve the calendar), or replace some existing things! 

Things to check if you're not sure:
-  The tailwind CSS documentation to see what UI elements can be added
-  Check out `message.txt` to see if any requirements are missing / too complex to implement (provide alternative).
-  Common sense :)
   -  Does it look ugly?
   -  Is something unusable?
  
Remember, if you feel like you can do something to improve it, just do it. Don't need to ask. If it turns out to be bad, we can always revert it.

MOST IMPORTANT: *Commit frequently!!!!* This allows us to revert versions without removing too many new changes, and allows us to see new changes with more granularity. 

### Build and Run Locally

> [!NOTE]
> You do not need to install Tailwind via npm for the pages to work. The app uses a CDN script that loads Tailwind in the browser at runtime. You only need to install Tailwind locally if you want to build CSS ahead of production, use custom Tailwind config/plugins, or avoid relying on the CDN in production app.

First, ensure you have node.js installed (see [installation](https://nodejs.org/en)). Node is the official JavaScript package manager and is needed to install Vite. Vite is the local development web server we will use, since it is quick and easy to setup.

First, in a local directory (not in a OneDrive-backed up folder T_T) clone the repository:

`git clone https://github.com/uojsa/website`

and cd into the new repository folder:

`cd website`

Once the contents of the repository have been cloned to your local directory, run the following:

`npm install`

This ensures any new packages added to `package.json` are installed to your project. Missing dependencies are often a cause for errors during build. Additionally, if you have not already, this command will install Vite.

Finally, run the following:

`npx vite`

This will execute the vite package, setting up a local development server hosted usually on port 5173 at http://localhost:5173. If the port is already occupied, it should default to the next available port. Keep this is mind if it starts up on 5174 or higher. You might already have an old server running on 5173.

Note: in order for the command to work, there must be a file called `index.html` in that directory. Ensure you are inside the correct folder where such file exists.


### Development references

-  [Tailwind CSS Docs](https://tailwindcss.com/docs/styling-with-utility-classes)
- [Vite](https://vite.dev/)
