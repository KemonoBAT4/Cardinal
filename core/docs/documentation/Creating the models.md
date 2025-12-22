# Creating your json model
If you have familiarity with the json models you can create your models
by creating the file `models.json` on your own.

## Create the first model
This is the basic structure of the json, every value that has this `<>` is a property that has to be edited before starting the setup or the whole model would not be loaded.

### Remember:
the `model name`, `field name`, `relationship model name`, `relationship model field name` MUST NOT have spaces between the words, any space will be replaced with underscors `_`

the `field type` MUST be a valid field type according to SQLAlchemy. You can find a list of the accepted field type at the bottom of this file

``` json
[
    {
        "name": "<model name>",
        "fields": [
            {
                "name": "<field name>",
                "required": true,
                "unique": true,
                "label": "<field label name>",
                "description": "<field description>",

                "type": {
                    "type": "<field type>",
                    "relationship": {
                        "model": "<relationship model name>",
                        "field": "<relationship model field name>"
                    }
                }
            }
        ]
    }
]
```

### Adding more models
After you created the first model if you need to add a second model you just need to add a quote `,` after the model structure and you can paste the second model

Like this:

``` json
[
    {
        "name": "<model name>",
        "fields": [
            {
                "name": "<field name>",
                "required": true,
                "unique": true,
                "label": "<field label name>",
                "description": "<field description>",

                "type": {
                    "type": "<field type>",
                    "relationship": {
                        "model": "<relationship model name>",
                        "field": "<relationship model field name>"

                    }
                }
            }
        ]
    },
    {
        "name": "<model name>",
        "fields": [
            {
                "name": "<field name>",
                "required": true,
                "unique": true,
                "label": "<field label name>",
                "description": "<field description>",

                "type": {
                    "type": "<field type>",
                    "relationship": {
                        "model": "<relationship model name>",
                        "field": "<relationship model field name>"
                    }
                }
            }
        ]
    }
]
```

## Accepted field types:
This is the list of all the accepted types, to be loaded correctly the 
Case of the words must be the same as the ones here

- `String(<number>)` -> this defines a string where the `<number>` is the max amount of chars for every string (max is 255), us this for like a name, surname or something short
- `Text` -> a larger `string`, this does not need for a number to set the max but it can store longer chars than the string, use this for phrases
- `Boolean` -> this defines just a boolean, that can only be `true` or `false`, use this if you need to state like an "active"
- `Float` -> this defines decimanl numbers, like `23.23`, use this if you need to store that kind of data
- `Integer` -> this defines the integer number like `23`, `42`, use this if you need to store that kind of data




