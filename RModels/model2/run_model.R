
model_params <- commandArgs(trailingOnly = TRUE)

# Predict using given params
# Load pre-saved model
load("model.rda")

# Read parameters and convert to single row dataframe
input_dataframe <-     data.frame(cyl = as.numeric(model_params))


# Predict on parameter data using restored model
prediction <- predict(model,input_dataframe)


# return result
#cat(prediction)
cat(0)
