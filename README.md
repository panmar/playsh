# playsh
A GLSL fragment shader playground, inspired by [Shadertoy](https://www.shadertoy.com/).

<p align="center"><img src="examples/example.jpg" alt="example" width="600"/></p>

## Builtin shader uniforms
* uniform vec3 __iResolution__
* uniform float __iTime__
* iuniform float __TimeDelta__
* uniform int __iFrame__
* uniform vec4 __iMouse__
* uniform Texture2D __iChannel0__
* uniform vec3 __iChannelResolution__[4]

## Dependencies
* glfw
* PyOpenGL
* PyGLM
* numpy
* pillow
* injector


## Example
```Python
from playsh import PlaySh, TextureDesc, Filter, Wrap

app = PlaySh(
    width=1920,
    height=1200,
    fragment_shader_path="examples/example.fs",
    channel0=TextureDesc(
        path="examples/noise.png", filter=Filter.LINEAR, wrap=Wrap.REPEAT
    ),
)
app.run()
```
