# Prime Factorizer
## TODO
In this folder, you should write a service that listens for incoming Kafka messages from `server`, computes the prime factorization of the number received, and returns the prime factors to `server` using Kafka. The server should be responsible for routing the resulting prime factors to the relevant websocket. You should use any language of your choice OTHER THAN Python to write this service, though it is recommended to use a performant language (e.g., Rust, C++) if possible.
