# Why Copier?

This template started out as a [Cookiecutter][cookiecutter] template, and was inspired by the [Hypermodern Python Cookiecutter][hypermodern-cc]. Cookiecutter is a great platform, but I quickly ran into features I wanted that seemed to be unavailable, including:

* Conditional Questions
* Template Updating
  * This was available for Cookiecutters via [Cruft][cruft], but its featureset seemed to lag behind Cookiecutter's
* Proper `.jinja` Extension for Templates
  * Because Cookiecutter didn't use a proper template extension, it caused larger problems for linters and formatters

Copier provides these out of the box, and uses a friendly YAML syntax to boot.

[cruft]: https://cruft.github.io/cruft/
[cookiecutter]: https://www.cookiecutter.io/
[hypermodern-cc]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
