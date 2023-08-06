
<h1 align="center">Discord Webhooks</h1>

<div align="center">
    <strong><i>Interact with discord webhooks using python.</i></strong>
    <br>
    <br>
    
<a href="https://travis-ci.com/kyb3r/dhooks">
  <img src="https://img.shields.io/travis/com/kyb3r/dhooks/master.svg?style=flat" alt="Travis" />
</a>

<a href="https://pypi.org/project/dhooks/">
  <img src="https://img.shields.io/pypi/pyversions/dhooks.svg?style=flat" alt="Travis" />
</a>

<a href="https://pypi.org/project/dhooks/">
  <img src="https://img.shields.io/pypi/v/dhooks.svg?style=flat" alt="Travis" />
</a>

<a href="https://pypi.org/project/dhooks/">
  <img src="https://img.shields.io/pypi/dm/dhooks.svg?style=flat" alt="Travis" />
</a>

<a href="https://github.com/kyb3r/dhooks/blob/master/LICENSE">
  <img src="https://img.shields.io/github/license/kyb3r/dhooks.svg?style=flat" alt="Travis" />
</a>

</div>
<br>
<div align="center">
    This <strong>simple</strong> library enables you to easily interact with discord webhooks, allowing you to easily format discord messages and discord embeds, retrieve webhook information, modify and delete webhooks. Asynchronous usage is also supported.

</div>





### Installation
To install the library simply use [pipenv](http://pipenv.org/) (or pip, of course).

```
pipenv install dhooks
```

### Sending Messages:

<img src='https://i.imgur.com/8wu283y.png' align='right' width='380' height='125'>

```py
from dhooks import Webhook

hook = Webhook('WEBHOOK_URL')

hook.send("Hello there! I'm a webhook :open_mouth:")
```

### Sending Files:
You can easily send files as shown.
```py
from dhooks import Webhook, File
import requests
import io

hook = Webhook('WEBHOOK_URL')

file = File('path/to/file.png', name='cat.png') # optional name for discord

hook.execute('Look at this', file=file) # hook.execute is an alias for hook.send

# you can also pass in a File like object

response = await requests.get('https://i.imgur.com/rdm3W9t.png')
file = File(io.BytesIO(response.content), name='wow.png')

hook.send('Another one', file=file)
```

### Discord Embeds:
You can easily format and send embeds using this library. [**Result**](https://i.imgur.com/8Ms4OID.png)

Note: embed objects from `discord.py` are also compatible with this library.
```py
from dhooks import Webhook, Embed

hook = Webhook('WEBHOOK_URL')

embed = Embed(
    description='This is the **description** of the embed! :smiley:'
    color=0x1e0f3,
    timestamp=True # sets the timestamp to current time
    )
   
image1 = 'https://i.imgur.com/rdm3W9t.png'
image2 = 'https://i.imgur.com/f1LOr4q.png'

embed.set_author(name='Author Goes Here', icon_url=image1)
embed.add_field(name='Test Field',value='Value of the field \U0001f62e')
embed.add_field(name='Another Field',value='1234 😄')
embed.set_footer(text='Here is my footer text', icon_url=image1)

embed.set_thumbnail(image1)
embed.set_image(image2)

hook.send(embeds=embed)
```

### Get Webhook Info
You can get some basic information related to the webhook through Discord's api.

```py
hook.get_info()

# the following attributes will be populated with data from discord.

hook.guild_id, hook.channel_id, hook.default_name, hook.default_avatar_url 
```

### Modify and Delete Webhooks
You can change the default name and avatar of a webhook easily.
```py
with open('img.png', rb) as f:
    img = f.read() # bytes like object
    
hook.modify(name='Bob', avatar=img) # hook.edit is also an alias

hook.delete() # Webhook deleted permanently
```

### Asynchronous Usage:

To asynchronously make requests using aiohttp, simply pass in `is_async=True` as a parameter when creating a Webhook object. An example is as follows. Simply use the `await` keyword when calling api methods.

```py
import asyncio
from dhooks import Webhook

async def main():
    hook = Webhook('WEBHOOK_URL', is_async=True)
    
    await hook.send('hello') 
    await hook.modify('bob')
    await hook.get_info()
    await hook.delete()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
### [Documentation](https://dhooks.readthedocs.io)
You can find the full API reference here (https://dhooks.readthedocs.io)

### License
This project is licensed under MIT

### Contributing
Feel free to contribute to this project, a helping hand is always appreciated.

