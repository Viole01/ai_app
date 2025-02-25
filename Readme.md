# AI FastAPI Application

## Environment setup
- Create a virtual environment by running:
```sh
python -m venv <name of environment>
```

- Activate the virtual environment by running: 
```sh
source <path/to/venv/bin/activate>
```

- All required packages are listed in [requirements.txt](requirements.txt) file.

- To install dependencies, run:
 ```sh
 pip install -r requirements.txt
 ```


## Structuring of files

- Application instantiation and importing routes and their functions is done in [main.py](main.py) file.

- Each model and it's related files (eg. model file and preprocessing code) are put in a separate directory named after the respective route.

- All imports and logic related to model loading, request schema, route creation, and handling the incoming request body is stored in a single file named after the route's name.


## Application setup on EC2

### Use Certbot to setup SSL
- To install Certbot, run
```sh
sudo apt install certbot python3-certbot``.
```

- To issue a certificate for your domain, run:
```sh
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com``.
```
- Certbot saves the certificate files at:

1. Certificate: ``/etc/letsencrypt/live/yourdomain.com/fullchain.pem``
2. Private Key: ``/etc/letsencrypt/live/yourdomain.com/privkey.pem``

- To run your application with SSL, add these lines in your Hypercorn startup command:
```sh
hypercorn --bind 0.0.0.0:443 \
  --keyfile /etc/letsencrypt/live/yourdomain.com/privkey.pem \
  --certfile /etc/letsencrypt/live/yourdomain.com/fullchain.pem \
  main:app
```

### Service creation of application
- If you have a service file, put it at ``/etc/systemd/system/``.

- To create a new service file, run:
```sh
sudo nano /etc/systemd/system/fastapi.service
```
and define the service.

- To start your service:
1. Reload the daemon by running ``sudo systemctl daemon-reload``.
2. Enable your service - ``sudo systemctl enable fastapi.service``.
3. Start the service - `` sudo systemctl start fastapi.service``.
4. Check the service status by running - ``sudo systemctl status fastapi.service``.


### Cloudflare Tunnel setup
- Install connector using the command shown in the cloudflare console.
