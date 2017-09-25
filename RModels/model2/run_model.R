model_path <- paste0(Sys.getenv("R_MODEL2_DIRECTORY"),"/","model.rda")
model_params <- commandArgs(trailingOnly = TRUE)

# Load pre-saved model
load(model_path)
# Use parameters to create a single row dataframe
input_dataframe  <-     data.frame(cyl = as.numeric(model_params))

# Predict on parameter data using restored model
prediction <- predict(model,input_dataframe)

# return result
cat(prediction)

