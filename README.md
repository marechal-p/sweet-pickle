# ~ Sweet Pickle !

This repository is an illustration for "why you should not trust pickle".

The dirty pickle in question comes from [Python's standard lib](https://docs.python.org/3/library/pickle.html).

**Don't get me wrong, pickle is an amazing tool ! It serialize and deserialize almost anything !**

Here you will just see how to maliciously use this library to remote execute code on any host running unsecure pickling.

By default everything is in `localhost` so that it stays pretty isolated on your machine. Just know that any similar setup for the server side is potentially vulnerable to the exploit.

This project was made to illustrate the concept to myself. I couldn't believe this would work. **Yet it does**. I used to say "ok cool you used `pickle`, but if you really intend on sharing your work, please use another library". Until today I had nothing to back my fears, now I have I guess. Hopefully people will also better understand the technical / pratical details involved in this part of cyber-security.

The file `client.py` starts an interactive session for you to play with, it has a few useful classes to make any malicious attack you could try on yourself. Execute almost any Python code ! _(you might be limited by the socket recv buffer, but who said you couldn't send line by line ?)_

### Have fun toying with this !
