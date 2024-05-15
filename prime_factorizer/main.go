package main

import (
    "context"
    "fmt"
    "log"
    "math/big"
    "os"
    "os/signal"
    "syscall"
	"strings"

    "github.com/segmentio/kafka-go"
)

func ConvertFactorsToString(factors []*big.Int) string {
	// Convert each factor to a string and join them
	factorStrs := make([]string, len(factors))
	for idx, fac := range factors {
		factorStrs[idx] = fac.String()
	}
	result := fmt.Sprintf("[%s]", strings.Join(factorStrs, " "))
	return result
}

func main() {
    // Kafka reader configuration
    fmt.Println("Configuring Kafka reader...")
    r := kafka.NewReader(kafka.ReaderConfig{
        Brokers: []string{"localhost:9092"},
        Topic:   "numbers",
        GroupID: "prime-factorizer",
    })
    fmt.Println("Kafka reader configured.")

    // Kafka writer configuration
    fmt.Println("Configuring Kafka writer...")
    w := kafka.NewWriter(kafka.WriterConfig{
        Brokers: []string{"localhost:9092"},
        Topic:   "results",
    })
    fmt.Println("Kafka writer configured.")

    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Handle graceful shutdown
    go func() {
        sigchan := make(chan os.Signal, 1)
        signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)
        <-sigchan
        fmt.Println("Received shutdown signal, cancelling context...")
        cancel()
    }()

	for {
		fmt.Println("Listening for messages...")

		m, err := r.ReadMessage(ctx)
		if err != nil {
			log.Printf("could not read message: %v", err)
			break
		}
		fmt.Printf("Message read: %s\n", string(m.Value))
		identifier := string(m.Headers[0].Value)
		number := new(big.Int)
		number.SetString(string(m.Value), 10)
		originalNumber := number.String()
		fmt.Printf("Computing prime factors for number: %s\n", number.String())
		factors := PrimeFactors(number)

		result := ConvertFactorsToString(factors)
		result = fmt.Sprintf("%s : %s", originalNumber, result)

		fmt.Printf("Debug: Writing message to Kafka with identifier %s and result %s\n", identifier, result)
		err = w.WriteMessages(ctx, kafka.Message{
			Value: []byte(result),
			Headers: []kafka.Header{{Key: "ws-identifier", Value: []byte(identifier)}},
		})
		if err != nil {
			log.Printf("could not write message: %v", err)
		}
	}
}