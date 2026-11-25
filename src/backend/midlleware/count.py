"Confere o rate limit"
from src.backend.logs import logger
import threading
from datetime import datetime, timezone, timedelta
from src.backend.exceptions import InstanceNotFound
class CountThread:

    def __init__(self)->None:

        self.count = {}
        self.lock = threading.Lock()

    #adiciona em count
    async def add(self, instance_name:str) -> None:

        logger.info(f"Increment in {instance_name}...")

        with self.lock:

            now = datetime.now(timezone.utc)
            current = self.count.get(instance_name)

            #janela nova se não existe ou já venceu; senão só soma (o exp não é renovado)
            if current is None or current["exp"] < now:

                self.count[instance_name] = {
                    "count": 1,
                    "exp": now + timedelta(minutes=1)
                }

            else:

                current["count"] += 1

        logger.success(f"{instance_name} incremented!")


    #Pega o valor
    async def get(self, instance_name:str) -> dict|None:

        with self.lock:

            logger.info(f"Getting {instance_name}...")

            instance = self.count[instance_name] if instance_name in self.count.keys() else None 

            logger.success(f"{instance_name} {"exists" if instance is not None else "not exists"}!!")

        return instance


    #confere se ja exipirou
    async def expires(self, instance_name:str) -> bool:

        with self.lock:

            if not instance_name in self.count.keys():
                raise InstanceNotFound(f"{instance_name} not found")

            exp = self.count[instance_name]["exp"]
            now = datetime.now(timezone.utc)

            return exp>=now


            

            

            





            
        