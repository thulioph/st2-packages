# Bit.ly Sublime Plugin

Hello, this is a small plugin I've put together based on [a demo I found on the web at Nettuts+](http://bit.ly/HdS3BQ).

I find the URL-shortening service [Bit.ly](http://bitly.com) to be quite handy. Short URLs are aesthetically pleasing, to be sure. The thing I really like about Bit.ly though are the reports I can get about shortened links I've sent others.

_This is an early release._

Contributions are welcome, there are some bugs I'm quite sure. A little short on time here…aren't we all?

## Settings

The only settings for this plugin are account-related. You can use this plugin with your own account by using the following settings:

```
{
	"api_login": "<YOUR_BITLY_USERNAME_HERE>",
	"api_key": "<YOUR_API_KEY_HERE>"
}
```

To get a new API key from Bit.ly [visit this link](https://bitly.com/a/your_api_key). 

## Todos

* ~~Add instructions for obtaining API from Bit.ly~~
* Add in contextual menu, so you can choose 1 URL to shorten
* Check config, provide user feedback if the user provides invalid username/api-key
* New Features
	* "Shorten all Markdown formatted links"
* Rebrand/Rename this as a tool to "Monitor Links", the way I use it to verify if people bother to look at links I've put into a document.


## Issues

1. Needs tests
2. The regular expression used to detect URLs is not well-tested.
3. May change so it ensures no spaces in the highlighted string, as a safety precaution. As it works now a user may select a large string with spaces and this has unpredictable behavior. At least test out what happens and perhaps update the code to prevent it, if that is not already happening.