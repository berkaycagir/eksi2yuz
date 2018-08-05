# eksi2yuz

[eksi2yuz](https://twitter.com/eksi2yuz) is a Twitter bot that posts titles from ekşisözlük which has more than 200 entries in the "gündem". It is written with Python in one night, so excuse its mistakes.

## Dependencies

* a recent version of Python 2 with [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [requests](https://github.com/requests/requests), [tweepy](https://github.com/tweepy/tweepy), and [user_agent](https://github.com/lorien/user_agent)
* a Twitter account (_obviously_)
* a scheduled command daemon

## Installation

1. Install all the dependencies listed.
2. Enter the values required in the script, which can be obtained from https://developer.twitter.com
3. Configure your scheduled command daemon to run `eksi.py` with the desired interval.
4. Done!

## Data persistence

Python's [pickle](https://docs.python.org/2/library/pickle.html) module is being used for data persistence; and that's probably more than enough for this.

## Contribution

Pull requests are welcomed.

## License

You can do whatever you want under the MIT license. See the `LICENSE` for more information.
