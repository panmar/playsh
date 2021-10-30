import unittest
import glfw

from playsh.input import Input


class InputTest(unittest.TestCase):
    def test_key_press(self):
        # given
        input = Input()

        # when
        input.on_key_changed(glfw.KEY_A, 0, glfw.PRESS, 0)

        # then
        self.assertTrue(input.is_key_down(glfw.KEY_A))
        self.assertTrue(input.is_key_pressed(glfw.KEY_A))

    def test_key_down(self):
        # given
        input = Input()

        # when
        input.on_key_changed(glfw.KEY_A, 0, glfw.PRESS, 0)
        input.update()

        # then
        self.assertTrue(input.is_key_down(glfw.KEY_A))
        self.assertFalse(input.is_key_pressed(glfw.KEY_A))

    def test_key_release(self):
        # given
        input = Input()

        # when
        input.on_key_changed(glfw.KEY_A, 0, glfw.PRESS, 0)
        input.on_key_changed(glfw.KEY_A, 0, glfw.RELEASE, 0)

        # then
        self.assertFalse(input.is_key_down(glfw.KEY_A))
        self.assertFalse(input.is_key_pressed(glfw.KEY_A))

if __name__ == "__main__":
    unittest.main()
