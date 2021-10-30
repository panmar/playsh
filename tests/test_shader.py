import unittest
import glfw

from playsh.error import GlfwInitError, GlfwCreateWindowError, ShaderUniformNotFound
from playsh.graphics.shader import Shader
from sys import platform as _platform


class ShaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        if not glfw.init():
            raise GlfwInitError()

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 4)

        if _platform == "darwin":
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window = glfw.create_window(640, 480, "ShaderTest", None, None)

        if not window:
            glfw.terminate()
            raise GlfwCreateWindowError()

        glfw.make_context_current(window)

    def setUp(self) -> None:
        super().setUp()

        self.vs_text = """
        #version 330
        in vec4 position;
        uniform float test_uniform;
        void main() {
            gl_Position = vec4(position.xyz, test_uniform);
        }
        """

        self.fs_text = """
        #version 330
        out vec4 fragColor;
        void main() {
            fragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }
        """

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        glfw.terminate()

    def test_compilation(self) -> None:
        # given
        # when
        shader = Shader.from_text(self.vs_text, self.fs_text)
        # then
        self.assertNotEqual(shader.program, 0)

    def test_set_uniform(self) -> None:
        # given
        shader = Shader.from_text(self.vs_text, self.fs_text)

        # when
        shader.param("test_uniform", 42.0)

        # then
        self.assertTrue(True)

    def test_set_uniform_absent(self) -> None:
        def set_uniform_absent():
            # given
            shader = Shader.from_text(self.vs_text, self.fs_text)

            # when
            shader.param("absent_uniform", 42)

        # then
        self.assertRaises(ShaderUniformNotFound, set_uniform_absent)


if __name__ == "__main__":
    unittest.main()
