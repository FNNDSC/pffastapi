from fastapi import FastAPI
from pffastapi.router import create_description_router
from routes.dicom import router as notpdfdcm_router

__version__ = '1.0.0'


pffastapi_router = create_description_router(
    name='notpdfdcm',
    version=__version__,
    about='Does nothing'
)

app = FastAPI(
    title='Not pfdcm, just an example',
    version=__version__
)

app.include_router(pffastapi_router,
                   prefix='/api/v1')
app.include_router(notpdfdcm_router,
                   prefix='/api/v1')
