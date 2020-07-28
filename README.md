- Setting node_modules

```bash
cd docker-images-react && yarn install
```

- Build containers:

```bash
docker-compose build
```

- Run containers :

```bash
docker-compose up
```

You should be able to check it in your Docker container's URL, for example:

React(Frontend) : <a href="http://localhost" target="_blank">http://localhost</a>

Flask(Backend) : <a href="http://localhost:5000" target="_blank">http://localhost:5000</a>

You can check DB server, for example:

```bash
mysql -h 127.0.0.1 -u user -ppassword
```
