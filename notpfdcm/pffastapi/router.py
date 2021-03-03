from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Tuple

# hello dependencies
import platform
import psutil
import multiprocessing
import os
import socket


def create_description_router(name, about, version) -> APIRouter:
    """
    Example on how to create some predefined routes (hello and about)
    which produces data that can be set per-instance and is constant
    within an instance.
    """
    # ========== ========== ========== ==========
    # DEFINE RESPONSE DATA MODELS
    # ========== ========== ========== ==========

    # rename variables
    # https://bugs.python.org/issue43380
    # We want to create the AboutModel class in the scope of this function
    # so that its constant response can be generated in the interactive docs

    about_name = name
    about_about = about
    about_version = version

    class AboutModel(BaseModel):
        name: str = Field(about_name, title='Name of application')
        about: str = Field(about_about, title='About this application')
        version: str = Field(about_version, title='Version string')

    about_model = AboutModel()

    class SysInfoModel(BaseModel):
        """
        For the most part, copied from
        https://github.com/FNNDSC/pfcon/blob/87f5da953be7c2cc80542bef0e67727dda1b4958/pfcon/pfcon.py#L601-611
        """
        system: str = Field(platform.system(), title='Operating system')
        machine: str = Field(platform.machine(), title='Computer architecture')
        uname: List[str] = Field(list(platform.uname()), title='uname output',
                                 description='Uname output, converted from object to list')
        version: str = Field(platform.version(), title='Platform version')
        memory: List = Field(..., title='Details about virtual memory',
                             description="Actually a NamedTuple but I'm not typing it out")
        cpucount: int = Field(multiprocessing.cpu_count(), title='Number of CPU cores')
        loadavg: Tuple[float, float, float] = Field(..., title='System load',
                                                    description='Average system load over last 1, 5, and 15 minutes')
        cpu_percent: float = Field(..., title='Current CPU usage percent', le=100.0)
        hostname: str = Field(socket.gethostname(), title='Hostname')
        inet: str = Field(socket.gethostbyname(socket.gethostname()), title='Local IP address')
        platform: str = Field(platform.platform(), title='Kernel name')

    # TypedDict not supported yet in Python 3.8
    # https://pydantic-docs.helpmanual.io/usage/types/#typeddict
    class EchoModel(BaseModel):
        msg: str

    class HelloModel(BaseModel):
        name: str = about_model.name
        version: str = about_model.version
        sysinfo: SysInfoModel = SysInfoModel(uname=['Linux'], memory=[], cpu_percent=0.0, loadavg=(0.0, 0.0, 0.0))
        echoBack: Optional[EchoModel]

    # ========== ========== ========== ==========
    # DEFINE ROUTES
    # ========== ========== ========== ==========
    router = APIRouter()

    @router.get(
        '/about/',
        tags=['pffastapi'],
        response_model=AboutModel)
    async def read_about():
        """
        A description of this service.
        """
        return about_model

    @router.get(
        '/hello/',
        tags=['pffastapi'],
        response_model=HelloModel
    )
    async def read_hello(echoBack: Optional[str] = Query(None, description='something to print back verbatim')):
        """
        Produce some information like the OG pfcon
        """
        # return EchoModel(msg = echoBack)
        d_ret = {
            'sysinfo': {}
        }
        d_ret['sysinfo']['system'] = platform.system()
        d_ret['sysinfo']['machine'] = platform.machine()
        d_ret['sysinfo']['platform'] = platform.platform()
        d_ret['sysinfo']['uname'] = platform.uname()
        d_ret['sysinfo']['version'] = platform.version()
        d_ret['sysinfo']['memory'] = psutil.virtual_memory()
        d_ret['sysinfo']['cpucount'] = multiprocessing.cpu_count()
        d_ret['sysinfo']['loadavg'] = os.getloadavg()
        d_ret['sysinfo']['cpu_percent'] = psutil.cpu_percent()
        d_ret['sysinfo']['hostname'] = socket.gethostname()
        d_ret['sysinfo']['inet'] = socket.gethostbyname(socket.gethostname())
        sysinfo = SysInfoModel(**d_ret['sysinfo'])

        if echoBack:
            echo = EchoModel(msg=echoBack)
            return HelloModel(echoBack=echo, sysinfo=sysinfo)

        return HelloModel(sysinfo=sysinfo)

    return router
