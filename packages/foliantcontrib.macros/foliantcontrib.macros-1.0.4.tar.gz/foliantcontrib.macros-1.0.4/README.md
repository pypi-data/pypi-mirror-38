# Macros for Foliant

*Macro* is a string with placeholders that is replaced with predefined content during documentation build. Macros are defined in the config.


## Installation

```shell
$ pip install foliantcontrib.macros
```


## Config

Enable the preprocessor by adding it to `preprocessors` and listing your macros in `macros` dictionary:

```yaml
preprocessors:
  - macros:
      macros:
        foo: This is a macro definition.
        bar: "This is macro with a parameter: {0}"
```


## Usage

Here's the simplest usecase for macros:

```yaml
preprocessors:
  - macros:
      macros:
        support_number: "8 800 123-45-67"
```

Now, every time you need to insert your support phone number, you put a macro instead:

```markdown
Call you support team: <<macro>support_number</macro>.

Here's the number again: <<m>support_number</m>.
```

Macros are useful in documentation that should be built into multiple targets, e.g. site and pdf, when the same thing is done differently in one target than in the other.

For example, to reference a page in MkDocs, you just put the Markdown file in the link:

```markdown
Here is [another page](another_page.md).
```

But when building documents with Pandoc all sources are flattened into a single Markdown, so you refer to different parts of the document by anchor links:

```markdown
Here is [another page](#another_page).
```

This can be implemented using `<<if></if>` tag:

```markdown
Here is [another page](<if backends="pandoc">#another_page</if><if backends="mkdocs">another_page.md</if>).
```

This bulky construct quickly gets old when you use many cross-references in your documentation.

To make your sources cleaner, move this construct to the config as a reusable macro:

```yaml
preprocessors:
  - macros:
      macros:
        ref: <<if backends="pandoc">{0}</if><if backends="mkdocs">{1}</if>
```

And use it in the source:

```markdown
Here is [another page](<<macro params="#another_page, another_page.md">ref</macro>).
```
