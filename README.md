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
