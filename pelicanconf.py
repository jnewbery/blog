SITENAME = "John Newbery's blog"
SITEURL = ""

PATH = "content"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
STATIC_PATHS = ["extra"]
EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/mpc-demo": {"path": "mpc-demo/index.html"},  # move mpc-demo to articles when no longer hosting the app on GCP
}

TIMEZONE = "UTC"
DEFAULT_LANG = "en"
AUTHOR = "John Newbery"

# Theme
THEME = "themes/john-theme"

# Site-specific settings used in templates
SITE_TITLE = "John Newbery"
HEADER_TEXT = "<p>Energy and Decentralization</p>"
AVATAR = "theme/img/avatar.jpg"
FAVICON = "theme/img/favicon.jpg"
GITHUB_USER = "jnewbery"
TWITTER_USER = "jfnewbery"
LINKEDIN_URL = "https://www.linkedin.com/in/johnnewbery/"
GOOGLE_FONTS = "Source+Sans+Pro:400,700,700italic,400italic"
KATEX = True

# Navigation
MENUITEMS = [
    ("About", "/about/"),
    ("Blog", "/blog/"),
    ("Talks", "/talks/"),
]

# URL structure matching Jekyll's /:title/ format
ARTICLE_URL = "{slug}/"
ARTICLE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORY_URL = "{slug}/"
CATEGORY_SAVE_AS = "{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"

# Feed
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = None
TAG_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Pagination (disabled to match original)
DEFAULT_PAGINATION = False

USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = "misc"

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
}
