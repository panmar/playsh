from playsh.graphics.texture import Filter, TextureDesc, Wrap
from playsh.playsh import PlaySh


def main() -> None:
    app = PlaySh(
        width=1920,
        height=1200,
        fragment_shader_path="examples/example.fs",
        texture=TextureDesc(
            path="examples/noise.png", filter=Filter.LINEAR, wrap=Wrap.REPEAT
        ),
    )
    app.run()


if __name__ == "__main__":
    main()
