### Deploy to docker hub

```sh
docker build -t tenkr/llm-chat-service-image:lastest .
docker login
docker push tenkr/llm-chat-service-image:lastest
```
