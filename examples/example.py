from playsh.playsh import PlaySh


def main() -> None:
    app = PlaySh(width=1920, height=1200, fragment_shader_path="examples/example.fs")
    app.run()


if __name__ == "__main__":
    main()
