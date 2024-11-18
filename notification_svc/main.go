package main

import (
	"log"
	"net/http"
	ROUTE "project/route"
	"github.com/joho/godotenv"
	"github.com/gin-gonic/gin"
)

func main() {

	r := gin.Default()
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	r.POST("/noti", func(c *gin.Context) {
		var notiInfo ROUTE.NotificationInfo
		if err := c.ShouldBindJSON(&notiInfo); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"error": err.Error(),
			})
			return
		}
		if err := ROUTE.SendEmail(notiInfo); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "Failed to send notification",
			})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Notification sent successfully"})
	})

	r.Run(":8082")
}
