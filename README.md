## Table of Contents
1. [How to Contribute](#how-to-contribute)
2. [Reviewing Pull Requests](#reviewing-pull-requests)
3. [Help](#help)

## How to Contribute

1. Go to the **Issues** tab and select any issue you want to tackle (that has not been assigned to anyone!)
2. On the right-hand side menu, click **Assign yourself** so the issue is now yours
3. Click on the issue and read the Description, Acceptance Criteria (AC), and Definition of Done
4. To start development, create a branch called **issue-1** (We call the branch by the issue name to ensure branches can be traced back to issues during review, to simplify naming and typing, and to ensure branches with the same name aren't created.)
```
git checkout -b issue-1
```
5. Make the necessary changes in your branch to meet the requirements in the issue, then commit your changes. If you have multiple commits, squash them into a single commit (this faciliates the PR review for reviewers). [See How to Squash Commits](#how-to-squash-commits)
7. Set your local branch to track the remote and push the changes to the remote branch
```
git push --set-upstream origin issue-1
```
9. On GitHub, go the **Pull requests** tab and click **New Pull Request**
10. Select your newly created branch **issue-1** (or other) in the "compare: branch" field (the one on the right)
11. In the description, make sure you write "Resolves #ISSUENUMBER". Describe your changes and explain how they meet the AC listed on the issue page.
  <img width="50%" alt="image" src="https://github.com/user-attachments/assets/2eaa8156-c4e8-4844-8c70-c97b2cc582f8" />

## Reviewing Pull Requests
1. Go to the **Pull requests** tab and select the PR you want to review
3. Read the summary of changes and look through the code
4. Checkout into the PR's branch (assuming branch is called "issue-1")
```
git checkout issue-1
```
5. Run the database migrations first, as the db cache are not saved to repository. This will safely update the database without pushing db code to the repository.
```
python manage.py migrate
```
7. Run the development server and test the changes
```
python manage.py runserver
```

## Help

### How to squash commits
1. Launch the rebase session. Run this command in your terminal, specifying how many (3 in this case) recent commits to squash:
```
git rebase -i HEAD~3
```
2. Configure the editor instructions. Your default text editor will open with a list of your recent commits ordered from oldest (top) to newest (bottom). It will look similar to this:
```
pick a1b2c3d First commit message
pick e4f5g6h Second commit message
pick i7j8k9l Third commit message
```
Leave the very first commit at the top as pick. Change the word pick to squash (or just s) for all subsequent lines below it.
```
pick a1b2c3d First commit message
squash e4f5g6h Second commit message
squash i7j8k9l Third commit message
```
3. Save and close. Save the file and close the editor (if using Vim, press Esc, type :wq, and hit Enter)
