- Setting node_modules

```bash
cd docker-images-next && yarn install
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

Next.js(Frontend) : <a href="http://localhost:3000" target="_blank">http://localhost:3000</a>

Flask(Backend) : <a href="http://localhost:5000" target="_blank">http://localhost:5000</a>

（他の例：<a href="http://localhost:5000/db" target="_blank">http://localhost:5000/db</a>

<a href="http://localhost:5000/tasks" target="_blank">http://localhost:5000/tasks</a>
）

You can check DB server, for example:

```bash
psql -h localhost -U postgres POSTGRESDB
```
