# ssml-builder

## Installation

```
pip install ssml-builder
```

## Usage

**Create a Speech object**

```
from ssml_builder.core import Speech
speech = Speech()
```

**Add text and tags**

```
# add text
speech.say("hello world")
# add pause tag
speech.pause("10s")
# add prosody tag
speech.prosody("x-fast")
```

**Output ssml with \<speak\> wrapper**
```
speech.speak()
```
