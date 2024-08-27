package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/rabbitmq/amqp091-go"
	"github.com/redis/go-redis/v9"
)

// Redis client
var rdb *redis.Client
var ctx = context.Background()

func main() {
	// Initialize Redis client
	rdb = redis.NewClient(&redis.Options{
		Addr: "localhost:6379", // Redis address
		DB:   0,                // use default DB
	})

	// Connect to RabbitMQ
	conn, err := amqp091.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel: %v", err)
	}
	defer ch.Close()

	// Declare a queue to send messages to
	q, err := ch.QueueDeclare(
		"crawl_queue", // queue name
		true,          // durable
		false,         // delete when unused
		false,         // exclusive
		false,         // no-wait
		nil,           // arguments
	)
	if err != nil {
		log.Fatalf("Failed to declare a queue: %v", err)
	}

	// Subscribe to Redis channel for completion notifications
	pubsub := rdb.Subscribe(ctx, "task_completions")
	defer pubsub.Close()

	// Create a terminal scanner to read input
	scanner := bufio.NewScanner(os.Stdin)

	fmt.Println("Enter tasks to send to the queue. Type 'exit' to quit.")

	for {
		fmt.Print("> ")
		scanner.Scan()
		input := strings.TrimSpace(scanner.Text())

		// Exit if the user types 'exit'
		if strings.ToLower(input) == "exit" {
			fmt.Println("Exiting...")
			break
		}

		if input != "" {
			// Generate a unique task ID
			taskID := fmt.Sprintf("task-%d", time.Now().UnixNano())

			// Publish the task and store it in Redis
			err := publishTask(ch, q.Name, taskID, input)
			if err != nil {
				log.Fatalf("Failed to send task: %v", err)
			}

			// Store initial task status in Redis
			err = rdb.HSet(ctx, taskID, map[string]interface{}{
				"task":      input,
				"result":    "pending",
				"processed": "false",
			}).Err()
			if err != nil {
				log.Fatalf("Failed to store task in Redis: %v", err)
			}

			fmt.Printf("Sent task: %s\n", input)

			// Wait for task completion notification
			msg, err := pubsub.ReceiveMessage(ctx)
			if err != nil {
				log.Fatalf("Failed to receive message from Redis: %v", err)
			}
			if msg.Payload == taskID {
				// Fetch task details from Redis
				taskDetails, err := rdb.HGetAll(ctx, taskID).Result()
				if err != nil {
					log.Fatalf("Failed to fetch task details from Redis: %v", err)
				}
				result := taskDetails["result"]
				fmt.Printf("Task %s is complete! Result: %s\n", taskID, result)
			}
		}
	}
}

// Helper function to publish tasks to RabbitMQ
func publishTask(ch *amqp091.Channel, queueName, taskID, task string) error {
	// Publish the task to RabbitMQ
	return ch.Publish(
		"",        // exchange
		queueName, // routing key (queue name)
		false,     // mandatory
		false,     // immediate
		amqp091.Publishing{
			ContentType: "text/plain",
			Body:        []byte(task),
			MessageId:   taskID,
		},
	)
}
