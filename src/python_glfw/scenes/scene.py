class Scene:
    def __init__(self) -> None:
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def key_callback(self, key: int, action: int):
        for component in self.components:
            component.key_callback(key, action)


    def update(self, time: float):
        for component in self.components:
            component.update(time)

    def render(self):
        for component in self.components:
            component.render()
