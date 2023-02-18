from onboarding.protocol import BaseModel


class CreateBookRequest(BaseModel):
    name: str
    category: str
    img_link: str
