# Title     : Project 1 for the course Forskningsmetodik för IT
# Objective : evaluate answers from SUS questionnaire

#loads .csv file into R session
answers <- read.csv("projekt1/SUSsvar18och20.csv", header = TRUE, sep = ";")

#Makes an empty vector for appending the results
resultVector <- c()

for (rows in 1:dim(answers)[1]){

  #Pics the rownumber
  row <- answers[rows,]

  #Factorises the row and uses summary to get how many of which number exsists
  factRow <- factor(row)
  sumFactRow <- summary(factRow)

  #Makes values numeric
  numericFactRow <- as.numeric(levels(factRow))

  #For loop to calculate the SUS values
  #Selects the number, checks if it is odd or even,
  #then makes the calculation and multiplies by the amount numbers of a number
  #Example
  # 1 2 3 4 Numbers
  # 1 3 1 5 How many numbers of a number
  count <- 0
  total <- 0
  for (val in sumFactRow){
    count = count + 1
    num <- numericFactRow[count]
    if((num %% 2) == 0) {
        #EVEN
        #Substracts the user response from 5 and multiplies by the amount of that number
        ans <- (5 - num) * sumFactRow[count]
    } else {
        #ODD
        #Substracts 1 from the user response and multiplies by the amount of that number
        ans <- (num - 1) * sumFactRow[count]
    }
    total = total + ans
  }

  #RESULT
  result <-  total * 2.5
  print(result)
  resultVector <- append(resultVector, result)
}
print(summary(resultVector))
