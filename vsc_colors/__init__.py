import json
from typing import Any, cast

# TODO: abuse iterators to make the code less "nesty"

with open(
    "/Users/jmgd/Documents/Work/repos/oolong/themes/Oolong-color-theme.json"
) as theme_json:
    lines = theme_json.readlines()

lines = [line.split("//")[0] for line in lines]
theme: dict[str, Any] = json.loads("".join(lines))

theme_colors = {}

if (colors := cast(dict[str, str] | None, theme.get("colors"))) is not None:
    for key, color in colors.items():
        color = color.upper()

        if len(color) != 7:
            color = color[:7]

        if (color_list := theme_colors.get(color)) is not None:
            color_list.append(key)
        else:
            theme_colors[color] = [key]

if (
    semantic_tokens := cast(dict[str, Any] | None, theme.get("semanticTokenColors"))
) is not None:
    for key, setting in semantic_tokens.items():
        if isinstance(setting, str):
            setting = setting.upper()

            if len(setting) != 7:
                setting = setting[:7]

            if (color_list := theme_colors.get(setting)) is not None:
                color_list.append(key)
            else:
                theme_colors[setting] = [key]
        else:
            if (color := setting.get("foreground")) is not None:
                color = color.upper()

                if len(color) != 7:
                    color = color[:7]

                if (color_list := theme_colors.get(color)) is not None:
                    color_list.append(key)
                else:
                    theme_colors[color] = [key]

if (token_colors := theme.get("tokenColors")) is not None:
    maybe_settings = map(lambda o: (o["name"], o.get("settings")), token_colors)
    settings = filter(lambda s: s[1] is not None, maybe_settings)
    maybe_foreground = map(lambda s: (s[0], s[1].get("foreground")), settings)
    foreground = filter(lambda f: f[1] is not None, maybe_foreground)
    for key, color in foreground:
        if (color_list := theme_colors.get(color)) is not None:
            color_list.append(key)
        else:
            theme_colors[color] = [key]


from pprint import pprint

pprint(theme_colors)
