from python_glfw.components import Component


class Scene:
    def __init__(self) -> None:
        self.components: list[Component] = []

    def add_component(self, component: Component):
        self.components.append(component)

    def key_callback(self, key: int, action: int):
        for component in self.components:
            component.key_callback(key, action)

    def update(self, delta_time: float):
        for component in self.components:
            component.update(delta_time)

    def render(self):
        for component in self.components:
            component.render()
