import os
import subprocess


class SceDockerHandler:

    container_dict = {
        'frontend': 'docker build Core-v4/. -t frontend && docker run -p 3000:80 frontend',
        'mongo': ' docker run -p 27017:27017 mongo',
        'led-sign': 'docker build /SCE-RPC/server/led_sign/. -t led-sign && docker run -p 5000:50051 led-sign',
        '2d-printing': 'docker build /SCE-RPC/server/printing/. -t 2d-printing && docker run -p 5001:50051 2d-printing',
        '3d-printing': 'docker build /SCE-RPC/server/printing_3d/. -t 3d-printing && docker run -p 5002:50051 3d-printing',
        'api': 'docker build Core-v4/api/. -t api && docker run -p 8080:8080 api',
        'logging': 'docker build Core-v4/api/logging/. -t logging && docker run -p 8081:8081 logging',
        'mailer': 'docker build Core-v4/api/mailer/Dockerfile -t mailer && docker run -p 8082:8082 mailer',
        'core-v4': 'cd Core-v4 && docker-compose up'
    }

    def run_services(self, services=None):
        print(services)

        if services == None:
            print("Mate, we are going to run everything")  # NEVER DELETE
        else:
            for service in services:
                if service not in self.container_dict:
                    print("GO TO HELL MATE!!")
                else:
                    subprocess.run(self.container_dict[service])
