from dataclasses import dataclass
import glfw
from typing import Callable, Dict
from injector import Injector, inject

from playsh.error import FragmentShaderIOError, GlfwInitError, GlfwCreateWindowError
from playsh.graphics.geometry import ScreenQuad
from playsh.graphics.shader import Shader
from playsh.graphics.renderer import ScreenRenderer
from playsh.input import Input
from playsh.store import Store
from OpenGL import GL as gl
from glm import vec2, vec3, vec4
from playsh.timer import Timer
import time


@inject
@dataclass
class System:
    input: Input
    store: Store
    screen_renderer: ScreenRenderer
    timer: Timer
    frame_index: int = 0


class PlaySh:
    def __init__(self, width: int, height: int, fragment_shader_path: str) -> None:
        self._width = width
        self._height = height

        try:
            with open(fragment_shader_path, "r") as file:
                self._fragment_shader_text = file.read()
        except IOError as e:
            raise FragmentShaderIOError(
                "Error reading file {} : {}".format(fragment_shader_path, repr(e))
            )

        self._system = Injector().get(System)
        self._startup()

    def _startup(self) -> None:
        if not glfw.init():
            raise GlfwInitError()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)

        self._window = glfw.create_window(
            self._width, self._height, "PlaySh", None, None
        )
        if not self._window:
            glfw.terminate()
            raise GlfwCreateWindowError()
        glfw.make_context_current(self._window)

        glfw.set_key_callback(
            self._window,
            lambda _, *args: self._system.input.on_key_changed(*args),
        )

        glfw.set_mouse_button_callback(
            self._window,
            lambda _, *args: self._system.input.on_mouse_key_changed(*args),
        )

        glfw.set_cursor_pos_callback(
            self._window,
            lambda _, *args: self._system.input.on_cursor_pos_changed(*args),
        )

        glfw.set_framebuffer_size_callback(
            self._window, lambda _, *args: self._on_framebuffer_size_change(*args)
        )

    def _update(self) -> None:
        self._system.timer.tick()
        self._system.frame_index = self._system.frame_index + 1

        if self._system.input.is_key_pressed(glfw.KEY_ESCAPE):
            glfw.set_window_should_close(self._window, True)

    def _collect_builtin_params(self) -> Dict[str, Shader.ParamType]:
        params: Dict[str, Shader.ParamType] = dict()
        params["iResolution"] = vec2(self._width, self._height)
        params["iTime"] = self._system.timer.total_elapsed_seconds
        params["iTimeDelta"] = self._system.timer.elapsed_seconds
        params["iFrame"] = self._system.frame_index
        mouse_param = vec4(0.0)
        if self._system.input.is_mouse_key_down(glfw.MOUSE_BUTTON_LEFT):
            mouse_param.x = self._system.input.cursor_pos[0]
            mouse_param.y = self._system.input.cursor_pos[1]
        if self._system.input.is_mouse_key_pressed(glfw.MOUSE_BUTTON_LEFT):
            mouse_param.z = self._system.input.cursor_pos[0]
            mouse_param.w = self._system.input.cursor_pos[1]
        params["iMouse"] = mouse_param
        return params

    def _render(self) -> None:
        gl.glClearColor(0.0, 0.0, 0.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glViewport(0, 0, self._width, self._height)

        self._system.screen_renderer.render(
            self._fragment_shader_text, self._collect_builtin_params()
        )

    def run(self) -> None:
        while not glfw.window_should_close(self._window):
            self._update()
            self._render()

            def sleep_until_framerate(frame_rate: int):
                frame_time = 1.0 / frame_rate
                sleep_time = self._system.timer.seconds_since_tick() - frame_time
                if sleep_time > 0.0:
                    time.sleep(sleep_time)

            sleep_until_framerate(frame_rate=30)
            glfw.swap_buffers(self._window)
            glfw.poll_events()

        glfw.terminate()

    def _on_framebuffer_size_change(self, width: int, height: int):
        self._width = width
        self._height = height