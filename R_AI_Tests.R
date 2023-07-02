library(class)
library(FNN)
library(tidyverse)

# KNN Regression
bikesharing <- read.csv("day.csv")
glimpse(bikesharing)

#atemp: normalized feeling temperature in Celsius
#hum: normalized humidity
#windspeed: normalized wind speed
#cnt: count of total rental bikes (response variable)

summary(bikesharing$cnt)
bikesharing %>% 
  ggplot()+
  geom_histogram(aes(cnt),bins=10,col="white")

#Temperature to wind and colour based on rented bikes
bikesharing %>% 
  ggplot()+
  geom_point(aes(x=atemp,y=windspeed,col=cnt))+
  scale_colour_gradientn(colours = rev(hcl.colors(12)))

# Regression ####
## 1 Training Set ####
# 3 subsets: 70% training 15% validating 15% test
set.seed(1, sample.kind = "Rejection")
index <- sample(1:3,
                size = nrow(bikesharing),
                prob= c(0.7, 0.15, 0.15),
                replace = T)
head(index)

# new DF training
bike_training <-  bikesharing[index == 1,]
head(bike_training)
# validate DF to tune model (elegir el mejor tuning parameter, el numero de neighbors que min 
# validation error)
bike_validate <- bikesharing[index ==2,]
head(bike_validate)
# test DF
bike_test <- bikesharing[index ==3,]
head(bike_test)

## 2 Implementation ####
# k = 1 
# the arguments y and k refer to the training response variable 
# vector and the number of neighbors, respectively
knn1 = knn.reg(train = dplyr::select(bike_training, atemp, windspeed, hum),
              test = dplyr::select(bike_validate, atemp, windspeed, hum),
              y= bike_training$cnt, 
              k = 1)
names(knn1)
# Mean error of prediction
mean((bike_validate$cnt - knn1$pred)^2)
# Predicted values
pred_df_k1 = data.frame(obs = bike_validate$cnt, # 'reales'
                        pred = knn1$pred) # 'predicted'
head(pred_df_k1)
plot1 <- pred_df_k1 %>% 
  ggplot() +
  geom_point(aes(x=obs,y=pred,col=(obs-pred)^2)) +
  scale_color_gradient(low="blue",high="red")
plot1

## 3 Different k ####
# create MSE vector
mse_vec = c()
k_vec = c(1, 10, 25, 50, 100, 200, 500, nrow(bike_training))
for(i in 1:length(k_vec)){
  knn = knn.reg(train = dplyr::select(bike_training, atemp, windspeed, hum),
                test = dplyr::select(bike_validate, atemp, windspeed, hum),
                y = bike_training$cnt,
                k = k_vec[i])
  # in the MSE vector 
  mse_vec[i] = mean((bike_validate$cnt - knn$pred)^2)
}
mse_vec
plot(k_vec,mse_vec,type="b")
# min MSE value
mse_knn = min(mse_vec)
mse_knn
# where
which.min(mse_vec)
# which k value
kbest = k_vec[which.min(mse_vec)]
kbest

## 4 Assesment ####
bike_newtraining <-  rbind(bike_validate, bike_training)
knnbest <- knn.reg(train = dplyr::select(bike_newtraining, atemp, hum, windspeed),
                   test = dplyr::select(bike_test, atemp, hum, windspeed),
                   y = bike_newtraining$cnt,
                   k = kbest)

mse_knn_final <-  mean((bike_test$cnt - knnbest$pred)^2)
mse_knn_final

## 5 Comparison ####
# a multiple regession with 3 factors 
modlm = lm(cnt ~ atemp + windspeed + hum,
           data = bike_training)
summary(modlm)
# Predict
pedlm = predict(modlm,
                newdata = bike_test)
mse_lm = mean((bike_test$cnt  - pedlm)^2)
mse_lm # is higher than the one from the KNN mse with k = 50
mse_knn_final

## 6 Compare quadratic ####
modlmpoly = lm(cnt ~ poly(atemp,2) +
                 poly(windspeed,2)+
                 poly(hum,2), data=bike_training)
summary(modlmpoly)
# predict
predlmpoly = predict(modlmpoly,
                     newdata = bike_test)
mse_lm2 = mean((bike_test$cnt-predlmpoly)^2)
mse_lm2 # is higher than the one from the KNN mse with k = 50
mse_lm 
mse_knn_final

# Classification ####
## 1 ####






































