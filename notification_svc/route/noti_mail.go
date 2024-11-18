package route

import (
	"fmt"
	"os"
	"strconv"

	gomail "gopkg.in/mail.v2"
)

type NotificationInfo struct {
	Username 		string `json:"username"`
	Email    		string `json:"email"`
	Temperature     float64 `json:"temperature"`
}

func SendEmail(notiInfo NotificationInfo) error {

	message := gomail.NewMessage()
	senderEmail := os.Getenv("SENDER_EMAIL")
	senderPassword := os.Getenv("SENDER_PASSWORD")

	message.SetHeader("From", senderEmail)
	message.SetHeader("To", notiInfo.Email)
	message.SetHeader("Subject", "Notification from Temp-Predictor")

	message.SetBody("text/plain", 
	`Hello ` + notiInfo.Username + `. Alert! from temperature prediction. The temperature is `+ 
	strconv.FormatFloat(notiInfo.Temperature, 'f', 2, 64) + `. Higher than 40 degree celcius! Please use sun-protection cream or bring an umbrella with you all day long. Have a good day ^^`)

	dialer := gomail.NewDialer("smtp.gmail.com", 587, senderEmail, senderPassword)

	if err := dialer.DialAndSend(message); err != nil {
		fmt.Println("Error:", err)
		return err
	} else {
		fmt.Println("Email sent successfully!")
		return nil
	}
}
