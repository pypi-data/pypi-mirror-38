class Layer:
    def __init__(self):
        self._game_objects = []

    def register_gameobject(self, game_object):
        self._game_objects.append(game_object)

    def remove_gameobject(self, game_object):
        self._game_objects.remove(game_object)

    def update(self, helperobject, num_iterations):
        # run default update
        for game_object in self._game_objects:
            game_object.update(helperobject)

        # run fixed update
        for _ in range(num_iterations):
            for game_object in self._game_objects:
                game_object.fixed_update(helperobject)

    def draw(self, helperobject):
        for game_object in self._game_objects:
            game_object.draw(helperobject)