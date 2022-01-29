# Introduction

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

These are the  basic commands for your use. Run these in the same directory as the `mkdocs.yml` file.

* `mkdocs serve` - Start the live-reloading docs server.
    - This is for previewing changes while working.
* `mkdocs build` - Build the documentation site.
    - This will convert the markdown files into a static site and place it in a `site/` directory. Not necessary to use this.
* `mkdocs -h` - Print help message and exit.

## Docs Guide

### File structure
Documentation for each app should be placed in a separate folder (refer to [project layout](#project-layout)).


Each app folder should generally contain these three folders:

1. `models.md`
2. `view.md`
3. `custom-additions.md` (_only if applicable_)

### Documentation content
These are the things that should be focused on while writing documentation.

* `models.md`
    - Explain what each model in `models.py` is used for.
    - Explain what each field should contain (also talk about the reason behind any constraints on the field).
* `views.md`
    - Explain what each view in `views.py` is doing/returning (pay attention to the context variable in the return statement).
    - Note all the variables being passed to the frontend (for reference of 
* `custom-additions.md`
    - Any functions or classes written by developers for utility or abstraction.
    - Any libraries used (include setup and usage details).

!!! note
    Any documentation page which is not complete should include the following line after the page title
        
        !!! todo "Incomplete"

Model fields data table template
```
| Field | Type | Required | Description| Contraints |
| :---: | ---- | :------: | :--------: | :--------: |
|       |      |          |            |            |
```


### Making a contribution

* `git checkout documentation`
* Create a markdown file in the required app folder.
* Follow [this](https://squidfunk.github.io/mkdocs-material/reference/) reference material for formatting options.
* `git add <file-name>`
* `git commit -m <addition-summary>`
* `git push`

To add documentation for `models.py` in core app, for example, this would be the directory structure:

    docs/
        core/
            models.md

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        <app-folder>
            models.md
            views.md
            custom-additions.md 
