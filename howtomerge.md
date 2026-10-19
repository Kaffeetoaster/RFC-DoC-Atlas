ok, so the problem is, that after merging dev to main in github, dev is always one commit behind main.
This makes sense, since main now has a merge commit, which is missing in dev.
This is standard github merge behaviour.

one solution is to set the merging to fastforward(?)
I think this is harder to do in github, so we will do the merge command in the terminal.


so the workflow is this:

## Update branches
git fetch origin
git switch dev
git pull origin dev

# add and commit or do this in vscode sourcecontrol gui
git switch dev
git add .
git commit -m "Your changes"
git push origin dev

# merge dev into main
git fetch origin
git switch main
git pull origin main
git merge --ff-only origin/dev
git push origin main


# or open pr in github and merge there
after this the dev branch will be behind main, so we will merge main back to dev in the terminal
git fetch origin
git switch dev
git merge origin/main
git push origin dev