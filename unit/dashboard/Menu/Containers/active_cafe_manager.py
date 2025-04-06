class ActiveCafeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActiveCafeManager, cls).__new__(cls)
            cls._instance.active_cafe_id = None
        return cls._instance

    def set_active_cafe(self, cafe_id):
        self.active_cafe_id = cafe_id

    def get_active_cafe(self):
        return self.active_cafe_id
