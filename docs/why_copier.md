# Why Copier?

This template started out as a [Cookiecutter][cookiecutter] template, and was inspired by the [Hypermodern Python Cookiecutter][hypermodern-cc]. Cookiecutter is a great platform, but lacks several features, including:

* Conditional Questions
* Template Updating
  * This was available for Cookiecutters via [Cruft][cruft], but its featureset seemed to lag behind Cookiecutter's
* Proper `.jinja` Extension for Templates
  * Because Cookiecutter didn't use a proper template extension, it caused larger problems for linters and formatters

Copier provides these out of the box, and uses a friendly YAML syntax to boot. The Copier project also explicitly indicates that they want to be a language-agnostic templating engine, which is nice as the Postmodern template family is designed to be useful for any/all purposes.

[cruft]: https://cruft.github.io/cruft/
[cookiecutter]: https://www.cookiecutter.io/
[hypermodern-cc]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
