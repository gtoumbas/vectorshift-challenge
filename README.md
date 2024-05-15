# VectorShift Technical Assessment
Thank you for taking the time to interview with us at VectorShift! As part of the interview process, we would like you to complete a technical assessment. This assessment will consist of extending an existing Python server, writing a non-Python service for computing the prime factors of a number, and using Kafka to connect the Python server with the prime factorization service.

Once complete, your program should:
1. Accept new websocket connections
2. Listen for messages through each websocket, sending incoming numbers to the prime factorizer using Kafka
3. Route results received from the prime factorizer to the relevant websocket, sending the result as text over the websocket
4. Close each websocket after 5 seconds of inactivity (e.g., no numbers currently being factorized for the given websocket)

You can find the existing FastAPI server code in `/technical_assessment/server/main.py`, and the server's Kafka client is in `technical_assessment/server/kafka_client.py`. There is a placeholder directory for your prime factorization service in `technical_assessment/prime_factorizer`, which includes a README file with additional details.

## Setup
To start the server:
1. Start Kafka by running `docker-compose up` in the `/technical_assessment` directory
2. Install `server` requirements by running `pip install -r requirements.txt` in the `/technical_assessment` directory
3. Start `server` by running `uvicorn main:app --reload` in the `/technical_assessment/server` directory

## Testing
You can test your code by running the `/technical_assessment/test.py` file, which opens two websockets and sends 5 numbers in total to be factorized. If your code is working as intended, the test script should print the prime factorization of each number along with the associated websocket. If the prime factorization is taking too long for testing purposes, feel free to change the test numbers to be smaller, though a performant prime factorizer should not take more than a few seconds to factorize each of the given numbers.

Feel free to reach out to <recruiting@vectorshift.ai> if you have any questions.


# George Toumbas
# Implementation Details

## Kafka Client
The `KafkaClient` class handles Kafka producer and consumer instances, message routing, and websocket connections.

### Routing Details
1. **Sending Messages**: The `send_message` method publishes messages to a Kafka topic with websocket identifiers in the headers.
2. **Receiving Messages**: The `listen_for_messages` method subscribes to a Kafka topic, extracts websocket identifiers from message headers, and routes messages to the appropriate websocket.
3. **Websocket Mapping**: The `websocket_map` dictionary maps websocket identifiers (UUIDs) to their connections and tracks pending messages to prevent timeouts.

## Prime Factorization
The Go-based prime factorization service uses Pollard's Rho algorithm. It listens for Kafka messages with numbers to factorize, computes the prime factors, and sends results back via Kafka, maintaining websocket identifiers in the headers for correct routing. 

The prime factorization service includes the original number in the response. For example, a response might look like `3211891798434562153 : [1000000087 3211891519]`, where the numbers in the square brackets are the prime factors of the first number.


### Running the Prime Factorization Service
To run the prime factorization service, you can use the following commands:

### Running the Service
**Direct Execution**: (I compiled on Mac ARM, so you may need to rebuild or use go run if you're on a different platform)
   ```sh
   ./prime_factorizer [-log]
   ```

**Using `go run`**:
   ```sh
   go run main.go factorizer.go [-log]
   ```

### Rebuilding the Service
   **Build**:
   ```sh
   go build -o prime_factorizer main.go factorizer.go
   ```
