
model_params <- commandArgs(trailingOnly = TRUE)

# Predict using given params
prediction <- sum(as.numeric(model_params))

# return result
cat(prediction)

