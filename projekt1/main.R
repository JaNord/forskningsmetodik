# Title     : Project 1 for the course Forskningsmetodik för IT
# Objective : evaluate susData from SUS questionnaire

#loads .csv file into R session
susData <- read.csv2("projekt1/SUSsvar18och20.csv")

#Builds a sequence of even numbers from 2 to column length of csv file
even <- seq(2, ncol(susData),2)

#Loops through the even sequence
for (evenValue in even){
  #Even numbers, substracts the response from 5 in all even columns
  susData[,evenValue] <- 5 - susData[,evenValue]
  #odd numbers, substracts one from the response in all odd columns
  susData[,evenValue - 1] <-  susData[,evenValue - 1] - 1
}

#Adds up all converted responses and converts the range from 0-40 to 0-100
susResult <- rowSums(susData) * 2.5
#Prints Min value, Median, Mean and Max
print(summary(susResult))
#Prints standard deviation
cat("Standard deviation: ", sd(susResult))
